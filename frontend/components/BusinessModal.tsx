'use client';

import Modal from './Modal';
import { Business } from '../lib/api';
import { translate, Language } from '../lib/i18n';

interface BusinessModalProps {
  business: Business | null;
  isOpen: boolean;
  onClose: () => void;
  lang: Language;
}

export default function BusinessModal({ business, isOpen, onClose, lang }: BusinessModalProps) {
  if (!business) return null;

  const getBusinessUrl = () => {
    return `/${lang}/business/${business.slug}`;
  };

  const generateAvatar = (name: string) => {
    const initials = name.split(' ').map(word => word[0]).join('').substring(0, 2).toUpperCase();
    const colors = [
      'bg-blue-500', 'bg-green-500', 'bg-purple-500', 'bg-pink-500', 'bg-indigo-500',
      'bg-red-500', 'bg-yellow-500', 'bg-teal-500', 'bg-orange-500', 'bg-cyan-500'
    ];
    const colorIndex = name.length % colors.length;
    return { initials, color: colors[colorIndex] };
  };

  const getRandomRating = () => {
    return (4 + Math.random()).toFixed(1);
  };

  const avatar = generateAvatar(business.name);
  const rating = getRandomRating();
  const reviews = 25 + Math.floor(Math.random() * 50);

  return (
    <Modal isOpen={isOpen} onClose={onClose} size="xl">
      <div className="max-h-[80vh] overflow-y-auto">
        {/* Header Section */}
        <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-blue-800 text-white p-6 rounded-t-2xl">
          <div className="flex items-start space-x-4">
            {/* Avatar */}
            <div className={`${avatar.color} w-16 h-16 rounded-xl flex items-center justify-center text-white font-bold text-lg shadow-lg`}>
              {avatar.initials}
            </div>
            
            {/* Business Info */}
            <div className="flex-1">
              <h1 className="text-2xl font-bold mb-2">{business.name}</h1>
              <div className="flex items-center space-x-4 text-blue-100">
                <div className="flex items-center space-x-1">
                  <span className="text-yellow-400">⭐</span>
                  <span className="font-medium">{rating}</span>
                  <span className="text-sm">({reviews} reviews)</span>
                </div>
                <div className="flex items-center space-x-1">
                  <span>📍</span>
                  <span className="text-sm">{business.city_name}, {business.country_id}</span>
                </div>
              </div>
            </div>
            
            {/* Category Badge */}
            <div className="bg-white bg-opacity-20 backdrop-blur-sm px-3 py-1 rounded-full text-sm font-medium">
              Business
            </div>
          </div>
        </div>

        {/* Content Section */}
        <div className="p-6 space-y-6">
          {/* Description */}
          <div className="bg-gray-50 p-4 rounded-xl">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">About</h3>
            <p className="text-gray-700 leading-relaxed">
              A professional business providing quality services in {business.city_name}. 
              Contact us for more information about our services and how we can help you.
            </p>
          </div>

          {/* Contact Information */}
          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Contact Information</h3>
              
              {/* Address */}
              <div className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                <div className="text-gray-500 mt-0.5">📍</div>
                <div>
                  <div className="font-medium text-gray-900">Address</div>
                  <div className="text-gray-600 text-sm">
                    {business.street && <div>{business.street}</div>}
                    {business.postcode && <div>{business.postcode}</div>}
                    <div>{business.city_name}, {business.country_id}</div>
                  </div>
                </div>
              </div>

              {/* Phone */}
              {business.phone && (
                <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                  <div className="text-gray-500">📞</div>
                  <div>
                    <div className="font-medium text-gray-900">Phone</div>
                    <a href={`tel:${business.phone}`} className="text-blue-600 hover:text-blue-800 text-sm">
                      {business.phone}
                    </a>
                  </div>
                </div>
              )}

              {/* Email */}
              {business.email && (
                <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                  <div className="text-gray-500">✉️</div>
                  <div>
                    <div className="font-medium text-gray-900">Email</div>
                    <a href={`mailto:${business.email}`} className="text-blue-600 hover:text-blue-800 text-sm">
                      {business.email}
                    </a>
                  </div>
                </div>
              )}

              {/* Website */}
              {business.website && (
                <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                  <div className="text-gray-500">🌐</div>
                  <div>
                    <div className="font-medium text-gray-900">Website</div>
                    <a 
                      href={business.website} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:text-blue-800 text-sm"
                    >
                      {business.website.replace(/^https?:\/\//, '')}
                    </a>
                  </div>
                </div>
              )}
            </div>

            {/* Additional Info */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Business Details</h3>
              
              {/* Business Hours */}
              <div className="p-4 bg-green-50 rounded-lg">
                <div className="flex items-center space-x-2 mb-2">
                  <span className="text-green-600">🕒</span>
                  <span className="font-medium text-gray-900">Business Hours</span>
                </div>
                <div className="text-sm text-gray-600">
                  <div>Mon - Fri: 9:00 AM - 6:00 PM</div>
                  <div>Saturday: 10:00 AM - 4:00 PM</div>
                  <div>Sunday: Closed</div>
                </div>
              </div>

              {/* Services */}
              <div className="p-4 bg-blue-50 rounded-lg">
                <div className="flex items-center space-x-2 mb-2">
                  <span className="text-blue-600">⚙️</span>
                  <span className="font-medium text-gray-900">Services</span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {['Consultation', 'Support', 'Delivery', 'Warranty'].map((service) => (
                    <span key={service} className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                      {service}
                    </span>
                  ))}
                </div>
              </div>

              {/* Payment Methods */}
              <div className="p-4 bg-purple-50 rounded-lg">
                <div className="flex items-center space-x-2 mb-2">
                  <span className="text-purple-600">💳</span>
                  <span className="font-medium text-gray-900">Payment Methods</span>
                </div>
                <div className="text-sm text-gray-600">
                  Credit Cards, Cash, Bank Transfer
                </div>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-3 pt-4 border-t border-gray-100">
            <a
              href={getBusinessUrl()}
              className="flex-1 bg-gradient-to-r from-blue-600 to-blue-700 text-white py-3 px-6 rounded-xl font-medium text-center hover:from-blue-700 hover:to-blue-800 transition-all duration-200 shadow-sm hover:shadow-md"
              onClick={onClose}
            >
              View Full Page
            </a>
            
            {business.phone && (
              <button
                onClick={() => window.open(`tel:${business.phone}`, '_self')}
                className="bg-green-600 text-white py-3 px-6 rounded-xl font-medium hover:bg-green-700 transition-all duration-200 flex items-center space-x-2"
              >
                <span>📞</span>
                <span>Call Now</span>
              </button>
            )}
            
            {business.website && (
              <button
                onClick={() => window.open(business.website, '_blank', 'noopener,noreferrer')}
                className="bg-slate-600 text-white py-3 px-6 rounded-xl font-medium hover:bg-slate-700 transition-all duration-200 flex items-center space-x-2"
              >
                <span>🌐</span>
                <span>Visit Website</span>
              </button>
            )}
          </div>
        </div>
      </div>
    </Modal>
  );
}