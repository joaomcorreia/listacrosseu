"use client";

import { useRouter, useSearchParams } from 'next/navigation';
import { SupportedLanguage, getUIText } from '@/i18n/ui';

interface SearchFiltersProps {
  lang: SupportedLanguage;
  currentQuery: string;
}

export default function SearchFilters({ lang, currentQuery }: SearchFiltersProps) {
  const router = useRouter();
  const searchParams = useSearchParams();
  
  const currentCountry = searchParams.get('country') || '';
  const currentCity = searchParams.get('city') || '';
  const currentCategory = searchParams.get('category') || '';

  const countries = [
    { value: '', label: 'All Countries' },
    { value: 'France', label: 'France' },
    { value: 'Netherlands', label: 'Netherlands' },
    { value: 'Portugal', label: 'Portugal' },
    { value: 'Germany', label: 'Germany' },
    { value: 'Spain', label: 'Spain' },
    { value: 'Italy', label: 'Italy' }
  ];

  const cities = [
    { value: '', label: 'All Cities' },
    { value: 'Paris', label: 'Paris' },
    { value: 'Amsterdam', label: 'Amsterdam' },
    { value: 'Lisbon', label: 'Lisbon' },
    { value: 'Berlin', label: 'Berlin' },
    { value: 'Madrid', label: 'Madrid' },
    { value: 'Rome', label: 'Rome' },
    { value: 'Porto', label: 'Porto' },
    { value: 'Barcelona', label: 'Barcelona' }
  ];

  const categories = [
    { value: '', label: 'All Categories' },
    { value: 'Restaurant', label: 'Restaurant' },
    { value: 'Technology', label: 'Technology' },
    { value: 'Retail', label: 'Retail' },
    { value: 'Health', label: 'Health' },
    { value: 'Education', label: 'Education' },
    { value: 'Tourism', label: 'Tourism' },
    { value: 'Finance', label: 'Finance' }
  ];

  const updateFilter = (filterType: string, value: string) => {
    const params = new URLSearchParams(searchParams.toString());
    
    if (value) {
      params.set(filterType, value);
    } else {
      params.delete(filterType);
    }

    // Reset to page 1 when filters change
    params.delete('page');
    
    // Keep the search query
    if (currentQuery) {
      params.set('q', currentQuery);
    }

    router.push(`/${lang}/search?${params.toString()}`);
  };

  return (
    <div className="flex flex-wrap gap-4 mb-6 p-4 bg-gray-50 rounded-lg">
      <div className="flex-1 min-w-48">
        <label htmlFor="country" className="block text-sm font-medium text-gray-700 mb-1">
          Country
        </label>
        <select
          id="country"
          value={currentCountry}
          onChange={(e) => updateFilter('country', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
        >
          {countries.map((country) => (
            <option key={country.value} value={country.value}>
              {country.label}
            </option>
          ))}
        </select>
      </div>

      <div className="flex-1 min-w-48">
        <label htmlFor="city" className="block text-sm font-medium text-gray-700 mb-1">
          City
        </label>
        <select
          id="city"
          value={currentCity}
          onChange={(e) => updateFilter('city', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
        >
          {cities.map((city) => (
            <option key={city.value} value={city.value}>
              {city.label}
            </option>
          ))}
        </select>
      </div>

      <div className="flex-1 min-w-48">
        <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-1">
          Category
        </label>
        <select
          id="category"
          value={currentCategory}
          onChange={(e) => updateFilter('category', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
        >
          {categories.map((category) => (
            <option key={category.value} value={category.value}>
              {category.label}
            </option>
          ))}
        </select>
      </div>

      {/* Clear Filters Button */}
      {(currentCountry || currentCity || currentCategory) && (
        <div className="flex items-end">
          <button
            onClick={() => {
              const params = new URLSearchParams();
              if (currentQuery) params.set('q', currentQuery);
              router.push(`/${lang}/search?${params.toString()}`);
            }}
            className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
          >
            Clear Filters
          </button>
        </div>
      )}
    </div>
  );
}