type UploadArgs = {
  url: string;
  file: File;
  fieldName?: string;
  onProgress?: (percent: number) => void;
  signal?: AbortSignal;
};

// Uses XMLHttpRequest to provide upload progress.
export function uploadWithProgress({ url, file, fieldName = 'file', onProgress, signal }: UploadArgs) {
  return new Promise<{ analysisId: string }>((resolve, reject) => {
    const form = new FormData();
    form.append(fieldName, file);

    const xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);

    const abortHandler = () => {
      xhr.abort();
      reject(new DOMException('AbortError', 'AbortError'));
    };
    signal?.addEventListener('abort', abortHandler, { once: true });

    xhr.upload.onprogress = (e) => {
      if (!e.lengthComputable) return;
      const pct = Math.round((e.loaded / e.total) * 100);
      onProgress?.(pct);
    };

    xhr.onreadystatechange = () => {
      if (xhr.readyState !== XMLHttpRequest.DONE) return;
      try {
        if (xhr.status >= 200 && xhr.status < 300) {
          const json = JSON.parse(xhr.responseText || '{}');
          resolve({ analysisId: json.analysisId ?? json.id ?? '' });
        } else {
          reject(new Error(`HTTP ${xhr.status}: ${xhr.responseText || 'Upload failed'}`));
        }
      } catch (err) {
        reject(err);
      } finally {
        signal?.removeEventListener('abort', abortHandler);
      }
    };

    xhr.onerror = () => {
      reject(new Error('Network error'));
      signal?.removeEventListener('abort', abortHandler);
    };

    xhr.send(form);
  });
}
