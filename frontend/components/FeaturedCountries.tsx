'use client';

import Link from 'next/link';
import Image from 'next/image';
import { Country } from '@/lib/api';
import { Language } from '@/lib/i18n';

interface FeaturedCountriesProps {
  countries: Country[];
  lang: Language;
}

const countryImages: { [key: string]: string } = {
  'DE': 'https://images.unsplash.com/photo-1467269204594-9661b134dd2b?w=400&h=300&fit=crop', // Brandenburg Gate
  'FR': 'https://images.unsplash.com/photo-1502602898536-47ad22581b52?w=400&h=300&fit=crop', // Eiffel Tower
  'ES': 'https://images.unsplash.com/photo-1539037116277-4db20889f2d4?w=400&h=300&fit=crop', // Barcelona
  'IT': 'https://images.unsplash.com/photo-1515542622106-78bda8ba0e5b?w=400&h=300&fit=crop', // Colosseum
  'NL': 'https://images.unsplash.com/photo-1534351590666-13e3e96b5017?w=400&h=300&fit=crop', // Amsterdam
  'PT': 'https://images.unsplash.com/photo-1555881400-74d7acaacd8b?w=400&h=300&fit=crop', // Lisbon
  'BE': 'https://images.unsplash.com/photo-1588345921523-c2dcdb7f1dcd?w=400&h=300&fit=crop', // Brussels
  'AT': 'https://images.unsplash.com/photo-1516550893923-42d28e5677af?w=400&h=300&fit=crop', // Vienna
  'CH': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop', // Swiss Alps
  'PL': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=300&fit=crop', // Krakow
  'CZ': 'https://images.unsplash.com/photo-1541849546-216549ae216d?w=400&h=300&fit=crop', // Prague
  'HU': 'https://images.unsplash.com/photo-1541368111012-51962777b900?w=400&h=300&fit=crop', // Budapest
  'GR': 'https://images.unsplash.com/photo-1555993539-1732b0258235?w=400&h=300&fit=crop', // Greece
  'IE': 'https://images.unsplash.com/photo-1590736969955-71cc94901144?w=400&h=300&fit=crop', // Ireland
  'SE': 'https://images.unsplash.com/photo-1509356843151-3e7d96241e11?w=400&h=300&fit=crop', // Sweden
  'DK': 'https://images.unsplash.com/photo-1513622470522-26c3c8a854bc?w=400&h=300&fit=crop', // Copenhagen
  'LU': 'https://images.unsplash.com/photo-1581833971358-2c8b550f87b3?w=400&h=300&fit=crop', // Luxembourg City
};

const countryNames: { [key: string]: { [lang in Language]: string } } = {
  'DE': {
    en: 'Germany',
    es: 'Alemania',
    fr: 'Allemagne', 
    de: 'Deutschland',
    nl: 'Duitsland',
    pt: 'Alemanha'
  },
  'FR': {
    en: 'France',
    es: 'Francia',
    fr: 'France',
    de: 'Frankreich', 
    nl: 'Frankrijk',
    pt: 'França'
  },
  'ES': {
    en: 'Spain',
    es: 'España',
    fr: 'Espagne',
    de: 'Spanien',
    nl: 'Spanje', 
    pt: 'Espanha'
  },
  'IT': {
    en: 'Italy',
    es: 'Italia', 
    fr: 'Italie',
    de: 'Italien',
    nl: 'Italië',
    pt: 'Itália'
  },
  'NL': {
    en: 'Netherlands',
    es: 'Países Bajos',
    fr: 'Pays-Bas',
    de: 'Niederlande',
    nl: 'Nederland',
    pt: 'Países Baixos'
  },
  'PT': {
    en: 'Portugal',
    es: 'Portugal',
    fr: 'Portugal', 
    de: 'Portugal',
    nl: 'Portugal',
    pt: 'Portugal'
  },
  'BE': {
    en: 'Belgium',
    es: 'Bélgica',
    fr: 'Belgique',
    de: 'Belgien',
    nl: 'België',
    pt: 'Bélgica'
  },
  'AT': {
    en: 'Austria',
    es: 'Austria',
    fr: 'Autriche',
    de: 'Österreich', 
    nl: 'Oostenrijk',
    pt: 'Áustria'
  },
  'CH': {
    en: 'Switzerland',
    es: 'Suiza',
    fr: 'Suisse',
    de: 'Schweiz',
    nl: 'Zwitserland',
    pt: 'Suíça'
  },
  'PL': {
    en: 'Poland',
    es: 'Polonia',
    fr: 'Pologne',
    de: 'Polen',
    nl: 'Polen',
    pt: 'Polônia'
  },
  'LU': {
    en: 'Luxembourg',
    es: 'Luxemburgo',
    fr: 'Luxembourg',
    de: 'Luxemburg',
    nl: 'Luxemburg',
    pt: 'Luxemburgo'
  }
};

const getMasonryGridClass = (index: number): string => {
  const patterns = [
    'md:col-span-2 md:row-span-2', // Large 
    'md:col-span-1 md:row-span-1', // Small
    'md:col-span-1 md:row-span-2', // Tall
    'md:col-span-2 md:row-span-1', // Wide
    'md:col-span-1 md:row-span-1', // Small
    'md:col-span-1 md:row-span-1', // Small
    'md:col-span-2 md:row-span-1', // Wide
    'md:col-span-1 md:row-span-2', // Tall
    'md:col-span-1 md:row-span-1', // Small
  ];
  return patterns[index % patterns.length];
};

