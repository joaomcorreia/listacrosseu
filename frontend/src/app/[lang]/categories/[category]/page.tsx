import Link from "next/link";
import { apiCall } from "@/lib/api";
import CitiesSidebar from "@/components/CitiesSidebar";

type Lang = "en" | "nl" | "pt" | "fr" | "de" | "es";

const T = {
  en: {
    titlePrefix: "Category:",
    subtitle: "Discover businesses in this category across Europe",
    businessesText: "businesses found",
    noBusinesses: "No businesses found in this category.",
    backToCategories: "← Back to Categories",
    location: "Location",
    contact: "Contact",
    website: "Visit Website",
    phone: "Call",
    businessDirectory: "🏢 Business Directory",
    checkBackSoon: "Check back soon for more businesses in this category.",
    featured: "FEATURED"
  },
  nl: {
    titlePrefix: "Categorie:",
    subtitle: "Ontdek bedrijven in deze categorie in heel Europa",
    businessesText: "bedrijven gevonden",
    noBusinesses: "Geen bedrijven gevonden in deze categorie.",
    backToCategories: "← Terug naar Categorieën",
    location: "Locatie",
    contact: "Contact",
    website: "Bezoek Website",
    phone: "Bellen",
    businessDirectory: "🏢 Bedrijvengids",
    checkBackSoon: "Kom binnenkort terug voor meer bedrijven in deze categorie.",
    featured: "UITGELICHT"
  },
  pt: {
    titlePrefix: "Categoria:",
    subtitle: "Descubra empresas nesta categoria em toda a Europa",
    businessesText: "empresas encontradas",
    noBusinesses: "Nenhuma empresa encontrada nesta categoria.",
    backToCategories: "← Voltar às Categorias",
    location: "Localização",
    contact: "Contacto",
    website: "Visitar Website",
    phone: "Ligar",
    businessDirectory: "🏢 Diretório de Empresas",
    checkBackSoon: "Volte em breve para mais empresas nesta categoria.",
    featured: "EM DESTAQUE"
  },
  fr: {
    titlePrefix: "Catégorie:",
    subtitle: "Découvrez des entreprises de cette catégorie à travers l'Europe",
    businessesText: "entreprises trouvées",
    noBusinesses: "Aucune entreprise trouvée dans cette catégorie.",
    backToCategories: "← Retour aux Catégories",
    location: "Emplacement",
    contact: "Contact",
    website: "Visiter le Site",
    phone: "Appeler",
    businessDirectory: "🏢 Répertoire d'Entreprises",
    checkBackSoon: "Revenez bientôt pour plus d'entreprises dans cette catégorie.",
    featured: "EN VEDETTE"
  },
  de: {
    titlePrefix: "Kategorie:",
    subtitle: "Entdecken Sie Unternehmen in dieser Kategorie in ganz Europa",
    businessesText: "Unternehmen gefunden",
    noBusinesses: "Keine Unternehmen in dieser Kategorie gefunden.",
    backToCategories: "← Zurück zu Kategorien",
    location: "Standort",
    contact: "Kontakt",
    website: "Website Besuchen",
    phone: "Anrufen",
    businessDirectory: "🏢 Unternehmensverzeichnis",
    checkBackSoon: "Schauen Sie bald wieder vorbei für mehr Unternehmen in dieser Kategorie.",
    featured: "HERVORGEHOBEN"
  },
  es: {
    titlePrefix: "Categoría:",
    subtitle: "Descubre negocios en esta categoría en toda Europa",
    businessesText: "negocios encontrados",
    noBusinesses: "No se encontraron negocios en esta categoría.",
    backToCategories: "← Volver a Categorías",
    location: "Ubicación",
    contact: "Contacto",
    website: "Visitar Sitio Web",
    phone: "Llamar",
    businessDirectory: "🏢 Directorio de Empresas",
    checkBackSoon: "Vuelve pronto para más negocios en esta categoría.",
    featured: "DESTACADO"
  }
} as const;

async function fetchBusinesses(category: string) {
  const q = `/businesses/?category=${encodeURIComponent(category)}&limit=60`;
  return (await apiCall(q)) || { total: 0, results: [] };
}

