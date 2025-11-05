import Link from 'next/link';
import SearchBoxNew from '@/components/SearchBoxNew';

type Lang = "en" | "nl" | "pt" | "fr" | "de" | "es";

const T = {
  en: {
    trustBadge: "🌟 Trusted by 50,000+ European businesses",
    heroTitle: "Find Businesses",
    heroTitleGradient: "Across Europe",
    heroSubtitle: "Discover millions of businesses across 30+ European countries. From restaurants in Paris to tech companies in Amsterdam.",
    searchButton: "Start Searching Now",
    pricingButton: "View Pricing Plans",
    featuredTitle: "Featured Businesses",
    featuredSubtitle: "Discover top-rated businesses across Europe",
    categoriesTitle: "Popular Categories",
    categoriesSubtitle: "Browse by business type",
    seeAllCategories: "See All Categories",
    getStartedTitle: "Ready to Get Started?",
    getStartedSubtitle: "Join thousands of businesses and customers connecting across Europe",
    businessesText: "businesses",
    whyChooseTitle: "Why Choose ListAcross EU?",
    whyChooseSubtitle: "The most comprehensive European business directory",
    europeWideCoverage: "Europe-Wide Coverage",
    europeWideCoverageDesc: "Search across 30+ European countries with comprehensive coverage of local businesses, from major cities to small towns.",
    smartSearch: "Smart Search Technology",
    smartSearchDesc: "Advanced AI-powered search with instant suggestions, multilingual support, and intelligent filtering for precise results.",
    verifiedTrusted: "Verified & Trusted",
    verifiedTrustedDesc: "All business listings are verified with up-to-date contact information, reviews, and ratings from the European community.",
    restaurants: "Restaurants",
    hotels: "Hotels",
    technology: "Technology",
    healthcare: "Healthcare",
    retail: "Retail",
    services: "Services",
    popularSearches: "Popular searches:",
    featuredBusinessesSubtitle: "Discover top-rated businesses recommended by our European community"
  },
  nl: {
    trustBadge: "🌟 Vertrouwd door 50.000+ Europese bedrijven",
    heroTitle: "Vind Bedrijven",
    heroTitleGradient: "Door Europa",
    heroSubtitle: "Ontdek miljoenen bedrijven in 30+ Europese landen. Van restaurants in Parijs tot techbedrijven in Amsterdam.",
    searchButton: "Begin Nu Met Zoeken",
    pricingButton: "Bekijk Prijzen",
    featuredTitle: "Uitgelichte Bedrijven",
    featuredSubtitle: "Ontdek topgewaardeerde bedrijven in Europa",
    categoriesTitle: "Populaire Categorieën",
    categoriesSubtitle: "Bladeren op bedrijfstype",
    seeAllCategories: "Alle Categorieën Zien",
    getStartedTitle: "Klaar om te Beginnen?",
    getStartedSubtitle: "Sluit je aan bij duizenden bedrijven en klanten die verbinden in Europa",
    businessesText: "bedrijven",
    whyChooseTitle: "Waarom Kiezen Voor ListAcross EU?",
    whyChooseSubtitle: "De meest uitgebreide Europese bedrijvengids",
    europeWideCoverage: "Europa-brede Dekking",
    europeWideCoverageDesc: "Zoek in 30+ Europese landen met uitgebreide dekking van lokale bedrijven, van grote steden tot kleine dorpen.",
    smartSearch: "Slimme Zoektechnologie",
    smartSearchDesc: "Geavanceerd AI-aangedreven zoeken met directe suggesties, meertalige ondersteuning en intelligente filtering voor precieze resultaten.",
    verifiedTrusted: "Geverifieerd & Vertrouwd",
    verifiedTrustedDesc: "Alle bedrijfslijsten zijn geverifieerd met actuele contactinformatie, beoordelingen en ratings van de Europese gemeenschap.",
    restaurants: "Restaurants",
    hotels: "Hotels",
    technology: "Technologie",
    healthcare: "Gezondheidszorg",
    retail: "Detailhandel",
    services: "Diensten",
    popularSearches: "Populaire zoekopdrachten:",
    featuredBusinessesSubtitle: "Ontdek topgewaardeerde bedrijven aanbevolen door onze Europese gemeenschap"
  },
  pt: {
    trustBadge: "🌟 Confiado por 50.000+ empresas europeias",
    heroTitle: "Encontre Empresas",
    heroTitleGradient: "Por Toda Europa",
    heroSubtitle: "Descubra milhões de empresas em 30+ países europeus. De restaurantes em Paris a empresas de tecnologia em Amsterdam.",
    searchButton: "Comece a Pesquisar Agora",
    pricingButton: "Ver Planos de Preços",
    featuredTitle: "Empresas em Destaque",
    featuredSubtitle: "Descubra empresas com melhor classificação na Europa",
    categoriesTitle: "Categorias Populares",
    categoriesSubtitle: "Navegar por tipo de empresa",
    seeAllCategories: "Ver Todas as Categorias",
    getStartedTitle: "Pronto para Começar?",
    getStartedSubtitle: "Junte-se a milhares de empresas e clientes conectando-se pela Europa",
    businessesText: "empresas",
    whyChooseTitle: "Por Que Escolher ListAcross EU?",
    whyChooseSubtitle: "O diretório europeu de empresas mais abrangente",
    europeWideCoverage: "Cobertura em Toda a Europa",
    europeWideCoverageDesc: "Pesquise em 30+ países europeus com cobertura abrangente de empresas locais, desde grandes cidades até pequenas vilas.",
    smartSearch: "Tecnologia de Pesquisa Inteligente",
    smartSearchDesc: "Pesquisa avançada alimentada por IA com sugerências instantâneas, suporte multilíngue e filtragem inteligente para resultados precisos.",
    verifiedTrusted: "Verificado e Confiável",
    verifiedTrustedDesc: "Todas as listagens de empresas são verificadas com informações de contato atualizadas, avaliações e classificações da comunidade europeia.",
    restaurants: "Restaurantes",
    hotels: "Hotéis",
    technology: "Tecnologia",
    healthcare: "Saúde",
    retail: "Varejo",
    services: "Serviços",
    popularSearches: "Pesquisas populares:",
    featuredBusinessesSubtitle: "Descubra empresas bem avaliadas recomendadas pela nossa comunidade europeia"
  },
  de: {
    trustBadge: "🌟 Vertraut von 50.000+ europäischen Unternehmen",
    heroTitle: "Finde Unternehmen",
    heroTitleGradient: "Quer durch Europa",
    heroSubtitle: "Entdecke Millionen von Unternehmen in 30+ europäischen Ländern. Von Restaurants in Paris bis zu Tech-Unternehmen in Amsterdam.",
    searchButton: "Jetzt Suchen Starten",
    pricingButton: "Preispläne Anzeigen",
    featuredTitle: "Ausgewählte Unternehmen",
    featuredSubtitle: "Entdecke bestbewertete Unternehmen in Europa",
    categoriesTitle: "Beliebte Kategorien",
    categoriesSubtitle: "Nach Unternehmenstyp durchsuchen",
    seeAllCategories: "Alle Kategorien Anzeigen",
    getStartedTitle: "Bereit Anzufangen?",
    getStartedSubtitle: "Schließen Sie sich Tausenden von Unternehmen und Kunden an, die sich in Europa vernetzen",
    businessesText: "unternehmen",
    whyChooseTitle: "Warum ListAcross EU Wählen?",
    whyChooseSubtitle: "Das umfassendste europäische Unternehmensverzeichnis",
    europeWideCoverage: "Europaweite Abdeckung",
    europeWideCoverageDesc: "Suchen Sie in 30+ europäischen Ländern mit umfassender Abdeckung lokaler Unternehmen, von Großstädten bis zu kleinen Gemeinden.",
    smartSearch: "Intelligente Suchtechnologie",
    smartSearchDesc: "Erweiterte KI-gesteuerte Suche mit sofortigen Vorschlägen, mehrsprachiger Unterstützung und intelligenter Filterung für präzise Ergebnisse.",
    verifiedTrusted: "Verifiziert & Vertrauenswürdig",
    verifiedTrustedDesc: "Alle Unternehmenseinträge sind mit aktuellen Kontaktinformationen, Bewertungen und Ratings der europäischen Gemeinschaft verifiziert.",
    restaurants: "Restaurants",
    hotels: "Hotels",
    technology: "Technologie",
    healthcare: "Gesundheitswesen",
    retail: "Einzelhandel",
    services: "Dienstleistungen",
    popularSearches: "Beliebte Suchen:",
    featuredBusinessesSubtitle: "Entdecken Sie bestbewertete Unternehmen, die von unserer europäischen Gemeinschaft empfohlen werden"
  },
  fr: {
    trustBadge: "🌟 Fait confiance par 50 000+ entreprises européennes",
    heroTitle: "Trouvez des Entreprises",
    heroTitleGradient: "À Travers l'Europe",
    heroSubtitle: "Découvrez des millions d'entreprises dans 30+ pays européens. Des restaurants à Paris aux entreprises tech d'Amsterdam.",
    searchButton: "Commencer la Recherche",
    pricingButton: "Voir les Plans Tarifaires",
    featuredTitle: "Entreprises en Vedette",
    featuredSubtitle: "Découvrez les entreprises les mieux notées d'Europe",
    categoriesTitle: "Catégories Populaires",
    categoriesSubtitle: "Parcourir par type d'entreprise",
    seeAllCategories: "Voir Toutes les Catégories",
    getStartedTitle: "Prêt à Commencer?",
    getStartedSubtitle: "Rejoignez des milliers d'entreprises et clients qui se connectent à travers l'Europe",
    businessesText: "entreprises",
    whyChooseTitle: "Pourquoi Choisir ListAcross EU?",
    whyChooseSubtitle: "L'annuaire d'entreprises européennes le plus complet",
    europeWideCoverage: "Couverture Paneuropéenne",
    europeWideCoverageDesc: "Recherchez dans 30+ pays européens avec une couverture complète des entreprises locales, des grandes villes aux petites communes.",
    smartSearch: "Technologie de Recherche Intelligente",
    smartSearchDesc: "Recherche avancée alimentée par IA avec suggestions instantanées, support multilingue et filtrage intelligent pour des résultats précis.",
    verifiedTrusted: "Vérifié et Fiable",
    verifiedTrustedDesc: "Tous les listings d'entreprises sont vérifiés avec des informations de contact à jour, des avis et évaluations de la communauté européenne.",
    restaurants: "Restaurants",
    hotels: "Hôtels",
    technology: "Technologie",
    healthcare: "Santé",
    retail: "Commerce",
    services: "Services",
    popularSearches: "Recherches populaires :",
    featuredBusinessesSubtitle: "Découvrez les entreprises les mieux notées recommandées par notre communauté européenne"
  },
  es: {
    trustBadge: "🌟 Confiado por 50,000+ empresas europeas",
    heroTitle: "Encuentra Empresas",
    heroTitleGradient: "Por Toda Europa", 
    heroSubtitle: "Descubre millones de empresas en 30+ países europeos. Desde restaurantes en París hasta empresas tech en Ámsterdam.",
    searchButton: "Empezar Búsqueda Ahora",
    pricingButton: "Ver Planes de Precios",
    featuredTitle: "Empresas Destacadas",
    featuredSubtitle: "Descubre empresas mejor valoradas de Europa",
    categoriesTitle: "Categorías Populares",
    categoriesSubtitle: "Navegar por tipo de empresa",
    seeAllCategories: "Ver Todas las Categorías",
    getStartedTitle: "¿Listo para Empezar?",
    getStartedSubtitle: "Únete a miles de empresas y clientes conectándose por Europa",
    businessesText: "empresas",
    whyChooseTitle: "¿Por Qué Elegir ListAcross EU?",
    whyChooseSubtitle: "El directorio empresarial europeo más completo",
    europeWideCoverage: "Cobertura Paneuropea",
    europeWideCoverageDesc: "Busca en 30+ países europeos con cobertura completa de empresas locales, desde grandes ciudades hasta pueblos pequeños.",
    smartSearch: "Tecnología de Búsqueda Inteligente",
    smartSearchDesc: "Búsqueda avanzada impulsada por IA con sugerencias instantáneas, soporte multiidioma y filtrado inteligente para resultados precisos.",
    verifiedTrusted: "Verificado y Confiable",
    verifiedTrustedDesc: "Todos los listados empresariales están verificados con información de contacto actualizada, reseñas y calificaciones de la comunidad europea.",
    restaurants: "Restaurantes",
    hotels: "Hoteles",
    technology: "Tecnología",
    healthcare: "Salud",
    retail: "Comercio",
    services: "Servicios",
    popularSearches: "Búsquedas populares:",
    featuredBusinessesSubtitle: "Descubre empresas mejor valoradas recomendadas por nuestra comunidad europea"
  }
} as const;

