import { getPage } from '@/server/mockDb';
import { listPages } from '@/server/mockDb';
import type { AdminPageWithSeo } from '@/types/page';
import type { Lang } from '@/types/seo';

export function normalizePath(segments: string[] | undefined): string {
  if (!segments || segments.length === 0) return '/';
  let p = '/' + segments.join('/').replace(/\/+/g, '/');
  if (p !== '/' && p.endsWith('/')) p = p.slice(0, -1);
  return p;
}

export function detectLangFromPath(path: string): Lang {
  const first = path.split('/').filter(Boolean)[0]?.toLowerCase();
  switch (first) {
    case 'nl': return 'NL';
    case 'pt': return 'PT';
    case 'fr': return 'FR';
    case 'de': return 'DE';
    case 'es': return 'ES';
    default:   return 'EN';
  }
}

// NOTE: for now we search by path in the mock DB.
// Later, replace with a direct DB/DRF call.
export function findPageByPath(path: string): AdminPageWithSeo | undefined {
  const all = listPages(); // returns AdminPage[]; we need seo → use getPage per id
  // List is AdminPage[], fetch full with seo when match
  const hit = all.find(p => p.path === path);
  if (!hit) return undefined;
  return getPage(hit.id) as AdminPageWithSeo | undefined;
}