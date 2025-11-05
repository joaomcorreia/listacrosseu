export type Lang = 'NL'|'PT'|'EN'|'FR'|'DE'|'ES';
type T = {
  heroTitle: string;
  heroSubtitle: string;
  ctaStartFree: string;
  step1Title: string; step1Body: string;
  step2Title: string; step2Body: string;
  step3Title: string; step3Body: string;
  plansTitle: string;
  planFree: { title: string; bullets: string[] };
  planPaid: { title: string; bullets: string[] };
  planPremium: { title: string; bullets: string[] };
  seoTipsTitle: string; seoTipsItems: string[];
  faqTitle: string; faq: { q: string; a: string }[];
  finalCtaTitle: string; finalCtaBody: string; finalCtaButton: string;
  navLabel: string;          // label for main nav link
  slug: string;              // localized slug (without leading /)
};

export const HOW_SLUGS: Record<Lang,string> = {
  EN: 'how-it-works',
  NL: 'hoe-het-werkt',
  PT: 'como-funciona',
  FR: 'comment-ca-marche',
  DE: 'wie-es-funktioniert',
  ES: 'como-funciona'
};

const base = {
  planFree: { title: 'Free', bullets: [
    'Create a basic listing',
    'Appear in country/category pages',
    'Starter SEO (title & description)'
  ]},
  planPaid: { title: 'Growth', bullets: [
    'Featured placement in country/city',
    'Enhanced SEO (canonical, robots, social)',
    'Claim & verify your business'
  ]},
  planPremium: { title: 'Premium', bullets: [
    'EU-wide exposure options',
    'Full multilingual SEO (6 languages)',
    'Advanced schema (LocalBusiness, Services)'
  ]},
  seoTipsTitle: 'Smart SEO & Preview',
  seoTipsItems: [
    'Live preview for Google/Bing and social sharing',
    'Yoast-like counters for title pixels & description length',
    'Per-page, per-language controls (titles, slugs, canonicals)',
  ]
};

