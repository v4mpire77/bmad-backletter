export default function SkeletonLoader() {
  return (
    <div className="space-y-3" data-testid="skeleton-loader">
      {[...Array(6)].map((_, i) => (
        // eslint-disable-next-line react/no-array-index-key
        <div key={i} className="h-6 bg-gray-200/70 animate-pulse rounded" />
      ))}
    </div>
  );
}

