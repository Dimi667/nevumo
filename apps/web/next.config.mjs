import nextPWA from 'next-pwa';

const withPWA = nextPWA({
  dest: 'public',
  register: true,
  skipWaiting: true,
  disable: process.env.NODE_ENV === 'development',
});

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  allowedDevOrigins: ["192.168.0.15"],
  transpilePackages: ["@repo/ui"],
  turbopack: {},
  async rewrites() {
    return [
      {
        source: '/api/v1/:path*',
        destination: `${process.env.API_URL || process.env.NEXT_PUBLIC_API_URL}/api/v1/:path*`,
      },
      {
        source: '/api/:path*',
        destination: `${process.env.API_URL || process.env.NEXT_PUBLIC_API_URL}/api/v1/:path*`,
      },
      {
        source: '/:lang/api/v1/:path*',
        destination: `${process.env.API_URL || process.env.NEXT_PUBLIC_API_URL}/api/v1/:path*`,
      },
      {
        source: '/:lang/api/:path*',
        destination: `${process.env.API_URL || process.env.NEXT_PUBLIC_API_URL}/api/v1/:path*`,
      },
    ];
  },
  images: {
    remotePatterns: [
      {
        protocol: 'http',
        hostname: '127.0.0.1',
        port: '8000',
        pathname: '/**',
      },
      {
        protocol: 'http',
        hostname: 'localhost',
        port: '8000',
        pathname: '/**',
      },
      {
        protocol: 'https',
        hostname: 'i.pravatar.cc',
        pathname: '/**',
      },
    ],
  },
};

export default withPWA(nextConfig);
