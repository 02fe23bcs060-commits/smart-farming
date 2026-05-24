import type { NextConfig } from "next";

// Server-side proxy target (Docker service name or localhost for dev)
const apiInternal = process.env.API_INTERNAL_URL || "http://localhost:8000";

const nextConfig: NextConfig = {
  output: "standalone",
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${apiInternal}/api/:path*`,
      },
      {
        source: "/health",
        destination: `${apiInternal}/health`,
      },
    ];
  },
};

export default nextConfig;
