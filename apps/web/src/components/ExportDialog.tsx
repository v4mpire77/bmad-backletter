'use client';

import React, { useEffect, useRef, useState } from 'react';

interface ExportDialogProps {
  isOpen: boolean;
  onClose: () => void;
  analysisId: string;
}

export default function ExportDialog({
  isOpen,
  onClose,
  analysisId,
}: ExportDialogProps) {
  const dialogRef = useRef<HTMLDivElement>(null);
  const [includeLogo, setIncludeLogo] = useState(true);
  const [includeMeta, setIncludeMeta] = useState(true);
  const [dateFormat, setDateFormat] = useState('mm/dd/yyyy');

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      } else if (e.key === 'Tab' && dialogRef.current) {
        const focusable = dialogRef.current.querySelectorAll<HTMLElement>(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        if (focusable.length === 0) {
          return;
        }
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (e.shiftKey) {
          if (document.activeElement === first) {
            e.preventDefault();
            last.focus();
          }
        } else {
          if (document.activeElement === last) {
            e.preventDefault();
            first.focus();
          }
        }
      }
    };

    if (isOpen) {
      dialogRef.current?.focus();
      document.addEventListener('keydown', handleKeyDown);
    }
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  const handleConfirm = async () => {
    try {
      const res = await fetch(`/api/reports/${analysisId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          include_logo: includeLogo,
          include_meta: includeMeta,
          date_format: dateFormat,
        }),
      });

      if (!res.ok) {
        throw new Error('Failed to export');
      }

      const { url } = await res.json();
      const link = document.createElement('a');
      link.href = url;
      link.download = '';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      onClose();
    } catch (err) {
      // eslint-disable-next-line no-console
      console.error(err);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="fixed inset-0 bg-black/50" onClick={onClose} />
      <div
        ref={dialogRef}
        tabIndex={-1}
        className="relative z-10 rounded bg-white p-4 shadow-md"
      >
        <p className="mb-4">Export this analysis?</p>
        <div className="mb-4 space-y-2">
          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={includeLogo}
              onChange={(e) => setIncludeLogo(e.target.checked)}
            />
            Include logo
          </label>
          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={includeMeta}
              onChange={(e) => setIncludeMeta(e.target.checked)}
            />
            Include metadata
          </label>
          <label className="flex flex-col gap-1">
            Date format
            <select
              value={dateFormat}
              onChange={(e) => setDateFormat(e.target.value)}
              className="border p-1"
            >
              <option value="mm/dd/yyyy">MM/DD/YYYY</option>
              <option value="dd/mm/yyyy">DD/MM/YYYY</option>
              <option value="yyyy-mm-dd">YYYY-MM-DD</option>
            </select>
          </label>
        </div>
        <div className="flex justify-end gap-2">
          <button onClick={onClose}>Cancel</button>
          <button onClick={handleConfirm}>Confirm</button>
        </div>
      </div>
    </div>
  );
}
