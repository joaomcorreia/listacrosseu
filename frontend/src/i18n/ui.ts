// UI translations for ListAcross EU search functionality
// Supports nl, pt, en, fr, de, es (Arabic ready for dashboard later)

export const UI = {
  eu: {
    searchPlaceholder: "Search businesses across the EU, e.g. 'restaurant in Amsterdam'",
    search: "Search EU-wide",
    searchResults: "EU Search Results",
    resultsFor: "Results across the EU for",
    typeToSearch: "Type to search across 27 countries…",
    noResults: "No businesses found across the EU",
    loading: "Searching across the EU...",
    total: "total",
    showingResults: "Showing EU results",
    of: "of",
    searchSuggestions: "EU search suggestions",
    recentSearches: "Recent EU searches",
    clearHistory: "Clear history",
    category: "Category",
    location: "Location",
    address: "Address",
    website: "Website",
    phone: "Phone",
    email: "Email"
  },
  en: {
    searchPlaceholder: "Search businesses, e.g. 'florist in Porto'",
    search: "Search",
    searchResults: "Search Results",
    resultsFor: "Results for",
    typeToSearch: "Type to search…",
    noResults: "No businesses found",
    loading: "Searching...",
    total: "total",
    showingResults: "Showing results",
    of: "of",
    searchSuggestions: "Search suggestions",
    recentSearches: "Recent searches",
    clearHistory: "Clear history",
    category: "Category",
    location: "Location",
    address: "Address",
    website: "Website",
    phone: "Phone",
    email: "Email"
  },
  fr: {
    searchPlaceholder: "Rechercher des entreprises, ex. 'fleuriste à Porto'",
    search: "Rechercher",
    searchResults: "Résultats de recherche",
    resultsFor: "Résultats pour",
    typeToSearch: "Tapez pour rechercher…",
    noResults: "Aucune entreprise trouvée",
    loading: "Recherche en cours...",
    total: "au total",
    showingResults: "Affichage des résultats",
    of: "sur",
    searchSuggestions: "Suggestions de recherche",
    recentSearches: "Recherches récentes",
    clearHistory: "Effacer l'historique",
    category: "Catégorie",
    location: "Localisation",
    address: "Adresse",
    website: "Site web",
    phone: "Téléphone",
    email: "E-mail"
  },
  nl: {
    searchPlaceholder: "Zoek bedrijven, bv. 'bloemist in Porto'",
    search: "Zoeken",
    searchResults: "Zoekresultaten",
    resultsFor: "Resultaten voor",
    typeToSearch: "Typ om te zoeken…",
    noResults: "Geen bedrijven gevonden",
    loading: "Zoeken...",
    total: "totaal",
    showingResults: "Resultaten weergeven",
    of: "van",
    searchSuggestions: "Zoeksuggesties",
    recentSearches: "Recente zoekopdrachten",
    clearHistory: "Geschiedenis wissen",
    category: "Categorie",
    location: "Locatie",
    address: "Adres",
    website: "Website",
    phone: "Telefoon",
    email: "E-mail"
  },
  pt: {
    searchPlaceholder: "Pesquisar empresas, ex. 'florista no Porto'",
    search: "Pesquisar",
    searchResults: "Resultados da pesquisa",
    resultsFor: "Resultados para",
    typeToSearch: "Digite para pesquisar…",
    noResults: "Nenhuma empresa encontrada",
    loading: "Pesquisando...",
    total: "total",
    showingResults: "Mostrando resultados",
    of: "de",
    searchSuggestions: "Sugestões de pesquisa",
    recentSearches: "Pesquisas recentes",
    clearHistory: "Limpar histórico",
    category: "Categoria",
    location: "Localização",
    address: "Endereço",
    website: "Website",
    phone: "Telefone",
    email: "E-mail"
  },
  de: {
    searchPlaceholder: "Unternehmen suchen, z. B. 'Florist in Porto'",
    search: "Suchen",
    searchResults: "Suchergebnisse",
    resultsFor: "Ergebnisse für",
    typeToSearch: "Zum Suchen tippen…",
    noResults: "Keine Unternehmen gefunden",
    loading: "Suchen...",
    total: "insgesamt",
    showingResults: "Ergebnisse anzeigen",
    of: "von",
    searchSuggestions: "Suchvorschläge",
    recentSearches: "Letzte Suchanfragen",
    clearHistory: "Verlauf löschen",
    category: "Kategorie",
    location: "Standort",
    address: "Adresse",
    website: "Website",
    phone: "Telefon",
    email: "E-Mail"
  },
  es: {
    searchPlaceholder: "Buscar negocios, ej. 'floristería en Oporto'",
    search: "Buscar",
    searchResults: "Resultados de búsqueda",
    resultsFor: "Resultados para",
    typeToSearch: "Escribe para buscar…",
    noResults: "No se encontraron negocios",
    loading: "Buscando...",
    total: "total",
    showingResults: "Mostrando resultados",
    of: "de",
    searchSuggestions: "Sugerencias de búsqueda",
    recentSearches: "Búsquedas recientes",
    clearHistory: "Borrar historial",
    category: "Categoría",
    location: "Ubicación",
    address: "Dirección",
    website: "Sitio web",
    phone: "Teléfono",
    email: "Correo electrónico"
  },
  // Arabic ready for dashboard use
  ar: {
    searchPlaceholder: "ابحث عن الشركات، مثل 'بائع زهور في بورتو'",
    search: "بحث",
    searchResults: "نتائج البحث",
    resultsFor: "نتائج لـ",
    typeToSearch: "اكتب للبحث...",
    noResults: "لم يتم العثور على شركات",
    loading: "جاري البحث...",
    total: "المجموع",
    showingResults: "عرض النتائج",
    of: "من",
    searchSuggestions: "اقتراحات البحث",
    recentSearches: "عمليات البحث الحديثة",
    clearHistory: "مسح التاريخ",
    category: "الفئة",
    location: "الموقع",
    address: "العنوان",
    website: "الموقع الإلكتروني",
    phone: "الهاتف",
    email: "البريد الإلكتروني"
  }
} as const;

export type SupportedLanguage = keyof typeof UI;

// Helper function to get UI text safely
export function getUIText(lang: string, key: keyof typeof UI.en): string {
  const normalizedLang = lang as SupportedLanguage;
  if (UI[normalizedLang] && UI[normalizedLang][key]) {
    return UI[normalizedLang][key];
  }
  // Fallback to English
  return UI.en[key];
}

// Language configuration
export const SUPPORTED_LANGUAGES = ['eu', 'en', 'fr', 'nl', 'pt', 'de', 'es'] as const;
export const RTL_LANGUAGES = ['ar'] as const;

export function isRTL(lang: string): boolean {
  return RTL_LANGUAGES.includes(lang as any);
}