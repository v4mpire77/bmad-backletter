'use client';

import { useState, useRef, useEffect } from 'react';
import { Dialog, DialogPanel, DialogTitle } from '@headlessui/react';
import { useRouter } from 'next/navigation';
import { addMockExport } from '@/lib/mockStore';

interface ExportDialogProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function ExportDialog({ isOpen, onClose }: ExportDialogProps) {
  const router = useRouter();
  const [includeLogo, setIncludeLogo] = useState(true);
  const [includeMetadata, setIncludeMetadata] = useState(true);
  const [dateFormat, setDateFormat] = useState('mm/dd/yyyy');
  const dialogRef = useRef<HTMLDivElement>(null);

  // Handle ESC key to close the dialog
  useEffect(() => {
    const handleEsc = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEsc);
      // Focus the dialog for accessibility
      dialogRef.current?.focus();
    }

    return () => {
      document.removeEventListener('keydown', handleEsc);
    };
  }, [isOpen, onClose]);

  const handleConfirm = () => {
    // Log the selected options
    const options = {
      includeLogo,
      includeMetadata,
      dateFormat
    };
    
    console.log('Export options selected:', options);
    
    // Add to mock store
    const exportRecord = {
      id: `export-${Date.now()}`,
      fileName: 'ACME_DPA_MOCK.pdf',
      exportedAt: new Date().toISOString(),
      options
    };
    
    addMockExport(exportRecord);
    
    // Navigate to reports page
    router.push('/reports');
    
    // Close the dialog
    onClose();
  };

  return (
    <Dialog open={isOpen} onClose={onClose} className="relative z-50">
      {/* Backdrop */}
      <div className="fixed inset-0 bg-black/30" aria-hidden="true" />

      {/* Dialog panel */}
      <div className="fixed inset-0 flex items-center justify-center p-4">
        <DialogPanel
          ref={dialogRef}
          tabIndex={-1}
          className="w-full max-w-md rounded bg-white p-6 shadow-lg transition-all duration-300 ease-in-out data-[closed]:scale-95 data-[closed]:opacity-0"
        >
          <DialogTitle className="text-lg font-semibold text-gray-900 mb-4">
            Export Options
          </DialogTitle>
          
          <div className="space-y-4">
            <div className="flex items-center">
              <input
                id="include-logo"
                type="checkbox"
                className="h-4 w-4 text-blue-600 border-gray-300 rounded"
                checked={includeLogo}
                onChange={(e) => setIncludeLogo(e.target.checked)}
              />
              <label htmlFor="include-logo" className="ml-2 block text-sm text-gray-900">
                Include Logo
              </label>
            </div>
            
            <div className="flex items-center">
              <input
                id="include-metadata"
                type="checkbox"
                className="h-4 w-4 text-blue-600 border-gray-300 rounded"
                checked={includeMetadata}
                onChange={(e) => setIncludeMetadata(e.target.checked)}
              />
              <label htmlFor="include-metadata" className="ml-2 block text-sm text-gray-900">
                Include Metadata
              </label>
            </div>
            
            <div>
              <label htmlFor="date-format" className="block text-sm font-medium text-gray-700 mb-1">
                Date Format
              </label>
              <select
                id="date-format"
                className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                value={dateFormat}
                onChange={(e) => setDateFormat(e.target.value)}
              >
                <option value="mm/dd/yyyy">MM/DD/YYYY</option>
                <option value="dd/mm/yyyy">DD/MM/YYYY</option>
                <option value="yyyy-mm-dd">YYYY-MM-DD</option>
              </select>
            </div>
          </div>
          
          <div className="mt-6 flex justify-end space-x-3">
            <button
              type="button"
              className="inline-flex justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
              onClick={onClose}
            >
              Cancel
            </button>
            <button
              type="button"
              className="inline-flex justify-center rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
              onClick={handleConfirm}
            >
              Confirm Export
            </button>
          </div>
        </DialogPanel>
      </div>
    </Dialog>
  );
}