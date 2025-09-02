'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import GdprBadge from '@/components/GdprBadge';
import { uploadWithProgress } from '@/lib/uploader';
import { validateFile, ACCEPTED_TYPES, MAX_BYTES } from '@/lib/validation';

type Queued = {
  id: string;
  file: File;
  status: 'queued' | 'uploading' | 'success' | 'error' | 'canceled';
  progress: number;
  error?: string;
  analysisId?: string;
  abort?: AbortController;
};

export default function UploadContracts() {
  const inputRef = React.useRef<HTMLInputElement | null>(null);
  const [items, setItems] = React.useState<Queued[]>([]);
  const [dragOver, setDragOver] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  function onChoose() {
    inputRef.current?.click();
  }

  function addFiles(files: FileList | File[]) {
    const arr = Array.from(files);
    const next: Queued[] = [];
    for (const f of arr) {
      const v = validateFile(f);
      if (!v.ok) {
        setError(v.reason ?? 'Unsupported file');
        continue;
      }
      next.push({ id: crypto.randomUUID(), file: f, status: 'queued', progress: 0 });
    }
    if (next.length) {
      setError(null);
      setItems((prev) => [...next, ...prev]);
    }
  }

  async function onDrop(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault();
    setDragOver(false);
    if (e.dataTransfer.files?.length) addFiles(e.dataTransfer.files);
  }

  function onInput(e: React.ChangeEvent<HTMLInputElement>) {
    if (e.target.files?.length) addFiles(e.target.files);
    e.target.value = '';
  }

  function removeItem(id: string) {
    setItems((prev) => prev.filter((x) => x.id !== id));
  }

  async function startUpload(item: Queued) {
    setItems((prev) =>
      prev.map((x) => (x.id === item.id ? { ...x, status: 'uploading', progress: 0 } : x))
    );
    const controller = new AbortController();
    setItems((prev) => prev.map((x) => (x.id === item.id ? { ...x, abort: controller } : x)));

    try {
      const { analysisId } = await uploadWithProgress({
        file: item.file,
        url: '/api/contracts',
        fieldName: 'file',
        onProgress: (p) => {
          setItems((prev) => prev.map((x) => (x.id === item.id ? { ...x, progress: p } : x)));
        },
        signal: controller.signal,
      });

      setItems((prev) =>
        prev.map((x) =>
          x.id === item.id ? { ...x, status: 'success', progress: 100, analysisId } : x
        )
      );
    } catch (err: any) {
      if (controller.signal.aborted) {
        setItems((prev) => prev.map((x) => (x.id === item.id ? { ...x, status: 'canceled' } : x)));
        return;
      }
      const msg = err?.message ?? 'Upload failed';
      setItems((prev) => prev.map((x) => (x.id === item.id ? { ...x, status: 'error', error: msg } : x)));
    }
  }

  async function uploadAll() {
    const toUpload = items.filter((x) => x.status === 'queued');
    for (const item of toUpload) {
      // eslint-disable-next-line no-await-in-loop
      await startUpload(item);
    }
  }

  function cancel(id: string) {
    setItems((prev) =>
      prev.map((x) => {
        if (x.id === id) {
          x.abort?.abort();
          return { ...x, status: 'canceled' };
        }
        return x;
      })
    );
  }

  async function tryDemo() {
    try {
      const resp = await fetch('/sample/demo-contract.pdf');
      const blob = await resp.blob();
      const file = new File([blob], 'demo-contract.pdf', { type: 'application/pdf' });
      addFiles([file]);
    } catch {
      setError('Demo file unavailable');
    }
  }

  return (
    <div className="space-y-6">
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setDragOver(true);
        }}
        onDragLeave={() => setDragOver(false)}
        onDrop={onDrop}
        className={cn(
          'cursor-pointer rounded-2xl border border-dashed p-8 text-center transition',
          dragOver ? 'border-primary bg-primary/5' : 'border-muted-foreground/30'
        )}
        role="region"
        aria-label="Upload contracts"
      >
        <div className="flex flex-col items-center gap-3">
          <p className="text-base font-medium">Drag & drop your contract here</p>
          <p className="text-sm text-muted-foreground">or</p>
          <div className="flex gap-2">
            <Button onClick={onChoose}>Choose file</Button>
            <Button variant="secondary" onClick={tryDemo}>
              Try a demo file
            </Button>
          </div>
          <input
            ref={inputRef}
            type="file"
            accept={ACCEPTED_TYPES.join(',')}
            multiple
            onChange={onInput}
            className="hidden"
          />
          <p className="mt-3 text-xs text-muted-foreground">
            Accepted: {ACCEPTED_TYPES.join(', ')} • Max {(MAX_BYTES / (1024 * 1024)).toFixed(0)}MB each
          </p>
          <GdprBadge />
          {error && <p className="text-xs text-red-600">{error}</p>}
        </div>
      </div>

      {items.length > 0 && (
        <div className="space-y-3">
          {items.map((item) => (
            <div key={item.id} className="rounded-md border p-4">
              <div className="flex items-center justify-between gap-3">
                <div className="min-w-0">
                  <p className="truncate text-sm font-medium">{item.file.name}</p>
                  <p className="text-xs text-muted-foreground">
                    {(item.file.size / 1024 / 1024).toFixed(2)} MB • {item.file.type || 'unknown'}
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  {item.status === 'queued' && (
                    <Button size="sm" onClick={() => startUpload(item)}>
                      Upload
                    </Button>
                  )}
                  {item.status === 'uploading' && (
                    <Button size="sm" variant="destructive" onClick={() => cancel(item.id)}>
                      Cancel
                    </Button>
                  )}
                  {(item.status === 'queued' || item.status === 'canceled' || item.status === 'error') && (
                    <Button size="sm" variant="ghost" onClick={() => removeItem(item.id)}>
                      Remove
                    </Button>
                  )}
                  {item.status === 'success' && item.analysisId && (
                    <a
                      className="text-sm underline underline-offset-4"
                      href={`/analyses/${item.analysisId}`}
                    >
                      View analysis →
                    </a>
                  )}
                </div>
              </div>
              <div className="mt-3">
                {item.status === 'uploading' && <Progress value={item.progress} />}
                {item.status === 'success' && <Progress value={100} />}
                {item.status === 'error' && (
                  <p className="mt-1 text-xs text-red-600">Error: {item.error ?? 'Upload failed'}</p>
                )}
                {item.status === 'canceled' && (
                  <p className="mt-1 text-xs text-muted-foreground">Canceled</p>
                )}
              </div>
            </div>
          ))}

          {items.some((x) => x.status === 'queued') && (
            <div className="flex justify-end">
              <Button onClick={uploadAll}>Upload all</Button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
