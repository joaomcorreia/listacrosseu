'use client';

import DjangoAdmin from '@/components/DjangoAdmin';
import { Metadata } from 'next';

export default function DjangoAdminPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Django Admin</h1>
          <p className="mt-1 text-sm text-gray-600">
            Full Django administration interface with all models and settings.
          </p>
        </div>
        
        <div className="flex space-x-3">
          <a
            href="http://127.0.0.1:8000/admin/"
            target="_blank"
            rel="noopener noreferrer"
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
          >
            Open in New Tab
          </a>
        </div>
      </div>

      {/* Quick Access Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Users & Accounts</h3>
          <p className="text-gray-600 text-sm mb-4">Manage user profiles, permissions, and authentication.</p>
          <a 
            href="http://127.0.0.1:8000/admin/accounts/" 
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:text-blue-800 text-sm font-medium"
          >
            Manage Users →
          </a>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Business Listings</h3>
          <p className="text-gray-600 text-sm mb-4">Add, edit, and manage business listings and categories.</p>
          <a 
            href="http://127.0.0.1:8000/admin/listings/" 
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:text-blue-800 text-sm font-medium"
          >
            Manage Listings →
          </a>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">SEO Settings</h3>
          <p className="text-gray-600 text-sm mb-4">Configure global SEO settings and meta information.</p>
          <a 
            href="http://127.0.0.1:8000/admin/seo/" 
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:text-blue-800 text-sm font-medium"
          >
            Manage SEO →
          </a>
        </div>
      </div>

      {/* Embedded Django Admin */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b">
          <h2 className="text-lg font-semibold text-gray-900">Full Django Admin Interface</h2>
          <p className="text-sm text-gray-600 mt-1">
            Complete Django administration panel embedded in the Next.js admin interface.
          </p>
        </div>
        
        <div className="p-6">
          <DjangoAdmin height="600px" />
        </div>
      </div>
    </div>
  );
}