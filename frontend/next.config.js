/** @type {import('next').NextConfig} */
const nextConfig = {
    // i18n: {
    //   // Define all 27 supported locales
    //   locales: [
    //     'en', 'es', 'fr', 'de', 'nl', 'pt', 'it', 'pl', 'cs', 'sk', 
    //     'hu', 'ro', 'bg', 'hr', 'sl', 'et', 'lv', 'lt', 'mt', 'cy',
    //     'fi', 'se', 'da', 'no', 'is', 'ie', 'lu'
    //   ],
    //   defaultLocale: 'en',
    //   localeDetection: false, // We'll handle this in middleware
    // },
    async rewrites() {
        return [
            {
                source: '/api/:path*',
                destination: 'http://localhost:8000/api/:path*',
            },
        ];
    },
    images: {
        remotePatterns: [
            {
                protocol: 'https',
                hostname: 'images.unsplash.com',
                port: '',
                pathname: '/**',
            },
        ],
    },
};

module.exports = nextConfig;