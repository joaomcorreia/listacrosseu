'use client';

import { useState, useEffect } from 'react';

interface FinalCTASectionProps {
  lang: string;
  ui: any;
}

export function FinalCTASection({ lang, ui }: FinalCTASectionProps) {
  const [currentStat, setCurrentStat] = useState(0);
  const [email, setEmail] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);

  const stats = [
    { number: '2.8M+', label: 'Businesses Listed', icon: '🏢' },
    { number: '27', label: 'EU Countries', icon: '🇪🇺' },
    { number: '50K+', label: 'Daily Searches', icon: '🔍' },
    { number: '99.2%', label: 'Data Accuracy', icon: '✅' },
  ];

  const benefits = [
    { text: 'Instant listing activation', icon: '⚡' },
    { text: 'Free basic features forever', icon: '🆓' },
    { text: 'Multilingual support included', icon: '🌍' },
    { text: 'No hidden fees or commitments', icon: '💯' },
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStat((prev) => (prev + 1) % stats.length);
    }, 2000);

    return () => clearInterval(interval);
  }, [stats.length]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle newsletter signup
    setIsSubmitted(true);
    setTimeout(() => setIsSubmitted(false), 3000);
  };

  return (
    <section className="py-24 bg-gradient-to-br from-blue-900 via-blue-800 to-blue-900 text-white relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0">
        {/* Animated Stars */}
        <div className="absolute top-20 left-20 w-2 h-2 bg-yellow-300 rounded-full animate-pulse" />
        <div className="absolute top-40 right-32 w-1 h-1 bg-white rounded-full animate-ping" />
        <div className="absolute bottom-32 left-1/4 w-1.5 h-1.5 bg-yellow-400 rounded-full animate-pulse" />
        <div className="absolute top-1/3 right-1/4 w-1 h-1 bg-white rounded-full animate-ping" />
        
        {/* EU Flag Stars Pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="flex items-center justify-center h-full">
            <div className="relative w-96 h-64">
              {[...Array(12)].map((_, i) => (
                <div
                  key={i}
                  className="absolute w-4 h-4 text-yellow-300"
                  style={{
                    top: '50%',
                    left: '50%',
                    transform: `translate(-50%, -50%) rotate(${i * 30}deg) translateY(-80px) rotate(-${i * 30}deg)`,
                    animation: `spin 20s linear infinite`,
                    animationDelay: `${i * 0.1}s`,
                  }}
                >
                  ⭐
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-blue-900 to-transparent opacity-50" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          {/* Main Headline */}
          <div className="mb-12">
            <h2 className="text-6xl font-bold mb-6 leading-tight">
              Ready to Connect Across{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-yellow-300 to-yellow-500">
                Europe
              </span>
              ?
            </h2>
            <p className="text-2xl text-blue-100 max-w-4xl mx-auto leading-relaxed">
              Join thousands of businesses already growing their reach across the European Union. Start today and discover new opportunities tomorrow.
            </p>
          </div>

          {/* Rotating Statistics */}
          <div className="mb-16">
            <div className="bg-white bg-opacity-10 backdrop-blur-md rounded-3xl p-8 border border-white border-opacity-20 inline-block">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
                {stats.map((stat, index) => (
                  <div
                    key={index}
                    className={`text-center transition-all duration-500 transform ${
                      currentStat === index ? 'scale-110' : 'scale-100 opacity-70'
                    }`}
                  >
                    <div className="text-4xl mb-2">{stat.icon}</div>
                    <div className="text-3xl font-bold text-yellow-300 mb-1">
                      {stat.number}
                    </div>
                    <div className="text-sm text-blue-200">
                      {stat.label}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* CTA Buttons */}
          <div className="mb-16">
            <div className="flex flex-col sm:flex-row gap-6 justify-center items-center">
              <button className="group px-12 py-6 bg-gradient-to-r from-yellow-400 to-yellow-500 text-blue-900 font-bold text-xl rounded-2xl hover:shadow-2xl hover:shadow-yellow-500/25 transform hover:scale-105 transition-all duration-300 flex items-center space-x-3">
                <span>List Your Business</span>
                <div className="w-8 h-8 bg-blue-900 bg-opacity-20 rounded-full flex items-center justify-center group-hover:rotate-90 transition-transform duration-300">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </div>
              </button>
              
              <button className="px-12 py-6 border-3 border-white text-white font-bold text-xl rounded-2xl hover:bg-white hover:text-blue-900 transform hover:scale-105 transition-all duration-300">
                Search Businesses
              </button>
            </div>

            {/* Benefits List */}
            <div className="mt-12 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-5xl mx-auto">
              {benefits.map((benefit, index) => (
                <div
                  key={index}
                  className="flex items-center space-x-3 text-blue-100 animate-fade-in-up"
                  style={{ animationDelay: `${index * 200}ms` }}
                >
                  <div className="text-2xl">{benefit.icon}</div>
                  <span className="font-medium">{benefit.text}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Newsletter Signup */}
          <div className="bg-white bg-opacity-10 backdrop-blur-md rounded-3xl p-8 border border-white border-opacity-20 max-w-2xl mx-auto">
            <h3 className="text-2xl font-bold mb-4 text-yellow-300">
              Stay Updated with EU Business Trends
            </h3>
            <p className="text-blue-200 mb-6">
              Get weekly insights, new market opportunities, and platform updates delivered to your inbox.
            </p>
            
            {!isSubmitted ? (
              <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-4">
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your email address"
                  className="flex-1 px-6 py-4 rounded-xl bg-white bg-opacity-20 backdrop-blur-sm border border-white border-opacity-30 text-white placeholder-blue-200 focus:outline-none focus:ring-4 focus:ring-yellow-300 focus:ring-opacity-50"
                  required
                />
                <button
                  type="submit"
                  className="px-8 py-4 bg-gradient-to-r from-yellow-400 to-yellow-500 text-blue-900 font-bold rounded-xl hover:shadow-xl transform hover:scale-105 transition-all duration-300"
                >
                  Subscribe
                </button>
              </form>
            ) : (
              <div className="flex items-center justify-center space-x-3 py-4">
                <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                  <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                </div>
                <span className="text-green-300 font-semibold text-lg">Thank you for subscribing!</span>
              </div>
            )}
          </div>

          {/* Trust Badges */}
          <div className="mt-16 flex flex-col md:flex-row items-center justify-center space-y-4 md:space-y-0 md:space-x-12 text-blue-200 text-sm">
            <div className="flex items-center space-x-2">
              <div className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
                <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              </div>
              <span>GDPR Compliant</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center">
                <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
                </svg>
              </div>
              <span>SSL Secured</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-6 h-6 bg-yellow-500 rounded-full flex items-center justify-center">
                <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              </div>
              <span>4.8/5 Rating</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
                <span className="text-white font-bold text-xs">€</span>
              </div>
              <span>EU Based Company</span>
            </div>
          </div>
        </div>
      </div>

      {/* Custom CSS for animations */}
      <style jsx>{`
        @keyframes spin {
          from {
            transform: rotate(0deg);
          }
          to {
            transform: rotate(360deg);
          }
        }
      `}</style>
    </section>
  );
}