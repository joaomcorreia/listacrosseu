'use client';

import { useState, useEffect } from 'react';

interface SEOPreview {
  title: string;
  description: string;
  url: string;
}

interface SEOAnalysis {
  title_length: number;
  description_length: number;
  title_score: 'good' | 'warning' | 'error';
  description_score: 'good' | 'warning' | 'error';
  suggestions: string[];
}

export default function SEOManager() {
  const [activeTab, setActiveTab] = useState<'preview' | 'analysis' | 'bulk'>('preview');
  const [seoData, setSeoData] = useState({
    title: '',
    description: '',
    url: 'https://listacross.eu',
    keywords: '',
    og_title: '',
    og_description: '',
    og_image: '',
  });

  const [preview, setPreview] = useState<SEOPreview>({
    title: '',
    description: '',
    url: '',
  });

  useEffect(() => {
    // Update preview when seoData changes
    setPreview({
      title: seoData.title || 'ListAcross EU - European Business Directory',
      description: seoData.description || 'Discover and connect with businesses across the European Union. Find services, products, and opportunities in your country.',
      url: seoData.url,
    });
  }, [seoData]);

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
      <div>
        <h1 className="text-2xl font-bold text-gray-900">SEO Manager</h1>
        <p className="mt-2 text-sm text-gray-600">
          Optimize your content for search engines and social media platforms.
        </p>
      </div>

      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {[
            { id: 'preview', name: 'Live Preview', icon: '👁️' },
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

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left Column: Form */}
        <div className="space-y-6">
          <div className="bg-white shadow rounded-lg p-6">
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

          {/* Open Graph Settings */}
          <div className="bg-white shadow rounded-lg p-6">
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
            </div>
          </div>
        </div>

        {/* Right Column: Preview & Analysis */}
        <div className="space-y-6">
          {activeTab === 'preview' && (
            <div className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Search Engine Preview</h3>
              
              {/* Google SERP Preview */}
              <div className="border border-gray-200 rounded-lg p-4 bg-gray-50">
                <div className="space-y-2">
                  <div className="text-xs text-green-700">{preview.url}</div>
                  <div className="text-blue-700 text-lg font-medium hover:underline cursor-pointer">
                    {preview.title || 'Your page title will appear here'}
                  </div>
                  <div className="text-gray-600 text-sm">
                    {preview.description || 'Your meta description will appear here. It should be compelling and descriptive to encourage clicks.'}
                  </div>
                </div>
              </div>

              <h4 className="text-md font-medium text-gray-900 mt-6 mb-3">Social Media Preview</h4>
              
              {/* Facebook/LinkedIn Preview */}
              <div className="border border-gray-200 rounded-lg overflow-hidden">
                <div className="h-32 bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center">
                  {seoData.og_image ? (
                    <img src={seoData.og_image} alt="Preview" className="w-full h-full object-cover" />
                  ) : (
                    <span className="text-white text-sm">Social Image Preview</span>
                  )}
                </div>
                <div className="p-3 bg-white">
                  <div className="text-xs text-gray-500 uppercase">
                    {preview.url ? new URL(preview.url).hostname : 'listacross.eu'}
                  </div>
                  <div className="text-sm font-medium text-gray-900 mt-1">
                    {seoData.og_title || preview.title || 'Social media title'}
                  </div>
                  <div className="text-xs text-gray-600 mt-1">
                    {seoData.og_description || preview.description || 'Social media description'}
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'analysis' && (
            <div className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">SEO Analysis</h3>
              
              <div className="space-y-4">
                {/* Overall Score */}
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <div className="text-3xl font-bold text-gray-900">
                    {analysis.title_score === 'good' && analysis.description_score === 'good' ? '90' : 
                     analysis.title_score === 'warning' || analysis.description_score === 'warning' ? '65' : '40'}
                  </div>
                  <div className="text-sm text-gray-600">SEO Score</div>
                </div>

                {/* Detailed Analysis */}
                <div className="space-y-3">
                  <div className="flex items-center justify-between p-3 border rounded">
                    <span className="text-sm font-medium">Title Length</span>
                    <span className={`px-2 py-1 rounded text-xs ${getScoreColor(analysis.title_score)}`}>
                      {analysis.title_length} chars
                    </span>
                  </div>
                  
                  <div className="flex items-center justify-between p-3 border rounded">
                    <span className="text-sm font-medium">Description Length</span>
                    <span className={`px-2 py-1 rounded text-xs ${getScoreColor(analysis.description_score)}`}>
                      {analysis.description_length} chars
                    </span>
                  </div>

                  <div className="flex items-center justify-between p-3 border rounded">
                    <span className="text-sm font-medium">Keywords Set</span>
                    <span className={`px-2 py-1 rounded text-xs ${seoData.keywords ? 'text-green-600 bg-green-100' : 'text-red-600 bg-red-100'}`}>
                      {seoData.keywords ? 'Yes' : 'No'}
                    </span>
                  </div>

                  <div className="flex items-center justify-between p-3 border rounded">
                    <span className="text-sm font-medium">Social Meta</span>
                    <span className={`px-2 py-1 rounded text-xs ${seoData.og_title && seoData.og_description ? 'text-green-600 bg-green-100' : 'text-yellow-600 bg-yellow-100'}`}>
                      {seoData.og_title && seoData.og_description ? 'Complete' : 'Partial'}
                    </span>
                  </div>
                </div>

                {/* Suggestions */}
                {analysis.suggestions.length > 0 && (
                  <div className="mt-6">
                    <h4 className="text-sm font-medium text-gray-900 mb-2">Suggestions</h4>
                    <ul className="space-y-2">
                      {analysis.suggestions.map((suggestion, index) => (
                        <li key={index} className="flex items-start">
                          <span className="text-yellow-500 mr-2">⚠️</span>
                          <span className="text-sm text-gray-700">{suggestion}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'bulk' && (
            <div className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Bulk SEO Actions</h3>
              
              <div className="space-y-4">
                <div className="p-4 border border-gray-200 rounded-lg">
                  <h4 className="font-medium text-gray-900">Generate Missing Meta Descriptions</h4>
                  <p className="text-sm text-gray-600 mt-1">
                    Automatically generate meta descriptions for blog posts that don't have them.
                  </p>
                  <button className="mt-3 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                    Generate Descriptions
                  </button>
                </div>

                <div className="p-4 border border-gray-200 rounded-lg">
                  <h4 className="font-medium text-gray-900">Update Canonical URLs</h4>
                  <p className="text-sm text-gray-600 mt-1">
                    Update canonical URLs across all content to match current site structure.
                  </p>
                  <button className="mt-3 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
                    Update URLs
                  </button>
                </div>

                <div className="p-4 border border-gray-200 rounded-lg">
                  <h4 className="font-medium text-gray-900">SEO Audit Report</h4>
                  <p className="text-sm text-gray-600 mt-1">
                    Generate a comprehensive SEO audit report for all your content.
                  </p>
                  <button className="mt-3 px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700">
                    Generate Report
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Save Button */}
      <div className="flex justify-end">
        <button className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500">
          Save SEO Settings
        </button>
      </div>
    </div>
  );
}