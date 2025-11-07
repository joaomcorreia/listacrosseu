'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function NewBlogPost() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    topic: '',
    language: 'en',
  });
  const [titleSuggestions, setTitleSuggestions] = useState<string[]>([]);
  const [loadingSuggestions, setLoadingSuggestions] = useState(false);
  const [selectedTitle, setSelectedTitle] = useState('');

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

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const generateTitleSuggestions = async () => {
    if (!formData.topic.trim()) {
      alert('Please enter a topic first');
      return;
    }

    setLoadingSuggestions(true);
    setTitleSuggestions([]);
    
    try {
      console.log('Making AI request...');
      
      const response = await fetch('/api/v1/ai/generate/outline/', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({
          topic: formData.topic,
          language: formData.language,
          keywords: ['business', 'europe', 'guide'],
          tone: 'professional, engaging',
        }),
      });

      console.log('AI API Response status:', response.status);
      
      if (response.status === 401 || response.status === 403) {
        // User is not authenticated, redirect to Django admin login
        window.location.href = '/django-admin/login/?next=/admin/blog/posts/new';
        return;
      }

      if (!response.ok) {
        const errorText = await response.text();
        console.log('AI API Error response:', errorText);
        let errorData;
        try {
          errorData = JSON.parse(errorText);
        } catch {
          errorData = { error: `HTTP ${response.status}: ${response.statusText}` };
        }
        throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      
      // Generate multiple title variations based on the AI response
      const baseTitle = data.outline?.title || formData.topic;
      const suggestions = [
        baseTitle,
        `Complete Guide to ${formData.topic}`,
        `${formData.topic}: Everything You Need to Know`,
        `How to Master ${formData.topic} in 2025`,
        `The Ultimate ${formData.topic} Strategy`,
      ].filter(Boolean);
      
      console.log('Generated suggestions:', suggestions);
      setTitleSuggestions(suggestions);
    } catch (error) {
      console.error('Error generating title suggestions:', error);
      
      // For testing purposes, if AI fails, provide mock suggestions
      const mockSuggestions = [
        `Complete Guide to ${formData.topic}`,
        `${formData.topic}: Everything You Need to Know`,
        `How to Master ${formData.topic} in 2025`,
        `The Ultimate ${formData.topic} Strategy Guide`,
        `Expert Tips for ${formData.topic}`,
      ];
      
      setTitleSuggestions(mockSuggestions);
      console.log('Using mock suggestions due to AI error:', error);
      
      // Show a more user-friendly message
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      alert(`AI service temporarily unavailable (${errorMessage}). Showing sample suggestions that you can customize.`);
    } finally {
      setLoadingSuggestions(false);
    }
  };

  const selectTitle = (title: string) => {
    setSelectedTitle(title);
  };

  const handleManualCreate = async () => {
    if (!formData.topic) {
      alert('Please enter a topic');
      return;
    }
    if (!selectedTitle) {
      alert('Please select or enter a title');
      return;
    }

    try {
      console.log('Creating blog post...');
      
      const response = await fetch('/api/v1/admin/blog/posts/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          title_en: selectedTitle,
          slug: selectedTitle.toLowerCase()
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/(^-|-$)/g, '')
            .substring(0, 50) + '-' + Date.now(),
          content_en: `# ${selectedTitle}\n\nTopic: ${formData.topic}\n\n*This is a draft post. Add your content here.*`,
          excerpt_en: `Learn about ${formData.topic}. This article covers the key aspects you need to know.`,
          status: 'draft',
          is_featured: false,
          category_id: null,
          meta_title: selectedTitle,
          meta_description: `Learn about ${formData.topic}`,
        }),
      });

      if (response.status === 401 || response.status === 403) {
        window.location.href = '/django-admin/login/?next=/admin/blog/posts/new';
        return;
      }

      if (response.ok) {
        const data = await response.json();
        console.log('Post created successfully:', data);
        alert('Blog post created successfully!');
        router.push('/admin/blog/posts');
      } else {
        const errorText = await response.text();
        console.log('Create post error response:', errorText);
        console.log('Create post error status:', response.status);
        
        // Try to parse the error response
        let errorMessage = `HTTP ${response.status}`;
        try {
          const errorData = JSON.parse(errorText);
          if (errorData.error) {
            errorMessage = errorData.error;
          } else if (errorData.errors) {
            errorMessage = JSON.stringify(errorData.errors);
          }
        } catch (e) {
          errorMessage = errorText.substring(0, 200); // First 200 chars of error
        }
        
        throw new Error(`Failed to create post: ${errorMessage}`);
      }
    } catch (error) {
      console.error('Error creating blog post:', error);
      alert(`Failed to create blog post: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="bg-white shadow rounded-lg">
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900">Create New Blog Post</h1>
            <Link href="/admin/blog/posts" className="text-sm font-medium text-gray-600 hover:text-gray-900">
              ← Back to Posts
            </Link>
          </div>
        </div>

        <div className="p-6 space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Step 1: Enter Your Topic
            </label>
            <input
              type="text"
              name="topic"
              value={formData.topic}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              placeholder="e.g., Starting a business in Germany, Digital marketing for restaurants..."
            />
            <p className="text-xs text-gray-500 mt-1">
              Enter a topic you'd like to write about. This will be used to generate AI title suggestions.
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Language</label>
            <select
              name="language"
              value={formData.language}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="en">English</option>
              <option value="fr">French</option>
              <option value="de">German</option>
              <option value="es">Spanish</option>
              <option value="pt">Portuguese</option>
              <option value="nl">Dutch</option>
            </select>
          </div>

          {/* Step 2: AI Title Suggestions */}
          {formData.topic.trim() && (
            <div className="border-t pt-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-medium text-gray-900">
                  Step 2: Get AI Title Suggestions
                </h3>
                <button
                  onClick={generateTitleSuggestions}
                  disabled={loadingSuggestions}
                  className="px-4 py-2 text-sm font-medium text-white bg-purple-600 rounded-md hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
                >
                  {loadingSuggestions ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Generating...
                    </>
                  ) : (
                    <>
                      <span className="mr-2">🤖</span>
                      Generate Title Ideas
                    </>
                  )}
                </button>
              </div>
              
              <div className="bg-gray-50 p-4 rounded-md mb-4">
                <p className="text-sm text-gray-600">
                  <strong>Topic:</strong> {formData.topic}
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  Click "Generate Title Ideas" to get AI-powered suggestions for this topic
                </p>
              </div>

              {titleSuggestions.length > 0 && (
                <div className="space-y-3">
                  <p className="text-sm text-gray-600">Choose a title or use as inspiration:</p>
                  <div className="grid gap-2">
                    {titleSuggestions.map((title, index) => (
                      <button
                        key={index}
                        onClick={() => selectTitle(title)}
                        className={`p-3 text-left border rounded-md transition-colors ${
                          selectedTitle === title
                            ? 'border-blue-500 bg-blue-50 text-blue-900'
                            : 'border-gray-300 hover:border-gray-400 hover:bg-gray-50'
                        }`}
                      >
                        {title}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {selectedTitle && (
                <div className="mt-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Selected/Custom Title</label>
                  <input
                    type="text"
                    value={selectedTitle}
                    onChange={(e) => setSelectedTitle(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Edit the selected title or enter your own"
                  />
                </div>
              )}
            </div>
          )}

          <div className="space-y-4">
            {/* Test Buttons for Debugging */}
            <button
              onClick={async () => {
                try {
                  console.log('Testing basic Django connection via proxy...');
                  const response = await fetch('/api/v1/admin/blog/posts/');
                  const text = await response.text();
                  console.log('Proxy GET test:', response.status, text.substring(0, 200));
                  alert(`Proxy GET Test: ${response.status} - ${response.ok ? 'Success' : 'Failed'}`);
                } catch (error) {
                  console.error('Proxy GET test error:', error);
                  alert(`Proxy GET Test Error: ${error}`);
                }
              }}
              className="w-full px-4 py-2 text-sm bg-yellow-100 hover:bg-yellow-200 rounded border"
            >
              🔍 Test GET via Next.js Proxy
            </button>

            <button
              onClick={async () => {
                try {
                  console.log('Testing direct Django connection...');
                  const response = await fetch('http://127.0.0.1:8000/api/v1/admin/blog/posts/');
                  const text = await response.text();
                  console.log('Direct GET test:', response.status, text.substring(0, 200));
                  alert(`Direct GET Test: ${response.status} - ${response.ok ? 'Success' : 'Failed'}`);
                } catch (error) {
                  console.error('Direct GET test error:', error);
                  alert(`Direct GET Test Error: ${error}`);
                }
              }}
              className="w-full px-4 py-2 text-sm bg-blue-100 hover:bg-blue-200 rounded border"
            >
              🎯 Test Direct Django Connection
            </button>

            <button
              onClick={async () => {
                try {
                  console.log('Making test API request...');
                  const response = await fetch('/api/v1/admin/blog/posts/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                      title_en: 'Simple Test Post',
                      slug: 'simple-test-post-' + Date.now(),
                      content_en: 'Simple test content',
                      status: 'draft'
                    }),
                  });
                  
                  const responseText = await response.text();
                  console.log('Test API response status:', response.status);
                  console.log('Test API response text:', responseText);
                  console.log('Test API response headers:', Object.fromEntries(response.headers.entries()));
                  
                  if (response.ok) {
                    alert(`✅ Test API Success: ${response.status}`);
                  } else {
                    alert(`❌ Test API Error: ${response.status}\n${responseText.substring(0, 200)}`);
                  }
                } catch (error) {
                  console.error('Test API error:', error);
                  alert(`❌ Network Error: ${error}`);
                }
              }}
              className="w-full px-4 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded border"
            >
              🔧 Test API Connection (Debug)
            </button>

            <button
              onClick={handleManualCreate}
              disabled={!formData.topic.trim() || !selectedTitle}
              className="w-full px-6 py-4 text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {selectedTitle ? `Create Draft Post: "${selectedTitle}"` : 'Select a title to create post'}
            </button>
            {selectedTitle && (
              <p className="text-sm text-gray-500 mt-2 text-center">
                This will create a draft blog post that you can edit later
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
