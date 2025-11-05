"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { apiCall } from "@/lib/api";

interface BlogPost {
  title: string;
  slug: string;
  excerpt: string;
  cover_image: string;
  published_at: string;
  category: {
    name: string;
    slug: string;
  } | null;
  is_featured: boolean;
}

interface BlogSliderProps {
  lang: string;
  limit?: number;
  title?: string;
}

export default function BlogSlider({ lang, limit = 6, title = "Latest from the blog" }: BlogSliderProps) {
  const [posts, setPosts] = useState<BlogPost[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        setLoading(true);
        const data = await apiCall(`/blog/posts/featured/?limit=${limit}`);
        setPosts(data?.results || []);
      } catch (error) {
        console.error('Error fetching blog posts:', error);
        setPosts([]);
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();
  }, [limit]);

  if (loading) {
    return (
      <section className="mt-10">
        <h2 className="mb-6 text-lg font-semibold">{title}</h2>
        <div className="grid gap-4 md:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="bg-gray-200 animate-pulse rounded-lg h-64"></div>
          ))}
        </div>
      </section>
    );
  }

  if (!posts.length) {
    return null;
  }

  return (
    <section className="mt-10">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-lg font-semibold">{title}</h2>
        <Link 
          href={`/${lang}/blog`}
          className="text-blue-600 hover:text-blue-800 text-sm font-medium"
        >
          View all posts →
        </Link>
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {posts.map((post) => (
          <Link 
            key={post.slug} 
            href={`/${lang}/blog/${post.slug}`}
            className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden group"
          >
            {post.cover_image && (
              <div className="relative overflow-hidden h-32">
                <img 
                  src={post.cover_image} 
                  alt={post.title}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                />
                {post.is_featured && (
                  <span className="absolute top-2 right-2 text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full">
                    Featured
                  </span>
                )}
              </div>
            )}
            
            <div className="p-4">
              {post.category && (
                <div className="mb-2">
                  <span className="text-sm text-blue-600 font-medium">
                    {post.category.name}
                  </span>
                </div>
              )}
              
              <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2 group-hover:text-blue-600 transition-colors">
                {post.title}
              </h3>
              
              {post.excerpt && (
                <p className="text-sm text-gray-600 line-clamp-2 mb-3">
                  {post.excerpt}
                </p>
              )}
              
              <div className="text-xs text-gray-500">
                {new Date(post.published_at).toLocaleDateString(lang, {
                  year: 'numeric',
                  month: 'short',
                  day: 'numeric'
                })}
              </div>
            </div>
          </Link>
        ))}
      </div>
    </section>
  );
}