'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Language, translate, getTranslatedPath } from '@/lib/i18n';

interface HeroSlideshowProps {
  lang: Language;
}

interface Slide {
  title: string;
  subtitle: string;
  description: string;
  primaryButton: {
    text: string;
    href: string;
    icon: string;
  };
  secondaryButton: {
    text: string;
    href: string;
    icon: string;
  };
  backgroundGradient: string;
}

export default function HeroSlideshow({ lang }: HeroSlideshowProps) {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [slideDirection, setSlideDirection] = useState<'next' | 'prev'>('next');

  // Define slides based on language
  const slides: Slide[] = [
    // Slide 1: Business Discovery Focus
    {
      title: translate('homepage.slide1.title', lang),
      subtitle: translate('homepage.slide1.subtitle', lang),
      description: translate('homepage.slide1.description', lang),
      primaryButton: {
        text: translate('homepage.slide1.primary_button', lang),
        href: `/${lang}/${getTranslatedPath('businesses', lang)}`,
        icon: '🏢'
      },
      secondaryButton: {
        text: translate('homepage.slide1.secondary_button', lang),
        href: `/${lang}/${getTranslatedPath('categories', lang)}`,
        icon: '📂'
      },
      backgroundGradient: 'from-blue-600 via-blue-700 to-blue-800'
    },
    // Slide 2: Country Exploration Focus
    {
      title: translate('homepage.slide2.title', lang),
      subtitle: translate('homepage.slide2.subtitle', lang),
      description: translate('homepage.slide2.description', lang),
      primaryButton: {
        text: translate('homepage.slide2.primary_button', lang),
        href: `/${lang}/country/es`, // Example country
        icon: '🇪🇺'
      },
      secondaryButton: {
        text: translate('homepage.slide2.secondary_button', lang),
        href: `/${lang}/${getTranslatedPath('businesses', lang)}`,
        icon: '🔍'
      },
      backgroundGradient: 'from-purple-600 via-indigo-700 to-blue-800'
    }
  ];

  // Auto-advance slides
  useEffect(() => {
    const timer = setInterval(() => {
      handleSlideChange('next', (prev) => (prev + 1) % slides.length);
    }, 8000); // Change slide every 8 seconds

    return () => clearInterval(timer);
  }, [slides.length]);

  const handleSlideChange = (direction: 'next' | 'prev', slideFunction: (prev: number) => number) => {
    if (isTransitioning) return;
    
    setIsTransitioning(true);
    setSlideDirection(direction);
    
    // Start transition
    setTimeout(() => {
      setCurrentSlide(slideFunction);
    }, 100);
    
    // End transition
    setTimeout(() => {
      setIsTransitioning(false);
    }, 1200);
  };

  const goToSlide = (index: number) => {
    if (isTransitioning || index === currentSlide) return;
    
    const direction = index > currentSlide ? 'next' : 'prev';
    handleSlideChange(direction, () => index);
  };

  const nextSlide = () => {
    handleSlideChange('next', (prev) => (prev + 1) % slides.length);
  };

  const prevSlide = () => {
    handleSlideChange('prev', (prev) => (prev - 1 + slides.length) % slides.length);
  };

  return (
    <section className={`relative bg-gradient-to-br ${slides[currentSlide].backgroundGradient} text-white overflow-hidden transition-all duration-1000`}>
      {/* Animated Background Elements */}
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-32 h-32 bg-blue-400/10 rounded-full blur-xl animate-pulse"></div>
        <div className="absolute bottom-20 right-10 w-40 h-40 bg-amber-400/10 rounded-full blur-xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-blue-500/5 rounded-full blur-3xl"></div>
      </div>

      <div className="relative max-w-7xl mx-auto px-4 py-24 lg:py-32">
        <div className="text-center">
          {/* EU Stars Decoration */}
          <div className="flex justify-center mb-8">
            <div className="flex space-x-2">
              {[...Array(12)].map((_, i) => (
                <div 
                  key={i}
                  className="w-2 h-2 bg-amber-400 rounded-full animate-pulse" 
                  style={{ animationDelay: `${i * 100}ms` }}
                ></div>
              ))}
            </div>
          </div>

          {/* Slide Content */}
          <div className={`relative transition-all duration-1000 ${
            isTransitioning 
              ? slideDirection === 'next' 
                ? 'transform translate-x-full opacity-0' 
                : 'transform -translate-x-full opacity-0'
              : 'transform translate-x-0 opacity-100'
          }`}>
            {/* Main Title with Advanced Effects */}
            <h1 className={`text-5xl md:text-7xl lg:text-8xl font-bold mb-8 leading-tight ${
              isTransitioning 
                ? 'animate-title-exit' 
                : 'animate-title-enter'
            }`}>
              <span className="relative inline-block">
                {slides[currentSlide].title.split('').map((char, index) => (
                  <span
                    key={index}
                    className={`inline-block bg-gradient-to-r from-white via-blue-100 to-amber-200 bg-clip-text text-transparent ${
                      isTransitioning ? '' : 'animate-text-reveal'
                    }`}
                    style={{ 
                      animationDelay: isTransitioning ? '0ms' : `${index * 50}ms`,
                      transform: isTransitioning ? 'translateY(20px) rotateX(90deg)' : 'translateY(0) rotateX(0)'
                    }}
                  >
                    {char === ' ' ? '\u00A0' : char}
                  </span>
                ))}
              </span>
            </h1>
            
            {/* Subtitle with Typing Effect */}
            <p className={`text-xl md:text-3xl mb-8 text-blue-100 font-light leading-relaxed max-w-4xl mx-auto overflow-hidden ${
              isTransitioning 
                ? 'animate-slide-up-out' 
                : 'animate-typing'
            }`}>
              <span className={isTransitioning ? '' : 'animate-typewriter'}>
                {slides[currentSlide].subtitle}
              </span>
            </p>
            
            {/* Description with Blur Effect */}
            <p className={`text-lg mb-12 max-w-3xl mx-auto text-blue-50 leading-relaxed ${
              isTransitioning 
                ? 'animate-blur-out opacity-0' 
                : 'animate-blur-in opacity-90'
            }`}>
              {slides[currentSlide].description}
            </p>
            
            {/* Buttons with Stagger Animation */}
            <div className={`flex flex-col sm:flex-row gap-4 justify-center items-center ${
              isTransitioning 
                ? 'animate-buttons-out' 
                : 'animate-buttons-in'
            }`}>
              <Link
                href={slides[currentSlide].primaryButton.href}
                className="group relative bg-white text-blue-600 px-8 py-4 rounded-2xl font-semibold hover:bg-blue-50 transition-all duration-500 shadow-xl hover:shadow-2xl transform hover:-translate-y-2 hover:scale-105 animate-bounce-subtle"
              >
                <span className="flex items-center space-x-2">
                  <span className="animate-spin-slow">{slides[currentSlide].primaryButton.icon}</span>
                  <span>{slides[currentSlide].primaryButton.text}</span>
                  <span className="group-hover:translate-x-2 transition-all duration-300">→</span>
                </span>
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-0 group-hover:opacity-20 transform -skew-x-12 group-hover:translate-x-full transition-all duration-700"></div>
              </Link>
              
              <Link
                href={slides[currentSlide].secondaryButton.href}
                className="group relative bg-gradient-to-r from-blue-500 to-blue-600 text-white px-8 py-4 rounded-2xl font-semibold hover:from-blue-600 hover:to-blue-700 transition-all duration-500 border-2 border-blue-400 shadow-xl hover:shadow-2xl transform hover:-translate-y-2 hover:scale-105 animate-pulse-glow"
              >
                <span className="flex items-center space-x-2">
                  <span className="animate-bounce">{slides[currentSlide].secondaryButton.icon}</span>
                  <span>{slides[currentSlide].secondaryButton.text}</span>
                  <span className="group-hover:translate-x-2 transition-all duration-300">→</span>
                </span>
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-blue-300 to-transparent opacity-0 group-hover:opacity-30 transform -skew-x-12 group-hover:translate-x-full transition-all duration-700"></div>
              </Link>
            </div>
          </div>

          {/* Trust Indicators with Enhanced Animations */}
          <div className={`mt-16 flex flex-wrap justify-center items-center gap-8 text-blue-200 ${
            isTransitioning ? 'animate-trust-out' : 'animate-trust-in'
          }`}>
            <div className="flex items-center space-x-2 animate-float" style={{ animationDelay: '0ms' }}>
              <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center animate-pulse-ring">
                <span className="text-white text-sm font-bold animate-checkmark">✓</span>
              </div>
              <span className="text-sm font-medium">6,000+ Verified Businesses</span>
            </div>
            <div className="flex items-center space-x-2 animate-float" style={{ animationDelay: '200ms' }}>
              <div className="w-8 h-8 bg-amber-500 rounded-full flex items-center justify-center animate-spin-slow">
                <span className="text-white text-sm">🇪🇺</span>
              </div>
              <span className="text-sm font-medium">Across 27 EU Countries</span>
            </div>
            <div className="flex items-center space-x-2 animate-float" style={{ animationDelay: '400ms' }}>
              <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center animate-electric">
                <span className="text-white text-sm animate-bounce">⚡</span>
              </div>
              <span className="text-sm font-medium">Real-time Updates</span>
            </div>
          </div>
        </div>

        {/* Enhanced Navigation Controls */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex items-center space-x-6 animate-nav-in">
          {/* Previous Button */}
          <button
            onClick={prevSlide}
            disabled={isTransitioning}
            className="group w-12 h-12 bg-white/10 hover:bg-white/25 rounded-full flex items-center justify-center transition-all duration-300 backdrop-blur-md border border-white/20 hover:border-white/40 transform hover:scale-110 disabled:opacity-50 disabled:cursor-not-allowed"
            aria-label="Previous slide"
          >
            <span className="text-white text-lg transform group-hover:-translate-x-0.5 transition-transform">←</span>
            <div className="absolute inset-0 rounded-full bg-gradient-to-r from-blue-400/20 to-purple-400/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          </button>

          {/* Enhanced Slide Indicators */}
          <div className="flex space-x-3">
            {slides.map((_, index) => (
              <button
                key={index}
                onClick={() => goToSlide(index)}
                disabled={isTransitioning}
                className={`relative transition-all duration-500 disabled:cursor-not-allowed ${
                  index === currentSlide
                    ? 'w-8 h-3 bg-amber-400 rounded-full scale-125 shadow-lg shadow-amber-400/50'
                    : 'w-3 h-3 bg-white/40 hover:bg-white/70 rounded-full hover:scale-110'
                }`}
                aria-label={`Go to slide ${index + 1}`}
              >
                {index === currentSlide && (
                  <div className="absolute inset-0 bg-amber-300 rounded-full animate-ping opacity-75"></div>
                )}
              </button>
            ))}
          </div>

          {/* Next Button */}
          <button
            onClick={nextSlide}
            disabled={isTransitioning}
            className="group w-12 h-12 bg-white/10 hover:bg-white/25 rounded-full flex items-center justify-center transition-all duration-300 backdrop-blur-md border border-white/20 hover:border-white/40 transform hover:scale-110 disabled:opacity-50 disabled:cursor-not-allowed"
            aria-label="Next slide"
          >
            <span className="text-white text-lg transform group-hover:translate-x-0.5 transition-transform">→</span>
            <div className="absolute inset-0 rounded-full bg-gradient-to-r from-purple-400/20 to-blue-400/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          </button>
        </div>

        {/* Wave Separator */}
        <div className="absolute bottom-0 left-0 right-0">
          <svg viewBox="0 0 1200 120" preserveAspectRatio="none" className="w-full h-12 fill-white">
            <path d="M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z"></path>
          </svg>
        </div>
      </div>

      {/* Advanced CSS Animations */}
      <style jsx>{`
        /* Title Animations */
        @keyframes title-enter {
          from {
            opacity: 0;
            transform: translateY(-50px) scale(0.8);
            filter: blur(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0) scale(1);
            filter: blur(0);
          }
        }

        @keyframes title-exit {
          from {
            opacity: 1;
            transform: translateY(0) scale(1);
            filter: blur(0);
          }
          to {
            opacity: 0;
            transform: translateY(50px) scale(1.1);
            filter: blur(5px);
          }
        }

        .animate-title-enter {
          animation: title-enter 1.2s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .animate-title-exit {
          animation: title-exit 0.6s ease-in-out;
        }

        /* Text Reveal Animation */
        @keyframes text-reveal {
          from {
            opacity: 0;
            transform: translateY(30px) rotateX(90deg);
          }
          to {
            opacity: 1;
            transform: translateY(0) rotateX(0);
          }
        }

        .animate-text-reveal {
          animation: text-reveal 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) both;
        }

        /* Typing Animation */
        @keyframes typing {
          from {
            width: 0;
            opacity: 0;
          }
          to {
            width: 100%;
            opacity: 1;
          }
        }

        @keyframes slide-up-out {
          from {
            opacity: 1;
            transform: translateY(0);
          }
          to {
            opacity: 0;
            transform: translateY(-30px);
          }
        }

        .animate-typing {
          animation: typing 2s steps(40, end) 0.5s both;
        }

        .animate-slide-up-out {
          animation: slide-up-out 0.6s ease-in-out;
        }

        /* Blur Effects */
        @keyframes blur-in {
          from {
            opacity: 0;
            filter: blur(10px);
            transform: translateY(20px);
          }
          to {
            opacity: 0.9;
            filter: blur(0);
            transform: translateY(0);
          }
        }

        @keyframes blur-out {
          from {
            opacity: 0.9;
            filter: blur(0);
            transform: translateY(0);
          }
          to {
            opacity: 0;
            filter: blur(8px);
            transform: translateY(-20px);
          }
        }

        .animate-blur-in {
          animation: blur-in 1s ease-out 1s both;
        }

        .animate-blur-out {
          animation: blur-out 0.6s ease-in-out;
        }

        /* Button Animations */
        @keyframes buttons-in {
          from {
            opacity: 0;
            transform: translateY(40px) scale(0.8);
          }
          to {
            opacity: 1;
            transform: translateY(0) scale(1);
          }
        }

        @keyframes buttons-out {
          from {
            opacity: 1;
            transform: translateY(0) scale(1);
          }
          to {
            opacity: 0;
            transform: translateY(40px) scale(0.9);
          }
        }

        .animate-buttons-in {
          animation: buttons-in 0.8s cubic-bezier(0.16, 1, 0.3, 1) 1.5s both;
        }

        .animate-buttons-out {
          animation: buttons-out 0.5s ease-in-out;
        }

        /* Trust Indicators */
        @keyframes trust-in {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes trust-out {
          from {
            opacity: 1;
            transform: translateY(0);
          }
          to {
            opacity: 0;
            transform: translateY(-30px);
          }
        }

        .animate-trust-in {
          animation: trust-in 0.6s ease-out 2s both;
        }

        .animate-trust-out {
          animation: trust-out 0.4s ease-in-out;
        }

        /* Floating Animation */
        @keyframes float {
          0%, 100% {
            transform: translateY(0);
          }
          50% {
            transform: translateY(-10px);
          }
        }

        .animate-float {
          animation: float 3s ease-in-out infinite;
        }

        /* Navigation Animation */
        @keyframes nav-in {
          from {
            opacity: 0;
            transform: translateY(20px) translateX(-50%);
          }
          to {
            opacity: 1;
            transform: translateY(0) translateX(-50%);
          }
        }

        .animate-nav-in {
          animation: nav-in 0.8s ease-out 2.5s both;
        }

        /* Special Effects */
        @keyframes pulse-ring {
          0% {
            box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7);
          }
          70% {
            box-shadow: 0 0 0 10px rgba(59, 130, 246, 0);
          }
          100% {
            box-shadow: 0 0 0 0 rgba(59, 130, 246, 0);
          }
        }

        .animate-pulse-ring {
          animation: pulse-ring 2s infinite;
        }

        @keyframes checkmark {
          0% {
            transform: scale(0) rotate(0deg);
          }
          50% {
            transform: scale(1.2) rotate(180deg);
          }
          100% {
            transform: scale(1) rotate(360deg);
          }
        }

        .animate-checkmark {
          animation: checkmark 0.6s ease-out;
        }

        @keyframes electric {
          0%, 100% {
            box-shadow: 0 0 5px #10b981;
          }
          50% {
            box-shadow: 0 0 20px #10b981, 0 0 30px #10b981;
          }
        }

        .animate-electric {
          animation: electric 1.5s ease-in-out infinite;
        }

        @keyframes spin-slow {
          from {
            transform: rotate(0deg);
          }
          to {
            transform: rotate(360deg);
          }
        }

        .animate-spin-slow {
          animation: spin-slow 8s linear infinite;
        }

        @keyframes bounce-subtle {
          0%, 100% {
            transform: translateY(0);
          }
          50% {
            transform: translateY(-5px);
          }
        }

        .animate-bounce-subtle {
          animation: bounce-subtle 2s ease-in-out infinite;
        }

        @keyframes pulse-glow {
          0%, 100% {
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
          }
          50% {
            box-shadow: 0 0 40px rgba(59, 130, 246, 0.8);
          }
        }

        .animate-pulse-glow {
          animation: pulse-glow 2s ease-in-out infinite;
        }
      `}</style>
    </section>
  );
}