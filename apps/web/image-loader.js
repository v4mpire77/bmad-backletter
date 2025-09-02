// Custom image loader for static export
export default function imageLoader({ src, width, quality }) {
  // For static export, just return the src as-is
  // In production, you might want to use a CDN or image optimization service
  return src;
}
