"use client";

import { useEffect, useRef, useState } from "react";

type Props = {
  open: boolean;
  onClose: () => void;
  onConfirm?: (opts: { includeLogo: boolean; includeMeta: boolean; dateFormat: string }) => void;
};

export default function ExportDialog({ open, onClose, onConfirm }: Props) {
  const [includeLogo, setIncludeLogo] = useState(true);
  const [includeMeta, setIncludeMeta] = useState(true);
  const [dateFormat, setDateFormat] = useState("YYYY-MM-DD");
  const firstBtnRef = useRef<HTMLButtonElement | null>(null);

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") onClose();
    }
    if (open) {
      window.addEventListener("keydown", onKey);
      firstBtnRef.current?.focus();
    }
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  if (!open) return null;
  return (
    <div
      className="fixed inset-0 z-50 bg-black/30 flex items-center justify-center"
      role="dialog"
      aria-modal="true"
      aria-labelledby="export-title"
    >
      <div className="w-full max-w-md bg-white dark:bg-zinc-900 rounded-lg p-5 shadow-xl">
        <div className="flex items-center justify-between mb-3">
          <h2 id="export-title" className="text-lg font-semibold">Export Report</h2>
          <button ref={firstBtnRef} className="text-sm rounded border px-2 py-1 focus:ring-2 focus:ring-offset-2 focus:ring-black" onClick={onClose} aria-label="Close export dialog">
            Close
          </button>
        </div>

        <div className="space-y-3 text-sm">
          <label className="flex items-center gap-2">
            <input type="checkbox" checked={includeLogo} onChange={(e) => setIncludeLogo(e.target.checked)} />
            Include logo
          </label>
          <label className="flex items-center gap-2">
            <input type="checkbox" checked={includeMeta} onChange={(e) => setIncludeMeta(e.target.checked)} />
            Include metadata (filename, checksum)
          </label>
          <label className="block">
            <span className="block mb-1">Date format</span>
            <select
              className="border rounded px-2 py-1 w-full"
              value={dateFormat}
              onChange={(e) => setDateFormat(e.target.value)}
            >
              <option>YYYY-MM-DD</option>
              <option>DD/MM/YYYY</option>
              <option>MMM D, YYYY</option>
            </select>
          </label>
        </div>

        <div className="mt-4 flex justify-end gap-2">
          <button className="rounded border px-3 py-1 text-sm" onClick={onClose}>
            Cancel
          </button>
          <button
            className="rounded bg-black text-white px-3 py-1 text-sm"
            onClick={() => {
              onConfirm?.({ includeLogo, includeMeta, dateFormat });
              onClose();
            }}
          >
            Export (preview)
          </button>
        </div>
      </div>
    </div>
  );
}
