'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface BlogCategory {
  id: number;
  name: string;
  slug: string;
}

interface BlogFormData {
  title: string;
  content: string;
  category: number | '';
  status: 'draft' | 'published' | 'archived';
  meta_title: string;
  meta_description: string;
  og_title: string;
  og_description: string;
  og_image: string;
  canonical_url: string;
}

export default function NewBlogPost() {
  const router = useRouter();
  const [categories, setCategories] = useState<BlogCategory[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState<BlogFormData>({
    title: '',
    content: '',
    category: '',
    status: 'draft',
    meta_title: '',
    meta_description: '',
    og_title: '',
    og_description: '',
    og_image: '',
    canonical_url: '',
  });

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/blog/categories/');
      if (!response.ok) throw new Error('Failed to fetch categories');
      const data = await response.json();
      setCategories(data.results || data);
    } catch (err) {
      console.error('Error fetching categories:', err);
    }
  };

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'category' ? (value === '' ? '' : parseInt(value)) : value
    }));

    // Auto-fill SEO fields if they're empty
    if (name === 'title' && value) {
      if (!formData.meta_title) {
        setFormData(prev => ({ ...prev, meta_title: value }));
      }
      if (!formData.og_title) {
        setFormData(prev => ({ ...prev, og_title: value }));
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/api/v1/blog/posts/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          author: 1, // Assuming admin user ID is 1
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to create post');
      }

      const newPost = await response.json();
      router.push('/admin/blog/posts');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create post');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Create New Blog Post</h1>
        <p className="mt-2 text-sm text-gray-600">
          Create engaging content for your audience with built-in SEO optimization.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Basic Information */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Basic Information</h3>
          </div>
          <div className="p-6 space-y-6">
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700">
                Title *
              </label>
              <input
                type="text"
                id="title"
                name="title"
                required
                value={formData.title}
                onChange={handleInputChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                placeholder="Enter post title"
              />
            </div>

            <div>
              <label htmlFor="category" className="block text-sm font-medium text-gray-700">
                Category *
              </label>
              <select
                id="category"
                name="category"
                required
                value={formData.category}
                onChange={handleInputChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              >
                <option value="">Select a category</option>
                {categories.map((category) => (
                  <option key={category.id} value={category.id}>
                    {category.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="status" className="block text-sm font-medium text-gray-700">
                Status
              </label>
              <select
                id="status"
                name="status"
                value={formData.status}
                onChange={handleInputChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              >
                <option value="draft">Draft</option>
                <option value="published">Published</option>
                <option value="archived">Archived</option>
              </select>
            </div>

            <div>
              <label htmlFor="content" className="block text-sm font-medium text-gray-700">
                Content *
              </label>
              <textarea
                id="content"
                name="content"
                rows={12}
                required
                value={formData.content}
                onChange={handleInputChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                placeholder="Write your blog post content here..."
              />
              <p className="mt-2 text-sm text-gray-500">
                You can use HTML tags for formatting. Markdown support coming soon.
              </p>
            </div>
          </div>
        </div>

        {/* SEO Settings */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">SEO Settings</h3>
            <p className="text-sm text-gray-600">
              Optimize your post for search engines and social media sharing.
            </p>
          </div>
          <div className="p-6 space-y-6">
            <div>
              <label htmlFor="meta_title" className="block text-sm font-medium text-gray-700">
                Meta Title
              </label>
              <input
                type="text"
                id="meta_title"
                name="meta_title"
                value={formData.meta_title}
                onChange={handleInputChange}
                maxLength={60}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                placeholder="SEO title (60 characters max)"
              />
              <p className="mt-1 text-sm text-gray-500">
                {formData.meta_title.length}/60 characters
              </p>
            </div>

            <div>
              <label htmlFor="meta_description" className="block text-sm font-medium text-gray-700">
                Meta Description
              </label>
              <textarea
                id="meta_description"
                name="meta_description"
                rows={3}
                value={formData.meta_description}
                onChange={handleInputChange}
                maxLength={155}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                placeholder="SEO description (155 characters max)"
              />
              <p className="mt-1 text-sm text-gray-500">
                {formData.meta_description.length}/155 characters
              </p>
            </div>

            <div>
              <label htmlFor="canonical_url" className="block text-sm font-medium text-gray-700">
                Canonical URL
              </label>
              <input
                type="url"
                id="canonical_url"
                name="canonical_url"
                value={formData.canonical_url}
                onChange={handleInputChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                placeholder="https://listacross.eu/blog/post-slug"
              />
            </div>
          </div>
        </div>

        {/* Open Graph Settings */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Social Media (Open Graph)</h3>
            <p className="text-sm text-gray-600">
              Customize how your post appears when shared on social media.
            </p>
          </div>
          <div className="p-6 space-y-6">
            <div>
              <label htmlFor="og_title" className="block text-sm font-medium text-gray-700">
                Social Title
              </label>
              <input
                type="text"
                id="og_title"
                name="og_title"
                value={formData.og_title}
                onChange={handleInputChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                placeholder="Title for social media sharing"
              />
            </div>

            <div>
              <label htmlFor="og_description" className="block text-sm font-medium text-gray-700">
                Social Description
              </label>
              <textarea
                id="og_description"
                name="og_description"
                rows={3}
                value={formData.og_description}
                onChange={handleInputChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                placeholder="Description for social media sharing"
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
                value={formData.og_image}
                onChange={handleInputChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                placeholder="https://example.com/image.jpg"
              />
              <p className="mt-1 text-sm text-gray-500">
                Recommended size: 1200x630px
              </p>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-end space-x-3">
          <button
            type="button"
            onClick={() => router.push('/admin/blog/posts')}
            className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={loading}
            className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Creating...' : 'Create Post'}
          </button>
        </div>
      </form>

      {error && (
        <div className="mt-4 rounded-md bg-red-50 p-4">
          <div className="text-sm text-red-700">{error}</div>
        </div>
      )}
    </div>
  );
}