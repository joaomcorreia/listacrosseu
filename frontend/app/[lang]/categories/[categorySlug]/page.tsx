import { fetchCategoryCountries, generateHreflangLinks } from '@/lib/api';
import Listing from '@/components/Listing';

export const revalidate = 600;

interface PageProps {
  params: Promise<{
    lang: string;
    categorySlug: string;
  }>;
}

export async function generateMetadata({ params }: PageProps) {
  const { lang, categorySlug } = await params;
  
  return {
    title: `${categorySlug} - Countries - ListAcrossEU`,
    description: `Find ${categorySlug} businesses across European countries`,
    alternates: {
      languages: generateHreflangLinks(`/categories/${categorySlug}`),
    },
  };
}

export default async function CategoryCountriesPage({ params }: PageProps) {
  const { lang, categorySlug } = await params;
  
  const data = await fetchCategoryCountries(categorySlug, lang);
  
  // Generate JSON-LD structured data
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    name: `${categorySlug} - Countries`,
    description: `Find ${categorySlug} businesses across European countries`,
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