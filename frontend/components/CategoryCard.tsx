import Link from 'next/link';
import { translate, Language, getTranslatedPath } from '@/lib/i18n';

interface CategoryCardProps {
  category: {
    slug: string;
    name: string;
    count: number;
  };
  lang: string;
  variant?: 'default' | 'featured';
}

// Beautiful geometric icons for categories using CSS shapes with EU theme
const getCategoryIcon = (slug: string) => {
  const icons = {
    'restaurants': (
      <div className="w-6 h-6 relative">
        <div className="absolute inset-0 bg-amber-400 rounded-full opacity-90 shadow-sm"></div>
        <div className="absolute top-1 left-1 w-4 h-4 bg-amber-300 rounded-full shadow-inner"></div>
        <div className="absolute top-2 left-2 w-2 h-2 bg-white rounded-full opacity-60"></div>
      </div>
    ),
    'hotels': (
      <div className="w-6 h-6 relative flex items-center justify-center">
        <div className="w-5 h-5 bg-amber-400 rounded-sm transform rotate-45 opacity-90 shadow-md"></div>
        <div className="absolute w-3 h-3 bg-amber-300 rounded-sm transform rotate-45"></div>
      </div>
    ),
    'shopping': (
      <div className="w-6 h-6 flex flex-col justify-center space-y-0.5">
        <div className="w-6 h-1.5 bg-amber-400 rounded-full shadow-sm"></div>
        <div className="w-4 h-1.5 bg-amber-300 rounded-full ml-1 shadow-sm"></div>
        <div className="w-5 h-1.5 bg-amber-400 rounded-full shadow-sm"></div>
      </div>
    ),
    'health': (
      <div className="w-6 h-6 relative flex items-center justify-center">
        <div className="absolute w-4 h-1.5 bg-amber-400 rounded-sm shadow-md"></div>
        <div className="absolute w-1.5 h-4 bg-amber-400 rounded-sm shadow-md"></div>
      </div>
    ),
    'services': (
      <div className="w-6 h-6 grid grid-cols-2 gap-0.5 p-0.5">
        <div className="bg-amber-400 rounded-sm shadow-sm"></div>
        <div className="bg-amber-300 rounded-sm opacity-80 shadow-sm"></div>
        <div className="bg-amber-300 rounded-sm opacity-80 shadow-sm"></div>
        <div className="bg-amber-400 rounded-sm shadow-sm"></div>
      </div>
    ),
    'automotive': (
      <div className="w-6 h-6 relative flex items-center justify-center">
        <div className="w-6 h-2.5 bg-amber-400 rounded-full shadow-md"></div>
        <div className="absolute bottom-1 left-1 w-1 h-1 bg-amber-300 rounded-full shadow-sm"></div>
        <div className="absolute bottom-1 right-1 w-1 h-1 bg-amber-300 rounded-full shadow-sm"></div>
      </div>
    ),
    'finance': (
      <div className="w-6 h-6 relative flex items-center justify-center">
        <div className="w-5 h-5 border-2 border-amber-400 rounded-full"></div>
        <div className="absolute w-3 h-0.5 bg-amber-400 rounded-full"></div>
        <div className="absolute w-0.5 h-3 bg-amber-400 rounded-full"></div>
      </div>
    ),
    'education': (
      <div className="w-6 h-6 relative">
        <div className="w-6 h-4 bg-amber-400 rounded-t-lg opacity-90 shadow-sm"></div>
        <div className="absolute bottom-0 w-6 h-1 bg-amber-300 rounded-sm"></div>
        <div className="absolute top-1 left-1 w-4 h-0.5 bg-amber-300 rounded-full"></div>
        <div className="absolute top-2.5 left-1 w-3 h-0.5 bg-amber-300 rounded-full"></div>
      </div>
    ),
  };

  // Match category by keywords
  const lowerSlug = slug.toLowerCase();
  if (lowerSlug.includes('restaurant') || lowerSlug.includes('food') || lowerSlug.includes('cafe') || lowerSlug.includes('dining')) return icons.restaurants;
  if (lowerSlug.includes('hotel') || lowerSlug.includes('accommodation') || lowerSlug.includes('lodging')) return icons.hotels;
  if (lowerSlug.includes('shop') || lowerSlug.includes('retail') || lowerSlug.includes('store') || lowerSlug.includes('market')) return icons.shopping;
  if (lowerSlug.includes('health') || lowerSlug.includes('medical') || lowerSlug.includes('clinic') || lowerSlug.includes('hospital')) return icons.health;
  if (lowerSlug.includes('auto') || lowerSlug.includes('car') || lowerSlug.includes('repair') || lowerSlug.includes('garage')) return icons.automotive;
  if (lowerSlug.includes('bank') || lowerSlug.includes('finance') || lowerSlug.includes('insurance') || lowerSlug.includes('accounting')) return icons.finance;
  if (lowerSlug.includes('school') || lowerSlug.includes('education') || lowerSlug.includes('university') || lowerSlug.includes('learning')) return icons.education;
  
  // Default services icon
  return icons.services;
};



