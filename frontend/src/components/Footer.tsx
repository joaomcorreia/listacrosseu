'use client';
import Link from 'next/link';
import { useSiteSettings } from '@/hooks/useSiteSettings';
import { UI as FORMS_UI, FORMS_SLUG } from '@/i18n/forms';
import { HOW_SLUGS } from '@/i18n/howitworks';

interface FooterProps {
  lang: string;
}

export default function Footer({ lang }: FooterProps) {
  const { settings } = useSiteSettings();

  const UI = {
    en: { 
      intro: "ListAcross EU is the premier business directory for European markets, connecting companies and opportunities across all EU member states. Based in the Netherlands, we help businesses grow through strategic visibility and networking.",
      sources: "Sources",
      blogCategories: "Blog Categories", 
      menu: "Menu",
      search: "Search", 
      countries: "Countries", 
      categories: "Categories", 
      pricing: "Pricing", 
      aiDesign: "AI Design", 
      howItWorks: "How it works",
      googlePlaces: "Google Places"
    },
    fr: { 
      intro: "ListAcross EU est le premier annuaire d'entreprises pour les marchés européens, connectant les entreprises et les opportunités dans tous les États membres de l'UE. Basés aux Pays-Bas, nous aidons les entreprises à croître grâce à la visibilité stratégique.",
      sources: "Sources",
      blogCategories: "Catégories de blog", 
      menu: "Menu",
      search: "Recherche", 
      countries: "Pays", 
      categories: "Catégories", 
      pricing: "Tarifs", 
      aiDesign: "IA Design", 
      howItWorks: "Comment ça marche",
      googlePlaces: "Google Places"
    },
    nl: { 
      intro: "ListAcross EU is de vooraanstaande bedrijfsgids voor Europese markten, die bedrijven en kansen verbindt in alle EU-lidstaten. Gevestigd in Nederland helpen we bedrijven groeien door strategische zichtbaarheid en netwerken.",
      sources: "Bronnen",
      blogCategories: "Blog Categorieën", 
      menu: "Menu",
      search: "Zoeken", 
      countries: "Landen", 
      categories: "Categorieën", 
      pricing: "Prijzen", 
      aiDesign: "AI Design", 
      howItWorks: "Hoe het werkt",
      googlePlaces: "Google Places"
    },
    pt: { 
      intro: "ListAcross EU é o principal diretório de negócios para mercados europeus, conectando empresas e oportunidades em todos os estados membros da UE. Baseados nos Países Baixos, ajudamos negócios a crescer através de visibilidade estratégica.",
      sources: "Fontes",
      blogCategories: "Categorias do Blog", 
      menu: "Menu",
      search: "Pesquisa", 
      countries: "Países", 
      categories: "Categorias", 
      pricing: "Preços", 
      aiDesign: "Design IA", 
      howItWorks: "Como funciona",
      googlePlaces: "Google Places"
    },
    de: { 
      intro: "ListAcross EU ist das führende Unternehmensverzeichnis für europäische Märkte und verbindet Unternehmen und Möglichkeiten in allen EU-Mitgliedstaaten. Mit Sitz in den Niederlanden helfen wir Unternehmen durch strategische Sichtbarkeit zu wachsen.",
      sources: "Quellen",
      blogCategories: "Blog Kategorien", 
      menu: "Menü",
      search: "Suche", 
      countries: "Länder", 
      categories: "Kategorien", 
      pricing: "Preise", 
      aiDesign: "KI Design", 
      howItWorks: "So funktioniert es",
      googlePlaces: "Google Places"
    },
    es: { 
      intro: "ListAcross EU es el principal directorio empresarial para mercados europeos, conectando empresas y oportunidades en todos los estados miembros de la UE. Con sede en los Países Bajos, ayudamos a las empresas a crecer a través de visibilidad estratégica.",
      sources: "Fuentes",
      blogCategories: "Categorías del Blog", 
      menu: "Menú",
      search: "Buscar", 
      countries: "Países", 
      categories: "Categorías", 
      pricing: "Precios", 
      aiDesign: "Diseño IA", 
      howItWorks: "Cómo funciona",
      googlePlaces: "Google Places"
    },
  } as const;

  const langKey = lang as keyof typeof UI;
  const text = UI[langKey] || UI.en;
  const langUppercase = lang.toUpperCase() as keyof typeof FORMS_UI;
  const formsLabel = FORMS_UI[langUppercase]?.navLabel || FORMS_UI.EN.navLabel;

  // Mock blog categories - in real implementation, fetch from API
  const blogCategories = [
    { name: 'Business Tips', slug: 'business-tips' },
    { name: 'Market Insights', slug: 'market-insights' },
    { name: 'Success Stories', slug: 'success-stories' },
    { name: 'Industry News', slug: 'industry-news' },
    { name: 'EU Regulations', slug: 'eu-regulations' }
  ];

  return (
    <footer className="bg-gray-900 text-white">
      <div className="container mx-auto px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          
          {/* Column 1: Footer Logo & Intro */}
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              {settings.footerLogo && (
                <img 
                  src={settings.footerLogo} 
                  alt="ListAcross EU Footer Logo" 
                  className="h-12 w-auto"
                />
              )}
              <h3 className="text-xl font-bold">ListAcross EU</h3>
            </div>
            <p className="text-gray-300 text-sm leading-relaxed">
              {text.intro}
            </p>
          </div>

          {/* Column 2: Sources */}
          <div className="space-y-4">
            <h4 className="text-lg font-semibold">{text.sources}</h4>
            <ul className="space-y-2">
              <li>
                <Link 
                  href="https://maps.google.com" 
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-300 hover:text-white text-sm transition-colors"
                >
                  {text.googlePlaces}
                </Link>
              </li>
            </ul>
          </div>

          {/* Column 3: Blog Categories */}
          <div className="space-y-4">
            <h4 className="text-lg font-semibold">{text.blogCategories}</h4>
            <ul className="space-y-2">
              {blogCategories.map((category) => (
                <li key={category.slug}>
                  <Link 
                    href={`/${lang}/blog/category/${category.slug}`} 
                    className="text-gray-300 hover:text-white text-sm transition-colors"
                  >
                    {category.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Column 4: Menu */}
          <div className="space-y-4">
            <h4 className="text-lg font-semibold">{text.menu}</h4>
            <ul className="space-y-2">
              <li>
                <Link 
                  href={`/${lang}/search`} 
                  className="text-gray-300 hover:text-white text-sm transition-colors"
                >
                  {text.search}
                </Link>
              </li>
              <li>
                <Link 
                  href={`/${lang}/countries`} 
                  className="text-gray-300 hover:text-white text-sm transition-colors"
                >
                  {text.countries}
                </Link>
              </li>
              <li>
                <Link 
                  href={`/${lang}/categories`} 
                  className="text-gray-300 hover:text-white text-sm transition-colors"
                >
                  {text.categories}
                </Link>
              </li>
              <li>
                <Link 
                  href={`/${lang}/pricing`} 
                  className="text-gray-300 hover:text-white text-sm transition-colors"
                >
                  {text.pricing}
                </Link>
              </li>
              <li>
                <Link 
                  href={`/${lang}/ai-design`} 
                  className="text-gray-300 hover:text-white text-sm transition-colors"
                >
                  {text.aiDesign}
                </Link>
              </li>
              <li>
                <Link 
                  href={`/${lang}/${HOW_SLUGS[lang.toUpperCase() as keyof typeof HOW_SLUGS] || 'how-it-works'}`} 
                  className="text-gray-300 hover:text-white text-sm transition-colors"
                >
                  {text.howItWorks}
                </Link>
              </li>
              <li>
                <Link 
                  href={`/${lang}/${FORMS_SLUG[langUppercase] || FORMS_SLUG.EN}`} 
                  className="text-gray-300 hover:text-white text-sm transition-colors"
                >
                  {formsLabel}
                </Link>
              </li>
            </ul>
          </div>

        </div>

        {/* Copyright */}
        <div className="border-t border-gray-800 mt-8 pt-8 text-center">
          <p className="text-gray-400 text-sm">
            © {new Date().getFullYear()} ListAcross EU. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}