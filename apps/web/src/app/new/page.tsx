'use client';

import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useRouter } from 'next/navigation';

const UploadPage = () => {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [uploadStep, setUploadStep] = useState<
    'idle' | 'queued' | 'extracting' | 'detecting' | 'reporting' | 'done'
  >('idle');
  const [progress, setProgress] = useState(0);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Mock state machine logic
  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (uploadStep !== 'idle' && uploadStep !== 'done') {
      timer = setTimeout(() => {
        switch (uploadStep) {
          case 'queued':
            setUploadStep('extracting');
            setProgress(25);
            break;
          case 'extracting':
            setUploadStep('detecting');
            setProgress(50);
            break;
          case 'detecting':
            setUploadStep('reporting');
            setProgress(75);
            break;
          case 'reporting':
            setUploadStep('done');
            setProgress(100);
            break;
          default:
            break;
        }
      }, 900); // ~0.9s per step
    }
    return () => clearTimeout(timer);
  }, [uploadStep]);

  const handleFileChange = (selectedFile: File) => {
    setFile(selectedFile);
    setUploadStep('queued');
    setProgress(0);
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
  }, []);

  const handleViewFindings = () => {
    router.push('/analyses/mock-1');
  };

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
    const steps = ['queued', 'extracting', 'detecting', 'reporting', 'done'];
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
                <span>Extracting</span>
                <span>Detecting</span>
                <span>Reporting</span>
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
                  className={getStepStatus('queued') === 'completed' ? 'text-green-600' : getStepStatus('queued') === 'active' ? 'text-blue-600 font-semibold' : ''}
                >
                  Queued
                </span>
                <span
                  aria-current={getStepStatus('extracting') === 'active' ? 'step' : undefined}
                  className={getStepStatus('extracting') === 'completed' ? 'text-green-600' : getStepStatus('extracting') === 'active' ? 'text-blue-600 font-semibold' : ''}
                >
                  Extracting
                </span>
                <span
                  aria-current={getStepStatus('detecting') === 'active' ? 'step' : undefined}
                  className={getStepStatus('detecting') === 'completed' ? 'text-green-600' : getStepStatus('detecting') === 'active' ? 'text-blue-600 font-semibold' : ''}
                >
                  Detecting
                </span>
                <span
                  aria-current={getStepStatus('reporting') === 'active' ? 'step' : undefined}
                  className={getStepStatus('reporting') === 'completed' ? 'text-green-600' : getStepStatus('reporting') === 'active' ? 'text-blue-600 font-semibold' : ''}
                >
                  Reporting
                </span>
                <span
                  aria-current={getStepStatus('done') === 'active' ? 'step' : undefined}
                  className={getStepStatus('done') === 'completed' ? 'text-green-600' : getStepStatus('done') === 'active' ? 'text-blue-600 font-semibold' : ''}
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
        {file && uploadStep === 'idle' && (
          <p className="mt-4 text-sm text-gray-500 text-center">
            Selected file: {file.name}
          </p>
        )}
      </div>
    </div>
  );
};

export default UploadPage;