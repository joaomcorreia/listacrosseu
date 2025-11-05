import { apiCall } from "@/lib/api";
import { notFound } from "next/navigation";
import Link from "next/link";
import { Metadata } from "next";

interface BlogPost {
  title: string;
  slug: string;
  excerpt: string;
  content: string;
  cover_image: string;
  published_at: string;
  category: {
    name: string;
    slug: string;
  } | null;
  author_name: string;
  is_featured: boolean;
  // SEO fields
  meta_title: string;
  meta_description: string;
  canonical_url: string;
  robots: string;
  og_title: string;
  og_description: string;
  og_image: string;
}

export async function generateMetadata({ params }: { params: { lang: string; slug: string } }): Promise<Metadata> {
  const post: BlogPost | null = await apiCall(`/blog/posts/${params.slug}/?lang=${params.lang}`);
  
  if (!post) {
    return {
      title: 'Post Not Found | ListAcross EU',
      description: 'The requested blog post was not found.'
    };
  }

  return {
    title: post.meta_title || post.title,
    description: post.meta_description || post.excerpt,
    robots: post.robots || 'index,follow',
    openGraph: {
      title: post.og_title || post.title,
      description: post.og_description || post.excerpt,
      images: post.og_image || post.cover_image ? [{
        url: post.og_image || post.cover_image,
        alt: post.title
      }] : [],
      type: 'article',
      publishedTime: post.published_at
    },
    alternates: {
      canonical: post.canonical_url || `/${params.lang}/blog/${post.slug}`
    }
  };
}

export default async function BlogPostPage({ params }: { params: { lang: string; slug: string } }) {
  const post: BlogPost | null = await apiCall(`/blog/posts/${params.slug}/?lang=${params.lang}`);

  if (!post) {
    notFound();
  }

  return (
    <article className="max-w-4xl mx-auto">
      {/* Header */}
      <header className="mb-8">
        <div className="mb-4">
          <Link 
            href={`/${params.lang}/blog`}
            className="text-blue-600 hover:text-blue-800 text-sm font-medium"
          >
            ← Back to Blog
          </Link>
        </div>
        
        <div className="mb-4">
          {post.category && (
            <Link 
              href={`/${params.lang}/blog?category=${post.category.slug}`}
              className="text-blue-600 font-medium text-sm hover:text-blue-800"
            >
              {post.category.name}
            </Link>
          )}
          {post.is_featured && (
            <span className="ml-3 text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full">
              Featured
            </span>
          )}
        </div>
        
        <h1 className="text-4xl font-bold text-gray-900 mb-4 leading-tight">
          {post.title}
        </h1>
        
        {post.excerpt && (
          <p className="text-xl text-gray-600 leading-relaxed mb-6">
            {post.excerpt}
          </p>
        )}
        
        <div className="flex items-center text-sm text-gray-500 mb-8">
          <span>By {post.author_name}</span>
          <span className="mx-2">•</span>
          <time dateTime={post.published_at}>
            {new Date(post.published_at).toLocaleDateString(params.lang, {
              year: 'numeric',
              month: 'long',
              day: 'numeric'
            })}
          </time>
        </div>
      </header>

      {/* Cover Image */}
      {post.cover_image && (
        <div className="mb-8">
          <img 
            src={post.cover_image} 
            alt={post.title}
            className="w-full h-64 md:h-96 object-cover rounded-lg shadow-lg"
          />
        </div>
      )}

      {/* Content */}
      <div 
        className="prose prose-lg max-w-none"
        dangerouslySetInnerHTML={{ __html: post.content }}
      />

      {/* Footer */}
      <footer className="mt-12 pt-8 border-t border-gray-200">
        <div className="flex justify-between items-center">
          <Link 
            href={`/${params.lang}/blog`}
            className="text-blue-600 hover:text-blue-800 font-medium"
          >
            ← More blog posts
          </Link>
          
          {post.category && (
            <Link 
              href={`/${params.lang}/blog?category=${post.category.slug}`}
              className="text-blue-600 hover:text-blue-800 font-medium"
            >
              More in {post.category.name} →
            </Link>
          )}
        </div>
      </footer>
    </article>
  );
}