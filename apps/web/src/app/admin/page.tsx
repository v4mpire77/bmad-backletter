'use client';

import React, { useEffect, useState } from 'react';

interface Metric {
  name: string;
  value: number;
  slug: string;
}

interface Timeseries {
  [slug: string]: number[];
}

const Sparkline = ({ data }: { data: number[] }) => {
  if (!data || data.length === 0) return null;
  const width = 100;
  const height = 30;
  const max = Math.max(...data);
  const points = data
    .map((d, i) => {
      const x = (i / (data.length - 1)) * width;
      const y = height - (d / max) * height;
      return `${x},${y}`;
    })
    .join(' ');
  return (
    <svg
      width={width}
      height={height}
      className="mt-2 text-blue-600"
      aria-label="sparkline"
    >
      <polyline
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        points={points}
      />
    </svg>
  );
};

const MetricTile = ({ metric, series }: { metric: Metric; series: number[] }) => (
  <div className="bg-white rounded-lg shadow p-4">
    <div className="text-sm text-gray-500">{metric.name}</div>
    <div className="text-2xl font-bold">{metric.value}</div>
    <Sparkline data={series} />
  </div>
);

export default function AdminPage() {
  const [metrics, setMetrics] = useState<Metric[]>([]);
  const [timeseries, setTimeseries] = useState<Timeseries>({});

  useEffect(() => {
    async function loadData() {
      const metricsRes = await fetch('/api/admin/metrics');
      const metricsData = (await metricsRes.json()) as Metric[];
      const seriesRes = await fetch('/api/admin/metrics/timeseries');
      const seriesData = (await seriesRes.json()) as Timeseries;
      setMetrics(metricsData);
      setTimeseries(seriesData);
    }
    loadData();
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Admin Metrics</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
        {metrics.map((m) => (
          <MetricTile key={m.slug} metric={m} series={timeseries[m.slug] || []} />
        ))}
      </div>
    </div>
  );
}

