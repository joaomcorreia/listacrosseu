'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Language } from '../lib/i18n';

interface BlogPost {
  id: string;
  title: string;
  excerpt: string;
  image: string;
  author: string;
  publishedAt: string;
  readTime: number;
  slug: string;
  category: string;
  tags: string[];
}

interface BlogCardProps {
  post: BlogPost;
  lang: Language;
}

export default function BlogCard({ post, lang }: BlogCardProps) {
  const [imageError, setImageError] = useState(false);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString(lang === 'en' ? 'en-US' : lang === 'es' ? 'es-ES' : lang === 'fr' ? 'fr-FR' : lang === 'de' ? 'de-DE' : lang === 'nl' ? 'nl-NL' : 'pt-PT', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  return (
    <article className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden hover:shadow-xl transition-all duration-300 hover:-translate-y-1 group">
      {/* Blog Image */}
      <div className="relative h-48 bg-gradient-to-br from-blue-100 to-purple-100 overflow-hidden">
        {!imageError && post.image ? (
          <img
            src={post.image}
            alt={post.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            onError={() => setImageError(true)}
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <div className="text-6xl text-gray-300">📝</div>
          </div>
        )}
        
        {/* Category Badge */}
        <div className="absolute top-4 left-4">
          <span className="bg-white bg-opacity-90 backdrop-blur-sm text-gray-700 px-3 py-1 rounded-full text-xs font-medium">
            {post.category}
          </span>
        </div>

        {/* Read Time */}
        <div className="absolute top-4 right-4">
          <span className="bg-black bg-opacity-50 text-white px-2 py-1 rounded-full text-xs font-medium">
            {post.readTime} min read
          </span>
        </div>
      </div>

      {/* Blog Content */}
      <div className="p-6">
        {/* Title */}
        <h3 className="text-xl font-bold text-gray-900 mb-3 line-clamp-2 group-hover:text-blue-600 transition-colors">
          <Link href={`/${lang}/blog/${post.slug}`} className="hover:underline">
            {post.title}
          </Link>
        </h3>

        {/* Excerpt */}
        <p className="text-gray-600 mb-4 line-clamp-3 leading-relaxed">
          {post.excerpt}
        </p>

        {/* Tags */}
        <div className="flex flex-wrap gap-2 mb-4">
          {post.tags.slice(0, 3).map((tag) => (
            <span key={tag} className="bg-blue-50 text-blue-600 px-2 py-1 rounded-md text-xs font-medium">
              #{tag}
            </span>
          ))}
          {post.tags.length > 3 && (
            <span className="text-gray-400 text-xs">+{post.tags.length - 3} more</span>
          )}
        </div>

        {/* Author and Date */}
        <div className="flex items-center justify-between text-sm text-gray-500 pt-4 border-t border-gray-100">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-medium text-xs">
              {post.author.split(' ').map(n => n[0]).join('').toUpperCase()}
            </div>
            <span>By {post.author}</span>
          </div>
          <span>{formatDate(post.publishedAt)}</span>
        </div>
      </div>

      {/* Hover Effect Gradient */}
      <div className="absolute inset-0 bg-gradient-to-t from-blue-600/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
    </article>
  );
}