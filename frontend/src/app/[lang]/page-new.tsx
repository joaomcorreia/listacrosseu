import { getUIText } from '@/i18n/ui';
import { HeroSection } from '@/components/homepage/HeroSection';
import { TrustedPartnersSection } from '@/components/homepage/TrustedPartnersSection';
import { HowItWorksSection } from '@/components/homepage/HowItWorksSection';
import { CountryExplorerSection } from '@/components/homepage/CountryExplorerSection';
import { WhyChooseSection } from '@/components/homepage/WhyChooseSection';
import { FinalCTASection } from '@/components/homepage/FinalCTASection';

export default function HomePage({
  params,
}: {
  params: { lang: string };
}) {
  const ui = getUIText(params.lang);

  return (
    <div className="min-h-screen">
      <HeroSection lang={params.lang} ui={ui} />
      <TrustedPartnersSection lang={params.lang} ui={ui} />
      <HowItWorksSection lang={params.lang} ui={ui} />
      <CountryExplorerSection lang={params.lang} ui={ui} />
      <WhyChooseSection lang={params.lang} ui={ui} />
      <FinalCTASection lang={params.lang} ui={ui} />
    </div>
  );
}