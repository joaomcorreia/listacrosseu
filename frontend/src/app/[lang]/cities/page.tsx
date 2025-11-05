import Link from "next/link";
import { apiCall } from "@/lib/api";
import CitiesSidebar from "@/components/CitiesSidebar";

type Lang = "en" | "nl" | "pt" | "fr" | "de" | "es";

const T = {
  en: {
    title: "Explore Cities",
    subtitle: "Discover businesses in cities across Europe - from Amsterdam to Zagreb.",
    businessesText: "businesses",
    noCities: "No cities found.",
    backToHome: "← Back to Home",
    searchInCity: "Search businesses",
    cityDirectory: "🏙️ European City Directory",
    checkBackSoon: "Check back soon for more cities and businesses.",
    allCities: "All Cities"
  },
  nl: {
    title: "Steden Ontdekken",
    subtitle: "Ontdek bedrijven in steden door heel Europa - van Amsterdam tot Zagreb.",
    businessesText: "bedrijven",
    noCities: "Geen steden gevonden.",
    backToHome: "← Terug naar Home",
    searchInCity: "Zoek bedrijven",
    cityDirectory: "🏙️ Europese Steden Gids",
    checkBackSoon: "Kom binnenkort terug voor meer steden en bedrijven.",
    allCities: "Alle Steden"
  },
  pt: {
    title: "Explorar Cidades",
    subtitle: "Descubra empresas em cidades por toda a Europa - de Amsterdam a Zagreb.",
    businessesText: "empresas",
    noCities: "Nenhuma cidade encontrada.",
    backToHome: "← Voltar ao Início",
    searchInCity: "Buscar empresas",
    cityDirectory: "🏙️ Diretório de Cidades Europeias",
    checkBackSoon: "Volte em breve para mais cidades e empresas.",
    allCities: "Todas as Cidades"
  },
  fr: {
    title: "Explorer les Villes",
    subtitle: "Découvrez des entreprises dans les villes à travers l'Europe - d'Amsterdam à Zagreb.",
    businessesText: "entreprises",
    noCities: "Aucune ville trouvée.",
    backToHome: "← Retour à l'accueil",
    searchInCity: "Chercher des entreprises",
    cityDirectory: "🏙️ Répertoire de Villes Européennes",
    checkBackSoon: "Revenez bientôt pour plus de villes et d'entreprises.",
    allCities: "Toutes les Villes"
  },
  de: {
    title: "Städte Entdecken",
    subtitle: "Entdecken Sie Unternehmen in Städten in ganz Europa - von Amsterdam bis Zagreb.",
    businessesText: "Unternehmen",
    noCities: "Keine Städte gefunden.",
    backToHome: "← Zurück zur Startseite",
    searchInCity: "Unternehmen suchen",
    cityDirectory: "🏙️ Europäisches Städteverzeichnis",
    checkBackSoon: "Schauen Sie bald wieder vorbei für mehr Städte und Unternehmen.",
    allCities: "Alle Städte"
  },
  es: {
    title: "Explorar Ciudades",
    subtitle: "Descubre empresas en ciudades de toda Europa - desde Amsterdam hasta Zagreb.",
    businessesText: "empresas",
    noCities: "No se encontraron ciudades.",
    backToHome: "← Volver al Inicio",
    searchInCity: "Buscar empresas",
    cityDirectory: "🏙️ Directorio de Ciudades Europeas",
    checkBackSoon: "Vuelve pronto para más ciudades y empresas.",
    allCities: "Todas las Ciudades"
  }
} as const;

export default async function CitiesPage({ params }: { params: { lang: Lang } }) {
  const lang: Lang = params.lang || "en";
  const t = T[lang] || T.en;
  
  // Fetch cities with business counts from our new API
  const response = await apiCall(`/cities/?lang=${lang}`) || { cities: [], total_cities: 0 };
  const cities = response.cities || [];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-700 relative overflow-hidden pt-24 pb-16">
        {/* Animated Background Elements */}
        <div className="absolute inset-0">
          <div className="absolute top-20 left-10 w-32 h-32 bg-white/10 rounded-full animate-pulse"></div>
          <div className="absolute top-40 right-20 w-24 h-24 bg-white/5 rounded-full animate-bounce" style={{ animationDelay: '1s' }}></div>
          <div className="absolute bottom-20 left-1/4 w-40 h-40 bg-white/5 rounded-full animate-pulse" style={{ animationDelay: '2s' }}></div>
        </div>
        
        <div className="container mx-auto px-6 py-16 relative z-10 text-center text-white">
          <div className="inline-flex items-center bg-white/20 backdrop-blur-sm border border-white/30 rounded-full px-6 py-3 mb-8 animate-fade-in-up">
            <span className="text-sm text-white/90">{t.cityDirectory}</span>
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold mb-6 animate-fade-in-up" style={{ animationDelay: '0.2s' }}>{t.title}</h1>
          <p className="text-xl text-white/90 mb-12 max-w-3xl mx-auto animate-fade-in-up" style={{ animationDelay: '0.4s' }}>{t.subtitle}</p>
          
          <Link 
            href={`/${lang}`}
            className="inline-flex items-center text-white/80 hover:text-white transition-colors animate-fade-in-up"
            style={{ animationDelay: '0.6s' }}
          >
            {t.backToHome}
          </Link>
        </div>
      </section>

      {/* Cities Grid Section with Sidebar */}
      <section className="bg-white relative">
        <div className="absolute top-0 left-0 w-full h-32 bg-gradient-to-b from-blue-600/5 to-transparent"></div>
        <div className="flex relative z-10">
          <div className="flex-1 py-20 px-6">
          {cities.length > 0 ? (
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 max-w-7xl mx-auto">
              {cities.map((city: any, index: number) => (
                <Link 
                  key={`${city.city}-${city.country}`} 
                  href={`/${lang}/search?q=&country=${encodeURIComponent(city.country)}&city=${encodeURIComponent(city.city)}`}
                  className="group rounded-3xl p-8 bg-gradient-to-br from-white to-blue-50 border border-gray-200 hover:border-blue-300 shadow-lg hover:shadow-2xl transform hover:scale-105 transition-all duration-300 animate-fade-in-up"
                  style={{ animationDelay: `${0.1 * index}s` }}
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center text-white font-bold text-xl group-hover:scale-110 transition-transform duration-300">
                      {city.city.substring(0, 1).toUpperCase()}
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-blue-600">{city.business_count}</div>
                      <div className="text-sm text-gray-500">{t.businessesText}</div>
                    </div>
                  </div>
                  
                  <h3 className="text-xl font-bold text-gray-900 mb-1 group-hover:text-blue-600 transition-colors">
                    {city.city}
                  </h3>
                  <p className="text-sm text-gray-500 mb-4">{city.country}</p>
                  
                  <div className="flex items-center text-blue-600 font-medium group-hover:translate-x-2 transition-transform duration-300">
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
                href={`/${lang}`}
                className="inline-flex items-center bg-blue-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-blue-700 transition-colors"
              >
                {t.backToHome}
              </Link>
            </div>
          )}
          </div>
          <CitiesSidebar lang={lang} />
        </div>
      </section>
    </div>
  );
}