// Demo data - will be replaced with real data later
const DEMO_FEATURED_BUSINESSES = [
  {
    id: 1,
    name: "Café Central Paris",
    category: "Restaurant",
    city: "Paris",
    country: "France",
    rating: 4.8,
    image: "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=400&h=300&fit=crop",
    flag: "🇫🇷"
  },
  {
    id: 2,
    name: "Tech Solutions Amsterdam",
    category: "Technology",
    city: "Amsterdam",
    country: "Netherlands",
    rating: 4.9,
    image: "https://images.unsplash.com/photo-1497366216548-37526070297c?w=400&h=300&fit=crop",
    flag: "🇳🇱"
  },
  {
    id: 3,
    name: "Bella Vista Restaurant",
    category: "Restaurant",
    city: "Rome",
    country: "Italy",
    rating: 4.7,
    image: "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400&h=300&fit=crop",
    flag: "🇮🇹"
  },
  {
    id: 4,
    name: "Boutique Fashion Store",
    category: "Retail",
    city: "Madrid",
    country: "Spain", 
    rating: 4.6,
    image: "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400&h=300&fit=crop",
    flag: "🇪🇸"
  }
];

const getDemoPopularCategories = (t: any) => [
  { key: "restaurants", name: t.restaurants, count: "12,847", icon: "🍽️", color: "bg-red-100 text-red-700" },
  { key: "hotels", name: t.hotels, count: "8,234", icon: "🏨", color: "bg-blue-100 text-blue-700" },
  { key: "technology", name: t.technology, count: "5,692", icon: "💻", color: "bg-purple-100 text-purple-700" },
  { key: "healthcare", name: t.healthcare, count: "4,158", icon: "🏥", color: "bg-green-100 text-green-700" },
  { key: "retail", name: t.retail, count: "9,876", icon: "🛍️", color: "bg-orange-100 text-orange-700" },
  { key: "services", name: t.services, count: "7,543", icon: "🔧", color: "bg-indigo-100 text-indigo-700" }
];

