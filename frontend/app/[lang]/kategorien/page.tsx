import { fetchCategories, generateHreflangLinks } from '@/lib/api';
import Listing from '@/components/Listing';
import { translate, Language, getCountryFromLanguage } from '@/lib/i18n';

export const revalidate = 600;

interface PageProps {
  params: Promise<{
    lang: string;
  }>;
}

export async function generateMetadata({ params }: PageProps) {
  const { lang } = await params;
  
  return {
    title: `${translate('categories.title', lang as Language)} - ListAcrossEU`,
    description: translate('categories.subtitle', lang as Language),
    alternates: {
      languages: generateHreflangLinks(`/categories`),
    },
  };
}

export default async function CategoriesPage({ params }: PageProps) {
  const { lang } = await params;
  
  const country = getCountryFromLanguage(lang as Language);
  const data = await fetchCategories(lang, country || undefined);
  
  // Generate JSON-LD structured data
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    name: 'Business Categories',
    description: 'Browse business categories across Europe',
    breadcrumb: {
      '@type': 'BreadcrumbList',
      itemListElement: data.breadcrumbs.map((crumb, index) => ({
        '@type': 'ListItem',
        position: index + 1,
        name: crumb.label,
        item: `${process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000'}${crumb.href}`,
      })),
    },
  };
  
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <Listing data={data} lang={lang} />
    </>
  );
}