// app/[lang]/eu/page.tsx
// EU Landing page with Top Countries section (translation‑ready) and safe i18n fallbacks.
// Assumes: Next.js App Router, TailwindCSS, languages: nl, pt, en, fr, de, es.
// Place at: app/[lang]/eu/page.tsx

import type { Metadata } from 'next';
import Link from 'next/link';

// -------------------------
// Supported languages & helpers
// -------------------------
const SUPPORTED_LANGS = ['eu', 'en', 'nl', 'pt', 'fr', 'de', 'es'] as const;
type Lang = typeof SUPPORTED_LANGS[number];

function normalizeLang(raw?: string): Lang {
  const l = (raw || 'eu').toLowerCase();
  return (SUPPORTED_LANGS as readonly string[]).includes(l as Lang) ? (l as Lang) : 'eu';
}

// -------------------------
// i18n dictionary (inline demo). Swap to your real i18n loader later.
// -------------------------
const DICT: Record<string, any> = {
  eu: {
    seo: {
      title: 'Find trusted services across the EU',
      description: 'Discover featured businesses from all EU countries. Compare categories, explore hubs, and advertise EU‑wide.'
    },
    hero: {
      title: 'Find trusted services across the EU',
      subtitle: 'One directory. 27 countries. 6 languages. EU‑wide exposure for your business.'
    },
    sections: {
      topCountries: 'Top countries right now',
      explore: 'Explore',
      businesses: 'businesses',
      categories: 'categories',
      viewAll: 'View all countries'
    },
    cta: { advertise: 'Advertise EU‑wide' }
  },
  en: {
    seo: {
      title: 'Find trusted services across the EU',
      description: 'Discover featured businesses from all EU countries. Compare categories, explore hubs, and advertise EU‑wide.'
    },
    hero: {
      title: 'Find trusted services across the EU',
      subtitle: 'One directory. 27 countries. 6 languages. EU‑wide exposure for your business.'
    },
    sections: {
      topCountries: 'Top countries right now',
      explore: 'Explore',
      businesses: 'businesses',
      categories: 'categories',
      viewAll: 'View all countries'
    },
    cta: { advertise: 'Advertise EU‑wide' }
  },
  nl: {
    seo: {
      title: 'Vind betrouwbare diensten in de EU',
      description: 'Ontdek aanbevolen bedrijven uit alle EU‑landen. Vergelijk categorieën, bekijk hubs en adverteer EU‑breed.'
    },
    hero: {
      title: 'Vind betrouwbare diensten in de EU',
      subtitle: 'Eén gids. 27 landen. 6 talen. EU‑brede zichtbaarheid voor jouw bedrijf.'
    },
    sections: {
      topCountries: 'Populaire landen op dit moment',
      explore: 'Ontdek',
      businesses: 'bedrijven',
      categories: 'categorieën',
      viewAll: 'Alle landen bekijken'
    },
    cta: { advertise: 'EU‑breed adverteren' }
  },
  pt: {
    seo: {
      title: 'Encontre serviços de confiança na UE',
      description: 'Descubra empresas em destaque de todos os países da UE. Compare categorias, explore hubs e anuncie em toda a UE.'
    },
    hero: {
      title: 'Encontre serviços de confiança na UE',
      subtitle: 'Um diretório. 27 países. 6 idiomas. Exposição em toda a UE.'
    },
    sections: {
      topCountries: 'Países em destaque',
      explore: 'Explorar',
      businesses: 'empresas',
      categories: 'categorias',
      viewAll: 'Ver todos os países'
    },
    cta: { advertise: 'Anunciar em toda a UE' }
  },
  fr: {
    seo: {
      title: 'Trouvez des services fiables dans l\'UE',
      description: 'Découvrez des entreprises mises en avant dans toute l\'UE. Comparez les catégories, explorez les hubs et annoncez à l\'échelle européenne.'
    },
    hero: {
      title: 'Trouvez des services fiables dans l\'UE',
      subtitle: 'Un annuaire. 27 pays. 6 langues. Visibilité UE pour votre entreprise.'
    },
    sections: {
      topCountries: 'Pays à la une',
      explore: 'Explorer',
      businesses: 'entreprises',
      categories: 'catégories',
      viewAll: 'Voir tous les pays'
    },
    cta: { advertise: 'Annoncer dans toute l\'UE' }
  },
  de: {
    seo: {
      title: 'Finde vertrauenswürdige Services in der EU',
      description: 'Entdecke empfohlene Unternehmen aus allen EU‑Ländern. Kategorien vergleichen, Hubs erkunden und EU‑weit werben.'
    },
    hero: {
      title: 'Finde vertrauenswürdige Services in der EU',
      subtitle: 'Ein Verzeichnis. 27 Länder. 6 Sprachen. EU‑weite Sichtbarkeit.'
    },
    sections: {
      topCountries: 'Top‑Länder aktuell',
      explore: 'Entdecken',
      businesses: 'Unternehmen',
      categories: 'Kategorien',
      viewAll: 'Alle Länder ansehen'
    },
    cta: { advertise: 'EU‑weit werben' }
  },
  es: {
    seo: {
      title: 'Encuentra servicios fiables en la UE',
      description: 'Descubre negocios destacados de todos los países de la UE. Compara categorías, explora hubs y anúnciate en toda la UE.'
    },
    hero: {
      title: 'Encuentra servicios fiables en la UE',
      subtitle: 'Un directorio. 27 países. 6 idiomas. Exposición a nivel UE.'
    },
    sections: {
      topCountries: 'Países destacados',
      explore: 'Explorar',
      businesses: 'negocios',
      categories: 'categorías',
      viewAll: 'Ver todos los países'
    },
    cta: { advertise: 'Anunciar en toda la UE' }
  }
};

