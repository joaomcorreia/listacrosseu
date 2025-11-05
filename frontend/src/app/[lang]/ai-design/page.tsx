import AIDesignGenerator from '@/components/AIDesignGenerator';

export default function AIDesignPage({ params }: { params: { lang: string } }) {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-brand via-purple-600 to-indigo-800 relative overflow-hidden pt-24 pb-16">
        {/* Animated Background Elements */}
        <div className="absolute inset-0">
          <div className="absolute top-20 left-10 w-32 h-32 bg-white/10 rounded-full animate-pulse"></div>
          <div className="absolute top-40 right-20 w-24 h-24 bg-white/5 rounded-full animate-bounce" style={{ animationDelay: '1s' }}></div>
          <div className="absolute bottom-20 left-1/4 w-40 h-40 bg-white/5 rounded-full animate-pulse" style={{ animationDelay: '2s' }}></div>
          
          {/* AI Brain Animation */}
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 border-4 border-white/10 rounded-full animate-spin" style={{ animationDuration: '20s' }}></div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-48 h-48 border-4 border-white/20 rounded-full animate-spin" style={{ animationDuration: '15s', animationDirection: 'reverse' }}></div>
        </div>
        
        <div className="container mx-auto px-4 py-16 relative z-10 text-center text-white">
          <div className="inline-flex items-center bg-white/20 backdrop-blur-sm border border-white/30 rounded-full px-6 py-3 mb-8 animate-fade-in-up">
            <span className="text-sm text-white/90">🤖 Powered by GPT-4 AI Technology</span>
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold mb-6 animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
            AI Design 
            <span className="block bg-gradient-to-r from-yellow-300 via-white to-blue-300 bg-clip-text text-transparent">
              Generator
            </span>
          </h1>
          
          <p className="text-xl text-white/90 mb-12 max-w-4xl mx-auto leading-relaxed animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
            Create custom components for your European business directory using AI. 
            Describe what you want, and we'll generate beautiful, responsive designs with Tailwind CSS.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-6 justify-center animate-fade-in-up" style={{ animationDelay: '0.6s' }}>
            <div className="bg-white/20 backdrop-blur-sm border border-white/30 rounded-2xl px-6 py-4 flex items-center gap-3">
              <span className="text-2xl">⚡</span>
              <span>Instant Generation</span>
            </div>
            <div className="bg-white/20 backdrop-blur-sm border border-white/30 rounded-2xl px-6 py-4 flex items-center gap-3">
              <span className="text-2xl">🎨</span>
              <span>Professional Design</span>
            </div>
            <div className="bg-white/20 backdrop-blur-sm border border-white/30 rounded-2xl px-6 py-4 flex items-center gap-3">
              <span className="text-2xl">📱</span>
              <span>Responsive Code</span>
            </div>
          </div>
        </div>
      </section>

      {/* AI Generator Section */}
      <section className="py-20 bg-white relative">
        <div className="absolute top-0 left-0 w-full h-32 bg-gradient-to-b from-brand/5 to-transparent"></div>
        <div className="container mx-auto px-4 relative z-10">
          <AIDesignGenerator lang={params.lang} />
        </div>
      </section>
    </div>
  );
}