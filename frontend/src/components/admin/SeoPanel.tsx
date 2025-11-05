'use client';
import React, { useMemo, useState } from 'react';
import { DEFAULT_LANGS, type Lang, type SeoByLang, type SeoState } from '@/types/seo';

type Capabilities = {
  title?: boolean;
  description?: boolean;
  canonical?: boolean;
  slug?: boolean;
  keywords?: boolean;
  robots?: boolean;
  social?: boolean;
  jsonldPreview?: boolean;
};

type Props = {
  langs?: Lang[];
  valueByLang: SeoByLang;
  onChange: (next: SeoByLang) => void;
  baseUrl?: string;                // preview base url
  capabilities?: Capabilities;     // plan gating
};

const CAPS_DEFAULT: Required<Capabilities> = {
  title: true,
  description: true,
  canonical: true,
  slug: true,
  keywords: true,
  robots: true,
  social: true,
  jsonldPreview: true
};

// ---- helpers ----
function kwArray(input: string) {
  return input.split(',').map(s => s.trim()).filter(Boolean);
}
function estimateTitlePixels(title: string) {
  let px = 0;
  for (const ch of title) {
    if (/[A-ZW@#&%]/.test(ch)) px += 9;
    else if (/[il\'`\s.,:;|]/.test(ch)) px += 5;
    else px += 7;
  }
  return px;
}
function clampSerpTitle(title: string) {
  const limitPx = 580;
  let px = 0, out = '';
  for (const ch of title) {
    const add = /[A-ZW@#&%]/.test(ch) ? 9 : /[il\'`\s.,:;|]/.test(ch) ? 5 : 7;
    if (px + add > limitPx) break;
    px += add; out += ch;
  }
  return out;
}
function highlightKeywords(text: string, keywords: string[]) {
  if (!text) return text;
  let out = text;
  keywords.forEach((kw) => {
    const re = new RegExp(`(${kw.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&')})`, 'gi');
    out = out.replace(re, '<b>$1</b>');
  });
  return out;
}

export default function SeoPanel({
  langs = DEFAULT_LANGS,
  valueByLang,
  onChange,
  baseUrl = 'https://listacross.eu',
  capabilities
}: Props) {
  const caps = { ...CAPS_DEFAULT, ...(capabilities || {}) };
  const [activeLang, setActiveLang] = useState<Lang>(langs.includes('EN' as Lang) ? 'EN' : langs[0]);

  const s = valueByLang[activeLang];

  function update<K extends keyof SeoState>(key: K, val: SeoState[K]) {
    onChange({ ...valueByLang, [activeLang]: { ...s, [key]: val } });
  }

  const fullUrl = useMemo(() => {
    const slug = s.slug ? (s.slug.startsWith('/') ? s.slug : `/${s.slug}`) : '';
    return `${s.canonicalUrl || baseUrl}${slug}`.replace(/(?<!:)\/*\/+/g, '/');
  }, [s.canonicalUrl, s.slug, baseUrl]);

  const keywords = useMemo(() => kwArray(s.focusKeywords), [s.focusKeywords]);

  const titlePx = estimateTitlePixels(s.metaTitle);
  const clamped = clampSerpTitle(s.metaTitle);
  const titleTrimmed = s.metaTitle !== clamped ? `${clamped}…` : s.metaTitle;

  const jsonLd = useMemo(() => {
    const obj = {
      '@context': 'https://schema.org',
      '@type': 'WebPage',
      inLanguage: activeLang.toLowerCase(),
      url: fullUrl,
      name: s.metaTitle || '',
      description: s.metaDescription || '',
      isPartOf: {
        '@type': 'WebSite',
        name: 'ListAcross EU',
        url: 'https://listacross.eu'
      }
    };
    return JSON.stringify(obj, null, 2);
  }, [activeLang, fullUrl, s.metaTitle, s.metaDescription]);

  return (
    <div className="space-y-6">
      {/* Tabs */}
      <div className="flex items-center justify-between">
        <div className="flex gap-2 flex-wrap">
          {langs.map((l) => (
            <button key={l}
              onClick={() => setActiveLang(l)}
              className={`px-3 py-1 rounded-full text-sm border ${l === activeLang ? 'bg-blue-600 text-white border-blue-600' : 'bg-white text-gray-700 border-gray-300'}`}>
              {l}
            </button>
          ))}
        </div>
      </div>

      {/* Top row: Settings + Social */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white shadow-sm rounded-2xl p-5 border border-gray-100">
          <h3 className="text-lg font-semibold mb-4">SEO Settings</h3>

          {caps.title && (
            <>
              <label className="block text-sm font-medium">Meta Title</label>
              <input className="mt-1 mb-1 w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                     value={s.metaTitle} onChange={e=>update('metaTitle', e.target.value)} placeholder="Page title for search engines" maxLength={120}/>
              <div className="flex items-center justify-between text-xs text-gray-500 mb-3">
                <span>Chars: {s.metaTitle.length}/120</span>
                <span>≈ {titlePx}px (target ≤ 580px)</span>
              </div>
            </>
          )}

          {caps.description && (
            <>
              <label className="block text-sm font-medium">Meta Description</label>
              <textarea className="mt-1 w-full rounded-xl border border-gray-300 px-3 py-2 h-24 resize-y focus:outline-none focus:ring-2 focus:ring-blue-500"
                        value={s.metaDescription} onChange={e=>update('metaDescription', e.target.value)} placeholder="Brief description for search results" maxLength={300}/>
              <div className="text-xs text-gray-500 mb-3">Chars: {s.metaDescription.length}/300 (ideal ≤ 160)</div>
            </>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {caps.canonical && (
              <div>
                <label className="block text-sm font-medium">Canonical URL</label>
                <input className="mt-1 w-full rounded-xl border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                       value={s.canonicalUrl} onChange={e=>update('canonicalUrl', e.target.value)} placeholder={baseUrl}/>
              </div>
            )}
            {caps.slug && (
              <div>
                <label className="block text-sm font-medium">Slug</label>
                <input className="mt-1 w-full rounded-xl border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                       value={s.slug} onChange={e=>update('slug', e.target.value.replace(/\s/g, '-'))} placeholder="e.g. /pt/porto/carpinteiros"/>
              </div>
            )}
          </div>

          {caps.keywords && (
            <>
              <label className="block text-sm font-medium mt-3">Focus Keywords</label>
              <input className="mt-1 w-full rounded-xl border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                     value={s.focusKeywords} onChange={e=>update('focusKeywords', e.target.value)} placeholder="Separate keywords with commas"/>
              <p className="text-xs text-gray-500 mt-1">We check keywords in title & description.</p>
            </>
          )}

          {caps.robots && (
            <div className="mt-4 flex items-center gap-4 text-sm">
              <label className="inline-flex items-center gap-2">
                <input type="checkbox" checked={s.robotsIndex} onChange={e=>update('robotsIndex', e.target.checked)} />
                <span>Allow indexing</span>
              </label>
              <label className="inline-flex items-center gap-2">
                <input type="checkbox" checked={s.robotsFollow} onChange={e=>update('robotsFollow', e.target.checked)} />
                <span>Allow following links</span>
              </label>
            </div>
          )}
        </div>

        {caps.social && (
          <div className="bg-white shadow-sm rounded-2xl p-5 border border-gray-100">
            <h3 className="text-lg font-semibold mb-4">Social Media (Open Graph)</h3>

            <label className="block text-sm font-medium">Social Title</label>
            <input className="mt-1 mb-1 w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                   value={s.socialTitle} onChange={e=>update('socialTitle', e.target.value)} placeholder="Title when shared on social media" maxLength={120}/>
            <div className="text-xs text-gray-500 mb-2">Chars: {s.socialTitle.length}/120</div>

            <label className="block text-sm font-medium">Social Description</label>
            <textarea className="mt-1 w-full rounded-xl border border-gray-300 px-3 py-2 h-24 resize-y focus:outline-none focus:ring-2 focus:ring-blue-500"
                      value={s.socialDescription} onChange={e=>update('socialDescription', e.target.value)} placeholder="Description when shared" maxLength={300}/>
            <div className="text-xs text-gray-500 mb-2">Chars: {s.socialDescription.length}/300</div>

            <label className="block text-sm font-medium">Social Image URL</label>
            <input className="mt-1 w-full rounded-xl border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                   value={s.socialImageUrl} onChange={e=>update('socialImageUrl', e.target.value)} placeholder="https://listacross.eu/images/social-share.jpg"/>
            <p className="text-xs text-gray-500 mt-1">Recommended: 1200×630px</p>

            <div className="mt-3 border rounded-xl overflow-hidden">
              <div className="w-full h-40 bg-gray-100 flex items-center justify-center">
                {s.socialImageUrl ? (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img src={s.socialImageUrl} alt="Social preview" className="h-40 w-full object-cover" />
                ) : (
                  <div className="text-gray-400">Social Image Preview</div>
                )}
              </div>
              <div className="p-3">
                <div className="text-[10px] uppercase tracking-wide text-gray-500">{new URL((s.canonicalUrl||baseUrl)).hostname.toUpperCase()}</div>
                <div className="text-base font-semibold leading-tight">{s.socialTitle || s.metaTitle || 'ListAcross EU — European Business Directory'}</div>
                <div className="text-sm text-gray-600 line-clamp-2">{s.socialDescription || s.metaDescription}</div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Full width previews */}
      <div className="bg-white shadow-sm rounded-2xl p-5 border border-gray-100">
        <h3 className="text-lg font-semibold mb-4">Live Preview</h3>

        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
          {/* Google preview */}
          <div className="border rounded-2xl p-4">
            <div className="text-sm font-semibold mb-2">Google Search Result</div>
            <div className="space-y-1">
              <div className="text-[#1a0dab] text-xl leading-snug">{titleTrimmed || 'ListAcross EU — European Business Directory'}</div>
              <div className="text-[#006621] text-sm">{fullUrl}</div>
              <div className="text-[#4d5156] text-sm" dangerouslySetInnerHTML={{
                __html: highlightKeywords(s.metaDescription || 'Discover and connect with businesses across the EU.', keywords)
              }} />
            </div>
            <div className="mt-3 flex items-center gap-2 text-xs text-gray-500">
              <span className={`${titlePx <= 600 ? 'text-green-600' : 'text-red-600'}`}>Title width ≈ {titlePx}px</span>
              <span>•</span>
              <span className={`${s.metaDescription.length <= 160 ? 'text-green-600' : 'text-red-600'}`}>Description {s.metaDescription.length}/160</span>
            </div>
          </div>

          {/* Bing preview */}
          <div className="border rounded-2xl p-4">
            <div className="text-sm font-semibold mb-2">Bing Search Result</div>
            <div className="space-y-1">
              <div className="text-[#234] text-xl font-medium leading-snug">{titleTrimmed || 'ListAcross EU — European Business Directory'}</div>
              <div className="text-[#0b7a0b] text-sm">{fullUrl}</div>
              <div className="text-[#333] text-sm" dangerouslySetInnerHTML={{
                __html: highlightKeywords(s.metaDescription || 'Discover and connect with businesses across the EU.', keywords)
              }} />
            </div>
          </div>
        </div>

        {/* JSON-LD */}
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 mt-6">
          <div className="border rounded-2xl p-4">
            <div className="text-sm font-semibold mb-2">Robots & Canonicals</div>
            <div className="text-sm space-y-2">
              <div><span className="font-medium">robots</span>: <code className="ml-2 rounded bg-gray-100 px-2 py-1">{`${s.robotsIndex ? 'index':'noindex'}, ${s.robotsFollow ? 'follow':'nofollow'}`}</code></div>
              <div><span className="font-medium">canonical</span>: <code className="ml-2 rounded bg-gray-100 px-2 py-1">{fullUrl}</code></div>
              <div><span className="font-medium">keywords</span>: <code className="ml-2 rounded bg-gray-100 px-2 py-1">{kwArray(s.focusKeywords).join(', ') || '–'}</code></div>
            </div>
          </div>
          <div className="border rounded-2xl p-4">
            <div className="text-sm font-semibold mb-2">JSON-LD Preview (WebPage)</div>
            <textarea className="w-full h-48 rounded-xl border border-gray-300 p-3 font-mono text-xs" readOnly value={jsonLd}/>
            <div className="text-xs text-gray-500 mt-1">Server will emit this in &lt;head&gt;.</div>
          </div>
        </div>
      </div>
    </div>
  );
}