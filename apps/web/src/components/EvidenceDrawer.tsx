'use client';

import React, { Fragment } from 'react';
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
  if (!finding) return null;

  const rationale = finding.rationale
    ? DOMPurify.sanitize(finding.rationale)
    : '';

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
            <Dialog.Panel className="w-full max-w-2xl transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
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
                <h3 className="text-sm font-medium">Evidence</h3>
                <div
                  className="mt-2 max-h-64 overflow-y-auto border p-2 text-sm"
                  data-testid="evidence-panel"
                  // eslint-disable-next-line react/no-danger
                  dangerouslySetInnerHTML={{ __html: highlighted }}
                />
              </div>

              {finding.citations && finding.citations.length > 0 && (
                <div className="mt-4" data-testid="citations">
                  <h3 className="text-sm font-medium">Citations</h3>
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

