import Head from 'next/head';
import { SeoPage, buildMetaTags, getStructuredData } from '../../lib/seoApi';

interface SeoHeadProps {
  seoPage: SeoPage;
}

/**
 * SEO Head component that renders meta tags, canonical links, and structured data
 * based on the SEO page data and plan restrictions
 */
export default function SeoHead({ seoPage }: SeoHeadProps) {
  const metaTags = buildMetaTags(seoPage);
  const structuredData = getStructuredData(seoPage);

  return (
    <Head>
      {/* Basic meta tags (all plans) */}
      <title>{metaTags.title}</title>
      <meta name="description" content={metaTags.description} />
      <meta name="robots" content={metaTags.robots} />
      
      {metaTags.canonical && (
        <link rel="canonical" href={metaTags.canonical} />
      )}
      
      {seoPage.image_alt_fallback && (
        <meta name="image_alt" content={seoPage.image_alt_fallback} />
      )}

      {/* Growth plan features: Open Graph and Twitter Cards */}
      {seoPage.can_use_growth_features && (
        <>
          {metaTags['og:title'] && (
            <meta property="og:title" content={metaTags['og:title']} />
          )}
          {metaTags['og:description'] && (
            <meta property="og:description" content={metaTags['og:description']} />
          )}
          {metaTags['og:image'] && (
            <meta property="og:image" content={metaTags['og:image']} />
          )}
          <meta property="og:type" content="website" />
          <meta property="og:url" content={seoPage.canonical_url} />
          
          {metaTags['twitter:card'] && (
            <meta name="twitter:card" content={metaTags['twitter:card']} />
          )}
          {metaTags['twitter:image'] && (
            <meta name="twitter:image" content={metaTags['twitter:image']} />
          )}
        </>
      )}

      {/* Premium plan features: JSON-LD structured data */}
      {seoPage.can_use_premium_features && structuredData && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
        />
      )}
      
      {/* Viewport and other standard meta tags */}
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <meta httpEquiv="X-UA-Compatible" content="IE=edge" />
    </Head>
  );
}