"use client";

import { useEffect, useMemo, useRef, useState } from "react";

type Step = "queued" | "extracting" | "detecting" | "reporting" | "done";

const STEPS: Step[] = ["queued", "extracting", "detecting", "reporting", "done"];

function label(step: Step) {
  switch (step) {
    case "queued":
      return "Queued";
    case "extracting":
      return "Extracting";
    case "detecting":
      return "Detecting";
    case "reporting":
      return "Reporting";
    case "done":
      return "Done";
  }
}

export default function NewUploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [stepIndex, setStepIndex] = useState(0);
  const [running, setRunning] = useState(false);
  const [canceled, setCanceled] = useState(false);
  const timerRef = useRef<number | null>(null);

  const mockMode = process.env.NEXT_PUBLIC_USE_MOCKS === "1";

  const current = STEPS[Math.min(stepIndex, STEPS.length - 1)];

  const pickFile = (f: File | null) => {
    if (!f) return;
    setFile(f);
    setStepIndex(0);
    setCanceled(false);
    setRunning(true);
  };

  // ESC to cancel/reset simulation
  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") {
        cancel();
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Advance state machine on a timer when running
  useEffect(() => {
    if (!running) return;
    if (stepIndex >= STEPS.length - 1) return;

    // Deterministic vs jittered durations
    const base = mockMode ? 900 : 1100;
    const jitter = mockMode ? 0 : Math.floor(Math.random() * 600) - 300; // +/- 300ms
    const delay = Math.max(400, base + jitter);

    timerRef.current = window.setTimeout(() => {
      setStepIndex((i) => Math.min(i + 1, STEPS.length - 1));
    }, delay) as unknown as number;

    return () => {
      if (timerRef.current) window.clearTimeout(timerRef.current);
    };
  }, [running, stepIndex, mockMode]);

  function cancel() {
    if (timerRef.current) window.clearTimeout(timerRef.current);
    setRunning(false);
    setCanceled(true);
  }

  function reset() {
    if (timerRef.current) window.clearTimeout(timerRef.current);
    setFile(null);
    setStepIndex(0);
    setCanceled(false);
    setRunning(false);
  }

  const progress = useMemo(() => ((stepIndex + 1) / STEPS.length) * 100, [stepIndex]);

  return (
    <div className="mx-auto max-w-3xl p-8">
      <h1 className="text-2xl font-semibold mb-4">New Analysis</h1>

      {!file && (
        <DropZone onPick={pickFile} />
      )}

      {file && (
        <div className="space-y-4" aria-live="polite">
          <div className="border rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">{file.name}</p>
                <p className="text-xs text-gray-500">{Math.round(file.size / 1024)} KB</p>
              </div>
              <div className="flex gap-2">
                {!running && current !== "done" && (
                  <button className="rounded border px-3 py-1 text-sm" onClick={() => setRunning(true)}>
                    Resume
                  </button>
                )}
                {running && (
                  <button aria-label="Cancel upload simulation" className="rounded border px-3 py-1 text-sm" onClick={cancel}>
                    Cancel
                  </button>
                )}
                <button className="rounded border px-3 py-1 text-sm" onClick={reset}>
                  Start over
                </button>
              </div>
            </div>

            <div className="mt-4">
              <ol className="flex items-center justify-between gap-2" aria-label="Upload steps">
                {STEPS.map((s, i) => (
                  <li key={s} className="flex-1">
                    <div className="flex items-center gap-2">
                      <div
                        aria-label={`${label(s)} ${i <= stepIndex ? "(completed or active)" : "(upcoming)"}`}
                        className={`w-6 h-6 rounded-full border flex items-center justify-center text-xs ${
                          i < stepIndex
                            ? "bg-emerald-500 text-white border-emerald-500"
                            : i === stepIndex
                            ? "bg-sky-500 text-white border-sky-500"
                            : "bg-white border-gray-300"
                        }`}
                      >
                        {i < stepIndex ? "✓" : i + 1}
                      </div>
                      <span className="text-sm">{label(s)}</span>
                    </div>
                  </li>
                ))}
              </ol>

              <div className="mt-4 h-2 bg-gray-200 rounded">
                <div
                  className="h-2 bg-black rounded"
                  style={{ width: `${progress}%`, transition: "width 300ms ease" }}
                  role="progressbar"
                  aria-valuemin={0}
                  aria-valuemax={100}
                  aria-valuenow={Math.floor(progress)}
                  aria-label={`Upload progress: ${Math.floor(progress)} percent`}
                />
              </div>

              {canceled && (
                <p className="mt-2 text-sm text-amber-700">Simulation canceled. Press Resume to continue or Start over.</p>
              )}
            </div>
          </div>

          {current === "done" && (
            <div className="flex items-center justify-end gap-2">
              <a
                href="/analyses/mock-1"
                className="rounded bg-black text-white px-4 py-2 text-sm focus:ring-2 focus:ring-offset-2 focus:ring-black"
              >
                View Findings
              </a>
              <button className="rounded border px-4 py-2 text-sm" onClick={reset}>
                Start over
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function DropZone({ onPick }: { onPick: (f: File | null) => void }) {
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement | null>(null);

  function onDrop(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault();
    setDragging(false);
    const f = e.dataTransfer.files?.[0] || null;
    onPick(f);
  }

  return (
    <div
      className={`border-2 border-dashed rounded-lg p-10 text-center ${dragging ? "bg-black/5" : ""}`}
      onDragOver={(e) => {
        e.preventDefault();
        setDragging(true);
      }}
      onDragLeave={() => setDragging(false)}
      onDrop={onDrop}
      role="region"
      aria-label="File upload dropzone"
    >
      <p className="mb-2 text-sm">Drag and drop a contract file</p>
      <p className="text-xs text-gray-500 mb-4">or</p>
      <button
        className="rounded bg-black text-white px-3 py-2 text-sm focus:ring-2 focus:ring-offset-2 focus:ring-black"
        onClick={() => inputRef.current?.click()}
      >
        Choose File
      </button>
      <input
        ref={inputRef}
        type="file"
        className="hidden"
        onChange={(e) => onPick(e.target.files?.[0] || null)}
        aria-hidden
        tabIndex={-1}
      />
    </div>
  );
}

