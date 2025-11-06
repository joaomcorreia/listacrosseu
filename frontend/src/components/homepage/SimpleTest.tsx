'use client';

interface SimpleTestProps {
  lang: string;
}

export function SimpleTest({ lang }: SimpleTestProps) {
  return (
    <div className="py-20 bg-gradient-to-br from-blue-900 to-blue-800 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h1 className="text-6xl font-bold mb-6">
          Find Businesses{' '}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-yellow-300 to-yellow-500">
            Across Europe
          </span>
        </h1>
        <p className="text-2xl mb-12 max-w-4xl mx-auto opacity-90">
          Connect with over 2.8 million businesses across all 27 EU member states. 
          One platform, endless opportunities.
        </p>
        <div className="flex flex-col sm:flex-row gap-6 justify-center">
          <button className="px-12 py-6 bg-gradient-to-r from-yellow-400 to-yellow-500 text-blue-900 font-bold text-xl rounded-2xl hover:shadow-2xl hover:shadow-yellow-500/25 transform hover:scale-105 transition-all duration-300">
            Start Searching Now
          </button>
          <button className="px-12 py-6 border-3 border-white text-white font-bold text-xl rounded-2xl hover:bg-white hover:text-blue-900 transform hover:scale-105 transition-all duration-300">
            List Your Business Free
          </button>
        </div>
        
        {/* Stats Counter */}
        <div className="mt-16 grid grid-cols-1 md:grid-cols-4 gap-8 max-w-4xl mx-auto">
          <div className="text-center">
            <div className="text-4xl font-bold text-yellow-300 mb-2">2.8M+</div>
            <div className="text-blue-200">Businesses</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-yellow-300 mb-2">27</div>
            <div className="text-blue-200">Countries</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-yellow-300 mb-2">50K+</div>
            <div className="text-blue-200">Daily Searches</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-yellow-300 mb-2">4.8★</div>
            <div className="text-blue-200">User Rating</div>
          </div>
        </div>
      </div>
    </div>
  );
}