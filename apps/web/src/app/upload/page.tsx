"use client";

import React, { useRef, useState } from "react";
import { useRouter } from "next/navigation";

export default function UploadPage() {
  const router = useRouter();
  const inputRef = useRef<HTMLInputElement>(null);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<"idle" | "queued">("idle");
  const [retryFile, setRetryFile] = useState<File | null>(null);

  const handleFile = async (file: File) => {
    if (!/\.(pdf|docx)$/i.test(file.name)) {
      setError("Only PDF or DOCX files are allowed");
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setError("File must be 10MB or less");
      return;
    }
    setRetryFile(file);
    setError(null);
    try {
      const body = new FormData();
      body.append("file", file);
      const res = await fetch("/v1/docs/upload", { method: "POST", body });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error(data.detail || data.message || "Upload failed");
      }
      setStatus(data.status);
      router.push(`/analyses/${data.analysis_id}`);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Upload failed");
    }
  };

  const onDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    const file = e.dataTransfer.files?.[0];
    if (file) void handleFile(file);
  };

  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) void handleFile(file);
  };

  return (
    <div className="space-y-3">
      <h1 className="text-2xl font-semibold">Upload a contract</h1>
      <p className="text-sm text-muted-foreground">
        Drop a file to create a new analysis.
      </p>
      <div
        className="rounded-2xl border p-8 text-center cursor-pointer"
        onDragOver={(e) => e.preventDefault()}
        onDrop={onDrop}
        onClick={() => inputRef.current?.click()}
        role="button"
        tabIndex={0}
      >
        {status === "queued" ? "Queued" : "Drop PDF or DOCX here"}
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx"
          className="hidden"
          onChange={onChange}
        />
      </div>
      {error && (
        <div className="space-y-2">
          <p role="alert" className="text-sm text-red-600">
            {error}
          </p>
          {retryFile && (
            <button
              onClick={() => handleFile(retryFile)}
              className="text-sm underline"
            >
              Retry
            </button>
          )}
        </div>
      )}
    </div>
  );
}
