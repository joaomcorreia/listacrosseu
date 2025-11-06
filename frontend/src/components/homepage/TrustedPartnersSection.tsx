'use client';

interface TrustedPartnersSectionProps {
  lang: string;
  ui: any;
}

export function TrustedPartnersSection({ lang, ui }: TrustedPartnersSectionProps) {
  const categories = [
    { icon: '🍽️', name: 'Restaurants', count: '15,000+' },
    { icon: '💻', name: 'Technology', count: '8,500+' },
    { icon: '🏥', name: 'Healthcare', count: '12,000+' },
    { icon: '🏨', name: 'Hotels', count: '6,200+' },
    { icon: '🛍️', name: 'Retail', count: '20,000+' },
    { icon: '⚙️', name: 'Services', count: '18,500+' },
  ];

  return (
    <section className="py-20 bg-gradient-to-b from-gray-50 to-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Trusted Business Categories
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Explore thousands of verified businesses across Europe's most popular industries
          </p>
        </div>

        {/* Categories Grid */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
          {categories.map((category, index) => (
            <div
              key={category.name}
              className="group relative bg-white rounded-2xl p-6 shadow-lg hover:shadow-2xl border border-gray-100 hover:border-blue-200 transform hover:scale-105 transition-all duration-300 cursor-pointer"
              style={{
                animationDelay: `${index * 100}ms`,
              }}
            >
              {/* Icon */}
              <div className="text-4xl mb-3 group-hover:scale-110 transition-transform duration-300">
                {category.icon}
              </div>
              
              {/* Category Name */}
              <h3 className="font-semibold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors duration-300">
                {category.name}
              </h3>
              
              {/* Count */}
              <p className="text-sm text-gray-500 font-medium">
                {category.count}
              </p>
              
              {/* Hover Effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-blue-600/5 to-yellow-500/5 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
              
              {/* Pulse Animation on Hover */}
              <div className="absolute inset-0 rounded-2xl border-2 border-blue-400/20 opacity-0 group-hover:opacity-100 group-hover:animate-pulse" />
            </div>
          ))}
        </div>

        {/* Stats Bar */}
        <div className="mt-16 bg-gradient-to-r from-blue-600 to-blue-700 rounded-2xl p-8 text-white">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
            <div className="group hover:scale-105 transition-transform duration-300">
              <div className="text-3xl font-bold text-yellow-400 mb-2">50,000+</div>
              <div className="text-blue-100">Verified Businesses</div>
            </div>
            <div className="group hover:scale-105 transition-transform duration-300">
              <div className="text-3xl font-bold text-yellow-400 mb-2">27</div>
              <div className="text-blue-100">EU Countries</div>
            </div>
            <div className="group hover:scale-105 transition-transform duration-300">
              <div className="text-3xl font-bold text-yellow-400 mb-2">200+</div>
              <div className="text-blue-100">Cities Covered</div>
            </div>
            <div className="group hover:scale-105 transition-transform duration-300">
              <div className="text-3xl font-bold text-yellow-400 mb-2">95%</div>
              <div className="text-blue-100">Customer Satisfaction</div>
            </div>
          </div>
        </div>

        {/* EU Flag Accent */}
        <div className="mt-12 flex justify-center">
          <div className="flex items-center space-x-2 bg-blue-600 rounded-full px-6 py-3">
            <div className="flex space-x-1">
              {[...Array(12)].map((_, i) => (
                <div
                  key={i}
                  className="w-2 h-2 bg-yellow-400 rounded-full animate-pulse"
                  style={{
                    animationDelay: `${i * 0.1}s`,
                  }}
                />
              ))}
            </div>
            <span className="text-white font-medium ml-3">European Union Verified</span>
          </div>
        </div>
      </div>
    </section>
  );
}