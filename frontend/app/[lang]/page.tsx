import Link from 'next/link';
import { fetchCategories, fetchBusinesses } from '../../lib/api';
import { translate, Language, getTranslatedPath, getCountryFromLanguage } from '../../lib/i18n';
import LanguageSwitcher from '../../components/LanguageSwitcher';
import CategoryCard from '../../components/CategoryCard';
import BusinessCard from '../../components/BusinessCard';
import BlogSlider from '../../components/BlogSlider';
import HeroSlideshow from '../../components/HeroSlideshow';

interface HomePageProps {
  params: Promise<{
    lang: string;
  }>;
}

// Sample blog posts - In production, this would come from a CMS or API
function getBlogPosts(lang: Language) {
  const posts = [
    {
      id: '1',
      title: lang === 'en' ? 'The Future of Business in Europe: Digital Transformation Trends' 
        : lang === 'es' ? 'El Futuro de los Negocios en Europa: Tendencias de Transformación Digital'
        : lang === 'fr' ? 'L\'Avenir des Affaires en Europe : Tendances de Transformation Numérique'
        : lang === 'de' ? 'Die Zukunft der Geschäfte in Europa: Digitale Transformationstrends'
        : lang === 'nl' ? 'De Toekomst van Zaken in Europa: Digitale Transformatietrends'
        : 'O Futuro dos Negócios na Europa: Tendências de Transformação Digital',
      excerpt: lang === 'en' ? 'Discover how European businesses are embracing digital transformation to stay competitive in the modern marketplace.'
        : lang === 'es' ? 'Descubre cómo las empresas europeas están adoptando la transformación digital para mantenerse competitivas en el mercado moderno.'
        : lang === 'fr' ? 'Découvrez comment les entreprises européennes adoptent la transformation numérique pour rester compétitives sur le marché moderne.'
        : lang === 'de' ? 'Entdecken Sie, wie europäische Unternehmen die digitale Transformation annehmen, um auf dem modernen Markt wettbewerbsfähig zu bleiben.'
        : lang === 'nl' ? 'Ontdek hoe Europese bedrijven digitale transformatie omarmen om concurrerend te blijven op de moderne markt.'
        : 'Descubra como as empresas europeias estão adotando a transformação digital para se manterem competitivas no mercado moderno.',
      image: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&h=300&fit=crop',
      author: 'Maria Schmidt',
      publishedAt: '2025-10-28',
      readTime: 5,
      slug: 'digital-transformation-trends-europe',
      category: lang === 'en' ? 'Technology' : lang === 'es' ? 'Tecnología' : lang === 'fr' ? 'Technologie' : lang === 'de' ? 'Technologie' : lang === 'nl' ? 'Technologie' : 'Tecnologia',
      tags: ['Digital', 'Business', 'Europe', 'Innovation']
    },
    {
      id: '2',
      title: lang === 'en' ? 'Sustainable Business Practices Across EU Countries'
        : lang === 'es' ? 'Prácticas Empresariales Sostenibles en los Países de la UE'
        : lang === 'fr' ? 'Pratiques Commerciales Durables dans les Pays de l\'UE'
        : lang === 'de' ? 'Nachhaltige Geschäftspraktiken in EU-Ländern'
        : lang === 'nl' ? 'Duurzame Bedrijfspraktijken in EU-landen'
        : 'Práticas de Negócios Sustentáveis nos Países da UE',
      excerpt: lang === 'en' ? 'Learn about the green initiatives and sustainable practices that European businesses are implementing to reduce their environmental impact.'
        : lang === 'es' ? 'Aprende sobre las iniciativas verdes y prácticas sostenibles que las empresas europeas están implementando para reducir su impacto ambiental.'
        : lang === 'fr' ? 'Apprenez les initiatives vertes et les pratiques durables que les entreprises européennes mettent en œuvre pour réduire leur impact environnemental.'
        : lang === 'de' ? 'Erfahren Sie über grüne Initiativen und nachhaltige Praktiken, die europäische Unternehmen umsetzen, um ihre Umweltauswirkungen zu reduzieren.'
        : lang === 'nl' ? 'Leer over groene initiatieven en duurzame praktijken die Europese bedrijven implementeren om hun milieu-impact te verminderen.'
        : 'Aprenda sobre as iniciativas verdes e práticas sustentáveis que as empresas europeias estão implementando para reduzir seu impacto ambiental.',
      image: 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=600&h=300&fit=crop',
      author: 'Jean Dubois',
      publishedAt: '2025-10-25',
      readTime: 7,
      slug: 'sustainable-business-practices-eu',
      category: lang === 'en' ? 'Sustainability' : lang === 'es' ? 'Sostenibilidad' : lang === 'fr' ? 'Durabilité' : lang === 'de' ? 'Nachhaltigkeit' : lang === 'nl' ? 'Duurzaamheid' : 'Sustentabilidade',
      tags: ['Sustainability', 'Environment', 'Green Business']
    },
    {
      id: '3',
      title: lang === 'en' ? 'Cross-Border E-commerce: Opportunities and Challenges'
        : lang === 'es' ? 'Comercio Electrónico Transfronterizo: Oportunidades y Desafíos'
        : lang === 'fr' ? 'Commerce Électronique Transfrontalier : Opportunités et Défis'
        : lang === 'de' ? 'Grenzüberschreitender E-Commerce: Chancen und Herausforderungen'
        : lang === 'nl' ? 'Grensoverschrijdende E-commerce: Kansen en Uitdagingen'
        : 'E-commerce Transfronteiriço: Oportunidades e Desafios',
      excerpt: lang === 'en' ? 'Explore the growing trend of cross-border e-commerce in Europe and how businesses can capitalize on international opportunities.'
        : lang === 'es' ? 'Explora la tendencia creciente del comercio electrónico transfronterizo en Europa y cómo las empresas pueden capitalizar las oportunidades internacionales.'
        : lang === 'fr' ? 'Explorez la tendance croissante du commerce électronique transfrontalier en Europe et comment les entreprises peuvent capitaliser sur les opportunités internationales.'
        : lang === 'de' ? 'Erforschen Sie den wachsenden Trend des grenzüberschreitenden E-Commerce in Europa und wie Unternehmen internationale Chancen nutzen können.'
        : lang === 'nl' ? 'Verken de groeiende trend van grensoverschrijdende e-commerce in Europa en hoe bedrijven kunnen profiteren van internationale kansen.'
        : 'Explore a tendência crescente do e-commerce transfronteiriço na Europa e como as empresas podem capitalizar as oportunidades internacionais.',
      image: 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=600&h=300&fit=crop',
      author: 'Lars Anderson',
      publishedAt: '2025-10-22',
      readTime: 6,
      slug: 'cross-border-ecommerce-europe',
      category: lang === 'en' ? 'E-commerce' : lang === 'es' ? 'Comercio Electrónico' : lang === 'fr' ? 'Commerce Électronique' : lang === 'de' ? 'E-Commerce' : lang === 'nl' ? 'E-commerce' : 'Comércio Eletrônico',
      tags: ['E-commerce', 'International', 'Trade']
    },
    {
      id: '4',
      title: lang === 'en' ? 'The Rise of Fintech Startups in European Markets'
        : lang === 'es' ? 'El Auge de las Startups Fintech en los Mercados Europeos'
        : lang === 'fr' ? 'L\'Essor des Startups Fintech sur les Marchés Européens'
        : lang === 'de' ? 'Der Aufstieg von Fintech-Startups auf Europäischen Märkten'
        : lang === 'nl' ? 'De Opkomst van Fintech Startups op Europese Markten'
        : 'A Ascensão das Startups Fintech nos Mercados Europeus',
      excerpt: lang === 'en' ? 'How financial technology companies are revolutionizing traditional banking and financial services across Europe.'
        : lang === 'es' ? 'Cómo las empresas de tecnología financiera están revolucionando los servicios bancarios y financieros tradicionales en Europa.'
        : lang === 'fr' ? 'Comment les entreprises de technologie financière révolutionnent les services bancaires et financiers traditionnels en Europe.'
        : lang === 'de' ? 'Wie Fintech-Unternehmen traditionelle Bank- und Finanzdienstleistungen in Europa revolutionieren.'
        : lang === 'nl' ? 'Hoe financiële technologiebedrijven traditionele bank- en financiële diensten in Europa revolutioneren.'
        : 'Como as empresas de tecnologia financeira estão revolucionando os serviços bancários e financeiros tradicionais na Europa.',
      image: 'https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=600&h=300&fit=crop',
      author: 'Sofia Rodriguez',
      publishedAt: '2025-10-20',
      readTime: 8,
      slug: 'fintech-startups-european-markets',
      category: lang === 'en' ? 'Fintech' : lang === 'es' ? 'Fintech' : lang === 'fr' ? 'Fintech' : lang === 'de' ? 'Fintech' : lang === 'nl' ? 'Fintech' : 'Fintech',
      tags: ['Fintech', 'Startups', 'Finance', 'Innovation']
    },
    {
      id: '5',
      title: lang === 'en' ? 'Remote Work Culture: How European Companies Adapted'
        : lang === 'es' ? 'Cultura de Trabajo Remoto: Cómo se Adaptaron las Empresas Europeas'
        : lang === 'fr' ? 'Culture du Travail à Distance : Comment les Entreprises Européennes se Sont Adaptées'
        : lang === 'de' ? 'Remote-Work-Kultur: Wie Europäische Unternehmen Sich Angepasst Haben'
        : lang === 'nl' ? 'Werken op Afstand Cultuur: Hoe Europese Bedrijven Zich Aanpasten'
        : 'Cultura de Trabalho Remoto: Como as Empresas Europeias Se Adaptaram',
      excerpt: lang === 'en' ? 'An in-depth look at how European businesses have successfully transitioned to remote and hybrid work models.'
        : lang === 'es' ? 'Una mirada profunda a cómo las empresas europeas han hecho la transición exitosa a modelos de trabajo remoto e híbrido.'
        : lang === 'fr' ? 'Un regard approfondi sur la façon dont les entreprises européennes ont réussi la transition vers des modèles de travail à distance et hybrides.'
        : lang === 'de' ? 'Ein detaillierter Blick darauf, wie europäische Unternehmen erfolgreich auf Remote- und Hybrid-Arbeitsmodelle umgestellt haben.'
        : lang === 'nl' ? 'Een diepgaande blik op hoe Europese bedrijven succesvol zijn overgestapt op remote en hybride werkmodellen.'
        : 'Uma análise aprofundada de como as empresas europeias fizeram a transição bem-sucedida para modelos de trabalho remoto e híbrido.',
      image: 'https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=600&h=300&fit=crop',
      author: 'Marco Italiano',
      publishedAt: '2025-10-18',
      readTime: 4,
      slug: 'remote-work-culture-european-companies',
      category: lang === 'en' ? 'Workplace' : lang === 'es' ? 'Lugar de Trabajo' : lang === 'fr' ? 'Lieu de Travail' : lang === 'de' ? 'Arbeitsplatz' : lang === 'nl' ? 'Werkplek' : 'Local de Trabalho',
      tags: ['Remote Work', 'Culture', 'Productivity']
    }
  ];

  return posts;
}