export const HOW: Record<Lang, T> = {
  EN: {
    heroTitle: 'How ListAcross EU Works',
    heroSubtitle: 'Publish your business once. Reach customers across Europe with multilingual SEO.',
    ctaStartFree: 'Start free',
    step1Title: '1) Create or claim your page',
    step1Body: 'Sign up and add your business. Import basic info, then claim to unlock verification and upgrades.',
    step2Title: '2) Optimize with live previews',
    step2Body: 'Tweak titles, descriptions, and social share cards with instant Google/Bing previews—per language.',
    step3Title: '3) Get discovered',
    step3Body: 'Your listing appears on country, city, and category pages. Upgrade for featured placement and EU-wide reach.',
    plansTitle: 'Plans overview',
    ...base,
    faqTitle: 'Frequently asked questions',
    faq: [
      { q: 'Can I start for free?', a: 'Yes. Create a basic listing and upgrade later when you need more reach.' },
      { q: 'How do languages work?', a: 'You can manage SEO per language. Premium unlocks all 6 languages at once.' },
      { q: 'Can I edit SEO for each page?', a: 'Yes—every page has its own SEO panel (title, description, slug, canonical, robots, OG).' }
    ],
    finalCtaTitle: 'Ready to get listed?',
    finalCtaBody: 'Create your listing in minutes and start appearing in local searches across the EU.',
    finalCtaButton: 'Create my listing',
    navLabel: 'How it works',
    slug: HOW_SLUGS.EN
  },
  NL: {
    heroTitle: 'Hoe werkt ListAcross EU',
    heroSubtitle: 'Publiceer je bedrijf een keer. Bereik klanten in heel Europa met meertalige SEO.',
    ctaStartFree: 'Start gratis',
    step1Title: '1) Maak of claim je pagina',
    step1Body: 'Registreer en voeg je bedrijf toe. Importeer basisinformatie en claim voor verificatie en upgrades.',
    step2Title: '2) Optimaliseer met live previews',
    step2Body: 'Pas titels, beschrijvingen en social cards aan met directe Google/Bing-voorbeelden per taal.',
    step3Title: '3) Word gevonden',
    step3Body: 'Je vermelding verschijnt op land-, stad- en categoriepaginas. Upgrade voor uitgelichte posities en EU-bereik.',
    plansTitle: 'Pakketten in het kort',
    ...base,
    faqTitle: 'Veelgestelde vragen',
    faq: [
      { q: 'Kan ik gratis beginnen?', a: 'Ja. Maak een basisvermelding en upgrade later voor meer bereik.' },
      { q: 'Hoe werken de talen?', a: 'Je beheert SEO per taal. Premium ontgrendelt alle 6 talen tegelijk.' },
      { q: 'Kan ik SEO per pagina bewerken?', a: 'Ja, elke pagina heeft een eigen SEO-paneel (titel, beschrijving, slug, canonical, robots, OG).' }
    ],
    finalCtaTitle: 'Klaar om te starten?',
    finalCtaBody: 'Maak binnen minuten je vermelding en verschijn in lokale zoekopdrachten door de hele EU.',
    finalCtaButton: 'Maak mijn vermelding',
    navLabel: 'Hoe het werkt',
    slug: HOW_SLUGS.NL
  },
  PT: {
    heroTitle: 'Como funciona a ListAcross EU',
    heroSubtitle: 'Publique o seu negocio uma vez. Alcance clientes em toda a Europa com SEO multilingue.',
    ctaStartFree: 'Começar gratis',
    step1Title: '1) Crie ou reivindique a sua pagina',
    step1Body: 'Registe-se e adicione o seu negocio. Importe dados basicos e reivindique para verificacao e upgrades.',
    step2Title: '2) Otimize com pre-visualizacoes',
    step2Body: 'Ajuste titulos, descricoes e social cards com previas Google/Bing por idioma.',
    step3Title: '3) Seja encontrado',
    step3Body: 'Apareca em paginas de pais, cidade e categoria. Faca upgrade para destaque e alcance em toda a UE.',
    plansTitle: 'Planos',
    ...base,
    faqTitle: 'Perguntas frequentes',
    faq: [
      { q: 'Posso comecar gratis?', a: 'Sim. Crie uma listagem basica e faca upgrade quando precisar de mais alcance.' },
      { q: 'Como funcionam os idiomas?', a: 'Pode gerir SEO por idioma. O Premium desbloqueia os 6 idiomas.' },
      { q: 'Posso editar SEO por pagina?', a: 'Sim, cada pagina tem o seu painel de SEO (titulo, descricao, slug, canonical, robots, OG).' }
    ],
    finalCtaTitle: 'Pronto para comecar?',
    finalCtaBody: 'Crie a sua listagem em minutos e apareca nas pesquisas locais por toda a UE.',
    finalCtaButton: 'Criar minha listagem',
    navLabel: 'Como funciona',
    slug: HOW_SLUGS.PT
  },
  FR: {
    heroTitle: 'Comment ca marche — ListAcross EU',
    heroSubtitle: 'Publiez votre entreprise une fois. Touchez des clients dans toute l\'Europe avec un SEO multilingue.',
    ctaStartFree: 'Commencer gratuitement',
    step1Title: '1) Creez ou reclamez votre page',
    step1Body: 'Inscrivez-vous et ajoutez votre entreprise. Importez les infos de base et reclamez pour verification et options.',
    step2Title: '2) Optimisez avec apercus en direct',
    step2Body: 'Ajustez titres, descriptions et cartes sociales avec apercus Google/Bing par langue.',
    step3Title: '3) Soyez trouve',
    step3Body: 'Votre fiche apparait sur les pages pays, ville et categorie. Passez en version Pro pour etre mis en avant et viser l\'UE.',
    plansTitle: 'Offres',
    ...base,
    faqTitle: 'FAQ',
    faq: [
      { q: 'Puis-je commencer gratuitement ?', a: 'Oui. Creez une fiche basique et ameliorez-la ensuite selon vos besoins.' },
      { q: 'Comment fonctionnent les langues ?', a: 'Vous gerez le SEO par langue. Premium debloque les 6 langues.' },
      { q: 'SEO par page ?', a: 'Oui, chaque page a son panneau SEO (titre, description, slug, canonical, robots, OG).' }
    ],
    finalCtaTitle: 'Pret a etre visible ?',
    finalCtaBody: 'Creez votre fiche en quelques minutes et apparaissez dans les recherches locales a travers l\'UE.',
    finalCtaButton: 'Creer ma fiche',
    navLabel: 'Comment ca marche',
    slug: HOW_SLUGS.FR
  },
  DE: {
    heroTitle: 'So funktioniert ListAcross EU',
    heroSubtitle: 'Einmal veroffentlichen. Kunden in ganz Europa mit mehrsprachigem SEO erreichen.',
    ctaStartFree: 'Kostenlos starten',
    step1Title: '1) Seite erstellen oder beanspruchen',
    step1Body: 'Registrieren und Unternehmen hinzufugen. Basisdaten importieren und fur Verifizierung/Upgrades beanspruchen.',
    step2Title: '2) Mit Live-Vorschau optimieren',
    step2Body: 'Titel, Beschreibungen und Social Cards mit Google/Bing-Vorschau anpassen pro Sprache.',
    step3Title: '3) Gefunden werden',
    step3Body: 'Eintrag erscheint auf Lander-, Stadte- und Kategorieseiten. Upgrade fur hervorgehobene Platze und EU-Reichweite.',
    plansTitle: 'Pakete',
    ...base,
    faqTitle: 'Haufige Fragen',
    faq: [
      { q: 'Kostenloser Start?', a: 'Ja. Basis-Eintrag erstellen und spater upgraden.' },
      { q: 'Wie funktionieren Sprachen?', a: 'SEO pro Sprache. Premium schaltet alle 6 frei.' },
      { q: 'SEO je Seite?', a: 'Ja, jedes Objekt hat ein eigenes SEO-Panel (Titel, Beschreibung, Slug, Canonical, Robots, OG).' }
    ],
    finalCtaTitle: 'Bereit zum Start?',
    finalCtaBody: 'Erstellen Sie Ihren Eintrag in Minuten und erscheinen Sie in lokalen Suchen in der gesamten EU.',
    finalCtaButton: 'Eintrag erstellen',
    navLabel: 'So funktioniert es',
    slug: HOW_SLUGS.DE
  },
  ES: {
    heroTitle: 'Como funciona ListAcross EU',
    heroSubtitle: 'Publica tu negocio una vez. Llega a clientes en toda Europa con SEO multilingue.',
    ctaStartFree: 'Empezar gratis',
    step1Title: '1) Crea o reclama tu pagina',
    step1Body: 'Registrate y anade tu negocio. Importa datos basicos y reclamalo para verificacion y mejoras.',
    step2Title: '2) Optimiza con vistas previas',
    step2Body: 'Ajusta titulos, descripciones y tarjetas sociales con vistas de Google/Bing por idioma.',
    step3Title: '3) Te encontraran',
    step3Body: 'Tu ficha aparece en paginas de pais, ciudad y categoria. Mejora para posicion destacada y alcance UE.',
    plansTitle: 'Planes',
    ...base,
    faqTitle: 'Preguntas frecuentes',
    faq: [
      { q: 'Puedo empezar gratis?', a: 'Si. Crea una ficha basica y mejora despues cuando lo necesites.' },
      { q: 'Idiomas?', a: 'Gestiona SEO por idioma. Premium desbloquea los 6.' },
      { q: 'SEO por pagina?', a: 'Si, cada pagina tiene panel SEO propio (titulo, descripcion, slug, canonical, robots, OG).' }
    ],
    finalCtaTitle: 'Listo para empezar?',
    finalCtaBody: 'Crea tu ficha en minutos y aparece en busquedas locales por toda la UE.',
    finalCtaButton: 'Crear mi ficha',
    navLabel: 'Como funciona',
    slug: HOW_SLUGS.ES
  }
};