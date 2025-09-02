/**
 * Blackletter GDPR Processor - Dashboard Page
 * Context Engineering Framework v2.0.0 Compliant
 * Real-time job monitoring and results visualization
 */
"use client";

import React, { useEffect, useState, useCallback } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { Progress } from "@/components/ui/progress";
import { BlackletterAPIClient, BlackletterAPIError } from "@/lib/api";
import { 
  JobStatus, 
  JobResult, 
  JobStatusEnum, 
  JobWithDetails, 
  Issue, 
  Coverage,
  GDPR_ARTICLES
} from "@/lib/types";

// Initialize API client
const apiClient = new BlackletterAPIClient();

const POLL_INTERVAL = 5000; // 5 seconds
const MAX_RETRIES = 3;

export default function DashboardPage() {
  const [jobs, setJobs] = useState<JobWithDetails[]>([]);
  const [selectedJob, setSelectedJob] = useState<string | null>(null);
  const [jobResult, setJobResult] = useState<JobResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [retryCount, setRetryCount] = useState(0);

  // Fetch jobs from API
  const fetchJobs = useCallback(async () => {
    try {
      const jobsList = await apiClient.listJobs(50);
      setJobs(jobsList as JobWithDetails[]);
      setError(null);
      setRetryCount(0);
    } catch (err) {
      console.error('Failed to fetch jobs:', err);
      if (err instanceof BlackletterAPIError) {
        setError(`API Error: ${err.message} (${err.statusCode})`);
      } else {
        setError('Failed to fetch jobs. Please check your connection.');
      }
      
      // Retry logic
      if (retryCount < MAX_RETRIES) {
        setRetryCount(prev => prev + 1);
        setTimeout(fetchJobs, 1000 * (retryCount + 1)); // Exponential backoff
      }
    } finally {
      setLoading(false);
    }
  }, [retryCount]);

  // Fetch job result
  const fetchJobResult = useCallback(async (jobId: string) => {
    try {
      const result = await apiClient.getJobResult(jobId);
      setJobResult(result);
    } catch (err) {
      console.error(`Failed to fetch result for job ${jobId}:`, err);
      // Don't show error for 202 responses (still processing)
      if (err instanceof BlackletterAPIError && err.statusCode !== 202) {
        setError(`Failed to fetch job result: ${err.message}`);
      }
    }
  }, []);

  // Cancel job
  const handleCancelJob = async (jobId: string) => {
    try {
      await apiClient.cancelJob(jobId);
      fetchJobs(); // Refresh jobs list
    } catch (err) {
      console.error(`Failed to cancel job ${jobId}:`, err);
      if (err instanceof BlackletterAPIError) {
        setError(`Failed to cancel job: ${err.message}`);
      }
    }
  };

  // Initial load and polling
  useEffect(() => {
    fetchJobs();
    const interval = setInterval(fetchJobs, POLL_INTERVAL);
    return () => clearInterval(interval);
  }, [fetchJobs]);

  // Fetch result when job is selected
  useEffect(() => {
    if (selectedJob) {
      const job = jobs.find(j => j.job_id === selectedJob);
      if (job && job.status === 'completed') {
        fetchJobResult(selectedJob);
      } else {
        setJobResult(null);
      }
    }
  }, [selectedJob, jobs, fetchJobResult]);

  const getStatusColor = (status: JobStatusEnum): string => {
    switch (status) {
      case 'completed': return 'bg-green-500';
      case 'failed': return 'bg-red-500';
      case 'processing': return 'bg-yellow-500';
      case 'cancelled': return 'bg-gray-500';
      default: return 'bg-blue-500';
    }
  };

  const getStatusText = (status: JobStatusEnum): string => {
    return status.charAt(0).toUpperCase() + status.slice(1);
  };

  const getCoverageColor = (status: string): string => {
    switch (status) {
      case 'OK': return 'text-green-600 bg-green-50';
      case 'Partial': return 'text-yellow-600 bg-yellow-50';
      case 'GAP': return 'text-red-600 bg-red-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  const getSeverityColor = (severity: string): string => {
    switch (severity) {
      case 'High': return 'text-red-600 bg-red-50';
      case 'Medium': return 'text-yellow-600 bg-yellow-50';
      case 'Low': return 'text-blue-600 bg-blue-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  if (loading && jobs.length === 0) {
    return (
      <div className="container mx-auto py-10 px-4">
        <div className="space-y-6">
          <Skeleton className="h-8 w-64" />
          <div className="grid gap-4">
            {[1, 2, 3].map((i) => (
              <Skeleton key={i} className="h-24 w-full" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-10 px-4">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold">Contract Analysis Dashboard</h1>
            <p className="text-muted-foreground">
              Monitor GDPR Article 28(3) processor obligations analysis
            </p>
          </div>
          <Button onClick={fetchJobs} variant="outline">
            Refresh
          </Button>
        </div>

        {/* Error Display */}
        {error && (
          <Card className="border-red-200 bg-red-50">
            <CardContent className="pt-6">
              <p className="text-red-600">{error}</p>
              <Button onClick={fetchJobs} className="mt-2" variant="outline" size="sm">
                Retry
              </Button>
            </CardContent>
          </Card>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Jobs List */}
          <Card>
            <CardHeader>
              <CardTitle>Recent Jobs ({jobs.length})</CardTitle>
              <CardDescription>
                Analysis jobs with real-time status updates
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {jobs.length === 0 ? (
                <div className="text-center py-8 text-muted-foreground">
                  <p>No jobs found.</p>
                  <p className="text-sm">Upload a contract to get started!</p>
                </div>
              ) : (
                jobs.map((job) => (
                  <div
                    key={job.job_id}
                    className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                      selectedJob === job.job_id 
                        ? 'border-primary bg-primary/5' 
                        : 'border-border hover:border-primary/50'
                    }`}
                    onClick={() => setSelectedJob(job.job_id)}
                  >
                    <div className="flex justify-between items-start mb-2">
                      <div className="flex-1 min-w-0">
                        <p className="font-medium truncate">
                          {job.filename || `Job ${job.job_id.slice(0, 8)}`}
                        </p>
                        <p className="text-sm text-muted-foreground">
                          {new Date(job.created_at).toLocaleString()}
                        </p>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge className={getStatusColor(job.status)}>
                          {getStatusText(job.status)}
                        </Badge>
                        {(job.status === 'pending' || job.status === 'processing') && (
                          <Button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleCancelJob(job.job_id);
                            }}
                            variant="outline"
                            size="sm"
                          >
                            Cancel
                          </Button>
                        )}
                      </div>
                    </div>

                    {/* Progress Bar */}
                    {job.status === 'processing' && (
                      <div className="space-y-1">
                        <Progress value={job.progress * 100} className="h-2" />
                        <p className="text-xs text-muted-foreground">
                          {Math.round(job.progress * 100)}% complete
                        </p>
                      </div>
                    )}

                    {/* Status Message */}
                    {job.message && (
                      <p className="text-sm text-muted-foreground mt-2">
                        {job.message}
                      </p>
                    )}
                  </div>
                ))
              )}
            </CardContent>
          </Card>

          {/* Job Results */}
          <Card>
            <CardHeader>
              <CardTitle>Analysis Results</CardTitle>
              <CardDescription>
                {selectedJob 
                  ? `Results for job ${selectedJob.slice(0, 8)}...`
                  : 'Select a completed job to view results'
                }
              </CardDescription>
            </CardHeader>
            <CardContent>
              {!selectedJob ? (
                <div className="text-center py-8 text-muted-foreground">
                  Select a job from the list to view detailed results
                </div>
              ) : !jobResult ? (
                <div className="space-y-4">
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-3/4" />
                  <Skeleton className="h-4 w-1/2" />
                </div>
              ) : jobResult.error ? (
                <div className="text-center py-8">
                  <p className="text-red-600 font-medium">Analysis Failed</p>
                  <p className="text-sm text-muted-foreground mt-2">
                    {jobResult.error}
                  </p>
                </div>
              ) : (
                <div className="space-y-6">
                  {/* Summary */}
                  <div className="grid grid-cols-2 gap-4">
                    <div className="text-center p-3 bg-blue-50 rounded-lg">
                      <p className="text-2xl font-bold text-blue-600">
                        {jobResult.analysis?.issues.length || 0}
                      </p>
                      <p className="text-sm text-blue-600">Issues Found</p>
                    </div>
                    <div className="text-center p-3 bg-green-50 rounded-lg">
                      <p className="text-2xl font-bold text-green-600">
                        {jobResult.analysis?.coverage.filter(c => c.status === 'OK').length || 0}/8
                      </p>
                      <p className="text-sm text-green-600">Articles OK</p>
                    </div>
                  </div>

                  {/* GDPR Coverage */}
                  {jobResult.analysis?.coverage && (
                    <div>
                      <h4 className="font-medium mb-3">GDPR Article 28(3) Coverage</h4>
                      <div className="space-y-2">
                        {GDPR_ARTICLES.map((article) => {
                          const coverage = jobResult.analysis?.coverage.find(
                            c => c.article === article.article
                          );
                          const status = coverage?.status || 'GAP';
                          
                          return (
                            <div key={article.article} className="flex justify-between items-center p-2 border rounded">
                              <div>
                                <p className="font-medium text-sm">{article.article}</p>
                                <p className="text-xs text-muted-foreground">{article.name}</p>
                              </div>
                              <Badge className={getCoverageColor(status)}>
                                {status}
                              </Badge>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  )}

                  {/* Issues */}
                  {jobResult.analysis?.issues && jobResult.analysis.issues.length > 0 && (
                    <div>
                      <h4 className="font-medium mb-3">Issues Detected</h4>
                      <div className="space-y-3 max-h-64 overflow-y-auto">
                        {jobResult.analysis.issues.map((issue) => (
                          <div key={issue.id} className="p-3 border rounded-lg">
                            <div className="flex justify-between items-start mb-2">
                              <p className="font-medium text-sm">{issue.citation}</p>
                              <Badge className={getSeverityColor(issue.severity)}>
                                {issue.severity}
                              </Badge>
                            </div>
                            <p className="text-sm text-muted-foreground mb-2">
                              {issue.snippet}
                            </p>
                            <p className="text-xs text-muted-foreground">
                              Confidence: {Math.round(issue.confidence * 100)}%
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Processing Time */}
                  {jobResult.processing_time && (
                    <div className="text-xs text-muted-foreground text-center pt-4 border-t">
                      Processed in {jobResult.processing_time.toFixed(2)} seconds
                    </div>
                  )}
                </div>
              )}
            </CardContent>
          </Card>        </div>
      </div>
    </div>
  );
}