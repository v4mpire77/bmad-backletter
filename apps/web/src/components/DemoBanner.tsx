"use client";

import { useEffect, useState } from "react";

export default function DemoBanner() {
  const [mockMode, setMockMode] = useState<boolean>(false);
  const [apiDown, setApiDown] = useState<boolean>(false);

  useEffect(() => {
    const isMock = process.env.NEXT_PUBLIC_USE_MOCKS === "1";
    setMockMode(isMock);
    if (isMock) return;
    const base =
      process.env.NEXT_PUBLIC_API_BASE ||
      process.env.NEXT_PUBLIC_API_URL ||
      "";
    if (!base) return;
    const controller = new AbortController();
    const t = setTimeout(() => controller.abort(), 2500);
    fetch(`${base}/healthz`, { signal: controller.signal })
      .then((r) => {
        if (!r.ok) setApiDown(true);
      })
      .catch(() => setApiDown(true))
      .finally(() => clearTimeout(t));
    return () => clearTimeout(t);
  }, []);

  if (!mockMode && !apiDown) return null;
  return (
    <div className="mb-4 rounded border border-amber-400 bg-amber-50 text-amber-900 px-3 py-2 text-xs">
      {mockMode
        ? "Running in mock mode — connect API to use live analysis."
        : "API not reachable — showing mock data for demo."}
    </div>
  );
}

