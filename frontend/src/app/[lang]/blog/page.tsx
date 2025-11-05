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

export default async function BlogPage({ params }: { params: { lang: string } }) {
  const data = await apiCall(`/blog/posts/?limit=24&lang=${params.lang}`);
  const results: BlogPost[] = data?.results || [];

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold mb-4">Blog</h1>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Discover insights, tips, and stories about businesses across Europe. 
          Stay updated with the latest trends and opportunities in the European market.
        </p>
      </div>
      
      {results.length > 0 ? (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {results.map((post) => (
            <Link 
              key={post.slug} 
              href={`/${params.lang}/blog/${post.slug}`}
              className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden"
            >
              {post.cover_image && (
                <img 
                  src={post.cover_image} 
                  alt={post.title}
                  className="w-full h-48 object-cover"
                />
              )}
              <div className="p-6">
                <div className="mb-2">
                  {post.category && (
                    <span className="text-sm text-blue-600 font-medium">
                      {post.category.name}
                    </span>
                  )}
                  {post.is_featured && (
                    <span className="ml-2 text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full">
                      Featured
                    </span>
                  )}
                </div>
                
                <h2 className="text-xl font-bold text-gray-900 mb-3 line-clamp-2">
                  {post.title}
                </h2>
                
                {post.excerpt && (
                  <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                    {post.excerpt}
                  </p>
                )}
                
                <div className="text-sm text-gray-500">
                  {new Date(post.published_at).toLocaleDateString(params.lang, {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                  })}
                </div>
              </div>
            </Link>
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <h2 className="text-xl font-semibold text-gray-600 mb-2">No blog posts yet</h2>
          <p className="text-gray-500">Check back soon for exciting content!</p>
        </div>
      )}
    </div>
  );
}