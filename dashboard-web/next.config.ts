import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  output: "export", // Hasilkan folder 'out' statis untuk disajikan oleh Flask
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
