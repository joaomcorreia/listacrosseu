/** @type {import('next').NextConfig} */
const isProd = process.env.NODE_ENV === 'production';
const apiBaseUrl = isProd ? 'https://api.listacross.eu' : 'http://127.0.0.1:8000';

const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  compress: true,
  
  // Production optimizations
  ...(isProd && {
    output: 'standalone',
    experimental: {
      outputStandalone: true,
    },
  }),
  
  async rewrites() {
    return [
      // Proxy Django admin static files and URLs
      {
        source: '/django-admin/:path*',
        destination: `${apiBaseUrl}/admin/:path*`,
      },
      // Proxy Django API - handle with and without trailing slashes
      {
        source: '/api/admin/blog/posts/:path*',
        destination: `${apiBaseUrl}/api/v1/admin/blog/posts/:path*`,
      },
      {
        source: '/api/admin/:path*',
        destination: `${apiBaseUrl}/api/v1/admin/:path*`,
      },
      {
        source: '/api/v1/blog/posts/',
        destination: `${apiBaseUrl}/api/v1/blog/posts/`,
      },
      {
        source: '/api/v1/blog/posts',
        destination: `${apiBaseUrl}/api/v1/blog/posts/`,
      },
      {
        source: '/api/v1/:path*',
        destination: `${apiBaseUrl}/api/v1/:path*`,
      },
    ]
  },
  
  async redirects() {
    return [
      {
        source: '/',
        destination: '/eu',
        permanent: false,
      },
    ]
  },
  
  // Security headers
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
        ],
      },
    ]
  },
}

module.exports = nextConfig