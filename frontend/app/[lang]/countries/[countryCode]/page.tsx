'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { translate, Language } from '@/lib/i18n';

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
    { code: 'IE', name: { en: 'Ireland', es: 'Irlanda', fr: 'Irlande', nl: 'Ierland', pt: 'Irlanda', de: 'Irland' }, flag: '🇮🇪', capital: 'Dublin', population: '5.0M' },
    { code: 'IT', name: { en: 'Italy', es: 'Italia', fr: 'Italie', nl: 'Italië', pt: 'Itália', de: 'Italien' }, flag: '🇮🇹', capital: 'Rome', population: '60.4M' },
    { code: 'LT', name: { en: 'Lithuania', es: 'Lituania', fr: 'Lituanie', nl: 'Litouwen', pt: 'Lituânia', de: 'Litauen' }, flag: '🇱🇹', capital: 'Vilnius', population: '2.8M' },
    { code: 'LU', name: { en: 'Luxembourg', es: 'Luxemburgo', fr: 'Luxembourg', nl: 'Luxemburg', pt: 'Luxemburgo', de: 'Luxemburg' }, flag: '🇱🇺', capital: 'Luxembourg', population: '630K' },
    { code: 'LV', name: { en: 'Latvia', es: 'Letonia', fr: 'Lettonie', nl: 'Letland', pt: 'Letônia', de: 'Lettland' }, flag: '🇱🇻', capital: 'Riga', population: '1.9M' },
    { code: 'MT', name: { en: 'Malta', es: 'Malta', fr: 'Malte', nl: 'Malta', pt: 'Malta', de: 'Malta' }, flag: '🇲🇹', capital: 'Valletta', population: '520K' },
    { code: 'NL', name: { en: 'Netherlands', es: 'Países Bajos', fr: 'Pays-Bas', nl: 'Nederland', pt: 'Países Baixos', de: 'Niederlande' }, flag: '🇳🇱', capital: 'Amsterdam', population: '17.4M' },
    { code: 'PL', name: { en: 'Poland', es: 'Polonia', fr: 'Pologne', nl: 'Polen', pt: 'Polônia', de: 'Polen' }, flag: '🇵🇱', capital: 'Warsaw', population: '38.0M' },
    { code: 'PT', name: { en: 'Portugal', es: 'Portugal', fr: 'Portugal', nl: 'Portugal', pt: 'Portugal', de: 'Portugal' }, flag: '🇵🇹', capital: 'Lisbon', population: '10.3M' },
    { code: 'RO', name: { en: 'Romania', es: 'Rumania', fr: 'Roumanie', nl: 'Roemenië', pt: 'Romênia', de: 'Rumänien' }, flag: '🇷🇴', capital: 'Bucharest', population: '19.3M' },
    { code: 'SE', name: { en: 'Sweden', es: 'Suecia', fr: 'Suède', nl: 'Zweden', pt: 'Suécia', de: 'Schweden' }, flag: '🇸🇪', capital: 'Stockholm', population: '10.4M' },
    { code: 'SI', name: { en: 'Slovenia', es: 'Eslovenia', fr: 'Slovénie', nl: 'Slovenië', pt: 'Eslovênia', de: 'Slowenien' }, flag: '🇸🇮', capital: 'Ljubljana', population: '2.1M' },
    { code: 'SK', name: { en: 'Slovakia', es: 'Eslovaquia', fr: 'Slovaquie', nl: 'Slowakije', pt: 'Eslováquia', de: 'Slowakei' }, flag: '🇸🇰', capital: 'Bratislava', population: '5.5M' },
];

