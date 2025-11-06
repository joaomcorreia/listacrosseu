'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

type Lang = "en" | "nl" | "pt" | "fr" | "de" | "es";

const T = {
  en: {
    selectCountry: "Select a country to view cities",
    citiesIn: "Cities in",
    searchCities: "Search cities...",
    cities: "cities",
    loading: "Loading...",
    noCitiesFound: "No cities found",
    quickStats: "Quick Stats",
    totalCities: "Total Cities:",
    filtered: "Filtered:"
  },
  nl: {
    selectCountry: "Selecteer een land om steden te bekijken",
    citiesIn: "Steden in",
    searchCities: "Zoek steden...",
    cities: "steden",
    loading: "Laden...",
    noCitiesFound: "Geen steden gevonden",
    quickStats: "Snelle Statistieken",
    totalCities: "Totaal Steden:",
    filtered: "Gefilterd:"
  },
  pt: {
    selectCountry: "Selecione um país para ver as cidades",
    citiesIn: "Cidades em",
    searchCities: "Pesquisar cidades...",
    cities: "cidades",
    loading: "Carregando...",
    noCitiesFound: "Nenhuma cidade encontrada",
    quickStats: "Estatísticas Rápidas",
    totalCities: "Total de Cidades:",
    filtered: "Filtrado:"
  },
  fr: {
    selectCountry: "Sélectionnez un pays pour voir les villes",
    citiesIn: "Villes en",
    searchCities: "Rechercher des villes...",
    cities: "villes",
    loading: "Chargement...",
    noCitiesFound: "Aucune ville trouvée",
    quickStats: "Statistiques Rapides",
    totalCities: "Total des Villes:",
    filtered: "Filtré:"
  },
  de: {
    selectCountry: "Wählen Sie ein Land aus, um Städte anzuzeigen",
    citiesIn: "Städte in",
    searchCities: "Städte suchen...",
    cities: "städte",
    loading: "Laden...",
    noCitiesFound: "Keine Städte gefunden",
    quickStats: "Schnelle Statistiken",
    totalCities: "Städte Gesamt:",
    filtered: "Gefiltert:"
  },
  es: {
    selectCountry: "Selecciona un país para ver las ciudades",
    citiesIn: "Ciudades en",
    searchCities: "Buscar ciudades...",
    cities: "ciudades",
    loading: "Cargando...",
    noCitiesFound: "No se encontraron ciudades",
    quickStats: "Estadísticas Rápidas",
    totalCities: "Total de Ciudades:",
    filtered: "Filtrado:"
  }
} as const;

interface City {
  slug: string;
  name: string;
  total: number;
}

interface CitiesSidebarProps {
  selectedCountry?: string;
  lang: Lang;
  onCitySelect?: (city: string) => void;
}

export default function CitiesSidebar({ selectedCountry, lang, onCitySelect }: CitiesSidebarProps) {
  const [cities, setCities] = useState<City[]>([]);
  const [filteredCities, setFilteredCities] = useState<City[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  
  const t = T[lang] || T.en;

  useEffect(() => {
    if (selectedCountry) {
      fetchCities(selectedCountry);
    }
  }, [selectedCountry]);

  useEffect(() => {
    const filtered = cities.filter(city => 
      city.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredCities(filtered);
  }, [cities, searchTerm]);

  const fetchCities = async (country: string) => {
    setLoading(true);
    try {
      const response = await fetch(`/api/v1/countries/${country}/cities/`, {
        cache: 'no-store'
      });
      if (response.ok) {
        const data = await response.json();
        setCities(data);
        setFilteredCities(data);
      }
    } catch (error) {
      console.error('Error fetching cities:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCityClick = (city: City) => {
    if (onCitySelect) {
      onCitySelect(city.slug);
    } else {
      // Navigate to search with city and country filters
      router.push(`/${lang}/search?q=&city=${city.slug}&country=${selectedCountry}`);
    }
    setIsOpen(false);
  };

  if (!selectedCountry) {
    return (
      <div className="w-80 bg-white border-r border-gray-200 p-6">
        <div className="text-center text-gray-500">
          <div className="text-4xl mb-4">🗺️</div>
          <p className="text-sm">{t.selectCountry}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="w-80 bg-white border-r border-gray-200 p-6 h-screen overflow-y-auto sticky top-0">
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
          🏙️ {t.citiesIn} {selectedCountry}
        </h3>
        
        {/* Search Box */}
        <div className="relative mb-4">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <input
            type="text"
            placeholder={t.searchCities}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand focus:border-transparent text-sm"
          />
        </div>

        {/* Dropdown Toggle */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="w-full flex items-center justify-between p-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <span className="text-sm font-medium text-gray-700">
            {loading ? t.loading : `${filteredCities.length} ${t.cities}`}
          </span>
          <svg 
            className={`h-5 w-5 text-gray-400 transition-transform ${isOpen ? 'rotate-180' : ''}`} 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>
      </div>

      {/* Cities Dropdown */}
      {isOpen && (
        <div className="space-y-1 animate-fade-in-up">
          {loading ? (
            <div className="text-center py-8">
              <div className="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-brand"></div>
            </div>
          ) : filteredCities.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <div className="text-2xl mb-2">🔍</div>
              <p className="text-sm">{t.noCitiesFound}</p>
            </div>
          ) : (
            filteredCities.map((city) => (
              <button
                key={city.slug}
                onClick={() => handleCityClick(city)}
                className="w-full text-left p-3 hover:bg-brand/5 rounded-lg transition-colors group"
              >
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-900 group-hover:text-brand">
                    {city.name}
                  </span>
                  <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
                    {city.total}
                  </span>
                </div>
              </button>
            ))
          )}
        </div>
      )}

      {/* Quick Stats */}
      <div className="mt-8 p-4 bg-gradient-to-br from-brand/5 to-purple-50 rounded-xl">
        <h4 className="text-sm font-semibold text-gray-800 mb-2">{t.quickStats}</h4>
        <div className="space-y-2 text-sm text-gray-600">
          <div className="flex justify-between">
            <span>{t.totalCities}</span>
            <span className="font-medium">{cities.length}</span>
          </div>
          <div className="flex justify-between">
            <span>{t.filtered}</span>
            <span className="font-medium">{filteredCities.length}</span>
          </div>
        </div>
      </div>
    </div>
  );
}