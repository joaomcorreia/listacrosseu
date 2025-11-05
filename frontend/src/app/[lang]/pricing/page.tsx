"use client";

import React from "react";

type Lang = "en" | "nl" | "pt" | "fr" | "de" | "es";
const DEFAULT_LANG: Lang = "en";
const CURRENCY = "€";

const T = {
  en: {
    title: "Website + Social Plans",
    subtitle: "Start now. First 3 weeks of Facebook posts are free — build trust before you pay.",
    website: "Website (Multi-page)",
    social: "Facebook Posts (2 / week)",
    bundle: "Website + Facebook (2 / week)",
    perMonth: "/month",
    perWeek: "/week",
    ctaWebsite: "Choose Website",
    ctaSocial: "Choose Social",
    ctaBundle: "Choose Bundle",
    featuresWebsite: [
      "AI website builder (multi-page)",
      "6 languages ready (NL, PT, EN, FR, DE, ES)",
      "Basic SEO & analytics widgets",
      "Custom domain & SSL",
    ],
    featuresSocial: [
      "Page created & branded in 24h",
      "2 posts per week (templates + logo)",
      "3-week free posting trial",
      "Optional Instagram add-on",
    ],
    featuresBundle: [
      "Everything in Website + Social",
      "Unified support & billing",
      "Upgrade to Ads/Printing anytime",
      "Cancel anytime",
    ],
    trialNote: "Free trial: we'll post for you weekly for 2–3 weeks. Keep the same time slot if you upgrade.",
    smallPrint: "Prices excl. VAT where applicable. Instagram add-on and ads credit billed separately.",
  },
  nl: {
    title: "Website + Social-pakketten",
    subtitle: "Begin nu. De eerste 3 weken Facebook-posts zijn gratis — bewijs vóór je betaalt.",
    website: "Website (Multi-page)",
    social: "Facebook-berichten (2 / week)",
    bundle: "Website + Facebook (2 / week)",
    perMonth: "/maand",
    perWeek: "/week",
    ctaWebsite: "Kies Website",
    ctaSocial: "Kies Social",
    ctaBundle: "Kies Bundel",
    featuresWebsite: [
      "AI websitebouwer (meerdere pagina's)",
      "6 talen klaar (NL, PT, EN, FR, DE, ES)",
      "Basis SEO & analytics widgets",
      "Eigen domein & SSL",
    ],
    featuresSocial: [
      "Pagina aangemaakt & gebrand in 24u",
      "2 posts per week (templates + logo)",
      "3 weken gratis proef",
      "Optionele Instagram-add-on",
    ],
    featuresBundle: [
      "Alles in Website + Social",
      "Gecombineerde support & facturatie",
      "Upgrade naar Ads/Print op elk moment",
      "Maandelijks opzegbaar",
    ],
    trialNote: "Gratis proef: we posten 2–3 weken wekelijks. Behoud dezelfde tijdslot bij upgrade.",
    smallPrint: "Prijzen excl. btw. Instagram-add-on en advertentietegoed apart gefactureerd.",
  },
  pt: {
    title: "Planos de Website + Social",
    subtitle: "Comece agora. As primeiras 3 semanas de publicações no Facebook são grátis.",
    website: "Website (Múltiplas páginas)",
    social: "Publicações no Facebook (2 / semana)",
    bundle: "Website + Facebook (2 / semana)",
    perMonth: "/mês",
    perWeek: "/semana",
    ctaWebsite: "Escolher Website",
    ctaSocial: "Escolher Social",
    ctaBundle: "Escolher Pacote",
    featuresWebsite: [
      "Construtor de sites com IA (multi-página)",
      "6 idiomas prontos (NL, PT, EN, FR, DE, ES)",
      "SEO básico & widgets de análise",
      "Domínio próprio & SSL",
    ],
    featuresSocial: [
      "Página criada & com branding em 24h",
      "2 posts por semana (templates + logótipo)",
      "3 semanas de teste grátis",
      "Add-on opcional Instagram",
    ],
    featuresBundle: [
      "Tudo de Website + Social",
      "Suporte & faturação unificados",
      "Upgrade para Anúncios/Impressão",
      "Cancelar quando quiser",
    ],
    trialNote: "Teste grátis: publicamos semanalmente por 2–3 semanas. Mantém o horário ao fazer upgrade.",
    smallPrint: "Preços sem IVA onde aplicável. Instagram & crédito de anúncios cobrados à parte.",
  },
  fr: {
    title: "Offres Site Web + Réseaux sociaux",
    subtitle: "Commencez maintenant. 3 premières semaines de posts Facebook gratuites.",
    website: "Site web (Multi-pages)",
    social: "Posts Facebook (2 / semaine)",
    bundle: "Site + Facebook (2 / semaine)",
    perMonth: "/mois",
    perWeek: "/semaine",
    ctaWebsite: "Choisir Site",
    ctaSocial: "Choisir Social",
    ctaBundle: "Choisir Pack",
    featuresWebsite: [
      "Générateur de site IA (multi-pages)",
      "6 langues prêtes (NL, PT, EN, FR, DE, ES)",
      "SEO basique & widgets analytics",
      "Domaine & SSL",
    ],
    featuresSocial: [
      "Page créée & brandée en 24h",
      "2 posts / semaine (templates + logo)",
      "Essai gratuit 3 semaines",
      "Option Instagram",
    ],
    featuresBundle: [
      "Tout de Site + Social",
      "Support & facturation unifiés",
      "Upgrade vers Ads/Impression",
      "Résiliable à tout moment",
    ],
    trialNote: "Essai gratuit : posts hebdo pendant 2–3 semaines. Gardez le créneau si vous passez en payant.",
    smallPrint: "Prix HT. Option Instagram & budget pubs facturés séparément.",
  },
  de: {
    title: "Website + Social-Pakete",
    subtitle: "Starten Sie jetzt. Die ersten 3 Wochen Facebook-Posts sind kostenlos.",
    website: "Website (Mehrseitig)",
    social: "Facebook-Beiträge (2 / Woche)",
    bundle: "Website + Facebook (2 / Woche)",
    perMonth: "/Monat",
    perWeek: "/Woche",
    ctaWebsite: "Website wählen",
    ctaSocial: "Social wählen",
    ctaBundle: "Bundle wählen",
    featuresWebsite: [
      "KI-Website-Builder (mehrseitig)",
      "6 Sprachen bereit (NL, PT, EN, FR, DE, ES)",
      "Basis-SEO & Analytics-Widgets",
      "Eigene Domain & SSL",
    ],
    featuresSocial: [
      "Seite in 24h erstellt & gebrandet",
      "2 Posts pro Woche (Templates + Logo)",
      "3-wöchige Gratis-Testphase",
      "Optional: Instagram-Add-on",
    ],
    featuresBundle: [
      "Alles aus Website + Social",
      "Einheitlicher Support & Abrechnung",
      "Upgrade zu Ads/Druck jederzeit",
      "Monatlich kündbar",
    ],
    trialNote: "Gratis-Test: 2–3 Wochen wöchentliche Posts. Behalten Sie das Zeitfenster nach Upgrade.",
    smallPrint: "Preise zzgl. MwSt. Instagram & Werbebudget separat.",
  },
  es: {
    title: "Planes de Web + Social",
    subtitle: "Empieza ahora. Las primeras 3 semanas de publicaciones en Facebook son gratis.",
    website: "Sitio web (Multi-página)",
    social: "Publicaciones en Facebook (2 / semana)",
    bundle: "Web + Facebook (2 / semana)",
    perMonth: "/mes",
    perWeek: "/semana",
    ctaWebsite: "Elegir Web",
    ctaSocial: "Elegir Social",
    ctaBundle: "Elegir Paquete",
    featuresWebsite: [
      "Creador web con IA (multi-página)",
      "6 idiomas listos (NL, PT, EN, FR, DE, ES)",
      "SEO básico & widgets de analítica",
      "Dominio & SSL",
    ],
    featuresSocial: [
      "Página creada y con branding en 24h",
      "2 posts por semana (plantillas + logo)",
      "3 semanas de prueba gratis",
      "Add-on opcional Instagram",
    ],
    featuresBundle: [
      "Todo de Web + Social",
      "Soporte & facturación unificados",
      "Upgrade a Ads/Impresión",
      "Cancelar en cualquier momento",
    ],
    trialNote: "Prueba gratuita: publicamos semanalmente 2–3 semanas. Mantén la franja al mejorar el plan.",
    smallPrint: "Precios sin IVA. Instagram y crédito de anuncios por separado.",
  },
} as const;

