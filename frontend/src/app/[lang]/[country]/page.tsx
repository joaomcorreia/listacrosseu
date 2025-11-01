import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { fetchSeoPage } from '../../../lib/seoApi';
import Breadcrumbs from '../../../components/seo/Breadcrumbs';

interface CountryPageProps {
  params: {
    lang: string;
    country: string;
  };
}

export async function generateMetadata({ params }: CountryPageProps): Promise<Metadata> {
  const seoPage = await fetchSeoPage({
    lang: params.lang,
    country: params.country,
    type: 'country'
  });

  if (!seoPage) {
    return {
      title: `${params.country.toUpperCase()} - ListAcross EU`,
      description: `Discover businesses and services in ${params.country.toUpperCase()}`,
    };
  }

  const metadata: Metadata = {
    title: seoPage.meta_title,
    description: seoPage.meta_description,
    robots: seoPage.robots,
  };

  if (seoPage.canonical_url) {
    metadata.alternates = { canonical: seoPage.canonical_url };
  }

  if (seoPage.can_use_growth_features) {
    metadata.openGraph = {
      title: seoPage.og_title || seoPage.meta_title,
      description: seoPage.og_description || seoPage.meta_description,
      type: 'website',
      url: seoPage.canonical_url,
    };

    if (seoPage.og_image_url) {
      metadata.openGraph.images = [seoPage.og_image_url];
    }
  }

  return metadata;
}

export default async function CountryPage({ params }: CountryPageProps) {
  const seoPage = await fetchSeoPage({
    lang: params.lang,
    country: params.country,
    type: 'country'
  });

  if (!seoPage) {
    notFound();
  }

  return (
    <main className="country-page">
      <Breadcrumbs seoPage={seoPage} />
      
      <header>
        <h1>{seoPage.h1}</h1>
        {seoPage.h2 && <h2>{seoPage.h2}</h2>}
      </header>

      <div className="content">
        <p>{seoPage.meta_description}</p>
        
        {seoPage.content_blocks?.map((block: any) => (
          <div key={block.id} className={`content-block content-block-${block.key}`}>
            <div dangerouslySetInnerHTML={{ __html: block.content }} />
          </div>
        ))}
      </div>
    </main>
  );
}