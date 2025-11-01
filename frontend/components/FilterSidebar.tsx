'use client';

import { useRouter, useSearchParams } from 'next/navigation';
import { Language, translate } from '@/lib/i18n';
import { Category, Country } from '@/lib/api';

interface FilterSidebarProps {
  lang: Language;
  categories: Category[];
  countries: Country[];
  onFilterChange?: () => void;
}

export default function FilterSidebar({ lang, categories, countries, onFilterChange }: FilterSidebarProps) {
  const router = useRouter();
  const searchParams = useSearchParams();

  const currentCategory = searchParams?.get('category');
  const currentCountry = searchParams?.get('country');

  const handleFilterChange = (key: string, value: string | null) => {
    const params = new URLSearchParams(searchParams?.toString());
    
    if (value) {
      params.set(key, value);
    } else {
      params.delete(key);
    }
    params.delete('page'); // Reset to first page when filtering

    const queryString = params.toString();
    const newUrl = queryString ? `?${queryString}` : '';
    router.push(`/${lang}/businesses${newUrl}`);
    
    onFilterChange?.();
  };

  const clearAllFilters = () => {
    const params = new URLSearchParams(searchParams?.toString());
    params.delete('category');
    params.delete('country');
    params.delete('city');
    params.delete('town');
    params.delete('search');
    params.delete('page');

    const queryString = params.toString();
    const newUrl = queryString ? `?${queryString}` : '';
    router.push(`/${lang}/businesses${newUrl}`);
    
    onFilterChange?.();
  };

  const hasActiveFilters = currentCategory || currentCountry || searchParams?.get('search');

  return (
    <div className="bg-white rounded-2xl shadow-lg p-6 sticky top-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-bold text-slate-800">{translate('search.filters', lang)}</h3>
        {hasActiveFilters && (
          <button
            onClick={clearAllFilters}
            className="text-sm text-blue-600 hover:text-blue-700 font-medium"
          >
            {translate('common.clear_filters', lang)}
          </button>
        )}
      </div>

      {/* Active Filters Display */}
      {hasActiveFilters && (
        <div className="mb-6 p-4 bg-blue-50 rounded-xl">
          <p className="text-sm font-medium text-slate-700 mb-2">Active Filters:</p>
          <div className="flex flex-wrap gap-2">
            {currentCategory && (
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800">
                Category: {categories.find(c => c.slug === currentCategory)?.name || currentCategory}
                <button
                  onClick={() => handleFilterChange('category', null)}
                  className="ml-2 text-blue-600 hover:text-blue-800"
                >
                  ×
                </button>
              </span>
            )}
            {currentCountry && (
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-green-100 text-green-800">
                Country: {countries.find(c => c.code === currentCountry)?.name || currentCountry}
                <button
                  onClick={() => handleFilterChange('country', null)}
                  className="ml-2 text-green-600 hover:text-green-800"
                >
                  ×
                </button>
              </span>
            )}
            {searchParams?.get('search') && (
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-amber-100 text-amber-800">
                Search: "{searchParams.get('search')}"
              </span>
            )}
          </div>
        </div>
      )}

      {/* Categories Filter */}
      <div className="mb-8">
        <h4 className="font-semibold text-slate-700 mb-4 flex items-center">
          <span className="mr-2">📂</span>
          {translate('businesses.categories', lang)}
        </h4>
        <div className="space-y-2 max-h-60 overflow-y-auto">
          {categories.slice(0, 15).map((category) => (
            <button
              key={category.slug}
              onClick={() => handleFilterChange('category', 
                currentCategory === category.slug ? null : category.slug
              )}
              className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-all ${
                currentCategory === category.slug
                  ? 'bg-blue-100 text-blue-800 font-medium'
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
              }`}
            >
              <div className="flex items-center justify-between">
                <span>{category.name}</span>
                <span className="text-xs text-slate-400">{category.count}</span>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Countries Filter */}
      <div className="mb-8">
        <h4 className="font-semibold text-slate-700 mb-4 flex items-center">
          <span className="mr-2">🌍</span>
          {translate('businesses.countries', lang)}
        </h4>
        <div className="space-y-2 max-h-48 overflow-y-auto">
          {countries.slice(0, 12).map((country) => (
            <button
              key={country.code}
              onClick={() => handleFilterChange('country', 
                currentCountry === country.code ? null : country.code
              )}
              className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-all ${
                currentCountry === country.code
                  ? 'bg-green-100 text-green-800 font-medium'
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
              }`}
            >
              <div className="flex items-center justify-between">
                <span>{country.name}</span>
                <span className="text-xs text-slate-400">{country.count}</span>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="pt-6 border-t border-slate-200">
        <button
          onClick={() => router.push(`/${lang}/categories`)}
          className="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white px-4 py-3 rounded-xl font-medium hover:from-blue-700 hover:to-blue-800 transition-all duration-200 shadow-sm hover:shadow-md transform hover:-translate-y-0.5"
        >
          {translate('businesses.browse_categories', lang)}
        </button>
      </div>
    </div>
  );
}