const PRICE = {
  website: 30,
  social_2pw: 30,
  bundle: 60,
};

const STRIPE = {
  website_price_id: "price_WEBSITE_30_EUR_REPLACE",
  social_price_id: "price_SOCIAL_30_EUR_REPLACE",
  bundle_price_id: "price_BUNDLE_60_EUR_REPLACE",
};

function PlanCard(props: {
  title: string;
  price: number;
  per: string;
  features: readonly string[];
  cta: string;
  accent?: boolean;
  onSelect: () => void;
}) {
  return (
    <div
      className={`rounded-3xl p-8 shadow-xl relative overflow-hidden transform hover:scale-105 transition-all duration-300 animate-fade-in-up ${
        props.accent 
          ? "bg-gradient-to-br from-brand to-purple-600 text-white ring-4 ring-brand/30 scale-105" 
          : "bg-white border border-gray-200 hover:shadow-2xl"
      }`}
    >
      {props.accent && (
        <div className="absolute top-4 right-4 bg-yellow-400 text-black text-xs font-bold px-3 py-1 rounded-full animate-pulse">
          POPULAR
        </div>
      )}
      
      <h3 className={`text-2xl font-bold mb-4 ${props.accent ? "text-white" : "text-gray-900"}`}>
        {props.title}
      </h3>
      
      <div className="mb-6">
        <div className={`text-5xl font-bold ${props.accent ? "text-white" : "text-brand"}`}>
          {CURRENCY}{props.price}
        </div>
        <span className={`text-lg ${props.accent ? "text-white/80" : "text-gray-500"}`}>
          {props.per}
        </span>
      </div>
      
      <ul className="space-y-3 mb-8">
        {props.features.map((f, i) => (
          <li key={i} className="flex items-start gap-3">
            <span className={`mt-1 text-lg ${props.accent ? "text-green-300" : "text-green-500"}`}>✓</span>
            <span className={`${props.accent ? "text-white/90" : "text-gray-700"}`}>{f}</span>
          </li>
        ))}
      </ul>
      
      <button
        onClick={props.onSelect}
        className={`w-full py-4 px-6 rounded-xl font-bold text-lg transition-all duration-300 transform hover:scale-105 ${
          props.accent 
            ? "bg-white text-brand hover:bg-gray-100 shadow-lg" 
            : "bg-brand text-white hover:bg-brand-dark shadow-lg hover:shadow-xl"
        }`}
      >
        {props.cta}
      </button>
    </div>
  );
}

