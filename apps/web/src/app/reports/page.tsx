"use client";

import { getExports } from "@/lib/mockStore";
import Link from "next/link";
import { useEffect, useState } from "react";

export default function ReportsPage() {
  const [items, setItems] = useState(() => getExports());
  useEffect(() => {
    // Refresh on mount (in case of navigation back)
    setItems(getExports());
  }, []);

  return (
    <div className="mx-auto max-w-4xl p-6">
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-semibold">Reports</h1>
        <Link className="text-sm text-blue-600 hover:underline" href="/dashboard">
          Back to Dashboard
        </Link>
      </div>
      <div className="border rounded-lg overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-black/5">
            <tr>
              <th className="text-left p-3">Filename</th>
              <th className="text-left p-3">Created</th>
              <th className="text-left p-3">Type</th>
              <th className="text-left p-3">Options</th>
            </tr>
          </thead>
          <tbody>
            {items.length === 0 ? (
              <tr>
                <td colSpan={4} className="p-6 text-center text-gray-500">
                  No exports yet. Use Export on a Findings page.
                </td>
              </tr>
            ) : (
              items.map((x, i) => (
                <tr key={`${x.id}-${i}`} className="border-t">
                  <td className="p-3">{x.filename}</td>
                  <td className="p-3">{new Date(x.created_at).toLocaleString()}</td>
                  <td className="p-3">PDF (preview)</td>
                  <td className="p-3 text-gray-600">
                    {x.options.includeLogo ? "logo " : ""}
                    {x.options.includeMeta ? "meta " : ""}
                    {x.options.dateFormat}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

