import { HOW, HOW_SLUGS, type Lang } from '@/i18n/howitworks';
import Link from 'next/link';
import BlogPostsFooter from '@/components/BlogPostsFooter';

function getLangFromParam(lang?: string): Lang {
  const m = (lang||'en').toLowerCase();
  if (m === 'nl') return 'NL';
  if (m === 'pt') return 'PT';
  if (m === 'fr') return 'FR';
  if (m === 'de') return 'DE';
  if (m === 'es') return 'ES';
  return 'EN';
}

export default function HowItWorksPage({ params }: { params: { lang: string }}) {
  const L = getLangFromParam(params.lang);
  const t = HOW[L];

  return (
    <div className="min-h-screen">
      {/* Full-Width Hero Section with Gradient */}
      <section className="bg-gradient-to-br from-brand via-purple-600 to-indigo-800 relative overflow-hidden">
        {/* Animated Background Elements */}
        <div className="absolute inset-0">
          <div className="absolute top-20 left-10 w-32 h-32 bg-white/10 rounded-full animate-pulse"></div>
          <div className="absolute top-40 right-20 w-24 h-24 bg-white/5 rounded-full animate-bounce" style={{ animationDelay: '1s' }}></div>
          <div className="absolute bottom-20 left-1/4 w-40 h-40 bg-white/5 rounded-full animate-pulse" style={{ animationDelay: '2s' }}></div>
        </div>
        
        <div className="container mx-auto px-4 py-32 relative z-10">
          <div className="max-w-5xl mx-auto text-center text-white">
            <h1 className="text-6xl md:text-8xl font-bold mb-8 leading-tight animate-fade-in-up">
              {t.heroTitle}
            </h1>
            <p className="text-xl md:text-2xl text-white/90 mb-16 max-w-4xl mx-auto leading-relaxed">
              {t.heroSubtitle}
            </p>
            <div className="animate-fade-in-up" style={{ animationDelay: '0.6s' }}>
              <Link 
                href={`/${params.lang}/advertise`}
                className="group bg-white text-brand hover:bg-gray-100 font-bold text-lg px-10 py-5 rounded-2xl shadow-2xl transform hover:scale-110 transition-all duration-300 flex items-center justify-center gap-3 inline-flex"
              >
                <span className="group-hover:animate-bounce">🚀</span>
                {t.ctaStartFree}
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Steps */}
      <section className="py-24 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">How It Works</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">Simple steps to get your business discovered across Europe</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {[
              {title: t.step1Title, body: t.step1Body, icon: "📝", color: "from-blue-500 to-purple-600"},
              {title: t.step2Title, body: t.step2Body, icon: "🎯", color: "from-purple-500 to-pink-600"},
              {title: t.step3Title, body: t.step3Body, icon: "🌟", color: "from-pink-500 to-red-600"}
            ].map((step, i) => (
              <div key={i} className="group bg-white rounded-3xl p-8 shadow-lg hover:shadow-2xl transform hover:scale-105 transition-all duration-300">
                <div className={`inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-r ${step.color} text-white text-2xl mb-6 group-hover:animate-bounce`}>
                  {step.icon}
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-4">{step.title}</h3>
                <p className="text-gray-600 leading-relaxed">{step.body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Plans */}
      <section className="py-24 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">{t.plansTitle}</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">Choose the plan that fits your business needs</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {[
              {plan: t.planFree, popular: false, gradient: "from-gray-500 to-gray-700"},
              {plan: t.planPaid, popular: true, gradient: "from-brand to-purple-600"},
              {plan: t.planPremium, popular: false, gradient: "from-purple-600 to-pink-600"}
            ].map((item, i) => (
              <div key={i} className={`relative bg-white rounded-3xl p-8 shadow-lg transform hover:scale-105 transition-all duration-300 ${item.popular ? 'ring-4 ring-brand/20 shadow-2xl' : ''}`}>
                {item.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="bg-gradient-to-r from-brand to-purple-600 text-white px-6 py-2 rounded-full text-sm font-bold">Most Popular</span>
                  </div>
                )}
                <div className={`inline-flex items-center justify-center w-12 h-12 rounded-full bg-gradient-to-r ${item.gradient} text-white text-xl mb-6`}>
                  {i === 0 ? '💡' : i === 1 ? '🚀' : '👑'}
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-6">{item.plan.title}</h3>
                <ul className="space-y-3 mb-8">
                  {item.plan.bullets.map((bullet, idx) => (
                    <li key={idx} className="flex items-start gap-3">
                      <span className="text-green-500 text-lg">✓</span>
                      <span className="text-gray-600">{bullet}</span>
                    </li>
                  ))}
                </ul>
                <button className={`w-full py-4 px-6 rounded-xl font-bold transition-all duration-300 ${item.popular ? 'bg-gradient-to-r from-brand to-purple-600 text-white hover:shadow-lg transform hover:scale-105' : 'border-2 border-gray-300 text-gray-700 hover:border-brand hover:text-brand'}`}>
                  Get Started
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* SEO Features */}
      <section className="py-24 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">{t.seoTipsTitle}</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">Advanced SEO tools to maximize your online visibility</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {t.seoTipsItems.map((tip, i) => (
              <div key={i} className="group bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300">
                <div className="flex items-center gap-4 mb-4">
                  <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-r from-green-500 to-blue-500 rounded-full flex items-center justify-center text-white text-xl group-hover:animate-pulse">
                    {i === 0 ? '👀' : i === 1 ? '📊' : '⚙️'}
                  </div>
                  <h3 className="font-bold text-gray-900">SEO Feature</h3>
                </div>
                <p className="text-gray-600 leading-relaxed">{tip}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-24 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">{t.faqTitle}</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">Everything you need to know to get started</p>
          </div>
          
          <div className="max-w-4xl mx-auto space-y-6">
            {t.faq.map((item, i) => (
              <div key={i} className="bg-gray-50 rounded-2xl p-6 hover:bg-gray-100 transition-all duration-300">
                <h3 className="text-lg font-bold text-gray-900 mb-3">{item.q}</h3>
                <p className="text-gray-600 leading-relaxed">{item.a}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="py-24 bg-gradient-to-br from-brand via-purple-600 to-indigo-800 relative overflow-hidden">
        <div className="absolute inset-0">
          <div className="absolute top-10 right-10 w-32 h-32 bg-white/10 rounded-full animate-pulse"></div>
          <div className="absolute bottom-10 left-10 w-24 h-24 bg-white/5 rounded-full animate-bounce"></div>
        </div>
        
        <div className="container mx-auto px-4 relative z-10">
          <div className="text-center text-white max-w-4xl mx-auto">
            <h2 className="text-4xl md:text-6xl font-bold mb-6">{t.finalCtaTitle}</h2>
            <p className="text-xl md:text-2xl text-white/90 mb-12 leading-relaxed">{t.finalCtaBody}</p>
            <Link 
              href={`/${params.lang}/advertise`}
              className="group bg-white text-brand hover:bg-gray-100 font-bold text-lg px-12 py-6 rounded-2xl shadow-2xl transform hover:scale-110 transition-all duration-300 flex items-center justify-center gap-3 inline-flex"
            >
              <span className="group-hover:animate-bounce">🎯</span>
              {t.finalCtaButton}
            </Link>
          </div>
        </div>
      </section>

      {/* Latest Articles Section */}
      <BlogPostsFooter lang={params.lang} limit={6} />
    </div>
  );
}