export default function PricingPage({
  params,
}: {
  params: { lang: Lang };
}) {
  const lang: Lang = params.lang || DEFAULT_LANG;
  const t = T[lang];

  const handleCheckout = (priceId: string) => {
    const url = `/checkout?price_id=${encodeURIComponent(priceId)}&lang=${lang}`;
    window.location.href = url;
  };

  return (
    <div className="min-h-screen">
      <section className="bg-gradient-to-br from-brand via-purple-600 to-indigo-800 relative overflow-hidden pt-24 pb-16">
        <div className="absolute inset-0">
          <div className="absolute top-20 left-10 w-32 h-32 bg-white/10 rounded-full animate-pulse"></div>
          <div className="absolute top-40 right-20 w-24 h-24 bg-white/5 rounded-full animate-bounce" style={{ animationDelay: '1s' }}></div>
          <div className="absolute bottom-20 left-1/4 w-40 h-40 bg-white/5 rounded-full animate-pulse" style={{ animationDelay: '2s' }}></div>
        </div>
        
        <div className="container mx-auto px-6 py-16 relative z-10 text-center text-white">
          <div className="inline-flex items-center bg-white/20 backdrop-blur-sm border border-white/30 rounded-full px-6 py-3 mb-8 animate-fade-in-up">
            <span className="text-sm text-white/90">💰 Transparent pricing for European businesses</span>
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold mb-6 animate-fade-in-up" style={{ animationDelay: '0.2s' }}>{t.title}</h1>
          <p className="text-xl text-white/90 mb-12 max-w-3xl mx-auto animate-fade-in-up" style={{ animationDelay: '0.4s' }}>{t.subtitle}</p>
        </div>
      </section>

      <section className="py-20 bg-white relative">
        <div className="absolute top-0 left-0 w-full h-32 bg-gradient-to-b from-brand/5 to-transparent"></div>
        <div className="container mx-auto px-6 relative z-10">
          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            <PlanCard
              title={t.website}
              price={PRICE.website}
              per={t.perMonth}
              features={t.featuresWebsite}
              cta={t.ctaWebsite}
              onSelect={() => handleCheckout(STRIPE.website_price_id)}
            />
            <PlanCard
              title={t.social}
              price={PRICE.social_2pw}
              per={t.perMonth}
              features={t.featuresSocial}
              cta={t.ctaSocial}
              onSelect={() => handleCheckout(STRIPE.social_price_id)}
            />
            <PlanCard
              title={t.bundle}
              price={PRICE.bundle}
              per={t.perMonth}
              features={t.featuresBundle}
              cta={t.ctaBundle}
              accent
              onSelect={() => handleCheckout(STRIPE.bundle_price_id)}
            />
          </div>

          <div className="mt-16 max-w-4xl mx-auto rounded-2xl border border-dashed border-brand/30 bg-brand-light p-8 text-center animate-fade-in-up" style={{ animationDelay: '0.8s' }}>
            <div className="font-semibold text-lg mb-2 text-brand">🎯 Free Trial Available</div>
            <div className="text-gray-700">{t.trialNote}</div>
          </div>

          <p className="mt-8 text-center text-sm text-gray-500 animate-fade-in-up" style={{ animationDelay: '1s' }}>{t.smallPrint}</p>
        </div>
      </section>
    </div>
  );
}