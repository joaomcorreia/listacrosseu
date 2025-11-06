'use client';

import { useState } from 'react';

interface WhyChooseSectionProps {
  lang: string;
  ui: any;
}

export function WhyChooseSection({ lang, ui }: WhyChooseSectionProps) {
  const [activeFeature, setActiveFeature] = useState(0);

  const features = [
    {
      title: 'Verified Business Information',
      description: 'Every business listing is verified and regularly updated to ensure accuracy and reliability.',
      icon: '✓',
      color: 'from-green-500 to-emerald-600',
      stats: '99.2% Accuracy Rate',
      details: [
        'Manual verification process',
        'Regular data updates',
        'Contact information validation',
        'Business status monitoring'
      ]
    },
    {
      title: 'Complete EU Coverage',
      description: 'Access businesses across all 27 EU member states through one unified platform.',
      icon: '🇪🇺',
      color: 'from-blue-500 to-blue-600',
      stats: '27 Countries',
      details: [
        'All EU member states',
        'Multi-language support',
        'Local business insights',
        'Cultural adaptability'
      ]
    },
    {
      title: 'Advanced Search & Filters',
      description: 'Find exactly what you need with sophisticated search tools and smart filtering options.',
      icon: '🔍',
      color: 'from-purple-500 to-purple-600',
      stats: '50+ Filter Options',
      details: [
        'Location-based search',
        'Category refinement',
        'Rating and review filters',
        'Availability status'
      ]
    },
    {
      title: 'Free Basic Listings',
      description: 'Get your business discovered across Europe at no cost with our comprehensive free tier.',
      icon: '🆓',
      color: 'from-yellow-500 to-orange-500',
      stats: 'Always Free',
      details: [
        'No setup fees',
        'Basic business profile',
        'Contact information display',
        'Category placement'
      ]
    },
    {
      title: 'Mobile-Optimized Experience',
      description: 'Seamlessly browse and manage listings on any device with our responsive design.',
      icon: '📱',
      color: 'from-indigo-500 to-indigo-600',
      stats: '98% Mobile Score',
      details: [
        'Responsive design',
        'Touch-friendly interface',
        'Offline capabilities',
        'Fast loading times'
      ]
    },
    {
      title: '24/7 Customer Support',
      description: 'Get help when you need it with our dedicated multilingual support team.',
      icon: '🎧',
      color: 'from-red-500 to-pink-500',
      stats: '<2min Response',
      details: [
        'Multilingual support',
        'Live chat available',
        'Email assistance',
        'Phone support (premium)'
      ]
    }
  ];

  const testimonials = [
    {
      name: 'Maria González',
      role: 'Restaurant Owner, Madrid',
      content: 'ListAcross EU helped us connect with tourists and locals alike. Our visibility increased by 300% in just 3 months.',
      rating: 5,
      avatar: '👩‍🍳'
    },
    {
      name: 'Klaus Weber',
      role: 'Tech Consultant, Berlin',
      content: 'The platform made it incredibly easy to expand my services across Europe. I now have clients in 8 different countries.',
      rating: 5,
      avatar: '👨‍💻'
    },
    {
      name: 'Sophie Dubois',
      role: 'Boutique Owner, Paris',
      content: 'The verification process gave me confidence, and the multilingual support helped me reach international customers.',
      rating: 5,
      avatar: '👩‍💼'
    }
  ];

  return (
    <section className="py-24 bg-white relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-5">
        <div className="absolute inset-0" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23004494' fill-opacity='1' fill-rule='evenodd'/%3E%3C/svg%3E")`,
        }} />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-20">
          <h2 className="text-5xl font-bold text-gray-900 mb-6">
            Why Choose ListAcross EU?
          </h2>
          <p className="text-xl text-gray-600 max-w-4xl mx-auto leading-relaxed">
            We're not just another business directory. We're your gateway to European commerce, built by Europeans for Europeans, with the features that matter most.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-20">
          {features.map((feature, index) => (
            <div
              key={index}
              className={`group relative p-8 bg-white rounded-2xl border-2 border-gray-100 hover:border-blue-300 shadow-lg hover:shadow-2xl transform hover:-translate-y-2 transition-all duration-300 cursor-pointer animate-fade-in-up ${
                activeFeature === index ? 'ring-4 ring-blue-500 ring-opacity-50' : ''
              }`}
              style={{ animationDelay: `${index * 100}ms` }}
              onClick={() => setActiveFeature(index)}
            >
              {/* Icon Background */}
              <div className={`absolute top-4 right-4 w-12 h-12 rounded-full bg-gradient-to-r ${feature.color} flex items-center justify-center text-white font-bold text-xl shadow-lg`}>
                {feature.icon}
              </div>

              {/* Content */}
              <div className="space-y-4">
                <h3 className="text-xl font-bold text-gray-900 group-hover:text-blue-600 transition-colors duration-300 pr-16">
                  {feature.title}
                </h3>
                
                <p className="text-gray-600 leading-relaxed">
                  {feature.description}
                </p>

                {/* Stats Badge */}
                <div className={`inline-flex items-center px-4 py-2 rounded-full bg-gradient-to-r ${feature.color} text-white text-sm font-semibold shadow-md`}>
                  {feature.stats}
                </div>

                {/* Feature Details */}
                <div className="space-y-2">
                  {feature.details.map((detail, detailIndex) => (
                    <div key={detailIndex} className="flex items-center text-sm text-gray-500">
                      <div className="w-1.5 h-1.5 bg-blue-500 rounded-full mr-3" />
                      {detail}
                    </div>
                  ))}
                </div>
              </div>

              {/* Hover Effect */}
              <div className={`absolute inset-0 rounded-2xl bg-gradient-to-r ${feature.color} opacity-0 group-hover:opacity-5 transition-opacity duration-300`} />
            </div>
          ))}
        </div>

        {/* Testimonials Section */}
        <div className="bg-gradient-to-r from-blue-50 to-yellow-50 rounded-3xl p-12 border border-blue-100">
          <div className="text-center mb-12">
            <h3 className="text-3xl font-bold text-gray-900 mb-4">
              What Our Users Say
            </h3>
            <p className="text-lg text-gray-600">
              Real experiences from businesses across Europe
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div
                key={index}
                className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow duration-300 animate-fade-in-up"
                style={{ animationDelay: `${index * 200}ms` }}
              >
                {/* Rating Stars */}
                <div className="flex items-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <svg key={i} className="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                    </svg>
                  ))}
                </div>

                {/* Testimonial Content */}
                <blockquote className="text-gray-700 italic mb-4 leading-relaxed">
                  "{testimonial.content}"
                </blockquote>

                {/* Author */}
                <div className="flex items-center">
                  <div className="text-3xl mr-3">
                    {testimonial.avatar}
                  </div>
                  <div>
                    <div className="font-semibold text-gray-900">
                      {testimonial.name}
                    </div>
                    <div className="text-sm text-gray-500">
                      {testimonial.role}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Trust Indicators */}
          <div className="mt-12 grid grid-cols-2 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600 mb-2">4.8/5</div>
              <div className="text-sm text-gray-600">Average Rating</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600 mb-2">50K+</div>
              <div className="text-sm text-gray-600">Happy Businesses</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600 mb-2">2M+</div>
              <div className="text-sm text-gray-600">Monthly Searches</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600 mb-2">27</div>
              <div className="text-sm text-gray-600">Countries Covered</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}