export default function LangHomePage({ params }: { params: { lang: Lang } }) {
  const lang: Lang = params.lang || "en";
  const t = T[lang] || T.en;
  
  return (
    <div className="min-h-screen">
      {/* Full-Width Hero Section with Animations */}
      <section className="min-h-screen bg-gradient-to-br from-brand via-purple-600 to-indigo-800 relative overflow-hidden flex items-center">
        {/* Animated Background Elements */}
        <div className="absolute inset-0">
          {/* Floating Elements */}
          <div className="absolute top-20 left-10 w-32 h-32 bg-white/10 rounded-full animate-pulse"></div>
          <div className="absolute top-40 right-20 w-24 h-24 bg-white/5 rounded-full animate-bounce" style={{ animationDelay: '1s' }}></div>
          <div className="absolute bottom-20 left-1/4 w-40 h-40 bg-white/5 rounded-full animate-pulse" style={{ animationDelay: '2s' }}></div>
          <div className="absolute top-1/3 right-1/4 w-20 h-20 bg-white/10 rounded-full animate-bounce" style={{ animationDelay: '0.5s' }}></div>
          
          {/* Gradient Overlays with Animation */}
          <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-r from-brand/30 via-transparent to-purple-600/30 animate-pulse"></div>
          
          {/* Moving Particles */}
          <div className="absolute inset-0">
            {[...Array(20)].map((_, i) => (
              <div
                key={i}
                className="absolute w-2 h-2 bg-white/20 rounded-full animate-ping"
                style={{
                  left: `${Math.random() * 100}%`,
                  top: `${Math.random() * 100}%`,
                  animationDelay: `${Math.random() * 5}s`,
                  animationDuration: `${2 + Math.random() * 3}s`
                }}
              ></div>
            ))}
          </div>
        </div>
        
        <div className="container mx-auto px-4 py-32 relative z-10">
          <div className="max-w-5xl mx-auto text-center text-white">
            {/* Animated Trust Badge */}
            <div className="inline-flex items-center bg-white/20 backdrop-blur-sm border border-white/30 rounded-full px-6 py-3 mb-8 animate-fade-in-up">
              <span className="text-sm text-white/90">{t.trustBadge}</span>
            </div>
            
            {/* Animated Title */}
            <h1 className="text-6xl md:text-8xl font-bold mb-8 leading-tight animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
              {t.heroTitle}
              <span className="block bg-gradient-to-r from-yellow-300 via-white to-blue-300 bg-clip-text text-transparent animate-pulse">
                {t.heroTitleGradient}
              </span>
            </h1>
            
            {/* Animated Subtitle */}
            <p className="text-xl md:text-2xl text-white/90 mb-16 max-w-4xl mx-auto leading-relaxed animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
              {t.heroSubtitle}
            </p>
            
            {/* Enhanced Search Box with Animation */}
            <div className="max-w-4xl mx-auto mb-16 animate-fade-in-up" style={{ animationDelay: '0.6s' }}>
              <div className="bg-white/95 backdrop-blur-lg p-8 rounded-3xl shadow-2xl border border-white/50 transform hover:scale-105 transition-all duration-300">
                <SearchBoxNew lang={lang} />
                <div className="flex flex-wrap gap-3 mt-6 justify-center">
                  <span className="text-sm text-gray-500 font-medium">{t.popularSearches}</span>
                  {[t.restaurants, t.hotels, t.technology, t.healthcare, t.retail, t.services].map((term, index) => (
                    <button 
                      key={term} 
                      className="px-4 py-2 bg-brand/10 hover:bg-brand/20 rounded-full text-sm text-brand font-medium transition-all duration-300 transform hover:scale-105 animate-fade-in-up"
                      style={{ animationDelay: `${0.8 + index * 0.1}s` }}
                    >
                      {term}
                    </button>
                  ))}
                </div>
              </div>
            </div>
            
            {/* Enhanced Quick Actions with Animation */}
            <div className="flex flex-col sm:flex-row gap-6 justify-center mb-20 animate-fade-in-up" style={{ animationDelay: '1s' }}>
              <Link 
                href={`/${params.lang}/search`}
                className="group bg-white text-brand hover:bg-gray-100 font-bold text-lg px-10 py-5 rounded-2xl shadow-2xl transform hover:scale-110 transition-all duration-300 flex items-center justify-center gap-3"
              >
                <span className="group-hover:animate-bounce">🔍</span>
                Browse All Businesses
              </Link>
              <Link 
                href={`/${params.lang}/countries`}
                className="group border-2 border-white hover:bg-white hover:text-brand font-bold text-lg px-10 py-5 rounded-2xl backdrop-blur-sm transform hover:scale-110 transition-all duration-300 flex items-center justify-center gap-3"
              >
                <span className="group-hover:animate-spin">🌍</span>
                Explore by Country
              </Link>
            </div>

            {/* Animated Trust Indicators */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-3xl mx-auto animate-fade-in-up" style={{ animationDelay: '1.2s' }}>
              {[
                { number: "50K+", label: "Businesses", icon: "🏢" },
                { number: "30+", label: "Countries", icon: "🌍" },
                { number: "6", label: "Languages", icon: "🌐" },
                { number: "4.8★", label: "Rating", icon: "⭐" }
              ].map((item, index) => (
                <div key={item.label} className="text-center group cursor-pointer">
                  <div className="text-4xl mb-2 group-hover:animate-bounce">{item.icon}</div>
                  <div className="text-3xl font-bold text-white mb-1 group-hover:scale-110 transition-transform duration-300">{item.number}</div>
                  <div className="text-sm text-white/80 font-medium">{item.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Featured Businesses Section */}
      <section className="py-24 bg-white relative overflow-hidden">
        {/* Background decoration */}
        <div className="absolute top-0 left-0 w-full h-32 bg-gradient-to-b from-brand/5 to-transparent"></div>
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">{t.featuredTitle}</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              {t.featuredBusinessesSubtitle}
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-7xl mx-auto">
            {DEMO_FEATURED_BUSINESSES.map((business, index) => (
              <div 
                key={business.id} 
                className="card group hover:shadow-2xl transition-all duration-500 transform hover:scale-105 hover:-rotate-1 animate-fade-in-up"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="relative overflow-hidden rounded-t-xl">
                  <img 
                    src={business.image} 
                    alt={business.name}
                    className="w-full h-48 object-cover group-hover:scale-110 transition-transform duration-500"
                  />
                  <div className="absolute top-4 right-4 bg-white/90 backdrop-blur-sm px-2 py-1 rounded-full text-sm font-semibold flex items-center gap-1">
                    ⭐ {business.rating}
                  </div>
                  <div className="absolute top-4 left-4 text-2xl">{business.flag}</div>
                </div>
                <div className="card-body">
                  <h3 className="font-semibold text-lg mb-1">{business.name}</h3>
                  <div className="text-sm text-gray-600 mb-2">{business.category}</div>
                  <div className="text-sm text-gray-500 flex items-center gap-1">
                    📍 {business.city}, {business.country}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Popular Categories Section */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">{t.categoriesTitle}</h2>
            <p className="text-xl text-gray-600">
              {t.categoriesSubtitle}
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-4xl mx-auto">
            {getDemoPopularCategories(t).map((category) => (
              <Link 
                key={category.key}
                href={`/${params.lang}/search?category=${category.key}`}
                className="card hover:shadow-lg transition-all duration-300 transform hover:scale-105 cursor-pointer"
              >
                <div className="card-body">
                  <div className="flex items-center gap-4">
                    <div className={`w-12 h-12 rounded-xl ${category.color} flex items-center justify-center text-xl`}>
                      {category.icon}
                    </div>
                    <div className="flex-1">
                      <h3 className="font-semibold text-lg">{category.name}</h3>
                      <p className="text-gray-600">{category.count} {t.businessesText}</p>
                    </div>
                    <div className="text-gray-400">→</div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Enhanced Features Section */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">{t.whyChooseTitle}</h2>
              <p className="text-xl text-gray-600">
                {t.whyChooseSubtitle}
              </p>
            </div>
            
            <div className="grid md:grid-cols-3 gap-12">
              <div className="text-center group">
                <div className="w-20 h-20 bg-gradient-to-br from-brand to-purple-600 rounded-2xl flex items-center justify-center text-white text-3xl mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
                  🌍
                </div>
                <h3 className="text-2xl font-semibold mb-4">{t.europeWideCoverage}</h3>
                <p className="text-gray-600 leading-relaxed">
                  {t.europeWideCoverageDesc}
                </p>
              </div>
              
              <div className="text-center group">
                <div className="w-20 h-20 bg-gradient-to-br from-brand to-purple-600 rounded-2xl flex items-center justify-center text-white text-3xl mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
                  🔍
                </div>
                <h3 className="text-2xl font-semibold mb-4">{t.smartSearch}</h3>
                <p className="text-gray-600 leading-relaxed">
                  {t.smartSearchDesc}
                </p>
              </div>
              
              <div className="text-center group">
                <div className="w-20 h-20 bg-gradient-to-br from-brand to-purple-600 rounded-2xl flex items-center justify-center text-white text-3xl mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
                  ✅
                </div>
                <h3 className="text-2xl font-semibold mb-4">{t.verifiedTrusted}</h3>
                <p className="text-gray-600 leading-relaxed">
                  {t.verifiedTrustedDesc}
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-br from-brand to-purple-600 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-6">{t.getStartedTitle}</h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto opacity-90">
            {t.getStartedSubtitle}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              href={`/${lang}/search`}
              className="bg-white text-brand hover:bg-gray-100 font-semibold px-8 py-4 rounded-xl transition-colors"
            >
              {t.searchButton}
            </Link>
            <Link 
              href={`/${lang}/pricing`}
              className="border-2 border-white hover:bg-white hover:text-brand font-semibold px-8 py-4 rounded-xl transition-colors"
            >
              {t.pricingButton}
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}