import Link from "next/link";
import { apiCall } from "@/lib/api";
import CitiesSidebar from "@/components/CitiesSidebar";

type Lang = "en" | "nl" | "pt" | "fr" | "de" | "es";

const T = {
  en: {
    title: "Explore Countries",
    subtitle: "Discover businesses across Europe - from Portugal to Germany, find what you need.",
    businessesText: "businesses",
    noCountries: "No countries found.",
    backToHome: "← Back to Home",
    businessDirectory: "🌍 European Business Directory",
    exploreCities: "Explore cities",
    checkBackSoon: "Check back soon for more countries and businesses."
  },
  nl: {
    title: "Ontdek Landen",
    subtitle: "Ontdek bedrijven in heel Europa - van Portugal tot Duitsland, vind wat je nodig hebt.",
    businessesText: "bedrijven",
    noCountries: "Geen landen gevonden.",
    backToHome: "← Terug naar Home",
    businessDirectory: "🌍 Europese Bedrijvengids",
    exploreCities: "Ontdek steden",
    checkBackSoon: "Kom binnenkort terug voor meer landen en bedrijven."
  },
  pt: {
    title: "Explorar Países",
    subtitle: "Descubra negócios por toda a Europa - de Portugal à Alemanha, encontre o que precisa.",
    businessesText: "empresas",
    noCountries: "Nenhum país encontrado.",
    backToHome: "← Voltar ao Início",
    businessDirectory: "🌍 Diretório de Empresas Europeias",
    exploreCities: "Explorar cidades",
    checkBackSoon: "Volte em breve para mais países e empresas."
  },
  fr: {
    title: "Explorer les Pays",
    subtitle: "Découvrez des entreprises à travers l'Europe - du Portugal à l'Allemagne, trouvez ce dont vous avez besoin.",
    businessesText: "entreprises",
    noCountries: "Aucun pays trouvé.",
    backToHome: "← Retour à l'accueil",
    businessDirectory: "🌍 Répertoire d'Entreprises Européennes",
    exploreCities: "Explorer les villes",
    checkBackSoon: "Revenez bientôt pour plus de pays et d'entreprises."
  },
  de: {
    title: "Länder Entdecken",
    subtitle: "Entdecken Sie Unternehmen in ganz Europa - von Portugal bis Deutschland, finden Sie was Sie brauchen.",
    businessesText: "Unternehmen",
    noCountries: "Keine Länder gefunden.",
    backToHome: "← Zurück zur Startseite",
    businessDirectory: "🌍 Europäisches Unternehmensverzeichnis",
    exploreCities: "Städte erkunden",
    checkBackSoon: "Schauen Sie bald wieder vorbei für mehr Länder und Unternehmen."
  },
  es: {
    title: "Explorar Países",
    subtitle: "Descubre negocios en toda Europa - de Portugal a Alemania, encuentra lo que necesitas.",
    businessesText: "negocios",
    noCountries: "No se encontraron países.",
    backToHome: "← Volver al Inicio",
    businessDirectory: "🌍 Directorio de Empresas Europeas",
    exploreCities: "Explorar ciudades",
    checkBackSoon: "Vuelve pronto para más países y empresas."
  }
} as const;

export default async function CountriesPage({ params }: { params: { lang: Lang } }) {
  const lang: Lang = params.lang || "en";
  const t = T[lang] || T.en;
  
  // Fetch real countries data from our new API
  const response = await apiCall(`/countries/?lang=${lang}`) || { countries: [], total_countries: 0 };
  const countries = response.countries || [];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-brand via-purple-600 to-indigo-800 relative overflow-hidden pt-24 pb-16">
        {/* Animated Background Elements */}
        <div className="absolute inset-0">
          <div className="absolute top-20 left-10 w-32 h-32 bg-white/10 rounded-full animate-pulse"></div>
          <div className="absolute top-40 right-20 w-24 h-24 bg-white/5 rounded-full animate-bounce" style={{ animationDelay: '1s' }}></div>
          <div className="absolute bottom-20 left-1/4 w-40 h-40 bg-white/5 rounded-full animate-pulse" style={{ animationDelay: '2s' }}></div>
        </div>
        
        <div className="container mx-auto px-6 py-16 relative z-10 text-center text-white">
          <div className="inline-flex items-center bg-white/20 backdrop-blur-sm border border-white/30 rounded-full px-6 py-3 mb-8 animate-fade-in-up">
            <span className="text-sm text-white/90">{t.businessDirectory}</span>
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

      {/* Countries Grid Section with Sidebar */}
      <section className="bg-white relative">
        <div className="absolute top-0 left-0 w-full h-32 bg-gradient-to-b from-brand/5 to-transparent"></div>
        <div className="flex relative z-10">
          <div className="flex-1 py-20 px-6">
          {countries.length > 0 ? (
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 max-w-7xl mx-auto">
              {countries.map((country: any, index: number) => (
                <Link 
                  key={country.country} 
                  href={`/${lang}/countries/${encodeURIComponent(country.country)}`}
                  className="group rounded-3xl p-8 bg-gradient-to-br from-white to-gray-50 border border-gray-200 hover:border-brand/30 shadow-lg hover:shadow-2xl transform hover:scale-105 transition-all duration-300 animate-fade-in-up"
                  style={{ animationDelay: `${0.1 * index}s` }}
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="w-12 h-12 bg-gradient-to-br from-brand to-purple-600 rounded-2xl flex items-center justify-center text-white font-bold text-xl group-hover:scale-110 transition-transform duration-300">
                      {country.country.substring(0, 2).toUpperCase()}
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-brand">{country.business_count}</div>
                      <div className="text-sm text-gray-500">{t.businessesText}</div>
                    </div>
                  </div>
                  
                  <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-brand transition-colors">
                    {country.country}
                  </h3>
                  
                  <div className="flex items-center text-brand font-medium group-hover:translate-x-2 transition-transform duration-300">
                    {t.exploreCities} →
                  </div>
                </Link>
              ))}
            </div>
          ) : (
            <div className="text-center py-16 animate-fade-in-up">
              <div className="w-24 h-24 bg-gradient-to-br from-gray-100 to-gray-200 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-3xl">🌍</span>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">{t.noCountries}</h3>
              <p className="text-gray-600 mb-8">{t.checkBackSoon}</p>
              <Link 
                href={`/${lang}`}
                className="inline-flex items-center bg-brand text-white px-8 py-4 rounded-xl font-semibold hover:bg-brand-dark transition-colors"
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