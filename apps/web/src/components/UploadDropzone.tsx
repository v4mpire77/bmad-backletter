"use client";

import React, { useRef, useState } from "react";
import { useRouter } from "next/navigation";

export default function UploadDropzone() {
  const router = useRouter();
  const inputRef = useRef<HTMLInputElement>(null);
  const [localError, setLocalError] = useState<string | null>(null);
  const [networkError, setNetworkError] = useState<Error | null>(null);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState<"idle" | "uploading" | "queued">("idle");

  if (networkError) throw networkError;

  const handleFiles = (files: FileList | null) => {
    const file = files?.[0];
    if (!file) return;

    if (!/\.(pdf|docx)$/i.test(file.name)) {
      setLocalError("Only PDF or DOCX files are allowed");
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setLocalError("File must be 10MB or less");
      return;
    }

    setLocalError(null);
    const body = new FormData();
    // FastAPI expects field name "file"
    body.append("file", file);
    const xhr = new XMLHttpRequest();
    const apiBase = (process.env.NEXT_PUBLIC_API_URL ?? "").replace(/\/$/, "");
    const endpoint = `${apiBase}/api/contracts`;
    xhr.open("POST", endpoint);
    xhr.upload.onprogress = (e) => {
      if (e.lengthComputable) {
        setStatus("uploading");
        setProgress(Math.round((e.loaded / e.total) * 100));
      }
    };
    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        try {
          const parsed = JSON.parse(xhr.responseText || "{}");
          const nextStatus = parsed?.status ?? "queued";
          const redirectId = parsed?.analysis_id ?? parsed?.job_id ?? parsed?.id;
          setStatus(nextStatus);
          if (!redirectId) {
            setNetworkError(new Error("Invalid server response"));
            return;
          }
          router.push(`/analyses/${redirectId}`);
        } catch (e) {
          setNetworkError(new Error("Upload failed"));
        }
      } else {
        const msg = xhr.responseText || "Upload failed";
        setNetworkError(new Error(msg || "Upload failed"));
      }
    };
    xhr.onerror = () => setNetworkError(new Error("Upload failed"));
    xhr.send(body);
  };

  const onDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    handleFiles(e.dataTransfer.files);
  };

  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    handleFiles(e.target.files);
  };

  return (
    <div
      className="rounded-2xl border p-8 text-center cursor-pointer"
      onDragOver={(e) => e.preventDefault()}
      onDrop={onDrop}
      onClick={() => inputRef.current?.click()}
      role="button"
      tabIndex={0}
    >
      {status === "uploading"
        ? `${progress}%`
        : status === "queued"
        ? "Queued"
        : "Drop PDF or DOCX here"}
      {status === "uploading" && (
        <div className="mt-4 w-full bg-gray-200 rounded" aria-label="upload-progress">
          <div
            className="h-2 bg-blue-500 rounded"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.docx"
        className="hidden"
        onChange={onChange}
      />
      {localError && (
        <p role="alert" className="mt-2 text-sm text-red-600">
          {localError}
        </p>
      )}
    </div>
  );
}

export class UploadErrorBoundary extends React.Component<
  React.PropsWithChildren,
  { hasError: boolean }
> {
  constructor(props: React.PropsWithChildren) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return (
        <p role="alert" className="text-sm text-red-600">
          Upload failed
        </p>
      );
    }
    return this.props.children;
  }
}
