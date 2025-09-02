"use client";

import React from "react";
import { UploadErrorBoundary, default as UploadDropzone } from "@/components/UploadDropzone";

export default function UploadPage() {
  return (
    <div className="space-y-3">
      <h1 className="text-2xl font-semibold">Upload a contract</h1>
      <p className="text-sm text-muted-foreground">
        Drop a file to create a new analysis.
      </p>
      <UploadErrorBoundary>
        <UploadDropzone />
      </UploadErrorBoundary>
    </div>
  );
}
