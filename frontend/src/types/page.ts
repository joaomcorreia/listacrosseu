import type { Lang, SeoByLang } from './seo';

export type PageType = 'static' | 'dynamic';

export type AdminPage = {
  id: string;            // uuid
  name: string;          // human label
  path: string;          // e.g. /about, /pt/porto
  type: PageType;
  langs: Lang[];         // which languages are active
  updatedAt: string;     // ISO
};

export type AdminPageWithSeo = AdminPage & {
  seo: SeoByLang;
};