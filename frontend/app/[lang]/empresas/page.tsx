import { Suspense } from 'react';
import { fetchBusinesses, fetchCategories, fetchCountries, Business, Category, Country } from '@/lib/api';
import Link from 'next/link';
import { translate, Language, getCountryFromLanguage } from '@/lib/i18n';
import LanguageSwitcher from '@/components/LanguageSwitcher';

interface BusinessesPageProps {
  params: Promise<{ lang: string }>;
  searchParams: Promise<{ 
    category?: string;
    country?: string; 
    city?: string;
    town?: string;
  }>;
}

type SearchParamsType = { 
  category?: string;
  country?: string; 
  city?: string;
  town?: string;
};

async function BusinessList({ searchParams, lang }: { searchParams: SearchParamsType, lang: Language }) {
  // Add country filter based on language
  const country = getCountryFromLanguage(lang);
  const filtersWithCountry = {
    ...searchParams,
    ...(country && !searchParams.country ? { country } : {})
  };
  
  const businesses = await fetchBusinesses(filtersWithCountry);

  if (businesses.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">{translate('businesses.no_results', lang)}</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {businesses.map((business: Business) => (
        <div key={business.slug} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">{business.name}</h3>
          
          {business.street && (
            <p className="text-sm text-gray-600 mb-1">
              📍 {business.street}
              {business.postcode && `, ${business.postcode}`}
            </p>
          )}
          
          {business.phone && (
            <p className="text-sm text-gray-600 mb-1">
              📞 <a href={`tel:${business.phone}`} className="text-blue-600 hover:underline">
                {business.phone}
              </a>
            </p>
          )}
          
          {business.email && (
            <p className="text-sm text-gray-600 mb-1">
              ✉️ <a href={`mailto:${business.email}`} className="text-blue-600 hover:underline">
                {business.email}
              </a>
            </p>
          )}
          
          {business.website && (
            <p className="text-sm text-gray-600 mb-3">
              🌐 <a href={business.website} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                {translate('common.website', lang)}
              </a>
            </p>
          )}
          
          <div className="text-xs text-gray-500">
            {business.city_name}
            {business.town_name && `, ${business.town_name}`}
          </div>
        </div>
      ))}
    </div>
  );
}

async function FilterSidebar({ lang }: { lang: Language }) {
  const country = getCountryFromLanguage(lang);
  const [categories, countries] = await Promise.all([
    fetchCategories(lang, country || undefined),
    fetchCountries()
  ]);

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold mb-4">{translate('businesses.filter_businesses', lang)}</h3>
      
      <div className="space-y-4">
        <div>
          <h4 className="font-medium text-gray-700 mb-2">{translate('businesses.categories', lang)}</h4>
          <div className="space-y-1">
            {categories.items?.slice(0, 10).map((category: Category) => (
              <Link
                key={category.slug}
                href={`?category=${category.slug}`}
                className="block text-sm text-gray-600 hover:text-blue-600"
              >
                {category.name} ({category.count})
              </Link>
            ))}
          </div>
        </div>
        
        <div>
          <h4 className="font-medium text-gray-700 mb-2">{translate('businesses.countries', lang as Language)}</h4>
          <div className="space-y-1">
            {countries.slice(0, 8).map((country: Country) => (
              <Link
                key={country.code}
                href={`?country=${country.code}`}
                className="block text-sm text-gray-600 hover:text-blue-600"
              >
                {country.name}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default async function BusinessesPage({ params, searchParams }: BusinessesPageProps) {
  const resolvedParams = await params;
  const resolvedSearchParams = await searchParams;

  return (
    <>
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                {translate('businesses.title', resolvedParams.lang as Language)}
              </h1>
              <p className="text-gray-600 mt-1">
                {translate('businesses.subtitle', resolvedParams.lang as Language)}
              </p>
            </div>
            <LanguageSwitcher currentLang={resolvedParams.lang as Language} />
          </div>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar */}
          <div className="lg:col-span-1">
            <Suspense fallback={<div className="animate-pulse bg-gray-200 h-64 rounded-lg"></div>}>
              <FilterSidebar lang={resolvedParams.lang as Language} />
            </Suspense>
          </div>
          
          {/* Main Content */}
          <div className="lg:col-span-3">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold">
                {Object.keys(resolvedSearchParams).length > 0 
                  ? translate('businesses.filtered_results', resolvedParams.lang as Language)
                  : translate('businesses.all_businesses', resolvedParams.lang as Language)
                }
              </h2>
            </div>
            
            <Suspense fallback={
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {[...Array(6)].map((_, i) => (
                  <div key={i} className="animate-pulse bg-gray-200 h-48 rounded-lg"></div>
                ))}
              </div>
            }>
              <BusinessList searchParams={resolvedSearchParams} lang={resolvedParams.lang as Language} />
            </Suspense>
          </div>
        </div>
      </main>
    </>
  );
}