import { Suspense } from 'react';
import { notFound } from 'next/navigation';
import Link from 'next/link';
import { fetchBusinesses, fetchCategories, fetchCountries, Business, Category, Country, BusinessResponse } from '@/lib/api';
import { translate, Language, getCountryFromLanguage } from '@/lib/i18n';
import BusinessCard from '@/components/BusinessCard';
import SearchBar from '@/components/SearchBar';

interface CountryPageProps {
  params: Promise<{ lang: string; countryCode: string }>;
  searchParams: Promise<{ 
    category?: string;
    city?: string;
    search?: string;
  }>;
}

// Featured businesses component
async function FeaturedBusinesses({ countryCode, lang }: { countryCode: string, lang: Language }) {
  const businessesResponse = await fetchBusinesses({
    country: countryCode,
    page: 1,
    page_size: 6
  });

  const businesses = businessesResponse.items;

  if (businesses.length === 0) {
    return null;
  }

  return (
    <section className="mb-12">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">
          {translate('country.featured_businesses', lang)}
        </h2>
        <Link 
          href={`/${lang}/businesses?country=${countryCode}`}
          className="text-blue-600 hover:text-blue-800 font-medium"
        >
          {translate('common.view_all', lang)} →
        </Link>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {businesses.slice(0, 6).map((business: Business) => (
          <BusinessCard 
            key={business.slug} 
            business={business} 
            lang={lang}
            variant="featured"
          />
        ))}
      </div>
    </section>
  );
}

// Popular categories component
async function PopularCategories({ countryCode, lang }: { countryCode: string, lang: Language }) {
  try {
    const categoriesResponse = await fetchCategories(lang, countryCode);
    const categories = categoriesResponse.items;

    if (categories.length === 0) {
      return null;
    }

    return (
      <section className="mb-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          {translate('country.popular_categories', lang)}
        </h2>
        
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {categories.slice(0, 8).map((category: Category) => (
            <Link
              key={category.slug}
              href={`/${lang}/businesses?category=${category.name}&country=${countryCode}`}
              className="group bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-all duration-200 border border-gray-100 hover:border-blue-200"
            >
              <div className="text-center">
                <div className="text-3xl mb-3">🏢</div>
                <h3 className="font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                  {category.name}
                </h3>
                <p className="text-sm text-gray-500 mt-1">
                  {category.count || 0} {translate('common.businesses', lang)}
                </p>
              </div>
            </Link>
          ))}
        </div>
      </section>
    );
  } catch (error) {
    console.error('Error fetching categories:', error);
    return null;
  }
}

// Cities listing component
async function CitiesGrid({ countryCode, lang }: { countryCode: string, lang: Language }) {
  const businessesResponse = await fetchBusinesses({
    country: countryCode,
    page: 1,
    page_size: 100 // Get more to extract unique cities
  });

  // Extract unique cities from businesses
  const cities = Array.from(new Set(
    businessesResponse.items
      .filter((business: Business) => business.city_name)
      .map((business: Business) => business.city_name)
  )).slice(0, 12); // Show top 12 cities

  if (cities.length === 0) {
    return null;
  }

  return (
    <section className="mb-12">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">
        {translate('country.major_cities', lang)}
      </h2>
      
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {cities.map((city: string) => (
          <Link
            key={city}
            href={`/${lang}/businesses?city=${city}&country=${countryCode}`}
            className="bg-gradient-to-r from-blue-50 to-indigo-50 p-4 rounded-lg border border-blue-100 hover:border-blue-300 hover:shadow-md transition-all duration-200"
          >
            <div className="flex items-center">
              <span className="text-xl mr-3">🏙️</span>
              <span className="font-medium text-gray-900 hover:text-blue-600 transition-colors">
                {city}
              </span>
            </div>
          </Link>
        ))}
      </div>
    </section>
  );
}

