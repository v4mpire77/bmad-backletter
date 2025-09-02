'use client';

import React, { useEffect, useRef, useState } from 'react';

interface EvidenceDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
}

export default function EvidenceDrawer({ isOpen, onClose, children }: EvidenceDrawerProps) {
  const drawerRef = useRef<HTMLDivElement>(null);
  const snippetRef = useRef<HTMLDivElement>(null);
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    const text = snippetRef.current?.textContent ?? '';
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (e) {
      console.error('Copy failed', e);
    }
  };

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

    if (isOpen) {
      drawerRef.current?.focus();
      document.addEventListener('keydown', handleKeyDown);
    }
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-40">
      <div className="fixed inset-0 bg-black/50" onClick={onClose} />
      <div
        ref={drawerRef}
        tabIndex={-1}
        className="absolute right-0 top-0 h-full w-80 bg-white p-4 shadow-lg"
      >
        <div ref={snippetRef}>{children}</div>
        <div className="mt-4 flex justify-end space-x-2">
          <button onClick={handleCopy}>Copy</button>
          <button onClick={onClose}>Close</button>
        </div>
        {copied && (
          <div
            role="status"
            className="absolute bottom-4 right-4 rounded bg-gray-800 px-3 py-2 text-white"
          >
            Copied to clipboard
          </div>
        )}
      </div>
    </div>
  );
}
