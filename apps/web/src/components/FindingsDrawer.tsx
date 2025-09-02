'use client';

import React, { useEffect, useRef } from 'react';

interface FindingsDrawerProps {
  open: boolean;
  onClose: () => void;
  finding?: {
    rule: string;
    evidence: string;
    verdict?: string;
  } | null;
}

export default function FindingsDrawer({ open, onClose, finding }: FindingsDrawerProps) {
  const drawerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      } else if (e.key === 'Tab' && drawerRef.current) {
        const focusable = drawerRef.current.querySelectorAll<HTMLElement>(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        if (focusable.length === 0) return;
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

    if (open) {
      drawerRef.current?.focus();
      document.addEventListener('keydown', handleKeyDown);
    }
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50">
      <div className="fixed inset-0 bg-black/50" onClick={onClose} />
      <div
        ref={drawerRef}
        tabIndex={-1}
        className="absolute right-0 top-0 h-full w-80 bg-white p-6 shadow-lg space-y-4"
      >
        <div>
          <h2 className="text-lg font-semibold mb-2">Finding Details</h2>
          <p className="text-sm"><span className="font-medium">Rule:</span> {finding?.rule}</p>
          <p className="text-sm"><span className="font-medium">Evidence:</span> {finding?.evidence}</p>
          {finding?.verdict && (
            <p className="text-sm"><span className="font-medium">Verdict:</span> {finding.verdict}</p>
          )}
        </div>
        <div className="flex justify-end">
          <button onClick={onClose} className="text-sm underline">Close</button>
        </div>
      </div>
    </div>
  );
}

