'use client';

import { useState, useEffect } from 'react';
import { Navigation } from '@/components/Navigation';

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [showRaw, setShowRaw] = useState(false);
  const [apiHealth, setApiHealth] = useState<'ok' | 'error' | 'loading'>('loading');

  useEffect(() => {
    checkApiHealth();
  }, []);

  async function checkApiHealth() {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/health`);
      setApiHealth(res.ok ? 'ok' : 'error');
    } catch (e) {
      setApiHealth('error');
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/review`, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        throw new Error(await res.text());
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  }

  function downloadJSON() {
    if (!result) return;
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = (file?.name || 'review') + '.json';
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  function downloadSummaryMd() {
    if (!result) return;
    const md = `# Contract summary\n\n${result.summary || ''}\n\n## Key risks\n\n${(result.risks || [])
      .map((r: string) => `- ${r}`)
      .join('\n')}`;
    const blob = new Blob([md], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = (file?.name || 'review') + '.md';
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  const healthClass = apiHealth === 'ok' ? 'bg-green-500/10 text-green-400 border border-green-500/20' : apiHealth === 'error' ? 'bg-red-500/10 text-red-400 border border-red-500/20' : 'bg-gray-700 text-gray-400 border border-gray-600';
  const dotClass = apiHealth === 'ok' ? 'bg-green-400' : apiHealth === 'error' ? 'bg-red-400' : 'bg-gray-400';

  return (
    <div className="min-h-screen bg-gray-900">
      <Navigation />
      <div className="max-w-3xl mx-auto p-3">
        <div className="mb-2 flex items-center justify-between">
          <div>
            <h1 className="text-base font-medium text-gray-100">Contract Analysis</h1>
            <p className="mt-0.5 text-xs text-gray-400">Upload a contract for review</p>
          </div>

          <div className={`px-1.5 py-0.5 rounded-full text-[10px] flex items-center gap-1 ${healthClass}`}>
            <div className={`w-1.5 h-1.5 rounded-full ${dotClass}`} />
            {apiHealth === 'loading' ? 'Connecting...' : apiHealth.toUpperCase()}
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg border border-gray-700">
          <form onSubmit={handleSubmit} className="p-4">
            <div className="mb-4">
              <div className="flex items-center justify-center w-full">
                <label className="flex flex-col items-center justify-center w-full h-24 rounded border-2 border-dashed border-gray-600 hover:border-gray-500 bg-gray-700/50 hover:bg-gray-700 transition-colors cursor-pointer">
                  <div className="flex flex-col items-center justify-center py-2">
                    <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6 mb-1 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    <p className="text-xs text-gray-400">
                      <span className="font-medium">Upload</span> or drag PDF
                    </p>
                    <p className="text-[10px] text-gray-500 mt-0.5">Max: 10MB</p>
                  </div>
                  <input
                    type="file"
                    accept="application/pdf"
                    onChange={(e) => setFile(e.target.files?.[0] || null)}
                    className="hidden"
                  />
                </label>
              </div>

              {file && (
                <div className="mt-1.5 p-1.5 rounded bg-gray-700/50 border border-gray-600 flex items-center justify-between">
                  <div className="flex items-center gap-1.5">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 0a1 1 0 011-1h6a1 1 0 011 1v12a1 1 0 01-1 1H7a1 1 0 01-1-1V4zm3 3a1 1 0 011-1h2a1 1 0 110 2h-2a1 1 0 01-1-1z" clipRule="evenodd" />
                    </svg>
                    <div>
                      <div className="text-xs font-medium text-gray-200 truncate max-w-[200px]">{file.name}</div>
                      <div className="text-[10px] text-gray-400">{Math.round(file.size/1024)} KB</div>
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => setFile(null)}
                    className="text-gray-400 hover:text-gray-300"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                    </svg>
                  </button>
                </div>
              )}
            </div>

            <div className="flex justify-end">
              <button
                type="submit"
                disabled={!file || loading}
                className="bg-blue-500 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
              >
                {loading ? (
                  <>
                    <svg className="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Processing...
                  </>
                ) : (
                  <>
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M7 2a1 1 0 00-.707 1.707L7 4.414v3.758a1 1 0 01-.293.707l-4 4C.817 14.769 2.156 18 4.828 18h10.343c2.673 0 4.012-3.231 2.122-5.121l-4-4A1 1 0 0113 8.172V4.414l.707-.707A1 1 0 0013 2H7zm2 6.172V4h2v4.172a3 3 0 00.879 2.12l1.027 1.028a4 4 0 00-2.171.102l-.47.156a4 4 0 01-2.53 0l-.563-.187a1.993 1.993 0 00-.114-.035l1.063-1.063A3 3 0 009 8.172z" clipRule="evenodd" />
                    </svg>
                    Analyze
                  </>
                )}
              </button>
            </div>
          </form>

          {error && (
            <div className="mx-8 mb-8 p-4 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400">
              <div className="flex gap-3 items-start">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mt-0.5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
                <div className="flex-1">{error}</div>
              </div>
            </div>
          )}

          {result && (
            <div className="border-t border-gray-700">
              <div className="p-4">
                <div className="space-y-4">
                  <div>
                    <h3 className="text-xs font-medium text-gray-400 mb-2">SUMMARY</h3>
                    <p className="text-sm text-gray-200 leading-relaxed">{result.summary}</p>
                  </div>

                  <div>
                    <h3 className="text-xs font-medium text-gray-400 mb-2">KEY RISKS</h3>
                    <div className="space-y-2">
                      {(result.risks || []).map((risk: string, i: number) => (
                        <div key={i} className="flex items-start gap-2 p-2 rounded bg-red-500/10 border border-red-500/20">
                          <div className="w-4 h-4 rounded-full bg-red-500/20 flex items-center justify-center flex-none mt-0.5">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                            </svg>
                          </div>
                          <div className="text-sm text-red-400">{risk}</div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="pt-4 border-t border-gray-700">
                    <div className="flex flex-wrap items-center gap-2">
                      <button
                        onClick={downloadJSON}
                        className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-gray-700 hover:bg-gray-600 text-gray-200 text-xs transition-colors"
                      >
                        JSON
                      </button>
                      <button
                        onClick={downloadSummaryMd}
                        className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-gray-700 hover:bg-gray-600 text-gray-200 text-xs transition-colors"
                      >
                        MD
                      </button>
                      <label className="flex items-center gap-1.5 text-xs text-gray-400 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={showRaw}
                          onChange={(e) => setShowRaw(e.target.checked)}
                          className="w-3 h-3 rounded border-gray-600 bg-gray-700 text-blue-500 focus:ring-1 focus:ring-blue-500 focus:ring-offset-gray-800"
                        />
                        Raw JSON
                      </label>
                    </div>

                    {showRaw && (
                      <div className="mt-3">
                        <pre className="p-2 rounded bg-gray-700/50 border border-gray-600 text-xs text-gray-300 overflow-x-auto">
                          {JSON.stringify(result, null, 2)}
                        </pre>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
