import { Suspense } from 'react';
import { fetchBusinesses, fetchCategories, fetchCountries, Business, Category, Country, BusinessResponse } from '@/lib/api';
import Link from 'next/link';
import { translate, Language, getCountryFromLanguage } from '@/lib/i18n';
import LanguageSwitcher from '@/components/LanguageSwitcher';
import SearchBar from '@/components/SearchBar';
import FilterSidebar from '@/components/FilterSidebar';
import BusinessCard from '@/components/BusinessCard';

interface BusinessesPageProps {
  params: Promise<{ lang: string }>;
  searchParams: Promise<{ 
    category?: string;
    country?: string; 
    city?: string;
    town?: string;
    search?: string;
    page?: string;
  }>;
}

type SearchParamsType = { 
  category?: string;
  country?: string; 
  city?: string;
  town?: string;
  search?: string;
  page?: string;
};

async function BusinessList({ searchParams, lang }: { searchParams: SearchParamsType, lang: Language }) {
  // Add country filter based on language
  const country = getCountryFromLanguage(lang);
  const filtersWithCountry = {
    ...searchParams,
    page: searchParams.page ? parseInt(searchParams.page) : 1,
    page_size: 20,
    ...(country && !searchParams.country ? { country } : {})
  };
  
  const businessesResponse = await fetchBusinesses(filtersWithCountry);
  const { items: businesses, pagination } = businessesResponse;

  if (businesses.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">{translate('businesses.no_results', lang)}</p>
      </div>
    );
  }

  return (
    <>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {businesses.map((business: Business) => (
          <BusinessCard 
            key={business.slug} 
            business={business} 
            lang={lang}
          />
        ))}
    </div>
    
    {/* Pagination */}
    {pagination.total_pages > 1 && (
      <div className="mt-12 flex justify-center">
        <div className="flex items-center space-x-2">
          {pagination.has_previous && (
            <Link 
              href={`/${lang}/businesses?${new URLSearchParams({...searchParams, page: (pagination.page - 1).toString()}).toString()}`}
              className="px-4 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Previous
            </Link>
          )}
          
          <span className="px-4 py-2 text-sm font-medium text-gray-700">
            Page {pagination.page} of {pagination.total_pages}
          </span>
          
          {pagination.has_next && (
            <Link 
              href={`/${lang}/businesses?${new URLSearchParams({...searchParams, page: (pagination.page + 1).toString()}).toString()}`}
              className="px-4 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Next
            </Link>
          )}
        </div>
      </div>
    )}
  </>
  );
}

async function BusinessFilters({ lang }: { lang: Language }) {
  const country = getCountryFromLanguage(lang);
  const [categories, countries] = await Promise.all([
    fetchCategories(lang, country || undefined),
    fetchCountries()
  ]);

  return (
    <FilterSidebar
      lang={lang}
      categories={categories.items || []}
      countries={countries}
    />
  );
}

export default async function BusinessesPage({ params, searchParams }: BusinessesPageProps) {
  const resolvedParams = await params;
  const resolvedSearchParams = await searchParams;
  
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-gradient-to-br from-white via-blue-50/30 to-amber-50/30 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="flex justify-between items-start mb-6">
            <div className="flex-1">
              <h1 className="text-4xl font-bold bg-gradient-to-r from-slate-900 via-blue-800 to-slate-900 bg-clip-text text-transparent mb-2">
                {translate('businesses.title', resolvedParams.lang as Language)}
              </h1>
              <p className="text-slate-600 text-lg">{translate('businesses.subtitle', resolvedParams.lang as Language)}</p>
            </div>
            <LanguageSwitcher currentLang={resolvedParams.lang as Language} />
          </div>
          
          {/* Search Bar */}
          <div className="mb-6">
            <SearchBar 
              lang={resolvedParams.lang as Language} 
              placeholder={translate('search.placeholder', resolvedParams.lang as Language)}
            />
          </div>
          
          {/* Search Results Info */}
          {resolvedSearchParams.search && (
            <div className="mb-4">
              <p className="text-sm text-slate-600">
                <span className="font-medium">{translate('search.showing_results', resolvedParams.lang as Language)}</span>{' '}
                "<span className="font-semibold text-blue-600">{resolvedSearchParams.search}</span>"
              </p>
            </div>
          )}
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar */}
          <div className="lg:col-span-1">
            <Suspense fallback={<div className="animate-pulse bg-gray-200 h-64 rounded-lg"></div>}>
              <BusinessFilters lang={resolvedParams.lang as Language} />
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
              
              {Object.keys(resolvedSearchParams).length > 0 && (
                <Link
                  href={`/${resolvedParams.lang}/businesses`}
                  className="text-blue-600 hover:underline text-sm"
                >
                  {translate('common.clear_filters', resolvedParams.lang as Language)}
                </Link>
              )}
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
    </div>
  );
}