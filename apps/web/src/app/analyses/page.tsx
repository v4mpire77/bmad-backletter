"use client";

import { useEffect, useState } from "react";

type Analysis = { id: string; name: string; status: "pending" | "complete" };

export default function AnalysesPage() {
  const [items, setItems] = useState<Analysis[]>([]);

  useEffect(() => {
    let active = true;
    fetch("/api/analyses")
      .then(res => res.json())
      .then(data => {
        if (active) setItems(data);
      })
      .catch(() => {});
    return () => {
      active = false;
    };
  }, []);

  return (
    <div className="space-y-3">
      <h1 className="text-2xl font-semibold">Analyses</h1>
      {items.length === 0 ? (
        <p className="text-sm text-muted-foreground">No analyses yet.</p>
      ) : (
        <ul className="divide-y rounded-2xl border">
          {items.map(a => (
            <li key={a.id} className="flex items-center justify-between p-4">
              <span>{a.name}</span>
              <span className="text-xs uppercase">{a.status}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