// Country stats component
async function CountryStats({ countryCode, lang }: { countryCode: string, lang: Language }) {
  const [businessesResponse, categoriesResponse] = await Promise.all([
    fetchBusinesses({ country: countryCode, page: 1, page_size: 1 }),
    fetchCategories(lang, countryCode)
  ]);

  const totalBusinesses = businessesResponse.pagination?.total_count || 0;
  const totalCategories = categoriesResponse.items.length;

  // Extract unique cities count
  const citiesResponse = await fetchBusinesses({
    country: countryCode,
    page: 1,
    page_size: 100
  });
  
  const uniqueCities = new Set(
    citiesResponse.items
      .filter((business: Business) => business.city_name)
      .map((business: Business) => business.city_name)
  );

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 p-6 rounded-lg text-white">
        <div className="text-3xl font-bold">{totalBusinesses.toLocaleString()}</div>
        <div className="text-blue-100 mt-1">{translate('common.total_businesses', lang)}</div>
      </div>
      
      <div className="bg-gradient-to-r from-green-600 to-green-700 p-6 rounded-lg text-white">
        <div className="text-3xl font-bold">{totalCategories}</div>
        <div className="text-green-100 mt-1">{translate('common.categories', lang)}</div>
      </div>
      
      <div className="bg-gradient-to-r from-purple-600 to-purple-700 p-6 rounded-lg text-white">
        <div className="text-3xl font-bold">{uniqueCities.size}</div>
        <div className="text-purple-100 mt-1">{translate('common.cities', lang)}</div>
      </div>
    </div>
  );
}

export default async function CountryPage({ params, searchParams }: CountryPageProps) {
  const resolvedParams = await params;
  const resolvedSearchParams = await searchParams;
  
  const lang = resolvedParams.lang as Language;
  const countryCode = resolvedParams.countryCode.toUpperCase();

  // Verify country exists
  const countries = await fetchCountries();
  const country = countries.find((c: Country) => c.code === countryCode);
  
  if (!country) {
    notFound();
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 via-blue-700 to-indigo-800 text-white">
        <div className="container mx-auto px-4 py-16">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-4xl md:text-5xl font-bold mb-6">
              {translate('country.businesses_in', lang)} {country.name}
            </h1>
            <p className="text-xl text-blue-100 mb-8">
              {translate('country.discover_businesses', lang)} {country.name}
            </p>
            
            {/* Search Bar */}
            <div className="max-w-2xl mx-auto">
              <SearchBar 
                lang={lang}
                placeholder={`${translate('search.search_in', lang)} ${country.name}...`}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-12">
        {/* Country Stats */}
        <Suspense fallback={
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="animate-pulse bg-gray-200 h-24 rounded-lg"></div>
            ))}
          </div>
        }>
          <CountryStats countryCode={countryCode} lang={lang} />
        </Suspense>

        {/* Featured Businesses */}
        <Suspense fallback={
          <div className="mb-12">
            <div className="animate-pulse bg-gray-200 h-8 w-64 rounded mb-6"></div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="animate-pulse bg-gray-200 h-48 rounded-lg"></div>
              ))}
            </div>
          </div>
        }>
          <FeaturedBusinesses countryCode={countryCode} lang={lang} />
        </Suspense>

        {/* Popular Categories */}
        <Suspense fallback={
          <div className="mb-12">
            <div className="animate-pulse bg-gray-200 h-8 w-64 rounded mb-6"></div>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {[...Array(8)].map((_, i) => (
                <div key={i} className="animate-pulse bg-gray-200 h-24 rounded-lg"></div>
              ))}
            </div>
          </div>
        }>
          <PopularCategories countryCode={countryCode} lang={lang} />
        </Suspense>

        {/* Major Cities */}
        <Suspense fallback={
          <div className="mb-12">
            <div className="animate-pulse bg-gray-200 h-8 w-64 rounded mb-6"></div>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {[...Array(12)].map((_, i) => (
                <div key={i} className="animate-pulse bg-gray-200 h-16 rounded-lg"></div>
              ))}
            </div>
          </div>
        }>
          <CitiesGrid countryCode={countryCode} lang={lang} />
        </Suspense>

        {/* Call to Action */}
        <div className="text-center bg-gradient-to-r from-blue-50 to-indigo-50 p-8 rounded-lg border border-blue-100">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            {translate('country.explore_more', lang)}
          </h2>
          <p className="text-gray-600 mb-6">
            {translate('country.browse_all_businesses', lang)} {country.name}
          </p>
          <Link
            href={`/${lang}/businesses?country=${countryCode}`}
            className="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
          >
            {translate('country.view_all_businesses', lang)} →
          </Link>
        </div>
      </div>
    </div>
  );
}

export async function generateStaticParams() {
  // Generate static params for all EU countries and supported languages
  const countries = await fetchCountries();
  const languages = ['en', 'es', 'fr', 'de', 'nl']; // Add more as needed

  const params = [];
  for (const country of countries) {
    for (const lang of languages) {
      params.push({
        lang,
        countryCode: country.code.toLowerCase()
      });
    }
  }

  return params;
}