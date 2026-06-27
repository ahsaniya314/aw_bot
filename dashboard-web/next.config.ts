import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  output: "export", // Hasilkan folder 'out' statis untuk disajikan oleh Flask
  basePath: "/dashboard", // Menentukan base path aplikasi di Flask
  assetPrefix: "/dashboard", // Menentukan prefix untuk aset statis (CSS/JS)
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
