import Link from "next/link";
import { apiCall } from "@/lib/api";
import CitiesSidebar from "@/components/CitiesSidebar";

type Lang = "en" | "nl" | "pt" | "fr" | "de" | "es";

const T = {
  en: {
    titlePrefix: "Cities in",
    subtitle: "Explore local businesses in each city",
    businessesText: "businesses",
    noCities: "No cities found in this country.",
    backToCountries: "← Back to Countries",
    searchInCity: "Search businesses",
    cityExplorer: "🏙️ City Explorer",
    checkBackSoon: "Check back soon for more cities and businesses."
  },
  nl: {
    titlePrefix: "Steden in",
    subtitle: "Ontdek lokale bedrijven in elke stad",
    businessesText: "bedrijven",
    noCities: "Geen steden gevonden in dit land.",
    backToCountries: "← Terug naar Landen",
    searchInCity: "Zoek bedrijven",
    cityExplorer: "🏙️ Steden Verkenner",
    checkBackSoon: "Kom binnenkort terug voor meer steden en bedrijven."
  },
  pt: {
    titlePrefix: "Cidades em",
    subtitle: "Explore empresas locais em cada cidade",
    businessesText: "empresas",
    noCities: "Nenhuma cidade encontrada neste país.",
    backToCountries: "← Voltar aos Países",
    searchInCity: "Buscar empresas",
    cityExplorer: "🏙️ Explorador de Cidades",
    checkBackSoon: "Volte em breve para mais cidades e empresas."
  },
  fr: {
    titlePrefix: "Villes en",
    subtitle: "Explorez les entreprises locales dans chaque ville",
    businessesText: "entreprises",
    noCities: "Aucune ville trouvée dans ce pays.",
    backToCountries: "← Retour aux Pays",
    searchInCity: "Chercher des entreprises",
    cityExplorer: "🏙️ Explorateur de Villes",
    checkBackSoon: "Revenez bientôt pour plus de villes et d'entreprises."
  },
  de: {
    titlePrefix: "Städte in",
    subtitle: "Entdecken Sie lokale Unternehmen in jeder Stadt",
    businessesText: "Unternehmen",
    noCities: "Keine Städte in diesem Land gefunden.",
    backToCountries: "← Zurück zu Ländern",
    searchInCity: "Unternehmen suchen",
    cityExplorer: "🏙️ Städte-Explorer",
    checkBackSoon: "Schauen Sie bald wieder vorbei für mehr Städte und Unternehmen."
  },
  es: {
    titlePrefix: "Ciudades en",
    subtitle: "Explora negocios locales en cada ciudad",
    businessesText: "negocios",
    noCities: "No se encontraron ciudades en este país.",
    backToCountries: "← Volver a Países",
    searchInCity: "Buscar negocios",
    cityExplorer: "🏙️ Explorador de Ciudades",
    checkBackSoon: "Vuelve pronto para más ciudades y empresas."
  }
} as const;

export default async function CountryCitiesPage({ params }: { params: { lang: Lang; country: string } }) {
  const { lang, country } = params;
  const t = T[lang || "en"] || T.en;
  
  // Fetch businesses from this country to show cities
  const response = await apiCall(`/countries/${encodeURIComponent(country)}/businesses/?lang=${lang}&page_size=1000`) || { businesses: [], total_count: 0 };
  const businesses = response.businesses || [];
  
  // Group businesses by city to create city list with counts
  const citiesMap = new Map();
  businesses.forEach((business: any) => {
    const cityKey = business.city;
    if (!citiesMap.has(cityKey)) {
      citiesMap.set(cityKey, { 
        name: business.city, 
        slug: business.city.toLowerCase().replace(/[^a-z0-9]/g, '-'),
        total: 0 
      });
    }
    citiesMap.set(cityKey, { 
      ...citiesMap.get(cityKey), 
      total: citiesMap.get(cityKey).total + 1 
    });
  });
  
  const cities = Array.from(citiesMap.values()).sort((a, b) => b.total - a.total);
  
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-indigo-600 via-purple-600 to-brand relative overflow-hidden pt-24 pb-16">
        {/* Animated Background Elements */}
        <div className="absolute inset-0">
          <div className="absolute top-20 right-10 w-32 h-32 bg-white/10 rounded-full animate-pulse"></div>
          <div className="absolute top-40 left-20 w-24 h-24 bg-white/5 rounded-full animate-bounce" style={{ animationDelay: '1s' }}></div>
          <div className="absolute bottom-20 right-1/4 w-40 h-40 bg-white/5 rounded-full animate-pulse" style={{ animationDelay: '2s' }}></div>
        </div>
        
        <div className="container mx-auto px-6 py-16 relative z-10 text-center text-white">
          <div className="inline-flex items-center bg-white/20 backdrop-blur-sm border border-white/30 rounded-full px-6 py-3 mb-8 animate-fade-in-up">
            <span className="text-sm text-white/90">{t.cityExplorer}</span>
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold mb-6 animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
            {t.titlePrefix} {decodeURIComponent(country)}
          </h1>
          <p className="text-xl text-white/90 mb-12 max-w-3xl mx-auto animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
            {t.subtitle}
          </p>
          
          <Link 
            href={`/${lang}/countries`}
            className="inline-flex items-center text-white/80 hover:text-white transition-colors animate-fade-in-up"
            style={{ animationDelay: '0.6s' }}
          >
            {t.backToCountries}
          </Link>
        </div>
      </section>

      {/* Cities Grid Section with Sidebar */}
      <section className="bg-white relative">
        <div className="absolute top-0 left-0 w-full h-32 bg-gradient-to-b from-indigo-600/5 to-transparent"></div>
        <div className="flex relative z-10">
          <div className="flex-1 py-20 px-6">
          {cities.length > 0 ? (
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 max-w-7xl mx-auto">
              {cities.map((city: any, index: number) => (
                <Link 
                  key={city.slug} 
                  href={`/${lang}/search?q=&country=${encodeURIComponent(country)}&city=${encodeURIComponent(city.slug)}`}
                  className="group rounded-3xl p-8 bg-gradient-to-br from-white to-indigo-50 border border-gray-200 hover:border-indigo-300 shadow-lg hover:shadow-2xl transform hover:scale-105 transition-all duration-300 animate-fade-in-up"
                  style={{ animationDelay: `${0.1 * index}s` }}
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center text-white font-bold text-xl group-hover:scale-110 transition-transform duration-300">
                      {city.name.substring(0, 1).toUpperCase()}
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-indigo-600">{city.total}</div>
                      <div className="text-sm text-gray-500">{t.businessesText}</div>
                    </div>
                  </div>
                  
                  <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-indigo-600 transition-colors">
                    {city.name}
                  </h3>
                  
                  <div className="flex items-center text-indigo-600 font-medium group-hover:translate-x-2 transition-transform duration-300">
                    {t.searchInCity} →
                  </div>
                </Link>
              ))}
            </div>
          ) : (
            <div className="text-center py-16 animate-fade-in-up">
              <div className="w-24 h-24 bg-gradient-to-br from-gray-100 to-gray-200 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-3xl">🏙️</span>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">{t.noCities}</h3>
              <p className="text-gray-600 mb-8">{t.checkBackSoon}</p>
              <Link 
                href={`/${lang}/countries`}
                className="inline-flex items-center bg-indigo-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-indigo-700 transition-colors"
              >
                {t.backToCountries}
              </Link>
            </div>
          )}
          </div>
          <CitiesSidebar selectedCountry={decodeURIComponent(country)} lang={lang} />
        </div>
      </section>
    </div>
  );
}