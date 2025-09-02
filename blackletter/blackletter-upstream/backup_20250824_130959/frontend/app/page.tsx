/**
 * Blackletter GDPR Processor - Upload Page
 * Context Engineering Framework v2.0.0 Compliant
 */
'use client';

import React, { useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { 
  apiClient, 
  BlackletterAPIError, 
  isAPIError 
} from '@/lib/api';
import { 
  formatFileSize, 
  formatPercentage, 
  isValidFileType, 
  isValidFileSize 
} from '@/lib/utils';
import { 
  JobCreateResponse, 
  UploadProgress 
} from '@/lib/types';

const ALLOWED_FILE_TYPES = ['pdf', 'txt', 'docx'];
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

export default function UploadPage() {
  const router = useRouter();
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState<UploadProgress | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFiles = useCallback((files: FileList | null) => {
    if (!files || files.length === 0) return;
    
    const file = files[0];
    setError(null);
    
    // Validate file type
    if (!isValidFileType(file, ALLOWED_FILE_TYPES)) {
      setError(`Invalid file type. Allowed types: ${ALLOWED_FILE_TYPES.join(', ')}`);
      return;
    }
    
    // Validate file size
    if (!isValidFileSize(file, MAX_FILE_SIZE)) {
      setError(`File too large. Maximum size: ${formatFileSize(MAX_FILE_SIZE)}`);
      return;
    }
    
    setSelectedFile(file);
  }, []);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files);
    }
  }, [handleFiles]);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    handleFiles(e.target.files);
  }, [handleFiles]);

  const uploadFile = async () => {
    if (!selectedFile) return;
    
    setUploading(true);
    setError(null);
    setUploadProgress(null);
    
    try {
      const response: JobCreateResponse = await apiClient.uploadContract(
        selectedFile,
        (progress) => setUploadProgress(progress)
      );
      
      // Redirect to dashboard to track progress
      router.push(`/dashboard?job=${response.job_id}`);
      
    } catch (err) {
      console.error('Upload error:', err);
      
      if (isAPIError(err)) {
        setError(`Upload failed: ${err.message}`);
      } else {
        setError('Upload failed. Please try again.');
      }
    } finally {
      setUploading(false);
      setUploadProgress(null);
    }
  };

  const resetUpload = () => {
    setSelectedFile(null);
    setError(null);
    setUploadProgress(null);
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold tracking-tight mb-4">
          GDPR Contract Analysis
        </h1>
        <p className="text-lg text-muted-foreground mb-2">
          Upload your processor contract to analyze GDPR Article 28(3) compliance
        </p>
        <p className="text-sm text-muted-foreground">
          Detects missing, weak, or incomplete processor obligations with citations and recommendations
        </p>
      </div>

      <div className="space-y-6">
        {/* Upload Area */}
        <div 
          className={`
            relative border-2 border-dashed rounded-lg p-8 text-center transition-colors
            ${dragActive ? 'border-primary bg-primary/5' : 'border-gray-300'}
            ${uploading ? 'pointer-events-none opacity-50' : 'hover:border-primary hover:bg-primary/5'}
          `}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            type="file"
            id="file-upload"
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            accept={ALLOWED_FILE_TYPES.map(type => `.${type}`).join(',')}
            onChange={handleFileInput}
            disabled={uploading}
          />
          
          <div className="space-y-4">
            <div className="mx-auto w-16 h-16 text-gray-400">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            
            <div>
              <p className="text-lg font-medium">
                {selectedFile ? selectedFile.name : 'Drop your contract here or click to browse'}
              </p>
              <p className="text-sm text-muted-foreground mt-1">
                Supports PDF, TXT, DOCX up to {formatFileSize(MAX_FILE_SIZE)}
              </p>
              {selectedFile && (
                <p className="text-sm text-green-600 mt-2">
                  Selected: {formatFileSize(selectedFile.size)}
                </p>
              )}
            </div>
          </div>
        </div>

        {/* Upload Progress */}
        {uploadProgress && (
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span>Uploading...</span>
              <span>{formatPercentage(uploadProgress.percentage / 100)}</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-primary h-2 rounded-full transition-all duration-300"
                style={{ width: `${uploadProgress.percentage}%` }}
              />
            </div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="p-4 border border-red-200 bg-red-50 rounded-lg">
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex justify-center space-x-4">
          {selectedFile && !uploading && (
            <>
              <button
                onClick={resetUpload}
                className="px-6 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors"
              >
                Reset
              </button>
              <button
                onClick={uploadFile}
                className="px-6 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90 transition-colors"
              >
                Analyze Contract
              </button>
            </>
          )}
          
          {uploading && (
            <button
              disabled
              className="px-6 py-2 bg-primary/50 text-primary-foreground rounded-md text-sm font-medium cursor-not-allowed"
            >
              Uploading...
            </button>
          )}
        </div>

        {/* Information Panel */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-3">
            What We Analyze
          </h3>
          <div className="grid md:grid-cols-2 gap-4 text-sm text-blue-800">
            <div>
              <h4 className="font-medium mb-2">GDPR Article 28(3) Requirements:</h4>
              <ul className="space-y-1">
                <li>• (a) Processing instructions compliance</li>
                <li>• (b) Personnel confidentiality</li>
                <li>• (c) Security measures implementation</li>
                <li>• (d) Sub-processor management</li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium mb-2">Additional Checks:</h4>
              <ul className="space-y-1">
                <li>• (e) Data subject rights assistance</li>
                <li>• (f) Breach notification procedures</li>
                <li>• (g) Deletion/return obligations</li>
                <li>• (h) Audit and inspection rights</li>
              </ul>
            </div>
          </div>
          <p className="text-xs text-blue-600 mt-4">
            Analysis typically completes within 30-60 seconds. Results include specific citations, 
            confidence scores, and remediation recommendations.
          </p>
        </div>
      </div>
    </div>
  );
}