function tFor(rawLang?: string) {
  return DICT[normalizeLang(rawLang)];
}

// -------------------------
// Mock country metadata (replace with DB/API later)
// -------------------------
export type CountryMeta = {
  code: string; // ISO 3166-1 alpha-2
  name: string;
  flag: string; // emoji or image URL
  businessCount: number; // from analytics
  categoryCount: number; // from taxonomy
  topCategories: string[]; // a few popular categories
};

const ALL_COUNTRIES: CountryMeta[] = [
  { code: 'NL', name: 'Netherlands', flag: '🇳🇱', businessCount: 1240, categoryCount: 58, topCategories: ['Restaurants', 'Legal', 'Auto'] },
  { code: 'PT', name: 'Portugal', flag: '🇵🇹', businessCount: 980, categoryCount: 52, topCategories: ['Hotels', 'Health', 'Construction'] },
  { code: 'FR', name: 'France', flag: '🇫🇷', businessCount: 2120, categoryCount: 73, topCategories: ['Cafés', 'Fashion', 'Medical'] },
  { code: 'DE', name: 'Germany', flag: '🇩🇪', businessCount: 2310, categoryCount: 77, topCategories: ['IT', 'Automotive', 'Finance'] },
  { code: 'ES', name: 'Spain', flag: '🇪🇸', businessCount: 1650, categoryCount: 61, topCategories: ['Tourism', 'Health', 'Food'] },
  { code: 'IT', name: 'Italy', flag: '🇮🇹', businessCount: 1710, categoryCount: 65, topCategories: ['Restaurants', 'Design', 'Tourism'] },
  { code: 'BE', name: 'Belgium', flag: '🇧🇪', businessCount: 640, categoryCount: 44, topCategories: ['Logistics', 'Beer', 'Legal'] },
  { code: 'IE', name: 'Ireland', flag: '🇮🇪', businessCount: 420, categoryCount: 31, topCategories: ['Tech', 'Finance', 'Food'] },
  { code: 'PL', name: 'Poland', flag: '🇵🇱', businessCount: 890, categoryCount: 49, topCategories: ['Manufacturing', 'IT', 'Retail'] },
  { code: 'SE', name: 'Sweden', flag: '🇸🇪', businessCount: 510, categoryCount: 37, topCategories: ['Design', 'Tech', 'Outdoor'] },
];