export default async function CategoryBusinessesPage({ params }: { params: { lang: Lang; category: string } }) {
  const { lang, category } = params;
  const t = T[lang || "en"] || T.en;
  const data = await fetchBusinesses(category);
  const decodedCategory = decodeURIComponent(category);

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-orange-500 via-red-500 to-pink-600 relative overflow-hidden pt-24 pb-16">
        {/* Animated Background Elements */}
        <div className="absolute inset-0">
          <div className="absolute top-20 right-10 w-32 h-32 bg-white/10 rounded-full animate-pulse"></div>
          <div className="absolute top-40 left-20 w-24 h-24 bg-white/5 rounded-full animate-bounce" style={{ animationDelay: '1s' }}></div>
          <div className="absolute bottom-20 right-1/4 w-40 h-40 bg-white/5 rounded-full animate-pulse" style={{ animationDelay: '2s' }}></div>
        </div>
        
        <div className="container mx-auto px-6 py-16 relative z-10 text-center text-white">
          <div className="inline-flex items-center bg-white/20 backdrop-blur-sm border border-white/30 rounded-full px-6 py-3 mb-8 animate-fade-in-up">
            <span className="text-sm text-white/90">🏢 Business Directory</span>
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold mb-6 animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
            {t.titlePrefix} {decodedCategory}
          </h1>
          <p className="text-xl text-white/90 mb-8 max-w-3xl mx-auto animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
            {t.subtitle}
          </p>
          
          <div className="inline-flex items-center bg-white/20 backdrop-blur-sm border border-white/30 rounded-full px-6 py-3 mb-8 animate-fade-in-up" style={{ animationDelay: '0.5s' }}>
            <span className="text-white font-semibold">{data.total} {t.businessesText}</span>
          </div>
          
          <Link 
            href={`/${lang}/categories`}
            className="inline-flex items-center text-white/80 hover:text-white transition-colors animate-fade-in-up"
            style={{ animationDelay: '0.6s' }}
          >
            {t.backToCategories}
          </Link>
        </div>
      </section>

      {/* Businesses Grid Section with Sidebar */}
      <section className="bg-white relative">
        <div className="absolute top-0 left-0 w-full h-32 bg-gradient-to-b from-orange-500/5 to-transparent"></div>
        <div className="flex relative z-10">
          <div className="flex-1 py-20 px-6">
          {data.results.length > 0 ? (
            <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3 max-w-7xl mx-auto">
              {data.results.map((business: any, index: number) => (
                <article 
                  key={`${business.id}-${business.name}`} 
                  className="group rounded-3xl p-8 bg-gradient-to-br from-white to-orange-50 border border-gray-200 hover:border-orange-300 shadow-lg hover:shadow-2xl transform hover:scale-105 transition-all duration-300 animate-fade-in-up"
                  style={{ animationDelay: `${0.1 * index}s` }}
                >
                  <div className="flex items-start justify-between mb-6">
                    <div className="w-14 h-14 bg-gradient-to-br from-orange-500 to-red-500 rounded-2xl flex items-center justify-center text-white text-xl font-bold group-hover:scale-110 transition-transform duration-300">
                      {business.name.substring(0, 1).toUpperCase()}
                    </div>
                    {business.is_featured && (
                      <div className="bg-gradient-to-r from-yellow-400 to-orange-500 text-white text-xs font-bold px-3 py-1 rounded-full">
                        FEATURED
                      </div>
                    )}
                  </div>
                  
                  <h3 className="text-2xl font-bold text-gray-900 mb-3 group-hover:text-orange-600 transition-colors">
                    {business.name}
                  </h3>
                  
                  {business.description && (
                    <p className="text-gray-600 mb-4 line-clamp-3">
                      {business.description}
                    </p>
                  )}
                  
                  <div className="space-y-3 mb-6">
                    <div className="flex items-center text-sm text-gray-600">
                      <span className="w-5 h-5 flex items-center justify-center mr-3">📍</span>
                      <span>{business.city}, {business.country}</span>
                    </div>
                    
                    {business.address && (
                      <div className="flex items-start text-sm text-gray-600">
                        <span className="w-5 h-5 flex items-center justify-center mr-3 mt-0.5">🏠</span>
                        <span>{business.address}</span>
                      </div>
                    )}
                    
                    {business.phone && (
                      <div className="flex items-center text-sm text-gray-600">
                        <span className="w-5 h-5 flex items-center justify-center mr-3">📞</span>
                        <span>{business.phone}</span>
                      </div>
                    )}
                  </div>
                  
                  <div className="flex gap-3">
                    {business.website && (
                      <a 
                        href={business.website}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex-1 bg-gradient-to-r from-orange-500 to-red-500 text-white px-4 py-3 rounded-xl font-medium text-center hover:from-orange-600 hover:to-red-600 transition-all duration-300 text-sm"
                      >
                        {t.website}
                      </a>
                    )}
                    
                    {business.phone && (
                      <a 
                        href={`tel:${business.phone}`}
                        className="flex-1 bg-white border-2 border-orange-300 text-orange-600 px-4 py-3 rounded-xl font-medium text-center hover:bg-orange-50 transition-colors text-sm"
                      >
                        {t.phone}
                      </a>
                    )}
                  </div>
                </article>
              ))}
            </div>
          ) : (
            <div className="text-center py-16 animate-fade-in-up">
              <div className="w-24 h-24 bg-gradient-to-br from-gray-100 to-gray-200 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-3xl">🏢</span>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">{t.noBusinesses}</h3>
              <p className="text-gray-600 mb-8">Check back soon for more businesses in this category.</p>
              <Link 
                href={`/${lang}/categories`}
                className="inline-flex items-center bg-orange-500 text-white px-8 py-4 rounded-xl font-semibold hover:bg-orange-600 transition-colors"
              >
                {t.backToCategories}
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