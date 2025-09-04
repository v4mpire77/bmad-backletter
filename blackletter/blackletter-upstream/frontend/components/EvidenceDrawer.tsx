'use client';

import { useState, useRef, useEffect } from 'react';
import { Dialog, DialogPanel, DialogTitle } from '@headlessui/react';
import { Finding } from '@/lib/types';
import { highlightAnchors } from '@/lib/anchors';
import { copyToClipboard } from '@/lib/utils';

interface EvidenceDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  finding: Finding;
}

export default function EvidenceDrawer({ isOpen, onClose, finding }: EvidenceDrawerProps) {
  const [isReviewed, setIsReviewed] = useState(false);
  const drawerRef = useRef<HTMLDivElement>(null);

  // Handle ESC key to close the drawer
  useEffect(() => {
    const handleEsc = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEsc);
      // Focus the drawer for accessibility
      drawerRef.current?.focus();
    }

    return () => {
      document.removeEventListener('keydown', handleEsc);
    };
  }, [isOpen, onClose]);

  // Highlight anchors in the evidence text
  const highlightedEvidence = highlightAnchors(finding.evidence, finding.anchors);

  const handleCopyToClipboard = async () => {
    await copyToClipboard(highlightedEvidence);
    // Could add a toast notification here
  };

  const handleMarkReviewed = () => {
    setIsReviewed(!isReviewed);
    // In a real app, this would update the finding's status in the store
  };

  return (
    <Dialog open={isOpen} onClose={onClose} className="relative z-50">
      {/* Backdrop */}
      <div className="fixed inset-0 bg-black/30" aria-hidden="true" />

      {/* Drawer panel */}
      <div className="fixed inset-0 overflow-hidden">
        <div className="absolute inset-0 overflow-hidden">
          <div className="pointer-events-none fixed inset-y-0 right-0 flex max-w-full pl-10">
            <DialogPanel
              ref={drawerRef}
              tabIndex={-1}
              className="pointer-events-auto w-screen max-w-md transform transition duration-300 ease-in-out data-[closed]:translate-x-full"
            >
              <div className="flex h-full flex-col divide-y divide-gray-200 bg-white shadow-xl">
                <div className="flex min-h-0 flex-1 flex-col overflow-y-scroll">
                  <div className="px-4 py-6 sm:px-6">
                    <div className="flex items-start justify-between">
                      <DialogTitle className="text-lg font-semibold text-gray-900">
                        Evidence for {finding.detector}
                      </DialogTitle>
                      <div className="ml-3 flex h-7 items-center">
                        <button
                          type="button"
                          className="rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none"
                          onClick={onClose}
                        >
                          <span className="sr-only">Close panel</span>
                          <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>
                  <div className="relative flex-1 px-4 py-6 sm:px-6">
                    {/* Evidence content */}
                    <div className="mb-6">
                      <h3 className="text-md font-medium text-gray-900 mb-2">Evidence</h3>
                      <div 
                        className="border p-4 rounded bg-gray-50 max-h-60 overflow-y-auto"
                        dangerouslySetInnerHTML={{ __html: highlightedEvidence }}
                      />
                    </div>

                    {/* Anchors */}
                    <div className="mb-6">
                      <h3 className="text-md font-medium text-gray-900 mb-2">Anchors</h3>
                      <ul className="list-disc pl-5">
                        {finding.anchors.map((anchor, index) => (
                          <li key={index} className="mb-1">
                            {anchor.text} (Page: {anchor.page}, Offset: {anchor.offset})
                          </li>
                        ))}
                      </ul>
                    </div>

                    {/* Verdict and Rationale */}
                    <div className="mb-6">
                      <h3 className="text-md font-medium text-gray-900 mb-2">Verdict</h3>
                      <p className="mb-2">
                        <span className="font-medium">Verdict:</span> {finding.verdict}
                      </p>
                      <p>
                        <span className="font-medium">Rationale:</span> {finding.rationale}
                      </p>
                    </div>
                  </div>
                </div>
                <div className="flex flex-shrink-0 justify-end px-4 py-4">
                  <button
                    type="button"
                    className="mr-2 inline-flex justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                    onClick={handleCopyToClipboard}
                  >
                    Copy to Clipboard
                  </button>
                  <button
                    type="button"
                    className={`mr-2 inline-flex justify-center rounded-md px-3 py-2 text-sm font-semibold text-white shadow-sm ${
                      isReviewed ? 'bg-green-600 hover:bg-green-500' : 'bg-gray-600 hover:bg-gray-500'
                    }`}
                    onClick={handleMarkReviewed}
                  >
                    {isReviewed ? 'Reviewed' : 'Mark as Reviewed'}
                  </button>
                  <button
                    type="button"
                    className="inline-flex justify-center rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
                    onClick={onClose}
                  >
                    Close
                  </button>
                </div>
              </div>
            </DialogPanel>
          </div>
        </div>
      </div>
    </Dialog>
  );
}