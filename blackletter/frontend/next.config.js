/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: { serverActions: { allowedOrigins: ['*'] } },
  reactStrictMode: true,
  poweredByHeader: false,
}
module.exports = nextConfig