// Shuffle helper (deterministic seed optional)
function shuffle<T>(arr: T[]): T[] {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// Server function to fetch featured EU businesses (replace with real API)
async function fetchFeaturedEU(limit = 12) {
  const base = process.env.NEXT_PUBLIC_API_BASE;
  if (!base) return [];
  const res = await fetch(`${base}/api/businesses?scope=eu&featured=true&limit=${limit}`, {
    next: { revalidate: 300 }
  });
  if (!res.ok) return [];
  return res.json();
}

// -------------------------
// Components
// -------------------------
function SectionHeading({ children }: { children: React.ReactNode }) {
  return (
    <h2 className="text-2xl md:text-3xl font-semibold tracking-tight">{children}</h2>
  );
}

function CountryCard({ c, t, lang }: { c: CountryMeta; t: any; lang: string }) {
  const url = `/${lang}/countries/${c.code.toLowerCase()}/`;
  return (
    <Link href={url} className="group">
      <div className="rounded-2xl border border-gray-200 dark:border-gray-800 p-5 shadow-sm hover:shadow-md transition-shadow bg-white/60 dark:bg-neutral-900/60">
        <div className="flex items-center gap-3">
          <span className="text-3xl" aria-hidden>{c.flag}</span>
          <div>
            <div className="text-lg font-medium">{c.name}</div>
            <div className="text-sm text-gray-500 dark:text-gray-400">
              {c.businessCount.toLocaleString()} {t.sections.businesses} · {c.categoryCount} {t.sections.categories}
            </div>
          </div>
        </div>
        <div className="mt-3 flex flex-wrap gap-2">
          {c.topCategories.map((cat) => (
            <span key={cat} className="text-xs px-2 py-1 rounded-full border border-gray-200 dark:border-gray-700">
              {cat}
            </span>
          ))}
        </div>
        <div className="mt-4 inline-flex items-center gap-1 text-sm font-medium text-blue-600 dark:text-blue-400">
          {t.sections.explore}
          <svg className="size-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
        </div>
      </div>
    </Link>
  );
}

function TopCountries({ lang }: { lang: string }) {
  const t = tFor(lang);
  const randomized = shuffle(ALL_COUNTRIES).slice(0, 6);
  return (
    <section className="mt-8">
      <div className="flex items-end justify-between mb-4">
        <SectionHeading>{t.sections.topCountries}</SectionHeading>
        <Link href={`/${lang}/countries/`} className="text-sm text-blue-600 dark:text-blue-400 font-medium">{t.sections.viewAll}</Link>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {randomized.map((c) => (
          <CountryCard key={c.code} c={c} t={t} lang={lang} />
        ))}
      </div>
    </section>
  );
}

function Hero({ lang }: { lang: string }) {
  const t = tFor(lang);
  return (
    <section className="pt-6 pb-4">
      <div className="rounded-3xl p-6 md:p-10 bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-neutral-900 dark:to-neutral-800 border border-gray-200 dark:border-gray-800">
        <h1 className="text-3xl md:text-5xl font-bold leading-tight">{t.hero.title}</h1>
        <p className="mt-3 text-gray-600 dark:text-gray-300 max-w-2xl">{t.hero.subtitle}</p>
        <div className="mt-6">
          <Link href={`/${lang}/pricing/#eu-featured`} className="inline-flex items-center gap-2 rounded-2xl px-5 py-3 bg-blue-600 text-white font-medium shadow hover:shadow-md">
            {t.cta.advertise}
            <svg className="size-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </Link>
        </div>
      </div>
    </section>
  );
}

function FeaturedEUGrid({ items, lang }: { items: any[]; lang: string }) {
  if (!items?.length) return null;
  return (
    <section className="mt-10">
      <SectionHeading>EU Featured</SectionHeading>
      <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {items.map((b) => (
          <Link href={`/${lang}/b/${b.slug}/`} key={b.id} className="group">
            <article className="rounded-2xl overflow-hidden border border-gray-200 dark:border-gray-800 bg-white/60 dark:bg-neutral-900/60 hover:shadow-md transition-shadow">
              {b.cover_url ? (
                // eslint-disable-next-line @next/next/no-img-element
                <img src={b.cover_url} alt={b.name} className="w-full h-40 object-cover" />
              ) : (
                <div className="w-full h-40 bg-gray-100 dark:bg-neutral-800" />
              )}
              <div className="p-4">
                <div className="flex items-center gap-2">
                  {b.logo_url ? (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img src={b.logo_url} alt="" className="w-8 h-8 rounded-md" />
                  ) : null}
                  <h3 className="font-semibold line-clamp-1">{b.name}</h3>
                </div>
                <p className="mt-1 text-sm text-gray-600 dark:text-gray-400 line-clamp-2">{b.short_desc}</p>
                <div className="mt-2 text-xs text-gray-500 dark:text-gray-400">{b.city} · {b.country_code}</div>
              </div>
            </article>
          </Link>
        ))}
      </div>
    </section>
  );
}

export async function generateMetadata({ params }: { params: { lang?: string } }): Promise<Metadata> {
  const lang = normalizeLang(params?.lang);
  const t = tFor(lang);
  return {
    title: t.seo.title,
    description: t.seo.description,
    alternates: { canonical: `/${lang}/eu/` },
    openGraph: { title: t.seo.title, description: t.seo.description },
    twitter: { card: 'summary_large_image' }
  };
}

export default async function Page({ params }: { params: { lang?: string } }) {
  const lang = normalizeLang(params?.lang);
  const t = tFor(lang);

  const featured = await fetchFeaturedEU(12);

  // JSON-LD (safe i18n access)
  const ld = {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    name: t.seo.title,
    hasPart: {
      '@type': 'ItemList',
      itemListElement: (featured || []).slice(0, 10).map((b: any, i: number) => ({
        '@type': 'ListItem', position: i + 1, url: `/${lang}/b/${b.slug}/`, name: b.name
      }))
    }
  };

  return (
    <main className="container mx-auto px-4 max-w-6xl py-4">
      <Hero lang={lang} />
      <TopCountries lang={lang} />
      <FeaturedEUGrid items={featured} lang={lang} />
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(ld) }} />
    </main>
  );
}

// -------------------------
// Lightweight test hooks (won't run in production)
// -------------------------
export function __test_normalizeLang(v?: string) { return normalizeLang(v); }
export function __test_tFor(v?: string) { return tFor(v); }

if (process.env.NODE_ENV === 'test') {
  console.assert(__test_normalizeLang('EN') === 'en', 'normalizeLang should lowercase and accept EN→en');
  console.assert(__test_normalizeLang('xx') === 'en', 'normalizeLang should fallback to en for unsupported');
  console.assert(__test_tFor('xx')?.seo?.title?.length > 0, 'tFor should fallback to EN dict');
}