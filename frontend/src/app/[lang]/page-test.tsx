import { SimpleTest } from '@/components/homepage/SimpleTest';

export default function HomePage({
  params,
}: {
  params: { lang: string };
}) {
  return (
    <div className="min-h-screen">
      <SimpleTest lang={params.lang} />
      
      {/* Basic Features Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-5xl font-bold text-gray-900 mb-6">
              Why Choose ListAcross EU?
            </h2>
            <p className="text-xl text-gray-600 max-w-4xl mx-auto">
              The most comprehensive European business directory with verified listings and advanced search capabilities.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            <div className="text-center p-8">
              <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-3xl">🔍</span>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                Smart Search
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Find businesses across all 27 EU countries with our advanced search technology and intelligent filtering.
              </p>
            </div>
            
            <div className="text-center p-8">
              <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-3xl">✅</span>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                Verified Listings
              </h3>
              <p className="text-gray-600 leading-relaxed">
                All business information is verified and regularly updated to ensure accuracy and reliability.
              </p>
            </div>
            
            <div className="text-center p-8">
              <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-3xl">🇪🇺</span>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                EU Coverage
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Complete coverage across all European Union member states with multilingual support.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-24 bg-gradient-to-r from-blue-600 to-blue-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold mb-6">
            Ready to Connect Across Europe?
          </h2>
          <p className="text-xl mb-12 max-w-3xl mx-auto opacity-90">
            Join thousands of businesses and customers who trust ListAcross EU for European commerce.
          </p>
          <div className="flex flex-col sm:flex-row gap-6 justify-center">
            <button className="px-10 py-4 bg-yellow-500 text-blue-900 font-bold text-lg rounded-xl hover:bg-yellow-400 transform hover:scale-105 transition-all duration-300">
              Get Started Today
            </button>
            <button className="px-10 py-4 border-2 border-white text-white font-bold text-lg rounded-xl hover:bg-white hover:text-blue-800 transform hover:scale-105 transition-all duration-300">
              Learn More
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}