import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { fetchSeoPage } from '../../lib/seoApi';
import SeoHead from '../../components/seo/SeoHead';
import Breadcrumbs from '../../components/seo/Breadcrumbs';

interface LangPageProps {
  params: {
    lang: string;
  };
}

// Generate metadata for SEO
export async function generateMetadata({ params }: LangPageProps): Promise<Metadata> {
  const seoPage = await fetchSeoPage({
    lang: params.lang,
    type: 'home'
  });

  if (!seoPage) {
    return {
      title: 'Page Not Found',
      description: 'The requested page could not be found.',
    };
  }

  const metadata: Metadata = {
    title: seoPage.meta_title,
    description: seoPage.meta_description,
    robots: seoPage.robots,
  };

  if (seoPage.canonical_url) {
    metadata.alternates = {
      canonical: seoPage.canonical_url
    };
  }

  // Growth plan Open Graph
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

    metadata.twitter = {
      card: (seoPage.twitter_card as any) || 'summary',
      title: seoPage.og_title || seoPage.meta_title,
      description: seoPage.og_description || seoPage.meta_description,
    };

    if (seoPage.twitter_image_url) {
      metadata.twitter.images = [seoPage.twitter_image_url];
    }
  }

  return metadata;
}

export default async function LangPage({ params }: LangPageProps) {
  const seoPage = await fetchSeoPage({
    lang: params.lang,
    type: 'home'
  });

  if (!seoPage) {
    notFound();
  }

  // Parse JSON-LD for Premium users
  let structuredData = null;
  if (seoPage.can_use_premium_features && seoPage.json_ld) {
    try {
      structuredData = JSON.parse(seoPage.json_ld);
    } catch (error) {
      console.error('Invalid JSON-LD:', error);
    }
  }

  return (
    <main className="seo-page">
      <Breadcrumbs seoPage={seoPage} />
      
      <header>
        <h1>{seoPage.h1}</h1>
        {seoPage.h2 && <h2>{seoPage.h2}</h2>}
      </header>

      <div className="content">
        <p>{seoPage.meta_description}</p>
        
        {/* Render content blocks if available */}
        {seoPage.content_blocks?.map((block) => (
          <div key={block.id} className={`content-block content-block-${block.key}`}>
            <div dangerouslySetInnerHTML={{ __html: block.content }} />
          </div>
        ))}
        
        {/* Growth plan internal links */}
        {seoPage.can_use_growth_features && seoPage.internal_links && seoPage.internal_links.length > 0 && (
          <nav className="internal-links">
            <h3>Related Pages</h3>
            <ul>
              {seoPage.internal_links.map((link, index) => (
                <li key={index}>
                  <a href={link.href}>{link.title}</a>
                </li>
              ))}
            </ul>
          </nav>
        )}
      </div>

      {/* Premium plan JSON-LD structured data */}
      {structuredData && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
        />
      )}

      <style jsx>{`
        .seo-page {
          max-width: 1200px;
          margin: 0 auto;
          padding: 2rem;
        }
        header {
          margin-bottom: 2rem;
        }
        h1 {
          font-size: 2.5rem;
          font-weight: bold;
          color: #1f2937;
          margin-bottom: 1rem;
        }
        h2 {
          font-size: 1.5rem;
          color: #4b5563;
          margin-bottom: 1rem;
        }
        .content {
          line-height: 1.6;
          color: #374151;
        }
        .content-block {
          margin-bottom: 2rem;
        }
        .internal-links {
          margin-top: 2rem;
          padding: 1rem;
          background: #f9fafb;
          border-radius: 8px;
        }
        .internal-links h3 {
          margin-bottom: 1rem;
          color: #1f2937;
        }
        .internal-links ul {
          list-style: none;
          padding: 0;
        }
        .internal-links li {
          margin-bottom: 0.5rem;
        }
        .internal-links a {
          color: #2563eb;
          text-decoration: none;
          transition: color 0.2s;
        }
        .internal-links a:hover {
          color: #1d4ed8;
          text-decoration: underline;
        }
      `}</style>
    </main>
  );
}