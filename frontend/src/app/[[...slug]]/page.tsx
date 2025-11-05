import { notFound } from 'next/navigation';
import type { Metadata } from 'next';
import { detectLangFromPath, findPageByPath, normalizePath } from '@/server/publicPages';

type Props = { params: { slug?: string[] } };

export const dynamic = 'force-dynamic';   // render at request time while we're on mock DB
export const revalidate = 0;

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const path = normalizePath(params.slug);
  const page = findPageByPath(path);
  if (!page) return {};

  const lang = detectLangFromPath(path);
  const seo = page.seo[lang];

  const robots = {
    index: !!seo.robotsIndex,
    follow: !!seo.robotsFollow
  } as const;

  return {
    title: seo.metaTitle || 'ListAcross EU — European Business Directory',
    description: seo.metaDescription || 'Discover and connect with businesses across the EU.',
    alternates: {
      canonical: (seo.canonicalUrl || 'https://listacross.eu') + (seo.slug || '')
    },
    robots,
    openGraph: {
      title: seo.socialTitle || seo.metaTitle || 'ListAcross EU — European Business Directory',
      description: seo.socialDescription || seo.metaDescription || '',
      url: (seo.canonicalUrl || 'https://listacross.eu') + (seo.slug || ''),
      siteName: 'ListAcross EU',
      images: seo.socialImageUrl ? [{ url: seo.socialImageUrl }] : undefined
    },
    // Optional: Twitter summary_large_image, etc.
  };
}

export default function PublicPage({ params }: Props) {
  const path = normalizePath(params.slug);
  const page = findPageByPath(path);
  if (!page) return notFound();

  const lang = detectLangFromPath(path);
  const seo = page.seo[lang];

  // TEMP content placeholder – later replace with your real content renderer
  return (
    <main className="p-6 space-y-4">
      <h1 className="text-2xl font-semibold">Public Page</h1>
      <div className="text-gray-600">Path: <code>{path}</code> | Language: <code>{lang}</code></div>

      <div className="bg-white rounded-2xl border border-gray-100 p-5">
        <div className="text-sm text-gray-600">
          This is a placeholder view for <b>{page.name}</b>. Hook in your real page/content here.
        </div>
        <div className="mt-3 text-sm">
          <div><b>Title:</b> {seo.metaTitle || '—'}</div>
          <div><b>Description:</b> {seo.metaDescription || '—'}</div>
          <div><b>Canonical:</b> {(seo.canonicalUrl || 'https://listacross.eu') + (seo.slug || '')}</div>
        </div>
      </div>
    </main>
  );
}