'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface BlogCategory {
  id: number;
  name: string;
  slug: string;
}

interface BlogPost {
  id: number;
  title: string;
  slug: string;
  content: string;
  status: 'draft' | 'published' | 'archived';
  category: {
    id: number;
    name: string;
  };
  author: {
    id: number;
    username: string;
  };
  meta_title: string;
  meta_description: string;
  og_title: string;
  og_description: string;
  og_image: string;
  canonical_url: string;
  created_at: string;
  updated_at: string;
  published_at: string | null;
}

interface BlogFormData {
  title: string;
  content: string;
  category: number;
  status: 'draft' | 'published' | 'archived';
  meta_title: string;
  meta_description: string;
  og_title: string;
  og_description: string;
  og_image: string;
  canonical_url: string;
}

export default function EditBlogPost({ params }: { params: { id: string } }) {
  const router = useRouter();
  const [post, setPost] = useState<BlogPost | null>(null);
  const [categories, setCategories] = useState<BlogCategory[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState<BlogFormData>({
    title: '',
    content: '',
    category: 0,
    status: 'draft',
    meta_title: '',
    meta_description: '',
    og_title: '',
    og_description: '',
    og_image: '',
    canonical_url: '',
  });

  useEffect(() => {
    fetchPost();
    fetchCategories();
  }, [params.id]);

  const fetchPost = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/blog/posts/${params.id}/`);
      if (!response.ok) throw new Error('Failed to fetch post');
      
      const postData: BlogPost = await response.json();
      setPost(postData);
      
      // Populate form data
      setFormData({
        title: postData.title,
        content: postData.content,
        category: postData.category.id,
        status: postData.status,
        meta_title: postData.meta_title || '',
        meta_description: postData.meta_description || '',
        og_title: postData.og_title || '',
        og_description: postData.og_description || '',
        og_image: postData.og_image || '',
        canonical_url: postData.canonical_url || '',
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch post');
    } finally {
      setLoading(false);
    }
  };

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
      [name]: name === 'category' ? parseInt(value) : value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError(null);

    try {
      const response = await fetch(`http://localhost:8000/api/v1/blog/posts/${params.id}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          author: post?.author.id,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to update post');
      }

      router.push('/admin/blog/posts');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update post');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!post) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900">Post not found</h2>
        <p className="mt-2 text-gray-600">The blog post you're looking for doesn't exist.</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Edit Blog Post</h1>
            <p className="mt-2 text-sm text-gray-600">
              Last updated: {new Date(post.updated_at).toLocaleString()}
            </p>
          </div>
          <div className="text-sm text-gray-500">
            ID: {post.id} | Author: {post.author.username}
          </div>
        </div>
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
              />
              <p className="mt-1 text-sm text-gray-500">
                Current slug: {post.slug}
              </p>
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
              {post.published_at && (
                <p className="mt-1 text-sm text-gray-500">
                  Published: {new Date(post.published_at).toLocaleString()}
                </p>
              )}
            </div>

            <div>
              <label htmlFor="content" className="block text-sm font-medium text-gray-700">
                Content *
              </label>
              <textarea
                id="content"
                name="content"
                rows={15}
                required
                value={formData.content}
                onChange={handleInputChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>

        {/* SEO Settings */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">SEO Settings</h3>
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
              />
            </div>
          </div>
        </div>

        {/* Open Graph Settings */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Social Media (Open Graph)</h3>
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
              />
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-end space-x-3">
          <button
            type="button"
            onClick={() => router.push('/admin/blog/posts')}
            className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={saving}
            className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
          >
            {saving ? 'Saving...' : 'Update Post'}
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