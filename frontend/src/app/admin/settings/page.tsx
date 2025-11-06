'use client';
import React, { useState, useEffect } from 'react';

interface SiteSettings {
  siteName: string;
  siteDescription: string;
  contactEmail: string;
  supportEmail: string;
  defaultLanguage: string;
  languageSelectorDisplay: 'flags' | 'codes' | 'flags-and-codes';
  enableRegistration: boolean;
  enableComments: boolean;
  maintenanceMode: boolean;
  enableStarAnimation: boolean;
  analyticsCode: string;
  branding: {
    logo: string;
    favicon: string;
    footerLogo: string;
  };
  socialLinks: {
    facebook: string;
    twitter: string;
    linkedin: string;
    instagram: string;
  };
  seoSettings: {
    defaultTitle: string;
    defaultDescription: string;
    defaultKeywords: string;
    ogImageUrl: string;
  };
}

export default function SettingsPage() {
  const [settings, setSettings] = useState<SiteSettings>({
    siteName: 'ListAcross EU',
    siteDescription: 'The premier business directory for European markets',
    contactEmail: 'contact@listacrosseu.com',
    supportEmail: 'support@listacrosseu.com',
    defaultLanguage: 'eu',
    languageSelectorDisplay: 'flags',
    enableRegistration: true,
    enableComments: true,
    maintenanceMode: false,
    enableStarAnimation: true,
    analyticsCode: '',
    branding: {
      logo: '',
      favicon: '',
      footerLogo: ''
    },
    socialLinks: {
      facebook: '',
      twitter: '',
      linkedin: '',
      instagram: ''
    },
    seoSettings: {
      defaultTitle: 'ListAcross EU - European Business Directory',
      defaultDescription: 'Discover and connect with businesses across Europe. Find services, products, and opportunities in the European market.',
      defaultKeywords: 'business directory, Europe, listings, companies, services',
      ogImageUrl: ''
    }
  });

  const [activeTab, setActiveTab] = useState<'general' | 'branding' | 'social' | 'seo' | 'advanced'>('general');
  const [isSaving, setIsSaving] = useState(false);

  const handleInputChange = (field: keyof SiteSettings, value: any) => {
    setSettings(prev => ({ ...prev, [field]: value }));
  };

  const handleNestedChange = (parent: 'socialLinks' | 'seoSettings' | 'branding', field: string, value: string) => {
    setSettings(prev => ({
      ...prev,
      [parent]: { ...prev[parent], [field]: value }
    }));
  };

  const handleFileUpload = (field: 'logo' | 'favicon' | 'footerLogo', event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const result = e.target?.result as string;
        handleNestedChange('branding', field, result);
      };
      reader.readAsDataURL(file);
    }
  };

  // Load settings on component mount
  useEffect(() => {
    loadSettings();
  }, []);

  const getCsrfToken = async () => {
    try {
      const response = await fetch('/api/v1/csrf-token/');
      const data = await response.json();
      return data.csrf_token;
    } catch (error) {
      console.error('Error getting CSRF token:', error);
      return null;
    }
  };

  const loadSettings = async () => {
    try {
      const response = await fetch('/api/v1/core/settings/', {
        credentials: 'include'
      });
      if (response.ok) {
        const data = await response.json();
        if (data.ok) {
          setSettings(data.settings);
        }
      } else if (response.status === 401 || response.status === 403) {
        // User is not authenticated, redirect to Django admin login
        window.location.href = '/django-admin/login/?next=/admin/settings';
      }
    } catch (error) {
      console.error('Error loading settings:', error);
    }
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
      const csrfToken = await getCsrfToken();
      const response = await fetch('/api/v1/core/settings/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken || '',
        },
        credentials: 'include',
        body: JSON.stringify(settings),
      });
      
      if (response.status === 401 || response.status === 403) {
        // User is not authenticated, redirect to Django admin login
        window.location.href = '/django-admin/login/?next=/admin/settings';
        return;
      }
      
      const data = await response.json();
      
      if (data.ok) {
        alert('Settings saved successfully!');
        // Optionally reload settings to get any server-side updates
        await loadSettings();
      } else {
        alert('Error saving settings: ' + (data.error || 'Unknown error'));
      }
    } catch (error) {
      console.error('Error saving settings:', error);
      alert('Error saving settings');
    } finally {
      setIsSaving(false);
    }
  };

  const tabs = [
    { id: 'general', label: 'General', icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z' },
    { id: 'branding', label: 'Branding', icon: 'M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z' },
    { id: 'social', label: 'Social Media', icon: 'M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3z' },
    { id: 'seo', label: 'SEO', icon: 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z' },
    { id: 'advanced', label: 'Advanced', icon: 'M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4' }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Settings</h1>
          <p className="mt-1 text-sm text-gray-600">Manage your website configuration and preferences</p>
        </div>
        <button
          onClick={handleSave}
          disabled={isSaving}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {isSaving ? 'Saving...' : 'Save Changes'}
        </button>
      </div>

      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={tab.icon} />
              </svg>
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="bg-white rounded-lg shadow p-6">
        {activeTab === 'general' && (
          <div className="space-y-6">
            <h3 className="text-lg font-medium">General Settings</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Site Name</label>
                <input
                  type="text"
                  value={settings.siteName}
                  onChange={(e) => handleInputChange('siteName', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Default Language</label>
                <select
                  value={settings.defaultLanguage}
                  onChange={(e) => handleInputChange('defaultLanguage', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="eu">European Union</option>
                  <option value="en">English</option>
                  <option value="fr">French</option>
                  <option value="nl">Dutch</option>
                  <option value="pt">Portuguese</option>
                  <option value="de">German</option>
                  <option value="es">Spanish</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Site Description</label>
              <textarea
                value={settings.siteDescription}
                onChange={(e) => handleInputChange('siteDescription', e.target.value)}
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Contact Email</label>
                <input
                  type="email"
                  value={settings.contactEmail}
                  onChange={(e) => handleInputChange('contactEmail', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Support Email</label>
                <input
                  type="email"
                  value={settings.supportEmail}
                  onChange={(e) => handleInputChange('supportEmail', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            {/* Language Selector Display Settings */}
            <div className="border-t border-gray-200 pt-6">
              <h4 className="text-md font-medium text-gray-900 mb-4">Language Selector Display</h4>
              <p className="text-sm text-gray-600 mb-4">Choose how the language selector appears in the main navigation</p>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Display Style</label>
                <select
                  value={settings.languageSelectorDisplay}
                  onChange={(e) => handleInputChange('languageSelectorDisplay', e.target.value)}
                  className="w-full max-w-xs px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="flags">Flags Only</option>
                  <option value="codes">Country Codes Only</option>
                  <option value="flags-and-codes">Flags and Country Codes</option>
                </select>
                <p className="mt-2 text-xs text-gray-500">
                  This controls how users will see the language options in the website navigation
                </p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'branding' && (
          <div className="space-y-6">
            <h3 className="text-lg font-medium">Branding & Logo Settings</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Header Logo</label>
                <div className="space-y-3">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={(e) => handleFileUpload('logo', e)}
                    className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                  />
                  {settings.branding.logo && (
                    <div className="mt-2">
                      <img src={settings.branding.logo} alt="Header Logo" className="h-12 w-auto border rounded" />
                    </div>
                  )}
                  <p className="text-xs text-gray-500">Recommended: PNG or SVG, max height 48px</p>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Footer Logo</label>
                <div className="space-y-3">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={(e) => handleFileUpload('footerLogo', e)}
                    className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                  />
                  {settings.branding.footerLogo && (
                    <div className="mt-2">
                      <img src={settings.branding.footerLogo} alt="Footer Logo" className="h-16 w-auto border rounded" />
                    </div>
                  )}
                  <p className="text-xs text-gray-500">Recommended: PNG or SVG, max height 64px</p>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Favicon</label>
                <div className="space-y-3">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={(e) => handleFileUpload('favicon', e)}
                    className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                  />
                  {settings.branding.favicon && (
                    <div className="mt-2">
                      <img src={settings.branding.favicon} alt="Favicon" className="h-8 w-8 border rounded" />
                    </div>
                  )}
                  <p className="text-xs text-gray-500">Recommended: ICO, PNG, or SVG, 32x32px or 64x64px</p>
                </div>
              </div>
            </div>

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex">
                <svg className="flex-shrink-0 w-5 h-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd"/>
                </svg>
                <div className="ml-3">
                  <h4 className="text-sm font-medium text-blue-800">Logo Usage</h4>
                  <div className="mt-2 text-sm text-blue-700">
                    <ul className="list-disc pl-5 space-y-1">
                      <li>Header logo appears next to "ListAcross EU" text in the navigation</li>
                      <li>Footer logo is displayed prominently in the footer</li>
                      <li>Favicon appears in browser tabs and bookmarks</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'social' && (
          <div className="space-y-6">
            <h3 className="text-lg font-medium">Social Media Links</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Facebook URL</label>
                <input
                  type="url"
                  value={settings.socialLinks.facebook}
                  onChange={(e) => handleNestedChange('socialLinks', 'facebook', e.target.value)}
                  placeholder="https://facebook.com/yourpage"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Twitter URL</label>
                <input
                  type="url"
                  value={settings.socialLinks.twitter}
                  onChange={(e) => handleNestedChange('socialLinks', 'twitter', e.target.value)}
                  placeholder="https://twitter.com/youraccount"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">LinkedIn URL</label>
                <input
                  type="url"
                  value={settings.socialLinks.linkedin}
                  onChange={(e) => handleNestedChange('socialLinks', 'linkedin', e.target.value)}
                  placeholder="https://linkedin.com/company/yourcompany"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Instagram URL</label>
                <input
                  type="url"
                  value={settings.socialLinks.instagram}
                  onChange={(e) => handleNestedChange('socialLinks', 'instagram', e.target.value)}
                  placeholder="https://instagram.com/youraccount"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
          </div>
        )}

        {activeTab === 'seo' && (
          <div className="space-y-6">
            <h3 className="text-lg font-medium">SEO Settings</h3>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Default Page Title</label>
              <input
                type="text"
                value={settings.seoSettings.defaultTitle}
                onChange={(e) => handleNestedChange('seoSettings', 'defaultTitle', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Default Meta Description</label>
              <textarea
                value={settings.seoSettings.defaultDescription}
                onChange={(e) => handleNestedChange('seoSettings', 'defaultDescription', e.target.value)}
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Default Keywords</label>
              <input
                type="text"
                value={settings.seoSettings.defaultKeywords}
                onChange={(e) => handleNestedChange('seoSettings', 'defaultKeywords', e.target.value)}
                placeholder="Comma-separated keywords"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Default OG Image URL</label>
              <input
                type="url"
                value={settings.seoSettings.ogImageUrl}
                onChange={(e) => handleNestedChange('seoSettings', 'ogImageUrl', e.target.value)}
                placeholder="https://example.com/og-image.jpg"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        )}

        {activeTab === 'advanced' && (
          <div className="space-y-6">
            <h3 className="text-lg font-medium">Advanced Settings</h3>
            
            <div className="space-y-4">
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="enableRegistration"
                  checked={settings.enableRegistration}
                  onChange={(e) => handleInputChange('enableRegistration', e.target.checked)}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label htmlFor="enableRegistration" className="ml-2 block text-sm text-gray-900">
                  Enable user registration
                </label>
              </div>
              
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="enableComments"
                  checked={settings.enableComments}
                  onChange={(e) => handleInputChange('enableComments', e.target.checked)}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label htmlFor="enableComments" className="ml-2 block text-sm text-gray-900">
                  Enable comments on blog posts
                </label>
              </div>
              
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="maintenanceMode"
                  checked={settings.maintenanceMode}
                  onChange={(e) => handleInputChange('maintenanceMode', e.target.checked)}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label htmlFor="maintenanceMode" className="ml-2 block text-sm text-gray-900">
                  Maintenance mode (hide site from public)
                </label>
              </div>
              
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="enableStarAnimation"
                  checked={settings.enableStarAnimation}
                  onChange={(e) => handleInputChange('enableStarAnimation', e.target.checked)}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label htmlFor="enableStarAnimation" className="ml-2 block text-sm text-gray-900">
                  Enable star animation on homepage hero section
                </label>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Analytics Code (Google Analytics, etc.)</label>
              <textarea
                value={settings.analyticsCode}
                onChange={(e) => handleInputChange('analyticsCode', e.target.value)}
                rows={5}
                placeholder="Paste your analytics tracking code here"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}