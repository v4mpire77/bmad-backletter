'use client';

import React, { useEffect, useState } from 'react';

interface PerformanceMetrics {
  fcp?: number; // First Contentful Paint
  lcp?: number; // Largest Contentful Paint
  fid?: number; // First Input Delay
  cls?: number; // Cumulative Layout Shift
  ttfb?: number; // Time to First Byte
}

const PerformanceMonitor = React.memo(function PerformanceMonitor() {
  const [metrics, setMetrics] = useState<PerformanceMetrics>({});
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Only show in development or when explicitly enabled
    if (process.env.NODE_ENV !== 'development' && !process.env.NEXT_PUBLIC_SHOW_PERFORMANCE) {
      return;
    }

    setIsVisible(true);

    const measurePerformance = () => {
      if (typeof window === 'undefined' || !('performance' in window)) return;

      const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
      const paint = performance.getEntriesByType('paint');
      
      const fcp = paint.find(entry => entry.name === 'first-contentful-paint')?.startTime;
      const lcp = performance.getEntriesByType('largest-contentful-paint')[0]?.startTime;
      
      setMetrics({
        fcp: fcp ? Math.round(fcp) : undefined,
        lcp: lcp ? Math.round(lcp) : undefined,
        ttfb: navigation ? Math.round(navigation.responseStart - navigation.requestStart) : undefined,
      });
    };

    // Measure after page load
    if (document.readyState === 'complete') {
      measurePerformance();
    } else {
      window.addEventListener('load', measurePerformance);
    }

    // Measure LCP after a delay (it can change)
    const lcpTimeout = setTimeout(measurePerformance, 2000);

    return () => {
      window.removeEventListener('load', measurePerformance);
      clearTimeout(lcpTimeout);
    };
  }, []);

  if (!isVisible) return null;

  return (
    <div className="fixed bottom-4 right-4 bg-black/80 text-white text-xs p-2 rounded font-mono z-50">
      <div className="font-bold mb-1">Performance</div>
      {metrics.fcp && <div>FCP: {metrics.fcp}ms</div>}
      {metrics.lcp && <div>LCP: {metrics.lcp}ms</div>}
      {metrics.ttfb && <div>TTFB: {metrics.ttfb}ms</div>}
    </div>
  );
});

export default PerformanceMonitor;