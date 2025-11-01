import { searchBusinesses, generateHreflangLinks } from '@/lib/api';
import Listing from '@/components/Listing';

export const revalidate = 600;

interface PageProps {
  params: Promise<{
    lang: string;
    params: string[];
  }>;
}

export default async function BusinessCatchAllPage({ params }: PageProps) {
  const { lang, params: pathParams } = await params;
  
  // Parse the URL parameters
  // Format: [countryCode]/[citySlug]/[townSlug]/[categorySlug]
  // Or: [countryCode]/[citySlug]/[categorySlug]
  // Or: [countryCode]/[categorySlug]
  
  let countryCode = '';
  let citySlug = '';
  let townSlug = '';
  let categorySlug = '';
  
  if (pathParams.length >= 2) {
    countryCode = pathParams[0];
    if (pathParams.length === 2) {
      // [countryCode]/[categorySlug]
      categorySlug = pathParams[1];
    } else if (pathParams.length === 3) {
      // [countryCode]/[citySlug]/[categorySlug]
      citySlug = pathParams[1];
      categorySlug = pathParams[2];
    } else if (pathParams.length === 4) {
      // [countryCode]/[citySlug]/[townSlug]/[categorySlug]
      citySlug = pathParams[1];
      townSlug = pathParams[2];
      categorySlug = pathParams[3];
    }
  }
  
  const data = await searchBusinesses({
    category: categorySlug,
    country: countryCode,
    city: citySlug,
    town: townSlug,
    lang,
  });
  
  return <Listing data={data} lang={lang} />;
}