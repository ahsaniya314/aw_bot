import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  output: "standalone", // Optimal untuk Docker
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
