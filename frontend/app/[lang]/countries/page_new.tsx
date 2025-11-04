'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { translate, Language } from '@/lib/i18n';

interface Country {
    code: string;
    name: string;
    count: number;
}

export default function CountriesPage() {
    const params = useParams();
    const lang = params.lang as string;
    const [countries, setCountries] = useState<Country[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchCountries = async () => {
            try {
                const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/countries/`);
                if (!response.ok) {
                    throw new Error('Failed to fetch countries');
                }
                const data = await response.json();
                // API returns {items: [...], count: number}, so we need data.items
                setCountries(data.items || []);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'An error occurred');
            } finally {
                setLoading(false);
            }
        };

        fetchCountries();
    }, []);

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                    <p className="text-slate-600">Loading countries...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
                <div className="text-center">
                    <div className="text-6xl mb-4">❌</div>
                    <h2 className="text-2xl font-bold text-slate-800 mb-2">Error Loading Countries</h2>
                    <p className="text-slate-600">{error}</p>
                </div>
            </div>
        );
    }

    const getEmptyText = (lang: string) => {
        switch (lang) {
            case 'es': return 'Explora países de la UE con empresas listadas en nuestro directorio.';
            case 'fr': return 'Explorez les pays de l\'UE avec des entreprises répertoriées dans notre annuaire.';
            case 'nl': return 'Ontdek EU-landen met bedrijven vermeld in onze directory.';
            case 'pt': return 'Explore países da UE com empresas listadas em nosso diretório.';
            default: return 'Explore EU countries with businesses listed in our directory.';
        }
    };

    const getBusinessText = (lang: string, count: number) => {
        switch (lang) {
            case 'es': return `${count} empresa${count !== 1 ? 's' : ''}`;
            case 'fr': return `${count} entreprise${count !== 1 ? 's' : ''}`;
            case 'nl': return `${count} bedrijf${count !== 1 ? 'ven' : ''}`;
            case 'pt': return `${count} empresa${count !== 1 ? 's' : ''}`;
            default: return `${count} business${count !== 1 ? 'es' : ''}`;
        }
    };

    const getCountryFlag = (countryCode: string) => {
        const flagMap: { [key: string]: string } = {
            'AT': '🇦🇹', 'BE': '🇧🇪', 'BG': '🇧🇬', 'CY': '🇨🇾', 'CZ': '🇨🇿', 'DE': '🇩🇪',
            'DK': '🇩🇰', 'EE': '🇪🇪', 'ES': '🇪🇸', 'FI': '🇫🇮', 'FR': '🇫🇷', 'GR': '🇬🇷',
            'HR': '🇭🇷', 'HU': '🇭🇺', 'IE': '🇮🇪', 'IT': '🇮🇹', 'LT': '🇱🇹', 'LU': '🇱🇺',
            'LV': '🇱🇻', 'MT': '🇲🇹', 'NL': '🇳🇱', 'PL': '🇵🇱', 'PT': '🇵🇹', 'RO': '🇷🇴',
            'SE': '🇸🇪', 'SI': '🇸🇮', 'SK': '🇸🇰'
        };
        return flagMap[countryCode] || '🏳️';
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
            <div className="max-w-7xl mx-auto px-4">
                {/* Header */}
                <div className="text-center mb-12">
                    <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-4">
                        {translate('countries', lang as Language)}
                    </h1>
                    <p className="text-xl text-slate-600 max-w-2xl mx-auto">
                        {getEmptyText(lang)}
                    </p>
                </div>

                {/* Countries Grid */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-12">
                    {countries.map((country) => (
                        <div key={country.code} className="group">
                            <div className="bg-white rounded-xl p-6 shadow-sm hover:shadow-lg transition-all duration-300 border border-slate-200 hover:border-blue-300 h-full">
                                <div className="flex items-center justify-between mb-4">
                                    <div className="text-4xl">{getCountryFlag(country.code)}</div>
                                    <div className="text-right">
                                        <div className="text-2xl font-bold text-slate-800">{country.count}</div>
                                        <div className="text-sm text-slate-500">{getBusinessText(lang, country.count)}</div>
                                    </div>
                                </div>

                                <div className="space-y-2">
                                    <h3 className="text-lg font-semibold text-slate-800 group-hover:text-blue-600 transition-colors">
                                        {country.name}
                                    </h3>
                                    <div className="flex items-center text-sm text-slate-500">
                                        <span className="inline-block w-2 h-2 bg-green-400 rounded-full mr-2"></span>
                                        EU Member
                                    </div>
                                </div>

                                <div className="mt-4 pt-4 border-t border-slate-100">
                                    <button className="w-full text-center py-2 px-4 bg-gradient-to-r from-blue-500 to-indigo-500 text-white rounded-lg hover:from-blue-600 hover:to-indigo-600 transition-all duration-300 font-medium text-sm">
                                        View Businesses
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>

                {/* Empty State */}
                {countries.length === 0 && (
                    <div className="text-center py-12">
                        <div className="text-6xl mb-4">🌍</div>
                        <h3 className="text-xl font-semibold text-slate-800 mb-2">No Countries Found</h3>
                        <p className="text-slate-600">Countries will appear here once they are added to the system.</p>
                    </div>
                )}
            </div>
        </div>
    );
}