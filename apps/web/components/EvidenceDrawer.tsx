"use client";
import { useState } from "react";

export default function EvidenceDrawer() {
  const [open, setOpen] = useState(false);
  return (
    <>
      <button className="rounded border px-3 py-1" onClick={() => setOpen(true)}>Open Evidence</button>
      {open && (
        <div className="fixed inset-0 bg-black/40">
          <div className="absolute right-0 top-0 h-full w-full max-w-xl bg-white p-6 shadow-2xl">
            <button className="text-sm underline" onClick={() => setOpen(false)}>Close</button>
            <h3 className="text-lg font-medium mt-4">Evidence</h3>
            <p className="text-sm text-neutral-600">Wire this to a selected finding later.</p>
          </div>
        </div>
      )}
    </>
  );
}
