import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  compress: true,
  eslint: {
    // Avoid blocking production builds on lint errors. Address during CI.
    ignoreDuringBuilds: true,
  },
  typescript: { ignoreBuildErrors: true },
  // Uncomment to slim runtime with standalone output if desired:
  // output: "standalone",
};

export default nextConfig;
