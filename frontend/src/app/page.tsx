'use client';

import { useState, useEffect } from 'react';
import LanguageSelector from '@/components/LanguageSelector';

export default function Home() {
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [mounted, setMounted] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const [stats, setStats] = useState({
    businesses: 6593,
    countries: 27,
    plans: 3
  });

  useEffect(() => {
    setMounted(true);

    // Fetch real stats from our APIs
    const fetchStats = async () => {
      try {
        // Get business count from existing API
        const businessResponse = await fetch('http://127.0.0.1:8000/api/v1/businesses/');
        const businessData = await businessResponse.json();

        // Get plans count
        const plansResponse = await fetch('http://127.0.0.1:8000/api/plans/');
        const plansData = await plansResponse.json();

        setStats({
          businesses: businessData.count || 6593,
          countries: 27, // EU countries
          plans: plansData.count || 3
        });
      } catch (error) {
        console.error('Failed to fetch stats:', error);
        // Keep fallback values already set
      }
    };

    fetchStats();
  }, []);

  useEffect(() => {
    const handleScroll = () => {
      const scrollTop = window.scrollY;
      setIsScrolled(scrollTop > 50);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* EU Flag Colors Header Bar */}
      <div className="h-2 bg-gradient-to-r from-blue-600 via-yellow-400 to-blue-600"></div>

      {/* Navigation */}
      <nav className={`fixed top-2 left-0 right-0 z-50 transition-all duration-500 ${isScrolled
          ? 'bg-white/95 backdrop-blur-md shadow-xl'
          : 'bg-white/90 backdrop-blur-sm shadow-lg'
        }`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <div className="text-3xl animate-pulse">🇪🇺</div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                ListAcrossEU
              </h1>
            </div>
            <div className="flex items-center space-x-6">
              <LanguageSelector
                selectedLanguage={selectedLanguage}
                onLanguageChange={setSelectedLanguage}
              />
              <a
                href="http://127.0.0.1:8000/directory/"
                className="font-medium text-gray-700 hover:text-blue-600 transition-all duration-200 hover:scale-105"
                target="_blank"
                rel="noopener noreferrer"
              >
                🏢 Directory
              </a>
              <a
                href="http://127.0.0.1:8000/guides/"
                className="font-medium text-gray-700 hover:text-blue-600 transition-all duration-200 hover:scale-105"
                target="_blank"
                rel="noopener noreferrer"
              >
                📝 Travel Guides
              </a>
              <a
                href="http://127.0.0.1:8000/api/plans/"
                className="font-medium text-gray-700 hover:text-blue-600 transition-all duration-200 hover:scale-105"
                target="_blank"
                rel="noopener noreferrer"
              >
                💎 Plans API
              </a>
              <a
                href="http://127.0.0.1:8000/admin/"
                className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-2 rounded-full font-medium hover:from-blue-700 hover:to-purple-700 transition-all duration-200 hover:scale-105 shadow-lg"
                target="_blank"
                rel="noopener noreferrer"
              >
                Admin
              </a>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="relative overflow-hidden pt-20">
        <div className="relative min-h-screen bg-gradient-to-br from-blue-600 via-purple-700 to-blue-800">
          {/* Background Elements */}
          <div className="absolute inset-0 opacity-10">
            <div className="absolute top-20 left-10 text-8xl">🏢</div>
            <div className="absolute top-40 right-20 text-6xl">🌍</div>
            <div className="absolute bottom-40 left-20 text-7xl">💼</div>
            <div className="absolute bottom-20 right-10 text-5xl">⭐</div>
          </div>

          {/* Hero Content */}
          <div className="relative z-10 flex items-center justify-center min-h-screen">
            <div className="text-center max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
              <h1 className="text-5xl md:text-7xl font-bold text-white mb-8 drop-shadow-lg">
                European Business
                <br />
                <span className="bg-gradient-to-r from-yellow-400 to-orange-400 bg-clip-text text-transparent">
                  Directory
                </span>
              </h1>

              <p className="text-xl md:text-2xl text-blue-100 mb-8 drop-shadow-md max-w-3xl mx-auto leading-relaxed">
                Discover and connect with {mounted ? stats.businesses.toLocaleString() : '6,593'} businesses across Europe.
                Your gateway to the European market.
              </p>

              {/* Stats Grid */}
              <div className="grid grid-cols-3 gap-6 mb-12 max-w-2xl mx-auto">
                <div className="text-center">
                  <div className="text-3xl font-bold text-yellow-400 mb-1">{mounted ? stats.businesses.toLocaleString() : '6,593'}</div>
                  <div className="text-blue-200 text-sm">Businesses</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-yellow-400 mb-1">{stats.plans}</div>
                  <div className="text-blue-200 text-sm">Plans Available</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-yellow-400 mb-1">{stats.countries}</div>
                  <div className="text-blue-200 text-sm">EU Countries</div>
                </div>
              </div>

              {/* CTA Buttons */}
              <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
                <a
                  href="http://127.0.0.1:8000/directory/"
                  className="bg-white text-blue-600 px-8 py-4 rounded-full font-bold text-lg hover:bg-blue-50 transition-all duration-300 shadow-xl hover:shadow-2xl hover:scale-105 flex items-center gap-2"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <span>🔍</span>
                  Explore Directory
                </a>
                <a
                  href="http://127.0.0.1:8000/guides/"
                  className="bg-yellow-400 text-blue-900 px-8 py-4 rounded-full font-bold text-lg hover:bg-yellow-300 transition-all duration-300 shadow-xl hover:shadow-2xl hover:scale-105 flex items-center gap-2"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <span>�️</span>
                  Travel Guides
                </a>
              </div>
            </div>
          </div>
        </div>

        {/* Platform Features Section */}
        <div className="bg-gray-50 py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-4xl md:text-5xl font-bold mb-6">
                <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  Platform Features
                </span>
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Comprehensive business directory with advanced features for visibility and growth
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-8 mb-16">
              {/* CMS Pages */}
              <div className="bg-white rounded-2xl shadow-xl p-8 hover:shadow-2xl transition-all duration-300 hover:scale-105">
                <div className="text-5xl mb-6 text-center">📄</div>
                <h3 className="text-2xl font-bold mb-4 text-center">Content Management</h3>
                <p className="text-gray-600 text-center mb-6">
                  Dynamic pages with SEO optimization and multilingual support for maximum visibility.
                </p>
                <div className="text-center">
                  <a href="http://127.0.0.1:8000/api/v1/cms/pages/" className="text-blue-600 hover:text-blue-700 font-medium" target="_blank" rel="noopener noreferrer">
                    View Pages API →
                  </a>
                </div>
              </div>

              {/* Blog System */}
              <div className="bg-white rounded-2xl shadow-xl p-8 hover:shadow-2xl transition-all duration-300 hover:scale-105">
                <div className="text-5xl mb-6 text-center">📝</div>
                <h3 className="text-2xl font-bold mb-4 text-center">Business Blog</h3>
                <p className="text-gray-600 text-center mb-6">
                  Industry insights, success stories, and market analysis to keep you informed.
                </p>
                <div className="text-center">
                  <a href="http://127.0.0.1:8000/api/v1/blog/posts/" className="text-blue-600 hover:text-blue-700 font-medium" target="_blank" rel="noopener noreferrer">
                    Blog API →
                  </a>
                </div>
              </div>

              {/* Plans & Visibility */}
              <div className="bg-white rounded-2xl shadow-xl p-8 hover:shadow-2xl transition-all duration-300 hover:scale-105">
                <div className="text-5xl mb-6 text-center">💎</div>
                <h3 className="text-2xl font-bold mb-4 text-center">Visibility Plans</h3>
                <p className="text-gray-600 text-center mb-6">
                  Choose from Free, Product, or Premium plans to maximize your business exposure.
                </p>
                <div className="text-center">
                  <a href="http://127.0.0.1:8000/api/plans/" className="text-blue-600 hover:text-blue-700 font-medium" target="_blank" rel="noopener noreferrer">
                    Plans API →
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Why Choose Section */}
        <div className="bg-white py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-4xl md:text-5xl font-bold mb-6">
                <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  Why Choose ListAcrossEU?
                </span>
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Europe's most comprehensive business directory with AI-powered features and complete multilingual support
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
              <div className="text-center">
                <div className="bg-blue-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">🔍</span>
                </div>
                <h3 className="text-xl font-bold mb-2">Advanced Search</h3>
                <p className="text-gray-600">Filter by industry, location, and company size to find exactly what you need.</p>
              </div>

              <div className="text-center">
                <div className="bg-green-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">🌐</span>
                </div>
                <h3 className="text-xl font-bold mb-2">Multilingual</h3>
                <p className="text-gray-600">Full support for English, Dutch, French, Spanish, Portuguese, German, and Italian.</p>
              </div>

              <div className="text-center">
                <div className="bg-purple-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">🤖</span>
                </div>
                <h3 className="text-xl font-bold mb-2">AI-Powered</h3>
                <p className="text-gray-600">Intelligent SEO suggestions and content optimization powered by AI.</p>
              </div>

              <div className="text-center">
                <div className="bg-orange-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">📊</span>
                </div>
                <h3 className="text-xl font-bold mb-2">Analytics</h3>
                <p className="text-gray-600">Comprehensive insights and performance metrics for your listings.</p>
              </div>
            </div>

            <div className="text-center">
              <a
                href="http://127.0.0.1:8000/directory/"
                className="inline-flex items-center gap-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-full font-bold text-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-300 shadow-xl hover:shadow-2xl hover:scale-105"
                target="_blank"
                rel="noopener noreferrer"
              >
                <span>🏢</span>
                Explore {mounted ? stats.businesses.toLocaleString() : '6,593'} Businesses
              </a>
            </div>
          </div>
        </div>

      </main>

      {/* Footer */}
      <footer className="bg-gradient-to-r from-blue-900 via-purple-900 to-blue-900 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-6">
                <span className="text-2xl">🇪🇺</span>
                <h3 className="text-xl font-bold">ListAcrossEU</h3>
              </div>
              <p className="text-blue-200 mb-4">
                Europe's premier business directory connecting companies across all 27 EU member states.
              </p>
            </div>

            <div>
              <h4 className="text-lg font-semibold mb-4">Platform</h4>
              <ul className="space-y-2 text-blue-200">
                <li><a href="http://127.0.0.1:8000/directory/" className="hover:text-white transition-colors" target="_blank" rel="noopener noreferrer">Directory</a></li>
                <li><a href="http://127.0.0.1:8000/guides/" className="hover:text-white transition-colors" target="_blank" rel="noopener noreferrer">Travel Guides</a></li>
                <li><a href="http://127.0.0.1:8000/api/plans/" className="hover:text-white transition-colors" target="_blank" rel="noopener noreferrer">Plans API</a></li>
                <li><a href="http://127.0.0.1:8000/admin/" className="hover:text-white transition-colors" target="_blank" rel="noopener noreferrer">Admin</a></li>
              </ul>
            </div>

            <div>
              <h4 className="text-lg font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-blue-200">
                <li><a href="http://127.0.0.1:8000/api/v1/" className="hover:text-white transition-colors" target="_blank" rel="noopener noreferrer">API v1</a></li>
                <li><a href="http://127.0.0.1:8000/admin/data-overview/" className="hover:text-white transition-colors" target="_blank" rel="noopener noreferrer">Data Overview</a></li>
                <li><a href="http://127.0.0.1:8000/api/v1/cms/" className="hover:text-white transition-colors" target="_blank" rel="noopener noreferrer">CMS API</a></li>
              </ul>
            </div>

            <div>
              <h4 className="text-lg font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-blue-200">
                <li><a href="http://127.0.0.1:8000/sitemap.xml" className="hover:text-white transition-colors" target="_blank" rel="noopener noreferrer">Sitemap</a></li>
                <li><a href="http://127.0.0.1:8000/robots.txt" className="hover:text-white transition-colors" target="_blank" rel="noopener noreferrer">Robots.txt</a></li>
                <li><a href="http://127.0.0.1:8000/api/v1/blog/" className="hover:text-white transition-colors" target="_blank" rel="noopener noreferrer">Blog API</a></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-blue-800 mt-12 pt-8 text-center">
            <p className="text-blue-200">
              🇪🇺 &copy; 2025 ListAcrossEU - European Business Directory Platform
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}