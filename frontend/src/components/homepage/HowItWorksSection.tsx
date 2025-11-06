'use client';

interface HowItWorksSectionProps {
  lang: string;
  ui: any;
}

export function HowItWorksSection({ lang, ui }: HowItWorksSectionProps) {
  const steps = [
    {
      number: 1,
      icon: '🔍',
      title: 'Search',
      description: 'Find businesses by country, city, or category across all EU nations',
      color: 'from-blue-500 to-blue-600',
      delay: 0,
    },
    {
      number: 2,
      icon: '🤝',
      title: 'Connect',
      description: 'Contact or visit them directly with verified contact information',
      color: 'from-green-500 to-green-600',
      delay: 200,
    },
    {
      number: 3,
      icon: '📈',
      title: 'Grow',
      description: 'List your business and expand your reach across Europe',
      color: 'from-yellow-500 to-yellow-600',
      delay: 400,
    },
  ];

  return (
    <section className="py-24 bg-white relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-5">
        <div className="absolute inset-0" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23004494' fill-opacity='1'%3E%3Ccircle cx='30' cy='30' r='4'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
        }} />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-20">
          <h2 className="text-5xl font-bold text-gray-900 mb-6">
            How It Works
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Connect with European businesses in three simple steps. Our platform makes it easy to discover, connect, and grow across 27 EU countries.
          </p>
        </div>

        {/* Steps */}
        <div className="relative">
          {/* Connection Line */}
          <div className="hidden md:block absolute top-1/2 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 via-green-500 to-yellow-500 transform -translate-y-1/2 opacity-20" />
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12 relative z-10">
            {steps.map((step, index) => (
              <div
                key={step.number}
                className="group text-center animate-fade-in-up"
                style={{ animationDelay: `${step.delay}ms` }}
              >
                {/* Step Number & Icon Container */}
                <div className="relative mb-8">
                  {/* Step Number Background */}
                  <div className={`mx-auto w-24 h-24 rounded-full bg-gradient-to-br ${step.color} flex items-center justify-center shadow-2xl group-hover:scale-110 transform transition-all duration-300`}>
                    <span className="text-3xl">{step.icon}</span>
                  </div>
                  
                  {/* Step Number Badge */}
                  <div className="absolute -top-2 -right-2 w-8 h-8 bg-white border-4 border-gray-100 rounded-full flex items-center justify-center shadow-lg">
                    <span className="text-sm font-bold text-gray-800">{step.number}</span>
                  </div>

                  {/* Animated Ring */}
                  <div className={`absolute inset-0 rounded-full border-4 border-transparent bg-gradient-to-br ${step.color} opacity-20 group-hover:opacity-40 animate-pulse`} />
                </div>

                {/* Content */}
                <div className="space-y-4">
                  <h3 className="text-2xl font-bold text-gray-900 group-hover:text-blue-600 transition-colors duration-300">
                    {step.title}
                  </h3>
                  <p className="text-gray-600 leading-relaxed max-w-sm mx-auto">
                    {step.description}
                  </p>
                </div>

                {/* Connecting Arrow (Desktop) */}
                {index < steps.length - 1 && (
                  <div className="hidden md:block absolute top-12 -right-6 text-gray-300 group-hover:text-blue-500 transition-colors duration-300">
                    <svg className="w-12 h-6" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                    </svg>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Encouragement Paragraph */}
        <div className="mt-20 text-center">
          <div className="bg-gradient-to-r from-blue-50 to-yellow-50 rounded-2xl p-8 border border-blue-100">
            <h3 className="text-2xl font-semibold text-gray-900 mb-4">
              Ready to Connect Across Europe?
            </h3>
            <p className="text-lg text-gray-700 max-w-4xl mx-auto leading-relaxed mb-8">
              Join thousands of businesses and customers who trust ListAcross EU to bridge connections across European markets. Whether you're searching for services or promoting your business, we make European commerce simple and accessible.
            </p>
            
            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="px-8 py-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white font-semibold rounded-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300">
                Start Searching Now
              </button>
              <button className="px-8 py-3 bg-white border-2 border-blue-600 text-blue-600 font-semibold rounded-lg hover:bg-blue-50 transform hover:scale-105 transition-all duration-300">
                List Your Business
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}