const getMasonryImageClass = (index: number): string => {
  const patterns = [
    'h-80', // Large
    'h-40', // Small  
    'h-64', // Tall
    'h-40', // Wide
    'h-40', // Small
    'h-40', // Small
    'h-40', // Wide
    'h-64', // Tall
    'h-40', // Small
  ];
  return patterns[index % patterns.length];
};

export default function FeaturedCountries({ countries, lang }: FeaturedCountriesProps) {
  if (!countries || countries.length === 0) {
    return null;
  }

  // Define specific countries to display (even with 0 listings)
  const featuredCountryCodes = ['NL', 'BE', 'PT', 'FR', 'DE', 'LU'];
  
  // Filter to show only the featured countries, sort by count (businesses)
  const topCountries = countries
    .filter(country => featuredCountryCodes.includes(country.code))
    .sort((a, b) => b.count - a.count)
    .slice(0, 9);

  return (
    <section className="py-20 bg-gradient-to-b from-slate-50 to-white">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-16">
          <div className="inline-flex items-center space-x-2 bg-purple-100 text-purple-600 px-4 py-2 rounded-full text-sm font-medium mb-6">
            <span>🇪🇺</span>
            <span>Featured Countries</span>
          </div>
          <h2 className="text-4xl lg:text-5xl font-bold text-slate-900 mb-6">
            <span className="bg-gradient-to-r from-slate-900 via-purple-800 to-slate-900 bg-clip-text text-transparent">
              Explore European Markets
            </span>
          </h2>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed">
            Discover thriving business communities across Europe's most active markets
          </p>
        </div>

        {/* Masonry Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 md:grid-rows-4 gap-4 mb-12 auto-rows-min">
          {topCountries.map((country, index) => {
            const countryName = countryNames[country.code]?.[lang] || country.name;
            const imageUrl = countryImages[country.code] || 'https://images.unsplash.com/photo-1467269204594-9661b134dd2b?w=400&h=300&fit=crop';
            
            return (
              <Link
                key={country.code}
                href={`/${lang}/country/${country.code.toLowerCase()}`}
                className={`group relative overflow-hidden rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 ${getMasonryGridClass(index)}`}
              >
                <div className={`relative w-full ${getMasonryImageClass(index)} overflow-hidden`}>
                  <Image
                    src={imageUrl}
                    alt={countryName}
                    fill
                    className="object-cover transition-all duration-700 group-hover:scale-110"
                    sizes="(max-width: 768px) 100vw, (max-width: 1024px) 50vw, 33vw"
                  />
                  
                  {/* Gradient Overlay */}
                  <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent opacity-60 group-hover:opacity-40 transition-opacity duration-300" />
                  
                  {/* Content */}
                  <div className="absolute inset-0 p-6 flex flex-col justify-end text-white">
                    <div className="transform translate-y-2 group-hover:translate-y-0 transition-transform duration-300">
                      <div className="flex items-center space-x-2 mb-2">
                        <span className="text-2xl">{getFlagEmoji(country.code)}</span>
                        <span className="bg-white/20 backdrop-blur-sm px-2 py-1 rounded-full text-xs font-medium">
                          {country.count.toLocaleString()} businesses
                        </span>
                      </div>
                      
                      <h3 className="text-xl md:text-2xl font-bold mb-1 leading-tight">
                        {countryName}
                      </h3>
                      
                      <p className="text-white/80 text-sm opacity-0 group-hover:opacity-100 transition-opacity duration-300 delay-100">
                        Explore local businesses
                      </p>
                    </div>
                    
                    {/* Hover Arrow */}
                    <div className="absolute top-4 right-4 w-8 h-8 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300 transform translate-x-2 group-hover:translate-x-0">
                      <span className="text-white text-sm">→</span>
                    </div>
                  </div>
                </div>
              </Link>
            );
          })}
        </div>

        {/* View All Countries CTA */}
        <div className="text-center">
          <Link
            href={`/${lang}/businesses`} // For now, link to businesses page with country filter capability
            className="group inline-flex items-center space-x-3 bg-gradient-to-r from-purple-600 to-purple-700 text-white px-8 py-4 rounded-2xl font-semibold hover:from-purple-700 hover:to-purple-800 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
          >
            <span>🌍</span>
            <span>Explore All Countries</span>
            <span className="group-hover:translate-x-1 transition-transform">→</span>
          </Link>
        </div>
      </div>
    </section>
  );
}

function getFlagEmoji(countryCode: string): string {
  const flags: { [key: string]: string } = {
    'DE': '🇩🇪',
    'FR': '🇫🇷', 
    'ES': '🇪🇸',
    'IT': '🇮🇹',
    'NL': '🇳🇱',
    'PT': '🇵🇹',
    'BE': '🇧🇪',
    'AT': '🇦🇹',
    'CH': '🇨🇭',
    'PL': '🇵🇱',
    'CZ': '🇨🇿',
    'HU': '🇭🇺',
    'GR': '🇬🇷',
    'IE': '🇮🇪',
    'SE': '🇸🇪',
    'DK': '🇩🇰',
  };
  return flags[countryCode] || '🏳️';
}