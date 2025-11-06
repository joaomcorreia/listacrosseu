'use client';

import { useState, useEffect } from 'react';

interface CountryExplorerSectionProps {
  lang: string;
  ui: any;
}

export function CountryExplorerSection({ lang, ui }: CountryExplorerSectionProps) {
  const [selectedCountry, setSelectedCountry] = useState('germany');
  const [hoveredCountry, setHoveredCountry] = useState<string | null>(null);

  const countries = [
    { id: 'germany', name: 'Germany', flag: '🇩🇪', businesses: '2.8M', color: 'from-red-500 to-yellow-500' },
    { id: 'france', name: 'France', flag: '🇫🇷', businesses: '2.1M', color: 'from-blue-500 to-red-500' },
    { id: 'italy', name: 'Italy', flag: '🇮🇹', businesses: '1.9M', color: 'from-green-500 to-red-500' },
    { id: 'spain', name: 'Spain', flag: '🇪🇸', businesses: '1.7M', color: 'from-yellow-500 to-red-500' },
    { id: 'poland', name: 'Poland', flag: '🇵🇱', businesses: '1.2M', color: 'from-white to-red-500' },
    { id: 'netherlands', name: 'Netherlands', flag: '🇳🇱', businesses: '980K', color: 'from-red-500 to-white' },
    { id: 'belgium', name: 'Belgium', flag: '🇧🇪', businesses: '450K', color: 'from-black to-yellow-500' },
    { id: 'portugal', name: 'Portugal', flag: '🇵🇹', businesses: '380K', color: 'from-green-500 to-red-500' },
    { id: 'austria', name: 'Austria', flag: '🇦🇹', businesses: '320K', color: 'from-red-500 to-white' },
    { id: 'sweden', name: 'Sweden', flag: '🇸🇪', businesses: '290K', color: 'from-blue-500 to-yellow-500' },
    { id: 'denmark', name: 'Denmark', flag: '🇩🇰', businesses: '185K', color: 'from-red-500 to-white' },
    { id: 'finland', name: 'Finland', flag: '🇫🇮', businesses: '165K', color: 'from-white to-blue-500' },
  ];

  const featuredCategories = [
    { name: 'Restaurants', icon: '🍽️', count: '450K+', trend: '+12%' },
    { name: 'Tech Services', icon: '💻', count: '180K+', trend: '+24%' },
    { name: 'Healthcare', icon: '🏥', count: '320K+', trend: '+8%' },
    { name: 'Retail', icon: '🛍️', count: '680K+', trend: '+15%' },
    { name: 'Manufacturing', icon: '🏭', count: '290K+', trend: '+7%' },
    { name: 'Finance', icon: '💰', count: '95K+', trend: '+18%' },
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      const currentIndex = countries.findIndex(c => c.id === selectedCountry);
      const nextIndex = (currentIndex + 1) % countries.length;
      setSelectedCountry(countries[nextIndex].id);
    }, 4000);

    return () => clearInterval(interval);
  }, [selectedCountry, countries]);

  const selectedCountryData = countries.find(c => c.id === selectedCountry);

  return (
    <section className="py-24 bg-gradient-to-br from-gray-50 to-blue-50 relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-10 left-10 w-64 h-64 bg-blue-500 rounded-full blur-3xl" />
        <div className="absolute bottom-10 right-10 w-96 h-96 bg-yellow-500 rounded-full blur-3xl" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-5xl font-bold text-gray-900 mb-6">
            Explore European Markets
          </h2>
          <p className="text-xl text-gray-600 max-w-4xl mx-auto leading-relaxed">
            Discover businesses across all 27 EU member states. From bustling metropolises to charming local markets, connect with the heart of European commerce.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          {/* Interactive Country Grid */}
          <div className="space-y-8">
            <h3 className="text-3xl font-bold text-gray-900 text-center lg:text-left">
              Select a Country to Explore
            </h3>
            
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
              {countries.map((country, index) => (
                <button
                  key={country.id}
                  onClick={() => setSelectedCountry(country.id)}
                  onMouseEnter={() => setHoveredCountry(country.id)}
                  onMouseLeave={() => setHoveredCountry(null)}
                  className={`group relative p-4 rounded-xl border-2 transition-all duration-300 transform hover:scale-105 animate-fade-in ${
                    selectedCountry === country.id
                      ? 'border-blue-500 bg-blue-50 shadow-xl'
                      : 'border-gray-200 bg-white hover:border-blue-300 hover:shadow-lg'
                  }`}
                  style={{ animationDelay: `${index * 50}ms` }}
                >
                  <div className="text-center">
                    <div className="text-3xl mb-2 group-hover:scale-110 transition-transform duration-300">
                      {country.flag}
                    </div>
                    <div className="text-sm font-semibold text-gray-900 mb-1">
                      {country.name}
                    </div>
                    <div className="text-xs text-gray-500">
                      {country.businesses}
                    </div>
                  </div>

                  {/* Selection Indicator */}
                  {selectedCountry === country.id && (
                    <div className="absolute -top-1 -right-1 w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center">
                      <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                    </div>
                  )}

                  {/* Hover Effect */}
                  {hoveredCountry === country.id && (
                    <div className={`absolute inset-0 rounded-xl bg-gradient-to-r ${country.color} opacity-20 transition-opacity duration-300`} />
                  )}
                </button>
              ))}
            </div>

            {/* View All Countries Link */}
            <div className="text-center lg:text-left">
              <button className="inline-flex items-center text-blue-600 hover:text-blue-700 font-semibold group">
                View All 27 EU Countries
                <svg className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform duration-200" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </button>
            </div>
          </div>

          {/* Country Details & Categories */}
          <div className="space-y-8">
            {/* Selected Country Showcase */}
            {selectedCountryData && (
              <div className={`relative p-8 rounded-2xl bg-gradient-to-r ${selectedCountryData.color} text-white shadow-2xl transform transition-all duration-500`}>
                <div className="text-center">
                  <div className="text-6xl mb-4 animate-bounce">
                    {selectedCountryData.flag}
                  </div>
                  <h3 className="text-3xl font-bold mb-2">
                    {selectedCountryData.name}
                  </h3>
                  <p className="text-xl opacity-90 mb-4">
                    {selectedCountryData.businesses} Registered Businesses
                  </p>
                  <button className="px-6 py-3 bg-white bg-opacity-20 backdrop-blur-sm rounded-lg font-semibold hover:bg-opacity-30 transition-all duration-300">
                    Explore {selectedCountryData.name} →
                  </button>
                </div>
              </div>
            )}

            {/* Featured Categories */}
            <div className="bg-white rounded-2xl p-8 shadow-xl border border-gray-100">
              <h4 className="text-2xl font-bold text-gray-900 mb-6 text-center">
                Popular Business Categories
              </h4>
              
              <div className="grid grid-cols-2 gap-4">
                {featuredCategories.map((category, index) => (
                  <div
                    key={category.name}
                    className="group p-4 border border-gray-200 rounded-xl hover:border-blue-300 hover:shadow-lg transition-all duration-300 cursor-pointer animate-fade-in-up"
                    style={{ animationDelay: `${index * 100}ms` }}
                  >
                    <div className="flex items-center space-x-3">
                      <div className="text-2xl group-hover:scale-110 transition-transform duration-300">
                        {category.icon}
                      </div>
                      <div className="flex-1 min-w-0">
                        <h5 className="font-semibold text-gray-900 text-sm mb-1">
                          {category.name}
                        </h5>
                        <div className="flex items-center justify-between">
                          <span className="text-xs text-gray-500">
                            {category.count}
                          </span>
                          <span className="text-xs text-green-600 font-medium">
                            {category.trend}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-6 text-center">
                <button className="px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white font-semibold rounded-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300">
                  Browse All Categories
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}