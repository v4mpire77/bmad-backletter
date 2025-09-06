// Custom image loader for static export with optimization
export default function imageLoader({ src, width, quality }) {
  // For static export, we can still optimize by:
  // 1. Adding width/quality parameters for potential CDN optimization
  // 2. Converting to WebP format if supported
  // 3. Adding proper caching headers
  
  if (!src) return src;
  
  // If it's an external URL, return as-is
  if (src.startsWith('http')) {
    return src;
  }
  
  // For local images, we can add optimization parameters
  // This would work with services like Cloudinary, Vercel, or custom CDN
  const params = new URLSearchParams();
  if (width) params.set('w', width.toString());
  if (quality) params.set('q', quality.toString());
  params.set('f', 'webp'); // Prefer WebP format
  params.set('auto', 'format'); // Auto-optimize format
  
  const queryString = params.toString();
  return queryString ? `${src}?${queryString}` : src;
}
