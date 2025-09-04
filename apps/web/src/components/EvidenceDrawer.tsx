'use client';

import React, { Fragment, useEffect, useRef } from 'react';
import { Dialog, Transition } from '@headlessui/react';
import DOMPurify from 'isomorphic-dompurify';
import VerdictBadge from './VerdictBadge';
import type { Finding } from '@/lib/types';
import { useEvidenceHighlighting } from '@/lib/useEvidenceHighlighting';

interface EvidenceDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  finding: Finding | null;
  onOpenPage?: (page: number, offset?: number) => void;
}

function verdictToBadge(v: Finding['verdict']) {
  return v === 'ok' ? 'pass' : v;
}

export default function EvidenceDrawer({ isOpen, onClose, finding, onOpenPage }: EvidenceDrawerProps) {
  const highlighted = useEvidenceHighlighting(finding?.evidence ?? '', finding?.anchors ?? []);
  const panelRef = useRef<HTMLDivElement>(null);
  if (!finding) return null;

  const rationale = finding.rationale ? DOMPurify.sanitize(finding.rationale) : '';

  // When opened, focus the first diff segment and keep focus trapped within the drawer.
  // Tab cycles through diff segments then action buttons; Shift+Tab reverses this order.
  useEffect(() => {
    if (!isOpen || !panelRef.current) return;
    const panel = panelRef.current;

    const getFocusable = () =>
      panel.querySelectorAll<HTMLElement>(
        '[data-anchorkey], button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );

    const firstFocusable =
      panel.querySelector<HTMLElement>('[data-anchorkey]') ||
      panel.querySelector<HTMLElement>('button, [href], [tabindex]:not([tabindex="-1"])');
    firstFocusable?.focus();

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
        return;
      }
      if (e.key !== 'Tab') return;

      const items = Array.from(getFocusable());
      if (items.length === 0) return;
      const first = items[0];
      const last = items[items.length - 1];

      if (e.shiftKey) {
        if (document.activeElement === first) {
          e.preventDefault();
          (last as HTMLElement).focus();
        }
      } else if (document.activeElement === last) {
        e.preventDefault();
        (first as HTMLElement).focus();
      }
    };

    panel.addEventListener('keydown', handleKeyDown);
    return () => panel.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  return (
    <Transition show={isOpen} as={Fragment}>
      <Dialog as="div" className="fixed inset-0 z-50 overflow-y-auto" onClose={onClose} data-testid="evidence-drawer">
        <div className="flex min-h-screen items-center justify-center p-4">
          <Transition.Child
            as={Fragment}
            enter="ease-out duration-300"
            enterFrom="opacity-0"
            enterTo="opacity-100"
            leave="ease-in duration-200"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
          >
            <div className="fixed inset-0 bg-black/30" aria-hidden="true" />
          </Transition.Child>

          <Transition.Child
            as={Fragment}
            enter="ease-out duration-300"
            enterFrom="opacity-0 scale-95"
            enterTo="opacity-100 scale-100"
            leave="ease-in duration-200"
            leaveFrom="opacity-100 scale-100"
            leaveTo="opacity-0 scale-95"
          >
            <Dialog.Panel
              ref={panelRef}
              className="w-full max-w-2xl transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all"
            >
              <div className="flex items-center justify-between">
                <Dialog.Title className="text-lg font-semibold" data-testid="drawer-title">
                  {finding.title}
                </Dialog.Title>
                <VerdictBadge verdict={verdictToBadge(finding.verdict)} />
              </div>

              {finding.rationale && (
                <div className="mt-4 prose" data-testid="rationale" dangerouslySetInnerHTML={{ __html: rationale }} />
              )}

              <div className="mt-4">
                <h4 className="text-sm font-medium">Evidence</h4>
                <div
                  className="mt-2 max-h-64 overflow-y-auto border p-2 text-sm" 
                  data-testid="evidence-panel"
                  // eslint-disable-next-line react/no-danger
                  dangerouslySetInnerHTML={{ __html: highlighted }}
                />
              </div>

              {finding.citations && finding.citations.length > 0 && (
                <div className="mt-4" data-testid="citations">
                  <h4 className="text-sm font-medium">Citations</h4>
                  <ul className="mt-2 space-y-2">
                    {finding.citations.map((c, i) => (
                      <li key={i} className="flex items-start justify-between gap-2 text-sm" data-testid="citation-item">
                        <span>
                          p.{c.page}: {c.text}
                        </span>
                        {onOpenPage && (
                          <button
                            className="text-blue-600 underline"
                            onClick={() => onOpenPage(c.page, c.start)}
                            data-testid="citation-link"
                          >
                            Open on page
                          </button>
                        )}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="mt-6 flex justify-end">
                <button className="rounded bg-gray-200 px-4 py-2 text-sm" onClick={onClose} data-testid="close-button">
                  Close
                </button>
              </div>
            </Dialog.Panel>
          </Transition.Child>
        </div>
      </Dialog>
    </Transition>
  );
}

