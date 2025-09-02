"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { UploadDropzone } from "../../components/upload-dropzone";

export default function UploadPage() {
  const router = useRouter();
  const [disabled, setDisabled] = useState(false);

  const handleUpload = async (file: File) => {
    setDisabled(true);
    try {
      const body = new FormData();
      body.append("file", file);
      const res = await fetch("/api/uploads", { method: "POST", body });
      if (!res.ok) throw new Error("upload_failed");
      const { analysis_id } = await res.json();
      router.push(`/analyses/${analysis_id}`);
    } catch (e) {
      setDisabled(false);
      throw e;
    }
  };

  return (
    <div className="space-y-3">
      <h1 className="text-2xl font-semibold">Upload a contract</h1>
      <p className="text-sm text-muted-foreground">
        Drop a file to create a new analysis.
      </p>
      <UploadDropzone onUpload={handleUpload} disabled={disabled} />
    </div>
  );
}
