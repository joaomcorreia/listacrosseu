/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  // No experimental.turbo or Turbopack here
  async rewrites() {
    return [
      // Proxy Django admin static files and URLs
      {
        source: '/django-admin/:path*',
        destination: 'http://127.0.0.1:8000/admin/:path*',
      },
      // Proxy Django API - handle with and without trailing slashes
      {
        source: '/api/admin/blog/posts/:path*',
        destination: 'http://127.0.0.1:8000/api/v1/admin/blog/posts/:path*',
      },
      {
        source: '/api/admin/:path*',
        destination: 'http://127.0.0.1:8000/api/v1/admin/:path*',
      },
      {
        source: '/api/v1/blog/posts/',
        destination: 'http://127.0.0.1:8000/api/v1/blog/posts/',
      },
      {
        source: '/api/v1/blog/posts',
        destination: 'http://127.0.0.1:8000/api/v1/blog/posts/',
      },
      {
        source: '/api/v1/:path*',
        destination: 'http://127.0.0.1:8000/api/v1/:path*',
      },
    ]
  },
  async redirects() {
    return [
      {
        source: '/',
        destination: '/en',
        permanent: false,
      },
    ]
  },
}

module.exports = nextConfig