import Link from "next/link";
import { apiCall } from "@/lib/api";
import CitiesSidebar from "@/components/CitiesSidebar";

type Lang = "en" | "nl" | "pt" | "fr" | "de" | "es";

const T = {
  en: {
    title: "Browse Categories",
    subtitle: "Find businesses by type - restaurants, retail, services and more across Europe.",
    businessesText: "businesses",
    noCategories: "No categories found.",
    backToHome: "← Back to Home",
    explore: "Explore",
    businessCategories: "🏷️ Business Categories",
    checkBackSoon: "Check back soon for more categories and businesses."
  },
  nl: {
    title: "Categorieën Bekijken",
    subtitle: "Vind bedrijven per type - restaurants, retail, diensten en meer in heel Europa.",
    businessesText: "bedrijven",
    noCategories: "Geen categorieën gevonden.",
    backToHome: "← Terug naar Home",
    explore: "Ontdekken",
    businessCategories: "🏷️ Bedrijfscategorieën",
    checkBackSoon: "Kom binnenkort terug voor meer categorieën en bedrijven."
  },
  pt: {
    title: "Navegar Categorias",
    subtitle: "Encontre empresas por tipo - restaurantes, comércio, serviços e mais em toda a Europa.",
    businessesText: "empresas",
    noCategories: "Nenhuma categoria encontrada.",
    backToHome: "← Voltar ao Início",
    explore: "Explorar",
    businessCategories: "🏷️ Categorias de Empresas",
    checkBackSoon: "Volte em breve para mais categorias e empresas."
  },
  fr: {
    title: "Parcourir les Catégories",
    subtitle: "Trouvez des entreprises par type - restaurants, commerce, services et plus à travers l'Europe.",
    businessesText: "entreprises",
    noCategories: "Aucune catégorie trouvée.",
    backToHome: "← Retour à l'accueil",
    explore: "Explorer",
    businessCategories: "🏷️ Catégories d'Entreprises",
    checkBackSoon: "Revenez bientôt pour plus de catégories et d'entreprises."
  },
  de: {
    title: "Kategorien Durchsuchen",
    subtitle: "Finden Sie Unternehmen nach Typ - Restaurants, Einzelhandel, Dienstleistungen und mehr in Europa.",
    businessesText: "Unternehmen",
    noCategories: "Keine Kategorien gefunden.",
    backToHome: "← Zurück zur Startseite",
    explore: "Erkunden",
    businessCategories: "🏷️ Unternehmenskategorien",
    checkBackSoon: "Schauen Sie bald wieder vorbei für mehr Kategorien und Unternehmen."
  },
  es: {
    title: "Explorar Categorías",
    subtitle: "Encuentra negocios por tipo - restaurantes, comercio, servicios y más en toda Europa.",
    businessesText: "negocios",
    noCategories: "No se encontraron categorías.",
    backToHome: "← Volver al Inicio",
    explore: "Explorar",
    businessCategories: "🏷️ Categorías de Empresas",
    checkBackSoon: "Vuelve pronto para más categorías y empresas."
  }
} as const;

// Category icons mapping
const categoryIcons: { [key: string]: string } = {
  "Restaurant": "🍴",
  "Retail": "🛍️",
  "Services": "⚙️",
  "Food": "🥘",
  "Shopping": "🏪",
  "Technology": "💻",
  "Health": "🏥",
  "Beauty": "💄",
  "Education": "📚",
  "Entertainment": "🎭",
  "Finance": "💰",
  "Travel": "✈️",
  "Automotive": "🚗",
  "Real Estate": "🏠",
  "Legal": "⚖️"
};

export default async function CategoriesPage({ params }: { params: { lang: Lang } }) {
  const lang: Lang = params.lang || "en";
  const t = T[lang] || T.en;
  
  // Fetch categories with business counts from our new API
  const response = await apiCall(`/categories/counts/?lang=${lang}`) || { categories: [], total_categories: 0 };
  const categories = response.categories || [];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-emerald-500 via-teal-600 to-cyan-700 relative overflow-hidden pt-24 pb-16">
        {/* Animated Background Elements */}
        <div className="absolute inset-0">
          <div className="absolute top-20 left-10 w-32 h-32 bg-white/10 rounded-full animate-pulse"></div>
          <div className="absolute top-40 right-20 w-24 h-24 bg-white/5 rounded-full animate-bounce" style={{ animationDelay: '1s' }}></div>
          <div className="absolute bottom-20 left-1/4 w-40 h-40 bg-white/5 rounded-full animate-pulse" style={{ animationDelay: '2s' }}></div>
        </div>
        
        <div className="container mx-auto px-6 py-16 relative z-10 text-center text-white">
          <div className="inline-flex items-center bg-white/20 backdrop-blur-sm border border-white/30 rounded-full px-6 py-3 mb-8 animate-fade-in-up">
            <span className="text-sm text-white/90">{t.businessCategories}</span>
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

      {/* Categories Grid Section with Sidebar */}
      <section className="bg-white relative">
        <div className="absolute top-0 left-0 w-full h-32 bg-gradient-to-b from-emerald-500/5 to-transparent"></div>
        <div className="flex relative z-10">
          <div className="flex-1 py-20 px-6">
          {categories.length > 0 ? (
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 max-w-7xl mx-auto">
              {categories.map((category: any, index: number) => {
                const icon = categoryIcons[category.name] || "📋";
                return (
                  <Link 
                    key={category.slug} 
                    href={`/${lang}/categories/${encodeURIComponent(category.slug)}`}
                    className="group rounded-3xl p-8 bg-gradient-to-br from-white to-emerald-50 border border-gray-200 hover:border-emerald-300 shadow-lg hover:shadow-2xl transform hover:scale-105 transition-all duration-300 animate-fade-in-up"
                    style={{ animationDelay: `${0.1 * index}s` }}
                  >
                    <div className="flex items-center justify-between mb-4">
                      <div className="w-16 h-16 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-3xl flex items-center justify-center text-white text-2xl group-hover:scale-110 transition-transform duration-300">
                        {icon}
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-emerald-600">{category.business_count}</div>
                        <div className="text-sm text-gray-500">{t.businessesText}</div>
                      </div>
                    </div>
                    
                    <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-emerald-600 transition-colors">
                      {category.name_localized || category.name}
                    </h3>
                    
                    <div className="flex items-center text-emerald-600 font-medium group-hover:translate-x-2 transition-transform duration-300">
                      {t.explore} →
                    </div>
                  </Link>
                );
              })}
            </div>
          ) : (
            <div className="text-center py-16 animate-fade-in-up">
              <div className="w-24 h-24 bg-gradient-to-br from-gray-100 to-gray-200 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-3xl">🏷️</span>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">{t.noCategories}</h3>
              <p className="text-gray-600 mb-8">{t.checkBackSoon}</p>
              <Link 
                href={`/${lang}`}
                className="inline-flex items-center bg-emerald-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-emerald-700 transition-colors"
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