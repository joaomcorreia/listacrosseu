'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { translate } from '@/lib/i18n';
import { getLanguageForCountry, getCountryDisplayName, type Language } from '@/lib/countryLanguageMapping';

interface Business {
    id: number;
    name: string;
    category: string;
    address: string;
    city: string;
    phone: string;
    email: string;
    website: string;
    description: string;
}

interface Country {
    code: string;
    name: {
        en: string;
        es: string;
        fr: string;
        nl: string;
        pt: string;
        de: string;
    };
    flag: string;
    capital: string;
    population: string;
    count: number;
}

// Complete list of EU 27 countries
const EU_COUNTRIES = [
    { code: 'AT', name: { en: 'Austria', es: 'Austria', fr: 'Autriche', nl: 'Oostenrijk', pt: 'Áustria', de: 'Österreich' }, flag: '🇦🇹', capital: 'Vienna', population: '8.9M' },
    { code: 'BE', name: { en: 'Belgium', es: 'Bélgica', fr: 'Belgique', nl: 'België', pt: 'Bélgica', de: 'Belgien' }, flag: '🇧🇪', capital: 'Brussels', population: '11.5M' },
    { code: 'BG', name: { en: 'Bulgaria', es: 'Bulgaria', fr: 'Bulgarie', nl: 'Bulgarije', pt: 'Bulgária', de: 'Bulgarien' }, flag: '🇧🇬', capital: 'Sofia', population: '7.0M' },
    { code: 'CY', name: { en: 'Cyprus', es: 'Chipre', fr: 'Chypre', nl: 'Cyprus', pt: 'Chipre', de: 'Zypern' }, flag: '🇨🇾', capital: 'Nicosia', population: '1.2M' },
    { code: 'CZ', name: { en: 'Czech Republic', es: 'República Checa', fr: 'République tchèque', nl: 'Tsjechië', pt: 'República Checa', de: 'Tschechien' }, flag: '🇨🇿', capital: 'Prague', population: '10.7M' },
    { code: 'DE', name: { en: 'Germany', es: 'Alemania', fr: 'Allemagne', nl: 'Duitsland', pt: 'Alemanha', de: 'Deutschland' }, flag: '🇩🇪', capital: 'Berlin', population: '83.2M' },
    { code: 'DK', name: { en: 'Denmark', es: 'Dinamarca', fr: 'Danemark', nl: 'Denemarken', pt: 'Dinamarca', de: 'Dänemark' }, flag: '🇩🇰', capital: 'Copenhagen', population: '5.8M' },
    { code: 'EE', name: { en: 'Estonia', es: 'Estonia', fr: 'Estonie', nl: 'Estland', pt: 'Estônia', de: 'Estland' }, flag: '🇪🇪', capital: 'Tallinn', population: '1.3M' },
    { code: 'ES', name: { en: 'Spain', es: 'España', fr: 'Espagne', nl: 'Spanje', pt: 'Espanha', de: 'Spanien' }, flag: '🇪🇸', capital: 'Madrid', population: '47.4M' },
    { code: 'FI', name: { en: 'Finland', es: 'Finlandia', fr: 'Finlande', nl: 'Finland', pt: 'Finlândia', de: 'Finnland' }, flag: '🇫🇮', capital: 'Helsinki', population: '5.5M' },
    { code: 'FR', name: { en: 'France', es: 'Francia', fr: 'France', nl: 'Frankrijk', pt: 'França', de: 'Frankreich' }, flag: '🇫🇷', capital: 'Paris', population: '67.4M' },
    { code: 'GR', name: { en: 'Greece', es: 'Grecia', fr: 'Grèce', nl: 'Griekenland', pt: 'Grécia', de: 'Griechenland' }, flag: '🇬🇷', capital: 'Athens', population: '10.7M' },
    { code: 'HR', name: { en: 'Croatia', es: 'Croacia', fr: 'Croatie', nl: 'Kroatië', pt: 'Croácia', de: 'Kroatien' }, flag: '🇭🇷', capital: 'Zagreb', population: '3.9M' },
    { code: 'HU', name: { en: 'Hungary', es: 'Hungría', fr: 'Hongrie', nl: 'Hongarije', pt: 'Hungria', de: 'Ungarn' }, flag: '🇭🇺', capital: 'Budapest', population: '9.8M' },
    { code: 'IE', name: { en: 'Ireland', es: 'Irlanda', fr: 'Irlande', nl: 'Ierland', pt: 'Irlanda', de: 'Irland' }, flag: '🇮🇪', capital: 'Dublin', population: '4.9M' },
    { code: 'IT', name: { en: 'Italy', es: 'Italia', fr: 'Italie', nl: 'Italië', pt: 'Itália', de: 'Italien' }, flag: '🇮🇹', capital: 'Rome', population: '60.4M' },
    { code: 'LT', name: { en: 'Lithuania', es: 'Lituania', fr: 'Lituanie', nl: 'Litouwen', pt: 'Lituânia', de: 'Litauen' }, flag: '🇱🇹', capital: 'Vilnius', population: '2.8M' },
    { code: 'LU', name: { en: 'Luxembourg', es: 'Luxemburgo', fr: 'Luxembourg', nl: 'Luxemburg', pt: 'Luxemburgo', de: 'Luxemburg' }, flag: '🇱🇺', capital: 'Luxembourg', population: '0.6M' },
    { code: 'LV', name: { en: 'Latvia', es: 'Letonia', fr: 'Lettonie', nl: 'Letland', pt: 'Letônia', de: 'Lettland' }, flag: '🇱🇻', capital: 'Riga', population: '1.9M' },
    { code: 'MT', name: { en: 'Malta', es: 'Malta', fr: 'Malte', nl: 'Malta', pt: 'Malta', de: 'Malta' }, flag: '🇲🇹', capital: 'Valletta', population: '0.5M' },
    { code: 'NL', name: { en: 'Netherlands', es: 'Países Bajos', fr: 'Pays-Bas', nl: 'Nederland', pt: 'Países Baixos', de: 'Niederlande' }, flag: '🇳🇱', capital: 'Amsterdam', population: '17.4M' },
    { code: 'PL', name: { en: 'Poland', es: 'Polonia', fr: 'Pologne', nl: 'Polen', pt: 'Polônia', de: 'Polen' }, flag: '🇵🇱', capital: 'Warsaw', population: '38.0M' },
    { code: 'PT', name: { en: 'Portugal', es: 'Portugal', fr: 'Portugal', nl: 'Portugal', pt: 'Portugal', de: 'Portugal' }, flag: '🇵🇹', capital: 'Lisbon', population: '10.3M' },
    { code: 'RO', name: { en: 'Romania', es: 'Rumania', fr: 'Roumanie', nl: 'Roemenië', pt: 'Romênia', de: 'Rumänien' }, flag: '🇷🇴', capital: 'Bucharest', population: '19.3M' },
    { code: 'SE', name: { en: 'Sweden', es: 'Suecia', fr: 'Suède', nl: 'Zweden', pt: 'Suécia', de: 'Schweden' }, flag: '🇸🇪', capital: 'Stockholm', population: '10.3M' },
    { code: 'SI', name: { en: 'Slovenia', es: 'Eslovenia', fr: 'Slovénie', nl: 'Slovenië', pt: 'Eslovênia', de: 'Slowenien' }, flag: '🇸🇮', capital: 'Ljubljana', population: '2.1M' },
    { code: 'SK', name: { en: 'Slovakia', es: 'Eslovaquia', fr: 'Slovaquie', nl: 'Slowakije', pt: 'Eslováquia', de: 'Slowakei' }, flag: '🇸🇰', capital: 'Bratislava', population: '5.5M' }
];

