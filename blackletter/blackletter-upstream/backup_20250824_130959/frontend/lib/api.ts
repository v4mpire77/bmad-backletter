/**
 * Blackletter GDPR Processor - API Client
 * Context Engineering Framework v2.0.0 Compliant
 * Type-safe API client with proper error handling
 */
import axios, { AxiosInstance, AxiosError, AxiosResponse } from 'axios';
import { 
  JobCreateResponse, 
  JobStatus, 
  JobResult, 
  ErrorResponse, 
  HealthResponse,
  DashboardStats,
  UploadProgress
} from './types';

export class BlackletterAPIError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public path: string,
    public timestamp?: string
  ) {
    super(message);
    this.name = 'BlackletterAPIError';
  }
}

export class BlackletterAPIClient {
  private client: AxiosInstance;
  private readonly baseURL: string;

  constructor(baseURL?: string) {
    this.baseURL = baseURL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    
    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: 30000, // 30 seconds
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => {
        console.error('[API] Request error:', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response: AxiosResponse) => {
        console.log(`[API] Response ${response.status} from ${response.config.url}`);
        return response;
      },
      (error: AxiosError) => {
        console.error('[API] Response error:', error);
        return Promise.reject(this.handleError(error));
      }
    );
  }

  private handleError(error: AxiosError): BlackletterAPIError {
    if (error.response) {
      // Server responded with error status
      const errorData = error.response.data as ErrorResponse;
      return new BlackletterAPIError(
        errorData.error || error.message,
        error.response.status,
        errorData.path || error.config?.url || '',
        errorData.timestamp
      );
    } else if (error.request) {
      // Network error
      return new BlackletterAPIError(
        'Network error - please check your connection',
        0,
        error.config?.url || ''
      );
    } else {
      // Request configuration error
      return new BlackletterAPIError(
        error.message,
        0,
        error.config?.url || ''
      );
    }
  }

  /**
   * Health check endpoint
   */
  async checkHealth(): Promise<HealthResponse> {
    const response = await this.client.get<HealthResponse>('/health');
    return response.data;
  }

  /**
   * Check API root endpoint
   */
  async checkRoot(): Promise<{ message: string; version: string; framework: string }> {
    const response = await this.client.get('/');
    return response.data;
  }

  /**
   * Upload contract file and create analysis job
   * Returns 202 Accepted with job details
   */
  async uploadContract(
    file: File,
    onProgress?: (progress: UploadProgress) => void
  ): Promise<JobCreateResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await this.client.post<JobCreateResponse>('/api/v1/jobs/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const progress: UploadProgress = {
            loaded: progressEvent.loaded,
            total: progressEvent.total,
            percentage: Math.round((progressEvent.loaded / progressEvent.total) * 100)
          };
          onProgress(progress);
        }
      }
    });

    return response.data;
  }

  /**
   * Get job status for polling
   */
  async getJobStatus(jobId: string): Promise<JobStatus> {
    const response = await this.client.get<JobStatus>(`/api/v1/jobs/${jobId}/status`);
    return response.data;
  }

  /**
   * Get job result when completed
   * May return 202 if still processing
   */
  async getJobResult(jobId: string): Promise<JobResult> {
    const response = await this.client.get<JobResult>(`/api/v1/jobs/${jobId}/result`);
    return response.data;
  }

  /**
   * Cancel a job
   */
  async cancelJob(jobId: string): Promise<{ message: string; job_id: string }> {
    const response = await this.client.delete(`/api/v1/jobs/${jobId}`);
    return response.data;
  }

  /**
   * List recent jobs
   */
  async listJobs(limit: number = 50): Promise<JobStatus[]> {
    const response = await this.client.get<JobStatus[]>(`/api/v1/jobs/?limit=${limit}`);
    return response.data;
  }

  /**
   * Get job statistics (development only)
   */
  async getJobStats(): Promise<DashboardStats> {
    const response = await this.client.get<DashboardStats>('/api/v1/jobs/stats');
    return response.data;
  }

  /**
   * Check Context Engineering Framework compliance
   */
  async checkCompliance(): Promise<{
    framework_version: string;
    required_score: number;
    validation_enabled: boolean;
    status: string;
  }> {
    const response = await this.client.get('/api/v1/compliance');
    return response.data;
  }

  /**
   * Poll job status until completion
   * Useful for waiting for job results
   */
  async pollJobStatus(
    jobId: string,
    onProgress?: (status: JobStatus) => void,
    intervalMs: number = 2000,
    maxAttempts: number = 150 // 5 minutes at 2s intervals
  ): Promise<JobStatus> {
    let attempts = 0;
    
    while (attempts < maxAttempts) {
      try {
        const status = await this.getJobStatus(jobId);
        
        if (onProgress) {
          onProgress(status);
        }

        // Check if job is complete
        if (['completed', 'failed', 'cancelled'].includes(status.status)) {
          return status;
        }

        // Wait before next poll
        await new Promise(resolve => setTimeout(resolve, intervalMs));
        attempts++;
        
      } catch (error) {
        console.error(`[API] Polling error for job ${jobId}:`, error);
        attempts++;
        
        // If we're near the end, throw the error
        if (attempts >= maxAttempts - 5) {
          throw error;
        }
        
        // Otherwise, wait and retry
        await new Promise(resolve => setTimeout(resolve, intervalMs));
      }
    }
    
    throw new BlackletterAPIError(
      'Job polling timeout - job did not complete within expected time',
      408,
      `/api/v1/jobs/${jobId}/status`
    );
  }

  /**
   * Complete upload and analysis workflow
   * Uploads file, polls for completion, and returns result
   */
  async analyzeContract(
    file: File,
    onUploadProgress?: (progress: UploadProgress) => void,
    onStatusUpdate?: (status: JobStatus) => void
  ): Promise<JobResult> {
    // Step 1: Upload file
    const jobResponse = await this.uploadContract(file, onUploadProgress);
    
    // Step 2: Poll for completion
    const finalStatus = await this.pollJobStatus(
      jobResponse.job_id,
      onStatusUpdate
    );
    
    // Step 3: Get result
    if (finalStatus.status === 'completed') {
      return await this.getJobResult(jobResponse.job_id);
    } else {
      throw new BlackletterAPIError(
        `Job failed with status: ${finalStatus.status}`,
        500,
        `/api/v1/jobs/${jobResponse.job_id}/result`
      );
    }
  }
}

// Export singleton instance
export const apiClient = new BlackletterAPIClient();

// Export utility functions
export function isAPIError(error: any): error is BlackletterAPIError {
  return error instanceof BlackletterAPIError;
}

export function formatAPIError(error: BlackletterAPIError): string {
  return `API Error (${error.statusCode}): ${error.message}`;
}