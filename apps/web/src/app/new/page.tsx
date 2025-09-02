'use client';

import React, { useState, useCallback, useRef, useEffect } from 'react';
import { useRouter } from 'next/navigation';

const UploadPage = () => {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [uploadStep, setUploadStep] = useState<'idle' | 'queued' | 'processing' | 'done'>(
    'idle',
  );
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const jobRef = useRef<string | null>(null);

  const pollJob = useCallback(async (jobId: string) => {
    const interval = setInterval(async () => {
      const res = await fetch(`/api/jobs/${jobId}`);
      if (!res.ok) {
        return;
      }
      const data = await res.json();
      if (data.status === 'running') {
        setUploadStep('processing');
        setProgress(50);
      }
      if (data.status === 'done') {
        clearInterval(interval);
        setUploadStep('done');
        setProgress(100);
        router.push(`/analyses/${jobId}`);
      }
    }, 1000);
  }, [router]);
  const handleFileChange = async (selectedFile: File) => {
    setFile(selectedFile);
    setUploadStep('queued');
    setProgress(0);
    const fd = new FormData();
    fd.append('file', selectedFile);
    const res = await fetch('/api/contracts', {
      method: 'POST',
      body: fd,
    });
    if (res.ok) {
      const data = await res.json();
      const jobId = data.job_id || data.id;
      jobRef.current = jobId;
      pollJob(jobId);
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileChange(e.dataTransfer.files[0]);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFileChange(e.target.files[0]);
    }
  };

  const handleReset = useCallback(() => {
    setFile(null);
    setUploadStep('idle');
    setProgress(0);
    setError(null);
  }, []);

  const handleViewFindings = () => {
    if (jobRef.current) {
      router.push(`/analyses/${jobRef.current}`);
    }
  };

  useEffect(() => {
    return () => {
      // Cleanup if needed
    };
  }, []);

  // Cancel simulation on ESC key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && uploadStep !== 'idle') {
        handleReset();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [uploadStep, handleReset]);

  const getStepStatus = (step: string) => {
    const steps = ['queued', 'processing', 'done'];
    const currentIndex = steps.indexOf(uploadStep);
    const stepIndex = steps.indexOf(step);

    if (stepIndex < currentIndex) return 'completed';
    if (stepIndex === currentIndex) return 'active';
    return 'pending';
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-4">
      <div className="w-full max-w-md bg-white rounded-lg shadow-md p-6">
        <h1 className="text-2xl font-bold text-center mb-6">Upload Document</h1>
        {uploadStep === 'idle' ? (
          <div
            className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
              isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
            }`}
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onClick={() => fileInputRef.current?.click()}
            role="button"
            tabIndex={0}
            aria-label="Drag and drop area or click to select a file"
          >
            <p className="text-gray-500 mb-2">Drag &apos;n&apos; drop a file here, or click to select</p>
            <p className="text-sm text-gray-400">Supports PDF, DOCX, TXT</p>
            <input
              ref={fileInputRef}
              type="file"
              className="hidden"
              onChange={handleFileInput}
              aria-hidden="true"
            />
          </div>
        ) : (
          <div className="space-y-6">
            <div className="space-y-4">
              <div className="flex justify-between text-sm font-medium">
                <span>Queued</span>
                <span>Processing</span>
                <span>Done</span>
              </div>
              <div className="relative pt-1">
                <div className="flex items-center justify-between">
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div
                      className="bg-blue-600 h-2.5 rounded-full transition-all duration-500 ease-in-out"
                      style={{ width: `${progress}%` }}
                    ></div>
                  </div>
                </div>
              </div>
              <div className="flex justify-between text-xs text-gray-500">
                <span
                  aria-current={getStepStatus('queued') === 'active' ? 'step' : undefined}
                  className={
                    getStepStatus('queued') === 'completed'
                      ? 'text-green-600'
                      : getStepStatus('queued') === 'active'
                      ? 'text-blue-600 font-semibold'
                      : ''
                  }
                >
                  Queued
                </span>
                <span
                  aria-current={getStepStatus('processing') === 'active' ? 'step' : undefined}
                  className={
                    getStepStatus('processing') === 'completed'
                      ? 'text-green-600'
                      : getStepStatus('processing') === 'active'
                      ? 'text-blue-600 font-semibold'
                      : ''
                  }
                >
                  Processing
                </span>
                <span
                  aria-current={getStepStatus('done') === 'active' ? 'step' : undefined}
                  className={
                    getStepStatus('done') === 'completed'
                      ? 'text-green-600'
                      : getStepStatus('done') === 'active'
                      ? 'text-blue-600 font-semibold'
                      : ''
                  }
                >
                  Done
                </span>
              </div>
            </div>

            {uploadStep === 'done' && (
              <div className="flex flex-col space-y-3">
                <button
                  onClick={handleViewFindings}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                  aria-label="View Findings"
                >
                  View Findings
                </button>
                <button
                  onClick={handleReset}
                  className="w-full border border-gray-300 hover:bg-gray-50 text-gray-700 font-medium py-2 px-4 rounded-md transition focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                  aria-label="Start Over"
                >
                  Start Over
                </button>
              </div>
            )}
          </div>
        )}
        {error && (
          <p className="mt-4 text-sm text-red-600 text-center">{error}</p>
        )}
        {file && uploadStep === 'idle' && !error && (
          <p className="mt-4 text-sm text-gray-500 text-center">
            Selected file: {file.name}
          </p>
        )}
      </div>
    </div>
  );
};

export default UploadPage;