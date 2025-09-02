"use client";

import React, { useRef, useState } from "react";

export const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
const ACCEPTED_TYPES = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"];

export function validateFile(file: File): string | null {
  if (!ACCEPTED_TYPES.includes(file.type)) {
    return "Only PDF or DOCX files are allowed";
  }
  if (file.size > MAX_FILE_SIZE) {
    return "File must be 10MB or less";
  }
  return null;
}

interface UploadCardProps {
  onJobStart: (jobId: string) => void;
  disabled?: boolean;
}

export default function UploadCard({ onJobStart, disabled }: UploadCardProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFiles = async (files: FileList | null) => {
    const file = files?.[0];
    if (!file) return;

    const validationError = validateFile(file);
    if (validationError) {
      setError(validationError);
      return;
    }

    setError(null);
    const body = new FormData();
    body.append("file", file);
    try {
      const res = await fetch("/api/contracts", { method: "POST", body });
      if (res.status >= 500) {
        setError("Server error. Please try again later.");
        return;
      }
      if (!res.ok) {
        setError("Upload failed");
        return;
      }
      const data = await res.json();
      const id = data.job_id || data.id;
      onJobStart(id);
    } catch {
      setError("Network error. Check your connection.");
    }
  };

  const onDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    handleFiles(e.dataTransfer.files);
  };

  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    handleFiles(e.target.files);
  };

  return (
    <div className="space-y-2">
      {error && (
        <div role="alert" className="rounded bg-red-100 p-2 text-sm text-red-800">
          {error}
        </div>
      )}
      <div
        className="rounded-2xl border p-8 text-center cursor-pointer"
        onDragOver={(e) => e.preventDefault()}
        onDrop={onDrop}
        onClick={() => !disabled && inputRef.current?.click()}
        role="button"
        tabIndex={0}
      >
        Drop PDF or DOCX here
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx"
          className="hidden"
          onChange={onChange}
          disabled={disabled}
        />
      </div>
    </div>
  );
}