export default function CountryPage() {
    const params = useParams();
    const router = useRouter();
    const lang = params.lang as Language;
    const countryCode = (params.countryCode as string)?.toUpperCase();

    const [businesses, setBusinesses] = useState<Business[]>([]);
    const [loading, setLoading] = useState(true);
    const [categories, setCategories] = useState<string[]>([]);
    const [selectedCategory, setSelectedCategory] = useState<string>('all');

    const country = EU_COUNTRIES.find(c => c.code === countryCode);

    const texts = {
        en: {
            title: 'Businesses in',
            backToCountries: 'Back to Countries',
            capital: 'Capital',
            population: 'Population',
            allCategories: 'All Categories',
            noBusinesses: 'No businesses found in this country yet.',
            addBusiness: 'Add Your Business',
            contact: 'Contact',
            website: 'Website',
            loading: 'Loading businesses...',
            businessDirectory: 'Business Directory',
            countryInfo: 'Country Information',
            quickStats: 'Quick Stats',
            totalBusinesses: 'Total Businesses',
            categories: 'Categories Available',
        },
        es: {
            title: 'Empresas en',
            backToCountries: 'Volver a Países',
            capital: 'Capital',
            population: 'Población',
            allCategories: 'Todas las Categorías',
            noBusinesses: 'Aún no se han encontrado empresas en este país.',
            addBusiness: 'Agregar Su Empresa',
            contact: 'Contacto',
            website: 'Sitio Web',
            loading: 'Cargando empresas...',
            businessDirectory: 'Directorio de Empresas',
            countryInfo: 'Información del País',
            quickStats: 'Estadísticas Rápidas',
            totalBusinesses: 'Total de Empresas',
            categories: 'Categorías Disponibles',
        },
        fr: {
            title: 'Entreprises en',
            backToCountries: 'Retour aux Pays',
            capital: 'Capitale',
            population: 'Population',
            allCategories: 'Toutes les Catégories',
            noBusinesses: 'Aucune entreprise trouvée dans ce pays pour le moment.',
            addBusiness: 'Ajouter Votre Entreprise',
            contact: 'Contact',
            website: 'Site Web',
            loading: 'Chargement des entreprises...',
            businessDirectory: 'Annuaire des Entreprises',
            countryInfo: 'Informations sur le Pays',
            quickStats: 'Statistiques Rapides',
            totalBusinesses: 'Total des Entreprises',
            categories: 'Catégories Disponibles',
        },
        nl: {
            title: 'Bedrijven in',
            backToCountries: 'Terug naar Landen',
            capital: 'Hoofdstad',
            population: 'Bevolking',
            allCategories: 'Alle Categorieën',
            noBusinesses: 'Nog geen bedrijven gevonden in dit land.',
            addBusiness: 'Voeg Uw Bedrijf Toe',
            contact: 'Contact',
            website: 'Website',
            loading: 'Bedrijven laden...',
            businessDirectory: 'Bedrijvendirectory',
            countryInfo: 'Landinformatie',
            quickStats: 'Snelle Statistieken',
            totalBusinesses: 'Totaal Bedrijven',
            categories: 'Beschikbare Categorieën',
        },
        pt: {
            title: 'Empresas em',
            backToCountries: 'Voltar aos Países',
            capital: 'Capital',
            population: 'População',
            allCategories: 'Todas as Categorias',
            noBusinesses: 'Ainda não foram encontradas empresas neste país.',
            addBusiness: 'Adicionar Sua Empresa',
            contact: 'Contato',
            website: 'Website',
            loading: 'Carregando empresas...',
            businessDirectory: 'Diretório de Empresas',
            countryInfo: 'Informações do País',
            quickStats: 'Estatísticas Rápidas',
            totalBusinesses: 'Total de Empresas',
            categories: 'Categorias Disponíveis',
        },
        de: {
            title: 'Unternehmen in',
            backToCountries: 'Zurück zu den Ländern',
            capital: 'Hauptstadt',
            population: 'Bevölkerung',
            allCategories: 'Alle Kategorien',
            noBusinesses: 'Noch keine Unternehmen in diesem Land gefunden.',
            addBusiness: 'Ihr Unternehmen Hinzufügen',
            contact: 'Kontakt',
            website: 'Website',
            loading: 'Unternehmen werden geladen...',
            businessDirectory: 'Unternehmensverzeichnis',
            countryInfo: 'Länderinformationen',
            quickStats: 'Schnelle Statistiken',
            totalBusinesses: 'Gesamte Unternehmen',
            categories: 'Verfügbare Kategorien',
        },
    };

    const currentTexts = texts[lang] || texts.en;

    useEffect(() => {
        if (!country) {
            router.push(`/${lang}/countries`);
            return;
        }

        const fetchBusinesses = async () => {
            try {
                setLoading(true);
                const response = await fetch(`http://localhost:8000/api/businesses/?country=${countryCode}&lang=${lang}`);
                if (response.ok) {
                    const data = await response.json();
                    setBusinesses(data.items || []);

                    // Extract unique categories
                    const categorySet = new Set((data.items || []).map((b: Business) => b.category));
                    const uniqueCategories = Array.from(categorySet).filter(Boolean) as string[];
                    setCategories(uniqueCategories);
                }
            } catch (error) {
                console.error('Error fetching businesses:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchBusinesses();
    }, [countryCode, lang, country, router]);

    if (!country) {
        return null;
    }

    const getCountryName = () => {
        return country.name[lang] || country.name.en;
    };

    const filteredBusinesses = selectedCategory === 'all'
        ? businesses
        : businesses.filter(b => b.category === selectedCategory);

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
            <div className="container mx-auto px-4 py-8">
                {/* Header */}
                <div className="mb-8">
                    <Link
                        href={`/${lang}/countries`}
                        className="inline-flex items-center text-blue-600 hover:text-blue-800 transition-colors duration-200 mb-4"
                    >
                        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                        </svg>
                        {currentTexts.backToCountries}
                    </Link>

                    <div className="bg-white rounded-xl shadow-lg p-6 border border-slate-200">
                        <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-4">
                                <span className="text-6xl">{country.flag}</span>
                                <div>
                                    <h1 className="text-3xl font-bold text-slate-800">
                                        {currentTexts.title} {getCountryName()}
                                    </h1>
                                    <p className="text-slate-600 mt-1">{currentTexts.businessDirectory}</p>
                                </div>
                            </div>
                            <div className="bg-yellow-400 text-yellow-900 px-3 py-2 rounded-full text-sm font-medium flex items-center space-x-2 shadow-sm">
                                <span>⭐</span>
                                <span>EU Member</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
                    {/* Main Content */}
                    <div className="lg:col-span-3">
                        {/* Category Filter */}
                        {categories.length > 0 && (
                            <div className="mb-6 bg-white rounded-xl shadow-md p-4 border border-slate-200">
                                <div className="flex flex-wrap gap-2">
                                    <button
                                        onClick={() => setSelectedCategory('all')}
                                        className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${selectedCategory === 'all'
                                                ? 'bg-blue-500 text-white shadow-md'
                                                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                            }`}
                                    >
                                        {currentTexts.allCategories}
                                    </button>
                                    {categories.map((category) => (
                                        <button
                                            key={category}
                                            onClick={() => setSelectedCategory(category)}
                                            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${selectedCategory === category
                                                    ? 'bg-blue-500 text-white shadow-md'
                                                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                                }`}
                                        >
                                            {category}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Businesses List */}
                        {loading ? (
                            <div className="text-center py-12">
                                <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                                <p className="mt-4 text-slate-600">{currentTexts.loading}</p>
                            </div>
                        ) : filteredBusinesses.length > 0 ? (
                            <div className="space-y-6">
                                {filteredBusinesses.map((business) => (
                                    <div
                                        key={business.id}
                                        className="bg-white rounded-xl shadow-md hover:shadow-lg transition-all duration-300 border border-slate-200 p-6"
                                    >
                                        <div className="flex justify-between items-start mb-4">
                                            <div>
                                                <h3 className="text-xl font-semibold text-slate-800 mb-2">{business.name}</h3>
                                                <div className="flex items-center space-x-4 text-sm text-slate-600">
                                                    <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full font-medium">
                                                        {business.category}
                                                    </span>
                                                    <span>{business.city}</span>
                                                </div>
                                            </div>
                                        </div>

                                        {business.description && (
                                            <p className="text-slate-700 mb-4">{business.description}</p>
                                        )}

                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                                            {business.address && (
                                                <div className="flex items-center space-x-2">
                                                    <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                                                    </svg>
                                                    <span className="text-slate-700">{business.address}</span>
                                                </div>
                                            )}

                                            {business.phone && (
                                                <div className="flex items-center space-x-2">
                                                    <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                                                    </svg>
                                                    <span className="text-slate-700">{business.phone}</span>
                                                </div>
                                            )}

                                            {business.email && (
                                                <div className="flex items-center space-x-2">
                                                    <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                                    </svg>
                                                    <span className="text-slate-700">{business.email}</span>
                                                </div>
                                            )}

                                            {business.website && (
                                                <div className="flex items-center space-x-2">
                                                    <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                                                    </svg>
                                                    <a
                                                        href={business.website}
                                                        target="_blank"
                                                        rel="noopener noreferrer"
                                                        className="text-blue-600 hover:text-blue-800 transition-colors"
                                                    >
                                                        {currentTexts.website}
                                                    </a>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <div className="text-center py-12 bg-white rounded-xl shadow-md border border-slate-200">
                                <div className="text-6xl mb-4">🏢</div>
                                <h3 className="text-xl font-semibold text-slate-800 mb-2">{currentTexts.noBusinesses}</h3>
                                <p className="text-slate-600 mb-6">Be the first to list your business in {getCountryName()}!</p>
                                <button className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition-colors font-medium">
                                    {currentTexts.addBusiness}
                                </button>
                            </div>
                        )}
                    </div>

                    {/* Right Sidebar */}
                    <div className="lg:col-span-1">
                        <div className="sticky top-8 space-y-6">
                            {/* Country Info Card */}
                            <div className="bg-white rounded-xl shadow-md p-6 border border-slate-200">
                                <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center">
                                    <svg className="w-5 h-5 mr-2 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    {currentTexts.countryInfo}
                                </h3>
                                <div className="space-y-3">
                                    <div className="flex justify-between">
                                        <span className="text-slate-600">{currentTexts.capital}:</span>
                                        <span className="font-medium text-slate-800">{country.capital}</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-slate-600">{currentTexts.population}:</span>
                                        <span className="font-medium text-slate-800">{country.population}</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-slate-600">Code:</span>
                                        <span className="font-medium text-slate-800">{country.code}</span>
                                    </div>
                                </div>
                            </div>

                            {/* Quick Stats Card */}
                            <div className="bg-white rounded-xl shadow-md p-6 border border-slate-200">
                                <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center">
                                    <svg className="w-5 h-5 mr-2 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                                    </svg>
                                    {currentTexts.quickStats}
                                </h3>
                                <div className="space-y-4">
                                    <div className="text-center p-4 bg-blue-50 rounded-lg">
                                        <div className="text-2xl font-bold text-blue-600">{businesses.length}</div>
                                        <div className="text-sm text-slate-600">{currentTexts.totalBusinesses}</div>
                                    </div>
                                    <div className="text-center p-4 bg-green-50 rounded-lg">
                                        <div className="text-2xl font-bold text-green-600">{categories.length}</div>
                                        <div className="text-sm text-slate-600">{currentTexts.categories}</div>
                                    </div>
                                </div>
                            </div>

                            {/* Other EU Countries */}
                            <div className="bg-white rounded-xl shadow-md p-6 border border-slate-200">
                                <h3 className="text-lg font-semibold text-slate-800 mb-4">Other EU Countries</h3>
                                <div className="space-y-2">
                                    {EU_COUNTRIES
                                        .filter(c => c.code !== countryCode)
                                        .slice(0, 5)
                                        .map((c) => (
                                            <Link
                                                key={c.code}
                                                href={`/${lang}/countries/${c.code.toLowerCase()}`}
                                                className="flex items-center space-x-3 p-2 rounded-lg hover:bg-gray-50 transition-colors"
                                            >
                                                <span className="text-xl">{c.flag}</span>
                                                <span className="text-sm text-slate-700">{c.name[lang] || c.name.en}</span>
                                            </Link>
                                        ))}
                                    <Link
                                        href={`/${lang}/countries`}
                                        className="block text-center text-blue-600 hover:text-blue-800 text-sm mt-3 p-2"
                                    >
                                        View All Countries →
                                    </Link>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}