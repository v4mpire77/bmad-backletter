"use client";

import React, { useRef, useState } from "react";

interface UploadDropzoneProps {
  onUpload: (file: File) => Promise<void> | void;
  disabled?: boolean;
  messages?: {
    idle?: string;
    queued?: string;
    invalidType?: string;
    tooLarge?: string;
    uploadFailed?: string;
  };
}

export function UploadDropzone({
  onUpload,
  disabled = false,
  messages = {},
}: UploadDropzoneProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [error, setError] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleFiles = async (files: FileList | null) => {
    const file = files?.[0];
    if (!file) return;

    if (!/\.(pdf|docx)$/i.test(file.name)) {
      setError(messages.invalidType ?? "Only PDF or DOCX files are allowed");
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setError(messages.tooLarge ?? "File must be 10MB or less");
      return;
    }

    setError(null);
    try {
      await onUpload(file);
    } catch {
      setError(messages.uploadFailed ?? "Upload failed");
    }
  };

  const onDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    handleFiles(e.dataTransfer.files);
  };

  const onDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (!isDragging) setIsDragging(true);
  };

  const onDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    handleFiles(e.target.files);
  };

  const idleText = messages.idle ?? "Drop PDF or DOCX here";
  const queuedText = messages.queued ?? "Queued";

  return (
    <div className="space-y-3">
      <div
        className={`rounded-2xl border p-8 text-center cursor-pointer${
          isDragging ? " bg-muted" : ""
        }${disabled ? " opacity-50 cursor-not-allowed" : ""}`}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onDrop={onDrop}
        onClick={() => !disabled && inputRef.current?.click()}
        role="button"
        tabIndex={0}
        data-testid="dropzone"
      >
        {disabled ? queuedText : idleText}
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx"
          className="hidden"
          onChange={onChange}
          disabled={disabled}
        />
      </div>
      {error && (
        <p role="alert" className="text-sm text-red-600">
          {error}
        </p>
      )}
    </div>
  );
}

export default UploadDropzone;