export default async function HomePage({ params }: HomePageProps) {
  const { lang } = await params;
  const currentLang = lang as Language;
  
  // Get country filter based on language
  const country = getCountryFromLanguage(currentLang);
  
  // Fetch some sample data
  const [categoriesData, businessesData] = await Promise.all([
    fetchCategories(lang, country || undefined),
    fetchBusinesses(country ? { country, page: 1, page_size: 6 } : { page: 1, page_size: 6 }) // Get first 6 businesses for homepage
  ]);

  const topCategories = categoriesData.items?.slice(0, 6) || [];
  const featuredBusinesses = businessesData.items || [];

  return (
    <div className="min-h-screen">
      {/* Language Switcher - Positioned absolutely */}
      <div className="absolute top-8 right-8 z-50">
        <LanguageSwitcher currentLang={currentLang} />
      </div>

      {/* Hero Slideshow */}
      <HeroSlideshow lang={currentLang} />

      {/* Categories Section */}
      <section className="py-20 bg-gradient-to-b from-white to-slate-50">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <div className="inline-flex items-center space-x-2 bg-blue-100 text-blue-600 px-4 py-2 rounded-full text-sm font-medium mb-6">
              <span>🎯</span>
              <span>Popular Categories</span>
            </div>
            <h2 className="text-4xl lg:text-5xl font-bold text-slate-900 mb-6">
              <span className="bg-gradient-to-r from-slate-900 via-blue-800 to-slate-900 bg-clip-text text-transparent">
                {translate('homepage.popular_categories', currentLang)}
              </span>
            </h2>
            <p className="text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed">
              Discover thousands of businesses organized across the most popular categories in Europe
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
            {topCategories.map((category: any, index: number) => (
              <div
                key={category.slug}
                className="transform transition-all duration-300 hover:-translate-y-2"
                style={{ animationDelay: `${index * 150}ms` }}
              >
                <CategoryCard 
                  category={category}
                  lang={lang}
                  variant="featured"
                />
              </div>
            ))}
          </div>
          
          <div className="text-center">
            <Link
              href={`/${lang}/${getTranslatedPath('categories', currentLang)}`}
              className="group inline-flex items-center space-x-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white px-8 py-4 rounded-2xl font-semibold hover:from-blue-700 hover:to-blue-800 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
            >
              <span>View All Categories</span>
              <span className="group-hover:translate-x-1 transition-transform">→</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Featured Businesses Section */}
      <section className="py-20 bg-gradient-to-b from-slate-50 to-white">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <div className="inline-flex items-center space-x-2 bg-amber-100 text-amber-600 px-4 py-2 rounded-full text-sm font-medium mb-6">
              <span>⭐</span>
              <span>Featured Businesses</span>
            </div>
            <h2 className="text-4xl lg:text-5xl font-bold text-slate-900 mb-6">
              <span className="bg-gradient-to-r from-slate-900 via-amber-800 to-slate-900 bg-clip-text text-transparent">
                {translate('homepage.featured_businesses', currentLang)}
              </span>
            </h2>
            <p className="text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed">
              Explore exceptional businesses across Europe, handpicked for their quality and service
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
            {featuredBusinesses.map((business: any, index: number) => (
              <div
                key={business.slug}
                className="transform transition-all duration-300 hover:-translate-y-2"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <BusinessCard
                  business={business}
                  lang={currentLang}
                  variant="featured"
                />
              </div>
            ))}
          </div>
          
          <div className="text-center">
            <Link
              href={`/${lang}/${getTranslatedPath('businesses', currentLang)}`}
              className="group inline-flex items-center space-x-3 bg-gradient-to-r from-amber-500 to-amber-600 text-white px-8 py-4 rounded-2xl font-semibold hover:from-amber-600 hover:to-amber-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
            >
              <span>🏢</span>
              <span>Browse All Businesses</span>
              <span className="group-hover:translate-x-1 transition-transform">→</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Blog Section */}
      <section className="py-20 bg-gradient-to-b from-white to-gray-50">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <div className="inline-flex items-center space-x-2 bg-green-100 text-green-600 px-4 py-2 rounded-full text-sm font-medium mb-6">
              <span>📝</span>
              <span>Latest Articles</span>
            </div>
            <h2 className="text-4xl lg:text-5xl font-bold text-slate-900 mb-6">
              <span className="bg-gradient-to-r from-slate-900 via-green-800 to-slate-900 bg-clip-text text-transparent">
                Business Insights & News
              </span>
            </h2>
            <p className="text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed">
              Stay updated with the latest business trends, insights, and success stories from across Europe
            </p>
          </div>
          
          <BlogSlider posts={getBlogPosts(currentLang)} lang={currentLang} />
          
          <div className="text-center mt-12">
            <Link
              href={`/${lang}/blog`}
              className="group inline-flex items-center space-x-3 bg-gradient-to-r from-green-500 to-green-600 text-white px-8 py-4 rounded-2xl font-semibold hover:from-green-600 hover:to-green-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
            >
              <span>📖</span>
              <span>Read All Articles</span>
              <span className="group-hover:translate-x-1 transition-transform">→</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 text-white relative overflow-hidden">
        {/* Background Elements */}
        <div className="absolute inset-0">
          <div className="absolute top-10 left-10 w-32 h-32 bg-blue-400/10 rounded-full blur-xl animate-pulse"></div>
          <div className="absolute bottom-10 right-10 w-40 h-40 bg-amber-400/10 rounded-full blur-xl animate-pulse delay-1000"></div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-blue-500/5 rounded-full blur-3xl"></div>
        </div>
        
        <div className="relative max-w-7xl mx-auto px-4">
          {/* Section Header */}
          <div className="text-center mb-16">
            <div className="inline-flex items-center space-x-2 bg-blue-500/20 text-blue-300 px-4 py-2 rounded-full text-sm font-medium mb-6">
              <span>📊</span>
              <span>Our Impact</span>
            </div>
            <h2 className="text-4xl lg:text-5xl font-bold mb-6">
              <span className="bg-gradient-to-r from-white via-blue-200 to-amber-200 bg-clip-text text-transparent">
                Connecting Europe's Business Network
              </span>
            </h2>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center group">
              <div className="bg-gradient-to-br from-blue-500/20 to-blue-600/20 rounded-3xl p-8 mb-6 backdrop-blur-sm border border-blue-400/20 hover:border-blue-400/40 transition-all duration-300 transform group-hover:-translate-y-2">
                <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
                  <span className="text-2xl">🏢</span>
                </div>
                <h3 className="text-4xl lg:text-5xl font-bold mb-2 bg-gradient-to-r from-blue-300 to-blue-100 bg-clip-text text-transparent">
                  6,000+
                </h3>
                <p className="text-blue-200 font-medium text-lg">Verified Businesses</p>
                <p className="text-blue-300/70 text-sm mt-2">Across all major European markets</p>
              </div>
            </div>
            
            <div className="text-center group">
              <div className="bg-gradient-to-br from-amber-500/20 to-amber-600/20 rounded-3xl p-8 mb-6 backdrop-blur-sm border border-amber-400/20 hover:border-amber-400/40 transition-all duration-300 transform group-hover:-translate-y-2">
                <div className="w-16 h-16 bg-gradient-to-br from-amber-500 to-amber-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
                  <span className="text-2xl">📂</span>
                </div>
                <h3 className="text-4xl lg:text-5xl font-bold mb-2 bg-gradient-to-r from-amber-300 to-amber-100 bg-clip-text text-transparent">
                  40+
                </h3>
                <p className="text-amber-200 font-medium text-lg">Business Categories</p>
                <p className="text-amber-300/70 text-sm mt-2">From tech startups to traditional crafts</p>
              </div>
            </div>
            
            <div className="text-center group">
              <div className="bg-gradient-to-br from-green-500/20 to-green-600/20 rounded-3xl p-8 mb-6 backdrop-blur-sm border border-green-400/20 hover:border-green-400/40 transition-all duration-300 transform group-hover:-translate-y-2">
                <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-green-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
                  <span className="text-2xl">🇪🇺</span>
                </div>
                <h3 className="text-4xl lg:text-5xl font-bold mb-2 bg-gradient-to-r from-green-300 to-green-100 bg-clip-text text-transparent">
                  27
                </h3>
                <p className="text-green-200 font-medium text-lg">EU Countries</p>
                <p className="text-green-300/70 text-sm mt-2">United in business, diverse in culture</p>
              </div>
            </div>
          </div>

          {/* Bottom CTA */}
          <div className="text-center mt-16">
            <p className="text-blue-200 text-lg mb-8 max-w-2xl mx-auto">
              Join thousands of businesses already growing their reach across Europe with ListAcrossEU
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href={`/${lang}/${getTranslatedPath('businesses', currentLang)}`}
                className="group inline-flex items-center space-x-3 bg-white text-slate-900 px-8 py-4 rounded-2xl font-semibold hover:bg-blue-50 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
              >
                <span>Explore Businesses</span>
                <span className="group-hover:translate-x-1 transition-transform">→</span>
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}