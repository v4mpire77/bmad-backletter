'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import VerdictBadge from '@/components/VerdictBadge';

export default function Dashboard() {
  const [darkMode, setDarkMode] = useState(false);
  const [mockEnabled, setMockEnabled] = useState(false);

  // Check if mocks are enabled
  useEffect(() => {
    setMockEnabled(process.env.NEXT_PUBLIC_USE_MOCKS === '1');
  }, []);

  // Toggle dark mode
  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  return (
    <div className={darkMode ? 'min-h-screen bg-gray-900 text-white' : 'min-h-screen bg-gray-50 text-gray-900'}>
      <div className="p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold">
              Blackletter Dashboard
            </h1>
            <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
              {mockEnabled 
                ? 'Demo mode enabled with mock data' 
                : 'Connect to API for real data'}
            </p>
          </div>
          
          <div className="flex items-center gap-4">
            {/* Mock Status */}
            <div className={`px-3 py-1 rounded-full text-sm flex items-center gap-2 ${
              mockEnabled 
                ? 'bg-green-100 text-green-800' 
                : 'bg-red-100 text-red-800'
            }`}>
              <div className={`w-2 h-2 rounded-full ${
                mockEnabled ? 'bg-green-500' : 'bg-red-500'
              }`} />
              {mockEnabled ? 'MOCK' : 'LIVE'}
            </div>

            {/* Dark Mode Toggle */}
            <button
              onClick={toggleDarkMode}
              className="p-2 rounded-lg border hover:bg-gray-100 dark:hover:bg-gray-800"
            >
              {darkMode ? (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clipRule="evenodd" />
                </svg>
              ) : (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
                </svg>
              )}
            </button>
          </div>
        </div>

        {/* Main Content */}
        <div className="space-y-6">
          {/* Demo Contract Card */}
          <div className={`rounded-lg shadow ${darkMode ? 'bg-gray-800' : 'bg-white'} p-6`}>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold">Demo Contract</h2>
              {mockEnabled && (
                <Link 
                  href="/analyses/mock-1"
                  className="inline-flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  View Analysis
                  <svg xmlns="http://www.w3.org/2000/svg" className="ml-2 h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </Link>
              )}
            </div>
            
            <div className="flex items-start">
              <div className={`flex-shrink-0 w-16 h-16 rounded-lg flex items-center justify-center ${darkMode ? 'bg-gray-700' : 'bg-gray-100'}`}>
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-blue-500" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
                </svg>
              </div>
              
              <div className="ml-4 flex-grow">
                <h3 className="text-lg font-medium">ACME_DPA_MOCK.pdf</h3>
                <p className={`mt-1 text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                  This is a mock contract for demonstration purposes.
                </p>
                
                {mockEnabled ? (
                  <div className="mt-4 flex flex-wrap gap-2">
                    <VerdictBadge verdict="pass" />
                    <VerdictBadge verdict="weak" />
                    <VerdictBadge verdict="missing" />
                    <VerdictBadge verdict="needs_review" />
                  </div>
                ) : (
                  <div className="mt-4">
                    <p className={`text-sm ${darkMode ? 'text-red-400' : 'text-red-600'}`}>
                      Demo mode is disabled. Enable it by setting NEXT_PUBLIC_USE_MOCKS=1 in your environment.
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Additional Content */}
          <div className={`rounded-lg shadow ${darkMode ? 'bg-gray-800' : 'bg-white'} p-6`}>
            <h2 className="text-xl font-semibold mb-4">Getting Started</h2>
            <p className={`mb-4 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
              {mockEnabled
                ? 'Click "View Analysis" above to see the demo contract analysis. You can also upload your own contracts for analysis.'
                : 'To use the demo mode, set NEXT_PUBLIC_USE_MOCKS=1 in your environment variables. This will enable mock data for demonstration purposes.'}
            </p>
            
            <div className="flex flex-wrap gap-2">
              <Link 
                href="/upload"
                className="inline-flex items-center px-4 py-2 bg-green-600 text-white text-sm font-medium rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
              >
                Upload Contract
              </Link>
              <Link 
                href="/reports"
                className="inline-flex items-center px-4 py-2 bg-purple-600 text-white text-sm font-medium rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
              >
                View Reports
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}