import { v4 as uuid } from 'uuid';
import { DEFAULT_LANGS, EMPTY_SEO, type Lang, type SeoByLang } from '@/types/seo';
import type { AdminPage, AdminPageWithSeo } from '@/types/page';
import type { Listing, ClaimSubmission, UpgradeSubmission } from '@/types/listing';

const db = {
  pages: [] as AdminPageWithSeo[]
};

// seed sample pages if empty
if (db.pages.length === 0) {
  // Homepage
  const homepageId = uuid();
  const homepageSeo: SeoByLang = Object.fromEntries(DEFAULT_LANGS.map(l => [l, { 
    ...EMPTY_SEO,
    metaTitle: l === 'EN' ? 'ListAcross EU — European Business Directory' : 
               l === 'FR' ? 'ListAcross EU — Annuaire Européen des Entreprises' :
               l === 'NL' ? 'ListAcross EU — Europees Bedrijfsgids' :
               l === 'PT' ? 'ListAcross EU — Diretório de Negócios Europeu' :
               l === 'DE' ? 'ListAcross EU — Europäisches Firmenverzeichnis' :
               l === 'ES' ? 'ListAcross EU — Directorio Europeo de Empresas' : 'ListAcross EU',
    metaDescription: l === 'EN' ? 'Discover and connect with businesses across the EU. Find services, companies, and professionals in all European countries.' :
                     l === 'FR' ? 'Découvrez et connectez avec des entreprises à travers l\'UE. Trouvez des services, entreprises et professionnels.' :
                     'European business directory for all countries.',
    slug: l === 'EN' ? '' : `/${l.toLowerCase()}`,
    focusKeywords: 'business directory, european companies, eu marketplace, business search'
  }])) as SeoByLang;
  
  db.pages.push({
    id: homepageId,
    name: 'Homepage',
    path: '/',
    type: 'static',
    langs: DEFAULT_LANGS,
    updatedAt: new Date().toISOString(),
    seo: homepageSeo
  });

  // About page
  const aboutId = uuid();
  const aboutSeo: SeoByLang = Object.fromEntries(DEFAULT_LANGS.map(l => [l, {
    ...EMPTY_SEO,
    metaTitle: l === 'EN' ? 'About Us — ListAcross EU' :
               l === 'FR' ? 'À Propos — ListAcross EU' :
               l === 'NL' ? 'Over Ons — ListAcross EU' :
               l === 'PT' ? 'Sobre Nós — ListAcross EU' :
               l === 'DE' ? 'Über Uns — ListAcross EU' :
               l === 'ES' ? 'Acerca de — ListAcross EU' : 'About — ListAcross EU',
    metaDescription: l === 'EN' ? 'Learn about ListAcross EU, the premier European business directory connecting companies across all EU member states.' :
                     l === 'FR' ? 'Découvrez ListAcross EU, le premier annuaire européen connectant les entreprises de tous les états membres.' :
                     'European business directory information and mission.',
    slug: '/about',
    focusKeywords: 'about listacross, european business directory, company information'
  }])) as SeoByLang;

  db.pages.push({
    id: aboutId,
    name: 'About Us',
    path: '/about',
    type: 'static',
    langs: DEFAULT_LANGS,
    updatedAt: new Date().toISOString(),
    seo: aboutSeo
  });

  // Portuguese cities page
  const portugalId = uuid();
  const portugalSeo: SeoByLang = Object.fromEntries(DEFAULT_LANGS.map(l => [l, {
    ...EMPTY_SEO,
    metaTitle: l === 'PT' ? 'Portugal — Empresas e Serviços por Cidade' :
               l === 'EN' ? 'Portugal — Businesses by City' :
               l === 'FR' ? 'Portugal — Entreprises par Ville' :
               l === 'NL' ? 'Portugal — Bedrijven per Stad' :
               l === 'DE' ? 'Portugal — Unternehmen nach Stadt' :
               l === 'ES' ? 'Portugal — Empresas por Ciudad' : 'Portugal Business Directory',
    metaDescription: l === 'PT' ? 'Encontre empresas e serviços em Portugal. Diretório completo de negócios por cidade: Lisboa, Porto, Coimbra e mais.' :
                     l === 'EN' ? 'Find businesses and services in Portugal. Complete directory by city: Lisbon, Porto, Coimbra and more.' :
                     'Portuguese business directory by city and region.',
    slug: l === 'PT' ? '/pt/portugal' : `/${l.toLowerCase()}/portugal`,
    focusKeywords: 'portugal businesses, portuguese companies, lisboa porto, portugal directory'
  }])) as SeoByLang;

  db.pages.push({
    id: portugalId,
    name: 'Portugal Cities',
    path: '/pt/portugal',
    type: 'dynamic',
    langs: DEFAULT_LANGS,
    updatedAt: new Date().toISOString(),
    seo: portugalSeo
  });

  // How it Works pages for each language
  const howItWorksPages = [
    { path: '/en/how-it-works', name: 'How it works' },
    { path: '/nl/hoe-het-werkt', name: 'Hoe het werkt' },
    { path: '/pt/como-funciona', name: 'Como funciona' },
    { path: '/fr/comment-ca-marche', name: 'Comment ça marche' },
    { path: '/de/wie-es-funktioniert', name: 'So funktioniert es' },
    { path: '/es/como-funciona', name: 'Cómo funciona' }
  ];

  howItWorksPages.forEach(page => {
    const howItWorksId = uuid();
    const howItWorksSeo: SeoByLang = Object.fromEntries(DEFAULT_LANGS.map(l => [l, {
      ...EMPTY_SEO,
      metaTitle: l === 'EN' ? 'How ListAcross EU Works — Get Listed Today' :
                 l === 'FR' ? 'Comment ça marche — ListAcross EU' :
                 l === 'NL' ? 'Hoe het werkt — ListAcross EU' :
                 l === 'PT' ? 'Como funciona — ListAcross EU' :
                 l === 'DE' ? 'So funktioniert ListAcross EU — Jetzt listen' :
                 l === 'ES' ? 'Cómo funciona ListAcross EU — Regístrate hoy' : 'How it works — ListAcross EU',
      metaDescription: l === 'EN' ? 'Learn how ListAcross EU works. Create your business listing, optimize with live SEO previews, and get discovered across Europe.' :
                       l === 'FR' ? 'Découvrez comment ListAcross EU fonctionne. Créez votre fiche entreprise, optimisez avec des aperçus SEO en direct.' :
                       l === 'NL' ? 'Ontdek hoe ListAcross EU werkt. Maak je bedrijfsvermelding, optimaliseer met live SEO-voorbeelden, word gevonden.' :
                       l === 'PT' ? 'Saiba como funciona ListAcross EU. Crie sua listagem, otimize com pré-visualizações SEO, seja encontrado na Europa.' :
                       l === 'DE' ? 'Erfahren Sie, wie ListAcross EU funktioniert. Erstellen Sie Ihren Eintrag, optimieren Sie mit Live-SEO-Vorschau.' :
                       l === 'ES' ? 'Aprende cómo funciona ListAcross EU. Crea tu listado, optimiza con vistas SEO, te encuentran en Europa.' :
                       'How ListAcross EU works and how to get listed.',
      slug: page.path,
      focusKeywords: 'how it works, business listing, european directory, seo optimization, get discovered'
    }])) as SeoByLang;

    db.pages.push({
      id: howItWorksId,
      name: page.name,
      path: page.path,
      type: 'static',
      langs: DEFAULT_LANGS,
      updatedAt: new Date().toISOString(),
      seo: howItWorksSeo
    });
  });
}

