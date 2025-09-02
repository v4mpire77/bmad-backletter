'use client';

import { useEffect, useRef, useState } from 'react';
import { Dialog, Transition } from '@headlessui/react';
import type { Finding } from '@/lib/types';
import { highlightAnchors } from '@/lib/anchors';

interface EvidenceDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  finding: Finding | null; // allow null to simplify parent logic
}

export default function EvidenceDrawer({ isOpen, onClose, finding }: EvidenceDrawerProps) {
  const [isReviewed, setIsReviewed] = useState(false);
  const initialFocus = useRef<HTMLButtonElement | null>(null);

  useEffect(() => {
    if (isOpen && finding) {
      // no-op here; actual highlighting occurs in render via helper
    }
  }, [isOpen, finding]);

  if (!finding) return null;

  const highlighted = highlightAnchors(
    finding.snippet,
    finding.anchors ?? [],
    { tag: 'mark', className: 'bg-yellow-200' }
  );

  return (
    <Transition show={isOpen} appear>
      <Dialog as="div" className="fixed inset-0 z-50 overflow-y-auto" onClose={onClose} initialFocus={initialFocus}>
        <div className="min-h-screen px-4 text-center">
          <Transition.Child enter="ease-out duration-300" enterFrom="opacity-0" enterTo="opacity-100" leave="ease-in duration-200" leaveFrom="opacity-100" leaveTo="opacity-0">
            <div className="fixed inset-0 bg-black/30" />
          </Transition.Child>

          <span className="inline-block h-screen align-middle" aria-hidden="true">&#8203;</span>

          <Transition.Child enter="ease-out duration-300" enterFrom="opacity-0 scale-95" enterTo="opacity-100 scale-100" leave="ease-in duration-200" leaveFrom="opacity-100 scale-100" leaveTo="opacity-0 scale-95">
            <Dialog.Panel className="inline-block w-full max-w-2xl p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl">
              <Dialog.Title as="h3" className="text-lg font-semibold text-gray-900">Evidence — {finding.rule_id}</Dialog.Title>
              <div className="mt-3 prose">
                {/* eslint-disable-next-line react/no-danger */}
                <p className="text-sm text-gray-700" dangerouslySetInnerHTML={{ __html: highlighted }} />
              </div>
              {finding.location && (
                <p className="mt-2 text-xs text-gray-500">p.{finding.location.page} [{finding.location.start_char}–{finding.location.end_char}]</p>
              )}
              <div className="mt-6 flex items-center gap-3">
                <button ref={initialFocus} className="px-3 py-2 text-sm rounded-md bg-blue-600 text-white" onClick={onClose}>Close</button>
                <button className="px-3 py-2 text-sm rounded-md bg-gray-100" onClick={() => setIsReviewed(true)}>{isReviewed ? 'Reviewed' : 'Mark reviewed'}</button>
              </div>
            </Dialog.Panel>
          </Transition.Child>
        </div>
      </Dialog>
    </Transition>
  );
}