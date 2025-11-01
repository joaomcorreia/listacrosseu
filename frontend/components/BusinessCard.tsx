'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Business } from '../lib/api';
import { Language, translate } from '../lib/i18n';
import BusinessModal from './BusinessModal';

interface BusinessCardProps {
  business: Business;
  lang: Language;
  variant?: 'default' | 'featured' | 'compact';
}

export default function BusinessCard({ business, lang, variant = 'default' }: BusinessCardProps) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  const getBusinessUrl = () => {
    // For now, just use the name as ID - in future you might want a proper business page
    return `/${lang}/business/${business.slug}`;
  };

  const getCategoryTags = () => {
    // This would come from the business.categories in a real implementation
    // For now, we'll use some sample tags
    return ['Professional Services', 'Finance']; // Placeholder
  };

  const getRandomRating = () => {
    // In a real app, this would come from business.rating
    return (4 + Math.random()).toFixed(1);
  };

  const formatPhoneNumber = (phone: string) => {
    // Simple phone formatting - could be more sophisticated
    return phone.replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3');
  };

  if (variant === 'compact') {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-4 hover:shadow-md transition-all duration-300 hover:-translate-y-1">
        <div className="flex items-start justify-between mb-3">
          <h3 className="font-semibold text-slate-900 text-sm leading-tight">
            {business.name}
          </h3>
          <div className="flex items-center text-xs">
            <span className="text-amber-500">★</span>
            <span className="ml-1 text-slate-600">{getRandomRating()}</span>
          </div>
        </div>
        
        {business.street && (
          <p className="text-xs text-slate-500 mb-2 flex items-center">
            <span className="mr-1">📍</span>
            {business.street}
          </p>
        )}
        
        <Link
          href={getBusinessUrl()}
          className="text-xs text-blue-600 hover:text-blue-700 font-medium"
        >
          {translate('common.view', lang)} →
        </Link>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-2xl shadow-lg border border-slate-100 overflow-hidden transition-all duration-300 hover:shadow-xl hover:-translate-y-2 group ${
      variant === 'featured' ? 'ring-2 ring-blue-500/20' : ''
    }`}>
      {/* Header */}
      <div className="p-6 pb-4">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h3 className="text-xl font-bold text-slate-900 mb-2 group-hover:text-blue-600 transition-colors">
              {business.name}
            </h3>
            
            {/* Rating */}
            <div className="flex items-center space-x-2 mb-3">
              <div className="flex items-center">
                {[...Array(5)].map((_, i) => (
                  <span 
                    key={i} 
                    className={`text-sm ${i < Math.floor(parseFloat(getRandomRating())) ? 'text-amber-400' : 'text-gray-300'}`}
                  >
                    ★
                  </span>
                ))}
              </div>
              <span className="text-sm font-medium text-slate-700">{getRandomRating()}</span>
              <span className="text-sm text-slate-500">(42 reviews)</span>
            </div>
            
            {/* Category Tags */}
            <div className="flex flex-wrap gap-2 mb-4">
              {getCategoryTags().slice(0, 2).map((tag, index) => (
                <span 
                  key={index}
                  className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                >
                  {tag}
                </span>
              ))}
            </div>
          </div>
          
          {/* Business Avatar */}
          <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center text-white font-bold text-xl shadow-md">
            {business.name.charAt(0).toUpperCase()}
          </div>
        </div>
      </div>

      {/* Contact Information */}
      <div className="px-6 pb-4 space-y-3">
        {business.street && (
          <div className="flex items-start space-x-3 text-slate-600">
            <div className="w-8 h-8 bg-slate-100 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5">
              <span className="text-sm">📍</span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-slate-700">Address</p>
              <p className="text-sm text-slate-600 break-words">{business.street}</p>
              {business.city_name && business.country_id && (
                <p className="text-xs text-slate-500 mt-1">
                  {business.city_name}, {business.country_id}
                </p>
              )}
            </div>
          </div>
        )}

        {business.phone && (
          <div className="flex items-center space-x-3 text-slate-600">
            <div className="w-8 h-8 bg-slate-100 rounded-lg flex items-center justify-center flex-shrink-0">
              <span className="text-sm">📞</span>
            </div>
            <div className="flex-1">
              <p className="text-sm font-medium text-slate-700">Phone</p>
              <a 
                href={`tel:${business.phone}`}
                className="text-sm text-blue-600 hover:text-blue-700 font-medium"
              >
                {formatPhoneNumber(business.phone)}
              </a>
            </div>
          </div>
        )}

        {business.email && (
          <div className="flex items-center space-x-3 text-slate-600">
            <div className="w-8 h-8 bg-slate-100 rounded-lg flex items-center justify-center flex-shrink-0">
              <span className="text-sm">✉️</span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-slate-700">Email</p>
              <a 
                href={`mailto:${business.email}`}
                className="text-sm text-blue-600 hover:text-blue-700 font-medium break-all"
              >
                {business.email}
              </a>
            </div>
          </div>
        )}

        {business.website && (
          <div className="flex items-center space-x-3 text-slate-600">
            <div className="w-8 h-8 bg-slate-100 rounded-lg flex items-center justify-center flex-shrink-0">
              <span className="text-sm">🌐</span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-slate-700">Website</p>
              <a 
                href={business.website}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-blue-600 hover:text-blue-700 font-medium break-all"
              >
                {business.website.replace(/^https?:\/\//, '')} ↗
              </a>
            </div>
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="px-6 pb-6">
        <div className="flex space-x-3">
          <button
            onClick={() => setIsModalOpen(true)}
            className="flex-1 bg-gradient-to-r from-blue-600 to-blue-700 text-white py-3 px-4 rounded-xl font-medium text-center hover:from-blue-700 hover:to-blue-800 transition-all duration-200 shadow-sm hover:shadow-md transform hover:-translate-y-0.5"
          >
            {translate('common.view', lang)} Details
          </button>
          
          {business.phone && (
            <button
              onClick={() => window.open(`tel:${business.phone}`, '_self')}
              className="bg-green-100 text-green-700 py-3 px-4 rounded-xl font-medium hover:bg-green-200 transition-all duration-200 flex items-center justify-center"
              title={translate('common.phone', lang)}
            >
              📞
            </button>
          )}
          
          {business.website && (
            <button
              onClick={() => window.open(business.website, '_blank', 'noopener,noreferrer')}
              className="bg-slate-100 text-slate-700 py-3 px-4 rounded-xl font-medium hover:bg-slate-200 transition-all duration-200 flex items-center justify-center"
              title={translate('common.website', lang)}
            >
              🌐
            </button>
          )}
        </div>
      </div>

      {/* Featured Badge */}
      {variant === 'featured' && (
        <div className="absolute top-4 right-4">
          <div className="bg-gradient-to-r from-amber-400 to-amber-500 text-white text-xs font-bold px-2 py-1 rounded-full">
            ⭐ Featured
          </div>
        </div>
      )}

      {/* Business Modal - Rendered outside card container */}
      {isModalOpen && (
        <BusinessModal
          business={business}
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          lang={lang}
        />
      )}
    </div>
  );
}