export function listPages(): AdminPage[] {
  return db.pages.map(({ seo, ...rest }) => rest);
}

export function getPage(id: string): AdminPageWithSeo | undefined {
  return db.pages.find(p => p.id === id);
}

export function createPage(input: Pick<AdminPage, 'name'|'path'|'type'|'langs'>): AdminPageWithSeo {
  const id = uuid();
  const seo: SeoByLang = Object.fromEntries((input.langs || DEFAULT_LANGS).map(l => [l, { ...EMPTY_SEO }])) as SeoByLang;
  const page: AdminPageWithSeo = {
    id,
    name: input.name,
    path: input.path,
    type: input.type,
    langs: input.langs || DEFAULT_LANGS,
    updatedAt: new Date().toISOString(),
    seo
  };
  db.pages.push(page);
  return page;
}

export function updatePage(id: string, patch: Partial<AdminPage>): AdminPageWithSeo | undefined {
  const p = db.pages.find(x => x.id === id);
  if (!p) return;
  Object.assign(p, patch);
  p.updatedAt = new Date().toISOString();
  return p;
}

export function getSeo(id: string): SeoByLang | undefined {
  return db.pages.find(p => p.id === id)?.seo;
}

export function putSeo(id: string, next: SeoByLang): AdminPageWithSeo | undefined {
  const p = db.pages.find(x => x.id === id);
  if (!p) return;
  p.seo = next;
  p.updatedAt = new Date().toISOString();
  return p;
}

// Forms storage
const forms = {
  freeSubmissions: [] as Listing[],
  claimSubmissions: [] as ClaimSubmission[],
  upgradeSubmissions: [] as UpgradeSubmission[]
};

// Site settings storage
interface SiteSettings {
  logo?: string;
  favicon?: string;
  footerLogo?: string;
}

const siteSettings: SiteSettings = {
  logo: undefined,
  favicon: undefined,
  footerLogo: undefined
};

export function saveFreeListing(l: Listing) {
  forms.freeSubmissions.push(l);
  return l;
}
export function saveClaim(c: ClaimSubmission) {
  forms.claimSubmissions.push(c);
  return c;
}
export function saveUpgrade(u: UpgradeSubmission) {
  forms.upgradeSubmissions.push(u);
  return u;
}

// Site settings functions
export function getSiteSettings() {
  return { ...siteSettings };
}

export function updateSiteSettings(updates: Partial<SiteSettings>) {
  Object.assign(siteSettings, updates);
  return { ...siteSettings };
}