export default function CategoryCard({ category, lang, variant = 'default' }: CategoryCardProps) {
  
  return (
    <div className="group relative bg-gradient-to-br from-blue-50 via-white to-amber-50 rounded-xl shadow-lg hover:shadow-xl transition-all duration-500 transform hover:-translate-y-2 hover:scale-[1.02] border border-blue-100 overflow-hidden">
      {/* Shimmer effect on hover */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-blue-100/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700"></div>
      
      {/* Decorative corner accents - using static classes for Tailwind compatibility */}
      <div className="absolute top-0 right-0 w-20 h-20 bg-gradient-to-bl from-blue-600 to-blue-500 opacity-10 rounded-bl-full group-hover:opacity-20 transition-opacity duration-300"></div>
      <div className="absolute bottom-0 left-0 w-16 h-16 bg-gradient-to-tr from-amber-400 to-amber-300 opacity-10 rounded-tr-full group-hover:opacity-20 transition-opacity duration-300"></div>
      
      {/* Animated background dots */}
      <div className="absolute inset-0">
        <div className="absolute top-4 right-8 w-2 h-2 bg-blue-600 rounded-full animate-pulse opacity-20"></div>
        <div className="absolute bottom-8 right-4 w-1 h-1 bg-amber-500 rounded-full animate-pulse opacity-30" style={{animationDelay: '0.5s'}}></div>
        <div className="absolute top-12 left-4 w-1.5 h-1.5 bg-blue-500 rounded-full animate-pulse opacity-25" style={{animationDelay: '1s'}}></div>
      </div>
      
      <div className="relative p-6">
        {/* Icon with EU-themed gradient */}
        <div className="w-12 h-12 rounded-lg bg-gradient-to-r from-blue-600 to-blue-700 flex items-center justify-center mb-4 shadow-md group-hover:shadow-lg transition-shadow">
          {getCategoryIcon(category.slug)}
        </div>
        
        <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-blue-700 transition-colors leading-tight">
          {category.name}
        </h3>
        
        {/* Elegant divider with business count */}
        <div className="flex items-center mb-4">
          <div className="flex-1 h-px bg-gradient-to-r from-blue-200 to-amber-200"></div>
          <div className="px-3 text-sm font-medium text-gray-600 bg-gradient-to-r from-blue-100 to-amber-100 rounded-full py-1 shadow-sm">
            {category.count} {translate('common.businesses', lang as Language)}
          </div>
          <div className="flex-1 h-px bg-gradient-to-l from-blue-200 to-amber-200"></div>
        </div>
        
        {/* Call to action */}
        <Link
          href={`/${lang}/${getTranslatedPath('categories', lang as Language)}/${category.slug}`}
          className="inline-flex items-center text-blue-700 hover:text-blue-800 font-semibold group-hover:translate-x-1 transition-all duration-200"
        >
          <span className="mr-2">{translate('common.browse', lang as Language)}</span>
          <div className="w-5 h-5 rounded-full bg-gradient-to-r from-blue-600 to-amber-500 flex items-center justify-center shadow-sm group-hover:shadow-md transition-shadow">
            <span className="text-white text-xs font-bold">→</span>
          </div>
        </Link>
      </div>
      
      {/* Animated hover border */}
      <div className="absolute inset-0 rounded-xl border-2 border-transparent group-hover:shadow-lg group-hover:shadow-blue-200/30 transition-all duration-300 pointer-events-none"></div>
    </div>
  );
}