export default function CountryPage() {
    const params = useParams();
    const router = useRouter();
    const countryCode = (params?.countryCode as string)?.toUpperCase();

    // Get the language for this country (its native/primary language)
    const language = getLanguageForCountry(countryCode) as Language;

    const [businesses, setBusinesses] = useState<Business[]>([]);
    const [categories, setCategories] = useState<string[]>([]);
    const [selectedCategory, setSelectedCategory] = useState<string>('');
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // Find the current country data
    const country = EU_COUNTRIES.find(c => c.code === countryCode);

    useEffect(() => {
        if (!country) {
            router.push('/en');
            return;
        }

        const fetchData = async () => {
            try {
                setLoading(true);

                // Fetch businesses for this country
                const businessParams = new URLSearchParams({
                    page: currentPage.toString(),
                    page_size: '12',
                    country: countryCode,
                    ...(selectedCategory && { category: selectedCategory })
                });

                const businessResponse = await fetch(`http://127.0.0.1:8000/api/businesses/?${businessParams}`);
                if (!businessResponse.ok) throw new Error('Failed to fetch businesses');

                const businessData = await businessResponse.json();
                setBusinesses(businessData.items || []);
                setTotalPages(Math.ceil((businessData.total || 0) / 12));

                // Fetch categories for this country
                const categoryParams = new URLSearchParams({
                    country: countryCode,
                    lang: language
                });

                const categoryResponse = await fetch(`http://127.0.0.1:8000/api/categories/?${categoryParams}`);
                if (!categoryResponse.ok) throw new Error('Failed to fetch categories');

                const categoryData = await categoryResponse.json();
                setCategories(categoryData.items?.map((cat: any) => cat.name) || []);

            } catch (error) {
                console.error('Error fetching data:', error);
                setError('Failed to load data');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [countryCode, currentPage, selectedCategory, language, country, router]);

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                    <p className="text-gray-600">{translate('loading', language)}</p>
                </div>
            </div>
        );
    }

    if (error || !country) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <h1 className="text-4xl font-bold text-red-600 mb-4">404</h1>
                    <p className="text-gray-600 mb-4">{translate('countryNotFound', language)}</p>
                    <Link
                        href="/en"
                        className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                    >
                        {translate('backToHome', language)}
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Hero Section */}
            <div className="bg-gradient-to-r from-blue-600 to-purple-700 text-white py-16">
                <div className="container mx-auto px-4">
                    <div className="text-center">
                        <div className="text-6xl mb-4">{country.flag}</div>
                        <h1 className="text-4xl md:text-5xl font-bold mb-4">
                            {getCountryDisplayName(countryCode, country)}
                        </h1>
                        <p className="text-xl opacity-90 mb-6">
                            {translate('businessDirectory', language)}
                        </p>
                        <div className="flex justify-center items-center gap-6 text-sm opacity-75">
                            <span>{translate('capital', language)}: {country.capital}</span>
                            <span>{translate('population', language)}: {country.population}</span>
                        </div>
                    </div>
                </div>
            </div>

            <div className="container mx-auto px-4 py-8">
                <div className="flex flex-col lg:flex-row gap-8">

                    {/* Main Content */}
                    <div className="flex-1">
                        {/* Category Filter */}
                        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
                            <h2 className="text-xl font-semibold mb-4">{translate('filterByCategory', language)}</h2>
                            <div className="flex flex-wrap gap-2">
                                <button
                                    onClick={() => setSelectedCategory('')}
                                    className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${selectedCategory === ''
                                            ? 'bg-blue-600 text-white'
                                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                        }`}
                                >
                                    {translate('allCategories', language)}
                                </button>
                                {categories.map((category) => (
                                    <button
                                        key={category}
                                        onClick={() => setSelectedCategory(category)}
                                        className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${selectedCategory === category
                                                ? 'bg-blue-600 text-white'
                                                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                            }`}
                                    >
                                        {category}
                                    </button>
                                ))}
                            </div>
                        </div>

                        {/* Business Grid */}
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                            {businesses.map((business) => (
                                <div key={business.id} className="bg-white rounded-xl shadow-sm hover:shadow-lg transition-all duration-300 hover:-translate-y-1 border border-gray-100 overflow-hidden">
                                    {/* Card Header */}
                                    <div className="bg-gradient-to-r from-blue-50 to-purple-50 px-6 py-4 border-b border-gray-100">
                                        <div className="flex items-start justify-between">
                                            <div className="flex-1">
                                                <h3 className="text-lg font-bold text-gray-900 mb-1 line-clamp-2">{business.name}</h3>
                                                <div className="flex items-center space-x-2">
                                                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                                        {business.category}
                                                    </span>
                                                </div>
                                            </div>
                                            <div className="flex-shrink-0 ml-3">
                                                <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center text-white text-lg font-bold">
                                                    {business.name.charAt(0).toUpperCase()}
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                    {/* Card Content */}
                                    <div className="p-6">
                                        {/* Location */}
                                        <div className="flex items-center text-gray-600 text-sm mb-4">
                                            <svg className="w-4 h-4 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                                            </svg>
                                            <span className="font-medium">{business.city}</span>
                                        </div>

                                        {/* Contact Information */}
                                        <div className="space-y-3 mb-4">
                                            {business.phone && (
                                                <div className="flex items-center">
                                                    <svg className="w-4 h-4 mr-3 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                                                    </svg>
                                                    <a
                                                        href={`tel:${business.phone}`}
                                                        className="text-blue-600 hover:text-blue-700 font-medium text-sm transition-colors"
                                                    >
                                                        {business.phone}
                                                    </a>
                                                </div>
                                            )}

                                            {business.email && (
                                                <div className="flex items-center">
                                                    <svg className="w-4 h-4 mr-3 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                                    </svg>
                                                    <a
                                                        href={`mailto:${business.email}`}
                                                        className="text-blue-600 hover:text-blue-700 font-medium text-sm transition-colors truncate"
                                                    >
                                                        {business.email}
                                                    </a>
                                                </div>
                                            )}

                                            {business.website && (
                                                <div className="flex items-center">
                                                    <svg className="w-4 h-4 mr-3 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9m0 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                                                    </svg>
                                                    <a
                                                        href={business.website.startsWith('http') ? business.website : `https://${business.website}`}
                                                        target="_blank"
                                                        rel="noopener noreferrer"
                                                        className="text-blue-600 hover:text-blue-700 font-medium text-sm transition-colors inline-flex items-center"
                                                    >
                                                        {translate('visitWebsite', language)}
                                                        <svg className="w-3 h-3 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                                                        </svg>
                                                    </a>
                                                </div>
                                            )}
                                        </div>

                                        {/* Description */}
                                        {business.description && (
                                            <div className="border-t pt-4 mt-4">
                                                <p className="text-gray-700 text-sm leading-relaxed line-clamp-3">{business.description}</p>
                                            </div>
                                        )}
                                    </div>

                                    {/* Card Footer */}
                                    <div className="px-6 py-3 bg-gray-50 border-t border-gray-100">
                                        <div className="flex items-center justify-between">
                                            <span className="text-xs text-gray-500 font-medium">
                                                {translate('common.business_card', language)}
                                            </span>
                                            <div className="flex items-center space-x-1">
                                                {business.phone && (
                                                    <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                                                )}
                                                {business.email && (
                                                    <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
                                                )}
                                                {business.website && (
                                                    <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>

                        {/* Pagination */}
                        {totalPages > 1 && (
                            <div className="flex justify-center space-x-2">
                                {Array.from({ length: totalPages }, (_, i) => (
                                    <button
                                        key={i + 1}
                                        onClick={() => setCurrentPage(i + 1)}
                                        className={`px-4 py-2 rounded ${currentPage === i + 1
                                                ? 'bg-blue-600 text-white'
                                                : 'bg-white text-gray-700 hover:bg-gray-100'
                                            }`}
                                    >
                                        {i + 1}
                                    </button>
                                ))}
                            </div>
                        )}

                        {/* No Results */}
                        {businesses.length === 0 && !loading && (
                            <div className="text-center py-12">
                                <p className="text-gray-600 text-lg">{translate('noBusinessesFound', language)}</p>
                                <p className="text-gray-500 mt-2">{translate('tryDifferentCategory', language)}</p>
                            </div>
                        )}
                    </div>

                    {/* Right Sidebar */}
                    <div className="lg:w-80">
                        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
                            <h3 className="text-xl font-semibold mb-4">{translate('countryInfo', language)}</h3>

                            <div className="space-y-4">
                                <div className="flex items-center justify-between">
                                    <span className="text-gray-600">{translate('flag', language)}:</span>
                                    <span className="text-2xl">{country.flag}</span>
                                </div>

                                <div className="flex items-center justify-between">
                                    <span className="text-gray-600">{translate('capital', language)}:</span>
                                    <span className="font-medium">{country.capital}</span>
                                </div>

                                <div className="flex items-center justify-between">
                                    <span className="text-gray-600">{translate('population', language)}:</span>
                                    <span className="font-medium">{country.population}</span>
                                </div>
                            </div>
                        </div>

                        {/* Statistics */}
                        <div className="bg-white rounded-lg shadow-sm p-6">
                            <h3 className="text-xl font-semibold mb-4">{translate('statistics', language)}</h3>

                            <div className="space-y-4">
                                <div className="flex items-center justify-between">
                                    <span className="text-gray-600">{translate('totalBusinesses', language)}:</span>
                                    <span className="font-bold text-blue-600 text-xl">{businesses.length}</span>
                                </div>

                                <div className="flex items-center justify-between">
                                    <span className="text-gray-600">{translate('categories', language)}:</span>
                                    <span className="font-bold text-green-600 text-xl">{categories.length}</span>
                                </div>
                            </div>
                        </div>

                        {/* Language Switching */}
                        <div className="bg-white rounded-lg shadow-sm p-6 mt-6">
                            <h3 className="text-xl font-semibold mb-4">{translate('viewInLanguage', language)}</h3>

                            <div className="space-y-2">
                                <Link
                                    href={`/en/countries/${countryCode.toLowerCase()}`}
                                    className="block w-full text-left px-4 py-2 text-blue-600 hover:bg-blue-50 rounded transition-colors"
                                >
                                    🇬🇧 English
                                </Link>
                                <Link
                                    href={`/es/countries/${countryCode.toLowerCase()}`}
                                    className="block w-full text-left px-4 py-2 text-blue-600 hover:bg-blue-50 rounded transition-colors"
                                >
                                    🇪🇸 Español
                                </Link>
                                <Link
                                    href={`/fr/countries/${countryCode.toLowerCase()}`}
                                    className="block w-full text-left px-4 py-2 text-blue-600 hover:bg-blue-50 rounded transition-colors"
                                >
                                    🇫🇷 Français
                                </Link>
                                <Link
                                    href={`/nl/countries/${countryCode.toLowerCase()}`}
                                    className="block w-full text-left px-4 py-2 text-blue-600 hover:bg-blue-50 rounded transition-colors"
                                >
                                    🇳🇱 Nederlands
                                </Link>
                                <Link
                                    href={`/pt/countries/${countryCode.toLowerCase()}`}
                                    className="block w-full text-left px-4 py-2 text-blue-600 hover:bg-blue-50 rounded transition-colors"
                                >
                                    🇵🇹 Português
                                </Link>
                                <Link
                                    href={`/de/countries/${countryCode.toLowerCase()}`}
                                    className="block w-full text-left px-4 py-2 text-blue-600 hover:bg-blue-50 rounded transition-colors"
                                >
                                    🇩🇪 Deutsch
                                </Link>
                            </div>
                        </div>

                        {/* Quick Links */}
                        <div className="bg-white rounded-lg shadow-sm p-6 mt-6">
                            <h3 className="text-xl font-semibold mb-4">{translate('quickLinks', language)}</h3>

                            <div className="space-y-2">
                                <Link
                                    href="/en"
                                    className="block w-full text-left px-4 py-2 text-blue-600 hover:bg-blue-50 rounded transition-colors"
                                >
                                    {translate('allCountries', language)}
                                </Link>

                                {/* Links to neighboring or related countries */}
                                {countryCode === 'BE' && (
                                    <>
                                        <Link
                                            href="/country/fr"
                                            className="block w-full text-left px-4 py-2 text-blue-600 hover:bg-blue-50 rounded transition-colors"
                                        >
                                            🇫🇷 France
                                        </Link>
                                        <Link
                                            href="/country/nl"
                                            className="block w-full text-left px-4 py-2 text-blue-600 hover:bg-blue-50 rounded transition-colors"
                                        >
                                            🇳🇱 Nederland
                                        </Link>
                                        <Link
                                            href="/country/de"
                                            className="block w-full text-left px-4 py-2 text-blue-600 hover:bg-blue-50 rounded transition-colors"
                                        >
                                            🇩🇪 Deutschland
                                        </Link>
                                    </>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}