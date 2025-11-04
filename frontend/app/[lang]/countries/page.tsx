'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { translate, Language } from '@/lib/i18n';

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

// Complete list of EU 27 countries with their details
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
    { code: 'SK', name: { en: 'Slovakia', es: 'Eslovaquia', fr: 'Slovaquie', nl: 'Slowakije', pt: 'Eslováquia', de: 'Slowakei' }, flag: '🇸🇰', capital: 'Bratislava', population: '5.5M' }
];

export default function CountriesPage() {
    const params = useParams();
    const lang = params.lang as string;
    const [countries, setCountries] = useState<Country[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchCountriesData = async () => {
            try {
                // Fetch business counts from API
                const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/countries/`);
                const apiData = await response.json();

                // Merge API data with static country data
                const mergedCountries = EU_COUNTRIES.map(country => {
                    const apiCountry = apiData.items?.find((item: any) => item.code === country.code);
                    return {
                        ...country,
                        count: apiCountry?.count || 0
                    };
                });

                setCountries(mergedCountries);
            } catch (error) {
                console.error('Error fetching countries:', error);
                // Use static data without counts if API fails
                setCountries(EU_COUNTRIES.map(country => ({ ...country, count: 0 })));
            } finally {
                setLoading(false);
            }
        };

        fetchCountriesData();
    }, []);

    const getCountryName = (country: any, language: string) => {
        return country.name[language as keyof typeof country.name] || country.name.en;
    };

    const getBusinessText = (count: number, language: string) => {
        switch (language) {
            case 'es': return `${count} empresa${count !== 1 ? 's' : ''}`;
            case 'fr': return `${count} entreprise${count !== 1 ? 's' : ''}`;
            case 'nl': return `${count} bedrijf${count !== 1 ? 'ven' : ''}`;
            case 'pt': return `${count} empresa${count !== 1 ? 's' : ''}`;
            case 'de': return `${count} Unternehmen`;
            default: return `${count} business${count !== 1 ? 'es' : ''}`;
        }
    };

    const getPageTexts = (language: string) => {
        switch (language) {
            case 'es':
                return {
                    title: 'Países de la Unión Europea',
                    subtitle: 'Descubre empresas en todos los 27 países miembros de la UE',
                    capital: 'Capital',
                    population: 'Población',
                    viewBusinesses: 'Ver Empresas',
                    loading: 'Cargando países...'
                };
            case 'fr':
                return {
                    title: 'Pays de l\'Union Européenne',
                    subtitle: 'Découvrez des entreprises dans les 27 pays membres de l\'UE',
                    capital: 'Capitale',
                    population: 'Population',
                    viewBusinesses: 'Voir Entreprises',
                    loading: 'Chargement des pays...'
                };
            case 'nl':
                return {
                    title: 'Landen van de Europese Unie',
                    subtitle: 'Ontdek bedrijven in alle 27 EU-lidstaten',
                    capital: 'Hoofdstad',
                    population: 'Bevolking',
                    viewBusinesses: 'Bekijk Bedrijven',
                    loading: 'Landen laden...'
                };
            case 'pt':
                return {
                    title: 'Países da União Europeia',
                    subtitle: 'Descubra empresas em todos os 27 países membros da UE',
                    capital: 'Capital',
                    population: 'População',
                    viewBusinesses: 'Ver Empresas',
                    loading: 'Carregando países...'
                };
            case 'de':
                return {
                    title: 'Länder der Europäischen Union',
                    subtitle: 'Entdecken Sie Unternehmen in allen 27 EU-Mitgliedsländern',
                    capital: 'Hauptstadt',
                    population: 'Bevölkerung',
                    viewBusinesses: 'Unternehmen Anzeigen',
                    loading: 'Länder werden geladen...'
                };
            default:
                return {
                    title: 'European Union Countries',
                    subtitle: 'Discover businesses across all 27 EU member states',
                    capital: 'Capital',
                    population: 'Population',
                    viewBusinesses: 'View Businesses',
                    loading: 'Loading countries...'
                };
        }
    };

    const texts = getPageTexts(lang);

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                    <p className="text-slate-600">{texts.loading}</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
            <div className="max-w-7xl mx-auto px-4">
                {/* Header */}
                <div className="text-center mb-12">
                    <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-4">
                        {texts.title}
                    </h1>
                    <p className="text-xl text-slate-600 max-w-3xl mx-auto mb-8">
                        {texts.subtitle}
                    </p>

                    {/* EU Flag and Stats */}
                    <div className="flex items-center justify-center space-x-8 mb-8">
                        <div className="flex items-center space-x-2">
                            <span className="text-4xl">🇪🇺</span>
                            <span className="text-lg font-semibold text-slate-700">EU 27</span>
                        </div>
                        <div className="text-sm text-slate-600">
                            <span className="font-medium">{countries.reduce((sum, country) => sum + (country.count || 0), 0)}</span> businesses listed
                        </div>
                    </div>
                </div>

                {/* Countries Grid */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                    {countries.map((country) => (
                        <div
                            key={country.code}
                            className="group bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 border border-slate-200 hover:border-blue-300 overflow-hidden relative hover:scale-105 transform"
                        >
                            {/* Country Header */}
                            <div className="bg-gradient-to-r from-blue-500 to-indigo-500 p-4 text-white">
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center space-x-3">
                                        <span className="text-3xl">{country.flag}</span>
                                        <div>
                                            <h3 className="font-bold text-lg">{getCountryName(country, lang)}</h3>
                                            <p className="text-blue-100 text-sm">{country.code}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Country Details */}
                            <div className="p-4">
                                <div className="space-y-3 mb-4">
                                    <div className="flex justify-between items-center">
                                        <span className="text-sm text-slate-600">{texts.capital}:</span>
                                        <span className="text-sm font-medium text-slate-800">{country.capital}</span>
                                    </div>
                                    <div className="flex justify-between items-center">
                                        <span className="text-sm text-slate-600">{texts.population}:</span>
                                        <span className="text-sm font-medium text-slate-800">{country.population}</span>
                                    </div>
                                </div>

                                {/* Business Count */}
                                <div className="bg-gray-50 rounded-lg p-3 mb-4">
                                    <div className="text-center">
                                        <div className="text-2xl font-bold text-blue-600">{country.count || 0}</div>
                                        <div className="text-sm text-slate-600">{getBusinessText(country.count || 0, lang)}</div>
                                    </div>
                                </div>

                                {/* Action Button */}
                                <button
                                    onClick={() => window.location.href = `/country/${country.code.toLowerCase()}`}
                                    className="w-full bg-gradient-to-r from-blue-500 to-indigo-500 text-white py-2 px-4 rounded-lg hover:from-blue-600 hover:to-indigo-600 transition-all duration-300 font-medium text-sm group-hover:shadow-md"
                                >
                                    {texts.viewBusinesses}
                                </button>
                            </div>

                            {/* EU Membership Badge */}
                            <div className="absolute top-3 right-3">
                                <div className="bg-yellow-400 text-yellow-900 px-2 py-1 rounded-full text-xs font-medium flex items-center space-x-1 shadow-sm">
                                    <span>⭐</span>
                                    <span>EU</span>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>

                {/* Footer Info */}
                <div className="mt-12 text-center">
                    <div className="bg-white/80 backdrop-blur-sm rounded-xl p-6 border border-slate-200">
                        <h3 className="text-lg font-semibold text-slate-800 mb-2">About the European Union</h3>
                        <p className="text-slate-600 max-w-4xl mx-auto">
                            The European Union consists of 27 member countries working together to promote peace, prosperity, and cooperation across Europe.
                            Explore businesses and opportunities in each member state through our comprehensive directory.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
