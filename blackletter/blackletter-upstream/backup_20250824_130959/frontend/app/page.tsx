<<<<<<< HEAD
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
=======
'use client';

import { useState } from 'react';

// DEPLOYMENT TRIGGER: Force new deployment - 2025-08-24 - URGENT FIX
export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/analyze-contract`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(await response.text());
      }

      const data = await response.json();
      setAnalysis(data.analysis);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-violet-900 relative overflow-hidden">
      {/* Tailwind Test - Remove this after verification */}
      <div className="bg-red-500 text-white p-4 text-xl font-bold text-center">
        🔥 TEST: If you see red background, Tailwind is working!
      </div>
      
      {/* Background pattern */}
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiM5Qzk2Q0EiIGZpbGwtb3BhY2l0eT0iMC4xIj48cGF0aCBkPSJtMzYgMzQgNi0ydjEwbC02IDJ6bTAgNCA2LTJ2MTBsLTYgMnoiLz48L2c+PC9nPjwvc3ZnPg==')] opacity-20"></div>
      
      <div className="relative z-10 flex flex-col min-h-screen">
        {/* Header */}
        <header className="px-6 py-8">
          <div className="flex items-center justify-between max-w-7xl mx-auto">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-violet-600 rounded-xl flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">Blackletter Systems</h1>
                <p className="text-purple-300 text-sm">Old rules. New game.</p>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="relative">
                <svg className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <input
                  className="w-96 pl-12 pr-4 py-3 bg-gray-900/50 border border-gray-800/50 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all outline-none backdrop-blur-sm"
                  placeholder="Search contracts, clauses, parties..."
                />
              </div>
              <button className="px-4 py-2 bg-gray-800/50 hover:bg-gray-700/50 border border-gray-700/50 rounded-lg text-gray-300 transition-colors">
                Filter
              </button>
            </div>
          </div>
        </header>

        {/* Main content */}
        <main className="flex-1 px-6 pb-8">
          <div className="max-w-7xl mx-auto">
            {/* Upload Section */}
            <div className="mb-8">
              <h2 className="text-xl font-semibold text-white mb-6">Upload Contract for Review</h2>
              
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="bg-gray-900/30 backdrop-blur-sm border border-gray-800/50 rounded-xl p-8">
                  <div className="border-2 border-dashed border-gray-700 rounded-lg p-12 text-center hover:border-purple-500/50 transition-colors">
                    <div className="w-16 h-16 bg-purple-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                      <svg className="w-8 h-8 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                      </svg>
                    </div>
                    <h3 className="text-lg font-medium text-white mb-2">Upload PDF Contract</h3>
                    <p className="text-gray-400 mb-6">Drag and drop your contract file here, or click to browse</p>
                    
                    <input
                      type="file"
                      accept=".pdf"
                      onChange={(e) => setFile(e.target.files?.[0] || null)}
                      className="hidden"
                      id="file-upload"
                    />
                    <label
                      htmlFor="file-upload"
                      className="inline-flex items-center gap-2 px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white font-medium rounded-lg cursor-pointer transition-colors"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                      </svg>
                      Choose File
                    </label>
                    
                    {file && (
                      <div className="mt-4 p-3 bg-gray-800/50 rounded-lg inline-flex items-center gap-2 text-sm text-gray-300">
                        <svg className="w-4 h-4 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        {file.name}
                      </div>
                    )}
                  </div>
                </div>
                
                <div className="flex justify-center">
                  <button
                    type="submit"
                    disabled={!file || loading}
                    className="px-8 py-3 bg-gradient-to-r from-purple-600 to-violet-600 hover:from-purple-700 hover:to-violet-700 disabled:from-gray-600 disabled:to-gray-700 text-white font-semibold rounded-lg transition-all disabled:cursor-not-allowed flex items-center gap-2"
                  >
                    {loading ? (
                      <>
                        <svg className="animate-spin w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                        Analyzing Contract...
                      </>
                    ) : (
                      <>
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                        </svg>
                        Start Analysis
                      </>
                    )}
                  </button>
                </div>
              </form>
            </div>

            {/* Error display */}
            {error && (
              <div className="mb-8 p-4 bg-red-900/50 border border-red-700/50 rounded-lg text-red-300">
                <div className="flex items-center gap-2">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                  </svg>
                  {error}
                </div>
              </div>
            )}

            {/* Results display */}
            {analysis && (
              <div className="bg-gray-900/30 backdrop-blur-sm border border-gray-800/50 rounded-xl p-6">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                  <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Analysis Complete
                </h3>
                <div className="bg-gray-800/50 rounded-lg p-4 text-gray-300 font-mono text-sm overflow-auto max-h-96">
                  <pre className="whitespace-pre-wrap">{JSON.stringify(analysis, null, 2)}</pre>
                </div>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
>>>>>>> 47931f5adb3b90222b8a8032099a98d6ea0d662a
