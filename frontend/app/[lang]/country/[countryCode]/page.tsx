import { notFound } from 'next/navigation';
import Link from 'next/link';
import { fetchBusinesses, fetchCategories, fetchCountries, Business, Category, Country } from '@/lib/api';
import { translate, Language } from '@/lib/i18n';

// Format numbers consistently for both server and client
const formatNumber = (num: number): string => {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
};

interface CountryPageProps {
    params: Promise<{ lang: string; countryCode: string }>;
    searchParams: Promise<{
        category?: string;
        city?: string;
        search?: string;
    }>;
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

    // Fetch data
    const businessesResponse = await fetchBusinesses({
        country: countryCode,
        page: 1,
        page_size: 12,
        ...(resolvedSearchParams.category && { category: resolvedSearchParams.category })
    });

    const categoriesResponse = await fetchCategories(lang, countryCode);
    const businesses = businessesResponse.items;
    const categories = categoriesResponse.items;
    const totalBusinesses = businessesResponse.pagination?.total_count || 0;

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Breadcrumb */}
            <div className="bg-white border-b">
                <div className="container mx-auto px-4 py-3">
                    <Link 
                        href={`/${lang}`}
                        className="text-blue-600 hover:text-blue-800 font-medium inline-flex items-center"
                    >
                        ← Back to Countries
                    </Link>
                </div>
            </div>

            {/* Page Header */}
            <div className="bg-white border-b">
                <div className="container mx-auto px-4 py-8">
                    <div className="flex items-center">
                        <div className="text-6xl mr-6">
                            {countryCode === 'BE' && '🇧🇪'}
                            {countryCode === 'FR' && '🇫🇷'}
                            {countryCode === 'NL' && '🇳🇱'}
                            {countryCode === 'DE' && '🇩🇪'}
                            {countryCode === 'ES' && '🇪🇸'}
                            {countryCode === 'IT' && '🇮🇹'}
                            {!['BE', 'FR', 'NL', 'DE', 'ES', 'IT'].includes(countryCode) && '🇪🇺'}
                        </div>
                        <div>
                            <div className="text-3xl font-bold text-gray-600 mb-2">
                                {countryCode}
                            </div>
                            <h1 className="text-3xl font-bold text-gray-900">
                                Businesses in {country.name}
                            </h1>
                            <p className="text-gray-600 mt-2">Business Directory</p>
                        </div>
                        <div className="ml-auto">
                            <Link
                                href={`/${lang}/add-business?country=${countryCode}`}
                                className="bg-yellow-500 hover:bg-yellow-600 text-white px-6 py-2 rounded-lg font-medium transition-colors"
                            >
                                List Business
                            </Link>
                        </div>
                    </div>
                </div>
            </div>

            <div className="container mx-auto px-4 py-8">
                <div className="flex flex-col lg:flex-row gap-8">
                    {/* Main Content */}
                    <div className="flex-1">
                        {businesses.length === 0 ? (
                            <div className="bg-white rounded-lg shadow-sm p-12 text-center">
                                <div className="text-6xl mb-6">🏢</div>
                                <h2 className="text-2xl font-bold text-gray-900 mb-4">
                                    No businesses found in this country yet.
                                </h2>
                                <p className="text-gray-600 mb-8">
                                    Be the first to list your business in {country.name}!
                                </p>
                                <Link
                                    href={`/${lang}/add-business?country=${countryCode}`}
                                    className="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
                                >
                                    Add Your Business
                                </Link>
                            </div>
                        ) : (
                            <>
                                {/* Category Filter */}
                                <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
                                    <h2 className="text-xl font-semibold mb-4">Filter by Category</h2>
                                    <div className="flex flex-wrap gap-2">
                                        <Link
                                            href={`/${lang}/country/${countryCode.toLowerCase()}`}
                                            className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                                                !resolvedSearchParams.category
                                                    ? 'bg-blue-600 text-white'
                                                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                            }`}
                                        >
                                            All Categories
                                        </Link>
                                        {categories.map((category: Category) => (
                                            <Link
                                                key={category.slug}
                                                href={`/${lang}/country/${countryCode.toLowerCase()}?category=${category.name}`}
                                                className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                                                    resolvedSearchParams.category === category.name
                                                        ? 'bg-blue-600 text-white'
                                                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                                }`}
                                            >
                                                {category.name}
                                            </Link>
                                        ))}
                                    </div>
                                </div>

                                {/* Business Grid */}
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                    {businesses.map((business: Business, index: number) => (
                                        <div key={business.slug || index} className="bg-white rounded-xl shadow-sm hover:shadow-lg transition-all duration-300 hover:-translate-y-1 border border-gray-100 overflow-hidden">
                                            <div className="bg-gradient-to-r from-blue-50 to-purple-50 px-6 py-4 border-b border-gray-100">
                                                <div className="flex items-start justify-between">
                                                    <div className="flex-1">
                                                        <h3 className="text-lg font-bold text-gray-900 mb-1">{business.name}</h3>
                                                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                                            Business
                                                        </span>
                                                    </div>
                                                    <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center text-white text-lg font-bold">
                                                        {business.name.charAt(0).toUpperCase()}
                                                    </div>
                                                </div>
                                            </div>
                                            
                                            <div className="p-6">
                                                {business.city_name && (
                                                    <div className="flex items-center text-gray-600 text-sm mb-4">
                                                        <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                                        </svg>
                                                        <span className="font-medium">{business.city_name}</span>
                                                    </div>
                                                )}

                                                <div className="space-y-2">
                                                    {business.phone && (
                                                        <div className="flex items-center text-sm text-gray-600">
                                                            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                                                            </svg>
                                                            <a href={`tel:${business.phone}`} className="text-blue-600 hover:text-blue-700">
                                                                {business.phone}
                                                            </a>
                                                        </div>
                                                    )}
                                                    {business.email && (
                                                        <div className="flex items-center text-sm text-gray-600">
                                                            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                                            </svg>
                                                            <a href={`mailto:${business.email}`} className="text-blue-600 hover:text-blue-700">
                                                                {business.email}
                                                            </a>
                                                        </div>
                                                    )}
                                                    {business.website && (
                                                        <div className="flex items-center text-sm text-gray-600">
                                                            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9m0 9c1.657 0 3-4.03-3-9s1.343-9 3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                                                            </svg>
                                                            <a 
                                                                href={business.website.startsWith('http') ? business.website : `https://${business.website}`} 
                                                                target="_blank" 
                                                                rel="noopener noreferrer"
                                                                className="text-blue-600 hover:text-blue-700"
                                                            >
                                                                Visit Website
                                                            </a>
                                                        </div>
                                                    )}
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </>
                        )}
                    </div>

                    {/* Right Sidebar */}
                    <div className="lg:w-80">
                        {/* Country Information */}
                        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
                            <h3 className="text-xl font-semibold mb-4">Country Information</h3>
                            <div className="space-y-4">
                                <div className="flex items-center justify-between">
                                    <span className="text-gray-600">Capital:</span>
                                    <span className="font-medium">
                                        {countryCode === 'BE' && 'Brussels'}
                                        {countryCode === 'FR' && 'Paris'}
                                        {countryCode === 'NL' && 'Amsterdam'}
                                        {countryCode === 'DE' && 'Berlin'}
                                        {countryCode === 'ES' && 'Madrid'}
                                        {countryCode === 'IT' && 'Rome'}
                                        {!['BE', 'FR', 'NL', 'DE', 'ES', 'IT'].includes(countryCode) && 'Unknown'}
                                    </span>
                                </div>
                                <div className="flex items-center justify-between">
                                    <span className="text-gray-600">Population:</span>
                                    <span className="font-medium">
                                        {countryCode === 'BE' && '11.5M'}
                                        {countryCode === 'FR' && '67.4M'}
                                        {countryCode === 'NL' && '17.4M'}
                                        {countryCode === 'DE' && '83.2M'}
                                        {countryCode === 'ES' && '47.4M'}
                                        {countryCode === 'IT' && '60.4M'}
                                        {!['BE', 'FR', 'NL', 'DE', 'ES', 'IT'].includes(countryCode) && 'Unknown'}
                                    </span>
                                </div>
                                <div className="flex items-center justify-between">
                                    <span className="text-gray-600">Code:</span>
                                    <span className="font-medium">{countryCode}</span>
                                </div>
                            </div>
                        </div>

                        {/* Quick Stats */}
                        <div className="bg-white rounded-lg shadow-sm p-6">
                            <h3 className="text-xl font-semibold mb-4">Quick Stats</h3>
                            <div className="space-y-4">
                                <div className="flex items-center justify-between">
                                    <span className="text-gray-600">Total Businesses:</span>
                                    <span className="font-bold text-blue-600 text-xl">{formatNumber(totalBusinesses)}</span>
                                </div>
                                <div className="flex items-center justify-between">
                                    <span className="text-gray-600">Categories Available:</span>
                                    <span className="font-bold text-green-600 text-xl">{categories.length}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export async function generateStaticParams() {
    const countries = await fetchCountries();
    const languages = ['en', 'es', 'fr', 'de', 'nl'];

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