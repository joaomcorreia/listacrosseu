'use client';

import Link from 'next/link';
import { useState, useEffect } from 'react';
import { useAnimationSettings } from '@/hooks/useAnimationSettings';

interface HeroSectionProps {
  lang: string;
  ui: any;
}

// Predefined star positions to avoid SSR hydration issues
const STAR_POSITIONS = [
  { left: 10, top: 20, delay: 0.5 },
  { left: 85, top: 15, delay: 1.2 },
  { left: 15, top: 60, delay: 2.1 },
  { left: 70, top: 70, delay: 0.8 },
  { left: 25, top: 35, delay: 1.8 },
  { left: 90, top: 45, delay: 0.3 },
  { left: 5, top: 80, delay: 2.5 },
  { left: 50, top: 10, delay: 1.5 },
  { left: 80, top: 85, delay: 0.7 },
  { left: 35, top: 75, delay: 2.0 },
  { left: 60, top: 25, delay: 1.1 },
  { left: 45, top: 90, delay: 1.9 }
];

export function HeroSection({ lang, ui }: HeroSectionProps) {
  const [businessCount, setBusinessCount] = useState(50000);
  const [isMounted, setIsMounted] = useState(false);
  const { settings: animationSettings } = useAnimationSettings();

  useEffect(() => {
    setIsMounted(true);
    
    // Animated counter effect
    let start = 0;
    const end = 50000;
    const duration = 2000; // 2 seconds
    const stepTime = duration / end;
    
    const timer = setInterval(() => {
      start += Math.floor(end / (duration / 100));
      if (start >= end) {
        setBusinessCount(end);
        clearInterval(timer);
      } else {
        setBusinessCount(start);
      }
    }, 100);

    return () => clearInterval(timer);
  }, []);

  return (
    <section className="relative min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 via-blue-800 to-blue-600 overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <svg className="w-full h-full" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="eu-network" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
              <circle cx="10" cy="10" r="1" fill="#FFD700" opacity="0.5">
                <animate attributeName="opacity" values="0.5;1;0.5" dur="3s" repeatCount="indefinite" />
              </circle>
              <line x1="10" y1="10" x2="20" y2="10" stroke="#FFD700" strokeWidth="0.5" opacity="0.3" />
              <line x1="10" y1="10" x2="10" y2="20" stroke="#FFD700" strokeWidth="0.5" opacity="0.3" />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#eu-network)" />
        </svg>
      </div>

      {/* EU Stars Background - SSR Safe & Admin Controllable */}
      {isMounted && animationSettings.enableStarAnimation && (
        <div className="absolute inset-0">
          {STAR_POSITIONS.map((star, i) => (
            <div
              key={i}
              className="absolute animate-pulse"
              style={{
                left: `${star.left}%`,
                top: `${star.top}%`,
                animationDelay: `${star.delay}s`,
              }}
            >
              <div className="w-2 h-2 bg-yellow-400 rounded-full opacity-60" />
            </div>
          ))}
        </div>
      )}

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        {/* Trust Badge */}
        <div className="mb-8 animate-fade-in-up">
          <div className="inline-flex items-center bg-white/10 backdrop-blur-lg rounded-full px-6 py-3 border border-white/20">
            <span className="text-yellow-400 mr-2">⭐</span>
            <span className="text-white/90 font-medium">
              Trusted by {businessCount.toLocaleString()}+ European businesses
            </span>
          </div>
        </div>

        {/* Main Headline */}
        <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 animate-fade-in-up animation-delay-200">
          <span className="block">Find Businesses</span>
          <span className="block bg-gradient-to-r from-yellow-400 to-yellow-300 bg-clip-text text-transparent">
            Across Europe
          </span>
        </h1>

        {/* Subheadline */}
        <p className="text-xl md:text-2xl text-white/80 mb-12 max-w-4xl mx-auto leading-relaxed animate-fade-in-up animation-delay-400">
          One directory, 27 countries, all industries. Connect with trusted European companies instantly.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center animate-fade-in-up animation-delay-600">
          <Link
            href={`/${lang}/search`}
            className="group relative inline-flex items-center px-8 py-4 bg-gradient-to-r from-yellow-500 to-yellow-400 text-blue-900 font-semibold rounded-lg hover:shadow-2xl hover:shadow-yellow-400/25 transform hover:scale-105 transition-all duration-300"
          >
            <span className="relative z-10">Explore Businesses</span>
            <svg className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform duration-300" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </Link>
          
          <Link
            href={`/${lang}/advertise`}
            className="group inline-flex items-center px-8 py-4 bg-white/10 backdrop-blur-lg text-white font-semibold rounded-lg border border-white/20 hover:bg-white/20 hover:shadow-xl transform hover:scale-105 transition-all duration-300"
          >
            <span>Advertise for Free</span>
            <svg className="ml-2 w-5 h-5 group-hover:rotate-12 transition-transform duration-300" fill="currentColor" viewBox="0 0 20 20">
              <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3z" />
            </svg>
          </Link>
        </div>

        {/* Quick Search Bar */}
        <div className="mt-16 max-w-2xl mx-auto animate-fade-in-up animation-delay-800">
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
            <div className="flex flex-col sm:flex-row gap-3">
              <input
                type="text"
                placeholder="Search businesses, e.g. 'restaurant in Paris'"
                className="flex-1 px-4 py-3 bg-white/90 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 placeholder-gray-500"
              />
              <button className="px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg hover:shadow-lg transform hover:scale-105 transition-all duration-300">
                Search
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <svg className="w-6 h-6 text-white/60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
        </svg>
      </div>
    </section>
  );
}

// Add these animations to your global CSS
const styles = `
@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fade-in-up 0.8s ease-out forwards;
}

.animation-delay-200 {
  animation-delay: 200ms;
}

.animation-delay-400 {
  animation-delay: 400ms;
}

.animation-delay-600 {
  animation-delay: 600ms;
}

.animation-delay-800 {
  animation-delay: 800ms;
}
`;