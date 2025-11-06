'use client';
import React, { useEffect, useState } from 'react';
import Link from 'next/link';

// Get the current port dynamically
const getCurrentPort = () => {
  if (typeof window !== 'undefined') {
    return window.location.port || '3000';
  }
  return '3003'; // fallback
};

interface AdminPage {
  id: number;
  title: string;
  slug: string;
}

interface SEOAnalysis {
  title_length: number;
  description_length: number;
  title_score: 'good' | 'warning' | 'error';
  description_score: 'good' | 'warning' | 'error';
  suggestions: string[];
}

function SEOSettingsForm() {
  const [activeTab, setActiveTab] = useState<'settings' | 'analysis' | 'bulk'>('settings');
  const [seoData, setSeoData] = useState({
    title: '',
    description: '',
    url: 'https://listacross.eu',
    keywords: '',
    og_title: '',
    og_description: '',
    og_image: '',
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setSeoData(prev => ({ ...prev, [name]: value }));
  };

  const analyzeSEO = (): SEOAnalysis => {
    const titleLength = seoData.title.length;
    const descLength = seoData.description.length;
    
    const analysis: SEOAnalysis = {
      title_length: titleLength,
      description_length: descLength,
      title_score: titleLength >= 30 && titleLength <= 60 ? 'good' : titleLength > 60 ? 'error' : 'warning',
      description_score: descLength >= 120 && descLength <= 155 ? 'good' : descLength > 155 ? 'error' : 'warning',
      suggestions: [],
    };

    if (titleLength < 30) analysis.suggestions.push('Title is too short. Aim for 30-60 characters.');
    if (titleLength > 60) analysis.suggestions.push('Title is too long. Keep it under 60 characters.');
    if (descLength < 120) analysis.suggestions.push('Description is too short. Aim for 120-155 characters.');
    if (descLength > 155) analysis.suggestions.push('Description is too long. Keep it under 155 characters.');
    if (!seoData.keywords) analysis.suggestions.push('Add relevant keywords to improve discoverability.');

    return analysis;
  };

  const getScoreColor = (score: 'good' | 'warning' | 'error') => {
    switch (score) {
      case 'good': return 'text-green-600 bg-green-100';
      case 'warning': return 'text-yellow-600 bg-yellow-100';
      case 'error': return 'text-red-600 bg-red-100';
    }
  };

  const analysis = analyzeSEO();

  return (
    <div className="space-y-6">
      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {[
            { id: 'settings', name: 'SEO Settings', icon: '⚙️' },
            { id: 'analysis', name: 'SEO Analysis', icon: '📊' },
            { id: 'bulk', name: 'Bulk Actions', icon: '⚡' },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as typeof activeTab)}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              {tab.icon} {tab.name}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      {activeTab === 'settings' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Column: SEO Settings */}
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">SEO Settings</h3>
              
              <div className="space-y-4">
                <div>
                  <label htmlFor="title" className="block text-sm font-medium text-gray-700">
                    Meta Title
                  </label>
                  <input
                    type="text"
                    id="title"
                    name="title"
                    value={seoData.title}
                    onChange={handleInputChange}
                    maxLength={60}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    placeholder="Page title for search engines"
                  />
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>{seoData.title.length}/60 characters</span>
                    <span className={`px-2 py-1 rounded ${getScoreColor(analysis.title_score)}`}>
                      {analysis.title_score.toUpperCase()}
                    </span>
                  </div>
                </div>

                <div>
                  <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                    Meta Description
                  </label>
                  <textarea
                    id="description"
                    name="description"
                    rows={3}
                    value={seoData.description}
                    onChange={handleInputChange}
                    maxLength={155}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    placeholder="Brief description that appears in search results"
                  />
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>{seoData.description.length}/155 characters</span>
                    <span className={`px-2 py-1 rounded ${getScoreColor(analysis.description_score)}`}>
                      {analysis.description_score.toUpperCase()}
                    </span>
                  </div>
                </div>

                <div>
                  <label htmlFor="url" className="block text-sm font-medium text-gray-700">
                    Canonical URL
                  </label>
                  <input
                    type="url"
                    id="url"
                    name="url"
                    value={seoData.url}
                    onChange={handleInputChange}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    placeholder="https://listacross.eu/page"
                  />
                </div>

                <div>
                  <label htmlFor="keywords" className="block text-sm font-medium text-gray-700">
                    Focus Keywords
                  </label>
                  <input
                    type="text"
                    id="keywords"
                    name="keywords"
                    value={seoData.keywords}
                    onChange={handleInputChange}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    placeholder="business directory, european companies, eu marketplace"
                  />
                  <p className="mt-1 text-xs text-gray-500">Separate keywords with commas</p>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column: Social Media Settings */}
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">Social Media (Open Graph)</h3>
              
              <div className="space-y-4">
                <div>
                  <label htmlFor="og_title" className="block text-sm font-medium text-gray-700">
                    Social Title
                  </label>
                  <input
                    type="text"
                    id="og_title"
                    name="og_title"
                    value={seoData.og_title}
                    onChange={handleInputChange}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    placeholder="Title when shared on social media"
                  />
                </div>

                <div>
                  <label htmlFor="og_description" className="block text-sm font-medium text-gray-700">
                    Social Description
                  </label>
                  <textarea
                    id="og_description"
                    name="og_description"
                    rows={2}
                    value={seoData.og_description}
                    onChange={handleInputChange}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    placeholder="Description when shared on social media"
                  />
                </div>

                <div>
                  <label htmlFor="og_image" className="block text-sm font-medium text-gray-700">
                    Social Image URL
                  </label>
                  <input
                    type="url"
                    id="og_image"
                    name="og_image"
                    value={seoData.og_image}
                    onChange={handleInputChange}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    placeholder="https://listacross.eu/images/social-share.jpg"
                  />
                  <p className="mt-1 text-xs text-gray-500">Recommended size: 1200x630px</p>
                </div>

                {/* SEO Analysis */}
                {analysis.suggestions.length > 0 && (
                  <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-md">
                    <h4 className="text-sm font-medium text-yellow-800 mb-2">SEO Suggestions</h4>
                    <ul className="text-xs text-yellow-700 space-y-1">
                      {analysis.suggestions.map((suggestion, index) => (
                        <li key={index} className="flex items-start">
                          <span className="mr-2">•</span>
                          <span>{suggestion}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Save Button */}
                <div className="pt-4">
                  <button
                    type="button"
                    className="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
                  >
                    Save SEO Settings
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* SEO Analysis Tab */}
      {activeTab === 'analysis' && (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">SEO Analysis Report</h3>
          
          <div className="space-y-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-gray-900">{analysis.title_length}</div>
                <div className="text-xs text-gray-600">Title Length</div>
                <div className={`text-xs mt-1 px-2 py-1 rounded ${getScoreColor(analysis.title_score)}`}>
                  {analysis.title_score.toUpperCase()}
                </div>
              </div>
              
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-gray-900">{analysis.description_length}</div>
                <div className="text-xs text-gray-600">Description Length</div>
                <div className={`text-xs mt-1 px-2 py-1 rounded ${getScoreColor(analysis.description_score)}`}>
                  {analysis.description_score.toUpperCase()}
                </div>
              </div>

              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-gray-900">{seoData.keywords.split(',').filter(k => k.trim()).length}</div>
                <div className="text-xs text-gray-600">Keywords</div>
                <div className="text-xs mt-1 px-2 py-1 rounded bg-blue-100 text-blue-600">
                  {seoData.keywords ? 'SET' : 'MISSING'}
                </div>
              </div>

              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-gray-900">{seoData.og_image ? '✓' : '✗'}</div>
                <div className="text-xs text-gray-600">Social Image</div>
                <div className={`text-xs mt-1 px-2 py-1 rounded ${seoData.og_image ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'}`}>
                  {seoData.og_image ? 'SET' : 'MISSING'}
                </div>
              </div>
            </div>

            {analysis.suggestions.length > 0 && (
              <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-md">
                <h4 className="text-sm font-medium text-yellow-800 mb-2">Recommendations</h4>
                <ul className="text-sm text-yellow-700 space-y-1">
                  {analysis.suggestions.map((suggestion, index) => (
                    <li key={index} className="flex items-start">
                      <span className="mr-2 text-yellow-600">•</span>
                      <span>{suggestion}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Bulk Actions Tab */}
      {activeTab === 'bulk' && (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Bulk SEO Actions</h3>
          
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 border border-gray-200 rounded-lg">
                <h4 className="font-medium text-gray-900 mb-2">Bulk Update Meta Titles</h4>
                <p className="text-sm text-gray-600 mb-3">Update meta titles for all pages using a template</p>
                <div className="space-y-2">
                  <input
                    type="text"
                    placeholder="{{page_name}} - ListAcross EU"
                    className="w-full text-sm rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  />
                  <button className="w-full text-sm bg-blue-600 text-white px-3 py-2 rounded-md hover:bg-blue-700 transition-colors">
                    Apply to All Pages
                  </button>
                </div>
              </div>

              <div className="p-4 border border-gray-200 rounded-lg">
                <h4 className="font-medium text-gray-900 mb-2">Bulk Update Descriptions</h4>
                <p className="text-sm text-gray-600 mb-3">Update meta descriptions for all pages</p>
                <div className="space-y-2">
                  <textarea
                    rows={2}
                    placeholder="{{page_description}} | European business directory platform"
                    className="w-full text-sm rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  />
                  <button className="w-full text-sm bg-blue-600 text-white px-3 py-2 rounded-md hover:bg-blue-700 transition-colors">
                    Apply to All Pages
                  </button>
                </div>
              </div>

              <div className="p-4 border border-gray-200 rounded-lg">
                <h4 className="font-medium text-gray-900 mb-2">Generate Sitemaps</h4>
                <p className="text-sm text-gray-600 mb-3">Create XML sitemaps for search engines</p>
                <div className="space-y-2">
                  <button className="w-full text-sm bg-green-600 text-white px-3 py-2 rounded-md hover:bg-green-700 transition-colors">
                    Generate XML Sitemap
                  </button>
                  <button className="w-full text-sm bg-green-600 text-white px-3 py-2 rounded-md hover:bg-green-700 transition-colors">
                    Generate Image Sitemap
                  </button>
                </div>
              </div>

              <div className="p-4 border border-gray-200 rounded-lg">
                <h4 className="font-medium text-gray-900 mb-2">SEO Health Check</h4>
                <p className="text-sm text-gray-600 mb-3">Scan all pages for SEO issues</p>
                <div className="space-y-2">
                  <button className="w-full text-sm bg-purple-600 text-white px-3 py-2 rounded-md hover:bg-purple-700 transition-colors">
                    Run Full SEO Audit
                  </button>
                  <button className="w-full text-sm bg-purple-600 text-white px-3 py-2 rounded-md hover:bg-purple-700 transition-colors">
                    Export SEO Report
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default function AdminPagesList() {
  const [rows, setRows] = useState<AdminPage[]>([]);
  const [currentPort, setCurrentPort] = useState('3003');

  useEffect(() => {
    fetch('/api/admin/pages').then(r => r.json()).then(setRows);
    // Set the current port dynamically
    setCurrentPort(getCurrentPort());
  }, []);

  return (
    <div className="p-6 space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Pages Management</h1>
      </div>
      
      {/* Navigation & Page Management Section */}
      <div className="bg-white rounded-2xl border border-gray-100 overflow-hidden">
        <div className="p-4 border-b border-gray-100">
          <h2 className="text-lg font-semibold text-gray-800">Navigation & Page Management</h2>
          <p className="text-sm text-gray-600 mt-1">Configure main navigation and create new pages</p>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            {/* Main Navigation Editor */}
            <div className="space-y-4">
              <h3 className="text-md font-medium text-gray-900">Main Navigation Menu</h3>
              <p className="text-sm text-gray-600">Configure navigation items</p>
              
              <div className="space-y-2">
                {[
                  { label: 'Search', path: '/search', enabled: true },
                  { label: 'Countries', path: '/countries', enabled: true },
                  { label: 'Categories', path: '/categories', enabled: true },
                  { label: 'Pricing', path: '/pricing', enabled: true },
                  { label: 'AI Design', path: '/ai-design', enabled: true },
                  { label: 'Blog', path: '/blog', enabled: false }
                ].map((item, index) => (
                  <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded-lg">
                    <div className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={item.enabled}
                        onChange={() => {}} // TODO: Add state management
                        className="h-3 w-3 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <div>
                        <div className="text-sm font-medium text-gray-900">{item.label}</div>
                        <div className="text-xs text-gray-500">{item.path}</div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-1">
                      <button className="p-1 text-gray-400 hover:text-gray-600">
                        <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 16a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
                        </svg>
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Page Creator */}
            <div className="space-y-4">
              <h3 className="text-md font-medium text-gray-900">Create New Page</h3>
              <p className="text-sm text-gray-600">Add custom pages to your site</p>
              
              <div className="space-y-3">
                <div>
                  <input
                    type="text"
                    placeholder="Page title (e.g., About Us)"
                    className="w-full text-sm rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <input
                    type="text"
                    placeholder="URL slug (e.g., about-us)"
                    className="w-full text-sm rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <select className="w-full text-sm rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
                    <option>Select template</option>
                    <option>Basic Page</option>
                    <option>Landing Page</option>
                    <option>Contact Page</option>
                    <option>About Page</option>
                  </select>
                </div>
                <button className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm">
                  Create Page
                </button>
              </div>
            </div>

            {/* Existing Pages */}
            <div className="space-y-4">
              <h3 className="text-md font-medium text-gray-900">Existing Pages</h3>
              <p className="text-sm text-gray-600">Manage your current pages</p>
              
              <div className="space-y-2 max-h-64 overflow-y-auto">
                {rows.map((page) => (
                  <div key={page.id} className="flex items-center justify-between p-2 bg-gray-50 rounded-lg">
                    <div>
                      <div className="text-sm font-medium text-gray-900">{page.title}</div>
                      <div className="text-xs text-gray-500">{page.slug}</div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Link
                        href={`/admin/pages/${page.id}`}
                        className="text-xs text-blue-600 hover:text-blue-800 transition-colors"
                      >
                        Edit
                      </Link>
                    </div>
                  </div>
                ))}
                {rows.length === 0 && (
                  <div className="p-4 text-center text-gray-500 text-sm">No pages yet.</div>
                )}
              </div>
            </div>
          </div>
          
          {/* Action Buttons */}
          <div className="mt-6 pt-6 border-t border-gray-200 flex justify-between">
            <button className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors">
              Reset Navigation to Default
            </button>
            <div className="flex space-x-3">
              <button className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors">
                Preview Changes
              </button>
              <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                Save Navigation
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* SEO Settings Section */}
      <div className="bg-white rounded-2xl border border-gray-100 overflow-hidden">
        <div className="p-4 border-b border-gray-100">
          <h2 className="text-lg font-semibold text-gray-800">SEO Settings</h2>
          <p className="text-sm text-gray-600 mt-1">Optimize your content for search engines and social media platforms</p>
        </div>
        <div className="p-6">
          <SEOSettingsForm />
        </div>
      </div>
      
      {/* Website Preview Section */}
      <div className="bg-white rounded-2xl border border-gray-100 overflow-hidden">
        <div className="p-4 border-b border-gray-100">
          <h2 className="text-lg font-semibold text-gray-800">Website Preview</h2>
          
          {/* Complete SEO Settings for Current Page */}
          <div className="mt-4 mb-4 p-4 bg-gray-50 rounded-lg border">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-800">SEO Settings for Current Page</h3>
              <span className="text-xs text-gray-500 px-2 py-1 bg-white rounded border">
                /eu (default)
              </span>
            </div>
            
            {/* Tab Navigation */}
            <div className="border-b border-gray-200 mb-4">
              <nav className="-mb-px flex space-x-6">
                <button className="py-2 px-1 border-b-2 border-blue-500 text-blue-600 font-medium text-sm">
                  📝 Basic SEO
                </button>
                <button className="py-2 px-1 border-b-2 border-transparent text-gray-500 hover:text-gray-700 font-medium text-sm">
                  📱 Social Media
                </button>
                <button className="py-2 px-1 border-b-2 border-transparent text-gray-500 hover:text-gray-700 font-medium text-sm">
                  📊 Analysis
                </button>
              </nav>
            </div>

            {/* Basic SEO Tab Content */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Meta Title</label>
                  <input
                    type="text"
                    placeholder="Page title for search engines"
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    defaultValue="Find trusted services across the EU"
                    maxLength={60}
                  />
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>37/60 characters</span>
                    <span className="px-2 py-1 rounded text-green-600 bg-green-100">GOOD</span>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Meta Description</label>
                  <textarea
                    rows={3}
                    placeholder="Brief description that appears in search results"
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    defaultValue="Discover featured businesses from all EU countries. Compare categories, explore hubs, and advertise EU-wide."
                    maxLength={155}
                  />
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>109/155 characters</span>
                    <span className="px-2 py-1 rounded text-green-600 bg-green-100">GOOD</span>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Canonical URL</label>
                  <input
                    type="url"
                    placeholder="https://listacross.eu/page"
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    defaultValue="https://listacross.eu/eu"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Focus Keywords</label>
                  <input
                    type="text"
                    placeholder="business directory, european companies, eu marketplace"
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    defaultValue="eu business directory, european services, eu companies"
                  />
                  <p className="text-xs text-gray-500 mt-1">Separate keywords with commas</p>
                </div>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Social Title (Open Graph)</label>
                  <input
                    type="text"
                    placeholder="Title when shared on social media"
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    defaultValue="Find trusted services across the EU - ListAcross"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Social Description</label>
                  <textarea
                    rows={2}
                    placeholder="Description when shared on social media"
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    defaultValue="One directory. 27 countries. 6 languages. EU-wide exposure for your business."
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Social Image URL</label>
                  <input
                    type="url"
                    placeholder="https://listacross.eu/images/social-share.jpg"
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    defaultValue="https://listacross.eu/images/eu-social.jpg"
                  />
                  <p className="text-xs text-gray-500 mt-1">Recommended size: 1200x630px</p>
                </div>

                {/* Quick Actions */}
                <div className="pt-3 border-t border-gray-200">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3 text-xs text-gray-600">
                      <span className="flex items-center"><span className="w-2 h-2 bg-green-500 rounded-full mr-1"></span> SEO Score: 87%</span>
                      <span>Last saved: 2 min ago</span>
                    </div>
                    <div className="flex space-x-2">
                      <button className="px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded hover:bg-gray-200 transition-colors">
                        Preview
                      </button>
                      <button className="px-3 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors">
                        Save SEO
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <p className="text-sm text-gray-600 mt-1">Live preview of the main website</p>
        </div>
        <div className="relative">
          <iframe
            src={`http://localhost:${currentPort}/en`}
            className="w-full h-[600px] border-0"
            title="Website Preview"
            loading="lazy"
          />
          {/* Overlay for responsive control */}
          <div className="absolute top-2 right-2 flex gap-2">
            <button
              onClick={() => window.open(`http://localhost:${currentPort}/en`, '_blank')}
              className="px-3 py-1 text-xs bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              Open in New Tab
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}