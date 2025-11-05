export type Lang = 'NL'|'PT'|'EN'|'FR'|'DE'|'ES';

export type SeoState = {
  metaTitle: string;
  metaDescription: string;
  canonicalUrl: string;
  focusKeywords: string;    // comma separated
  slug: string;
  socialTitle: string;
  socialDescription: string;
  socialImageUrl: string;
  robotsIndex: boolean;
  robotsFollow: boolean;
};

export type SeoByLang = Record<Lang, SeoState>;

export const DEFAULT_LANGS: Lang[] = ['NL','PT','EN','FR','DE','ES'];

export const EMPTY_SEO: SeoState = {
  metaTitle: '',
  metaDescription: '',
  canonicalUrl: 'https://listacross.eu',
  focusKeywords: 'business directory, european companies, eu marketplace',
  slug: '',
  socialTitle: '',
  socialDescription: '',
  socialImageUrl: 'https://listacross.eu/images/social-share.jpg',
  robotsIndex: true,
  robotsFollow: true
};