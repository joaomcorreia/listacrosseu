'use client';

import React, { useState, useEffect, useRef } from 'react';
import Link from 'next/link';

interface BlogPost {
  id: number;
  title: string;
  slug: string;
  excerpt: string;
  cover_image?: string;
  published_at: string;
  author_name: string;
  category?: {
    name: string;
    slug: string;
    description?: string;
  };
  is_featured: boolean;
}

interface BlogPostsFooterProps {
  lang: string;
  limit?: number;
}

export default function BlogPostsFooter({ lang, limit = 3 }: BlogPostsFooterProps) {
  const [posts, setPosts] = useState<BlogPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isAutoScrolling, setIsAutoScrolling] = useState(true);
  const [canScrollLeft, setCanScrollLeft] = useState(false);
  const [canScrollRight, setCanScrollRight] = useState(true);
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const autoScrollIntervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    fetchPosts();
  }, [lang, limit]);

  useEffect(() => {
    const startAutoScroll = () => {
      if (autoScrollIntervalRef.current) {
        clearInterval(autoScrollIntervalRef.current);
      }
      
      autoScrollIntervalRef.current = setInterval(() => {
        if (scrollContainerRef.current && isAutoScrolling) {
          const container = scrollContainerRef.current;
          const scrollAmount = container.clientWidth * 0.8; // Scroll by 80% of container width
          
          if (container.scrollLeft + container.clientWidth >= container.scrollWidth) {
            // At end, scroll back to start
            container.scrollTo({ left: 0, behavior: 'smooth' });
          } else {
            // Scroll to the right
            container.scrollBy({ left: scrollAmount, behavior: 'smooth' });
          }
        }
      }, 4000); // Auto-scroll every 4 seconds
    };

    if (isAutoScrolling && posts.length > 3) {
      startAutoScroll();
    }

    return () => {
      if (autoScrollIntervalRef.current) {
        clearInterval(autoScrollIntervalRef.current);
      }
    };
  }, [isAutoScrolling, posts.length]);

  useEffect(() => {
    const updateScrollButtons = () => {
      if (scrollContainerRef.current) {
        const container = scrollContainerRef.current;
        setCanScrollLeft(container.scrollLeft > 0);
        setCanScrollRight(
          container.scrollLeft < container.scrollWidth - container.clientWidth
        );
      }
    };

    const container = scrollContainerRef.current;
    if (container) {
      container.addEventListener('scroll', updateScrollButtons);
      updateScrollButtons();
      
      return () => container.removeEventListener('scroll', updateScrollButtons);
    }
  }, [posts]);

  const scrollLeft = () => {
    if (scrollContainerRef.current) {
      const scrollAmount = scrollContainerRef.current.clientWidth * 0.8;
      scrollContainerRef.current.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
      setIsAutoScrolling(false); // Pause auto-scroll when user manually scrolls
    }
  };

  const scrollRight = () => {
    if (scrollContainerRef.current) {
      const scrollAmount = scrollContainerRef.current.clientWidth * 0.8;
      scrollContainerRef.current.scrollBy({ left: scrollAmount, behavior: 'smooth' });
      setIsAutoScrolling(false); // Pause auto-scroll when user manually scrolls
    }
  };

  const toggleAutoScroll = () => {
    setIsAutoScrolling(!isAutoScrolling);
  };

  const fetchPosts = async () => {
    try {
      setLoading(true);
      // Call Django API directly to avoid 308 redirect issues with Next.js proxy
      const response = await fetch(`http://localhost:8000/api/v1/blog/posts/?limit=${limit}&lang=${lang}`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch blog posts');
      }
      
      const data = await response.json();
      setPosts(data.results || []);
    } catch (err) {
      console.error('Error fetching blog posts:', err);
      setError(err instanceof Error ? err.message : 'Failed to fetch posts');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString(lang === 'fr' ? 'fr-FR' : 'en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const getTexts = (lang: string) => {
    switch (lang) {
      case 'fr':
        return {
          title: 'Derniers Articles',
          readMore: 'Lire Plus',
          viewAll: 'Voir Tous les Articles',
          by: 'Par',
          on: 'le',
          scrollLeft: 'Défiler vers la gauche',
          scrollRight: 'Défiler vers la droite',
          pauseAutoScroll: 'Suspendre le défilement automatique',
          resumeAutoScroll: 'Reprendre le défilement automatique'
        };
      case 'nl':
        return {
          title: 'Laatste Artikelen',
          readMore: 'Lees Meer',
          viewAll: 'Bekijk Alle Artikelen',
          by: 'Door',
          on: 'op',
          scrollLeft: 'Scroll naar links',
          scrollRight: 'Scroll naar rechts',
          pauseAutoScroll: 'Pauzeer auto-scroll',
          resumeAutoScroll: 'Hervat auto-scroll'
        };
      case 'pt':
        return {
          title: 'Últimos Artigos',
          readMore: 'Ler Mais',
          viewAll: 'Ver Todos os Artigos',
          by: 'Por',
          on: 'em',
          scrollLeft: 'Rolar para a esquerda',
          scrollRight: 'Rolar para a direita',
          pauseAutoScroll: 'Pausar rolagem automática',
          resumeAutoScroll: 'Retomar rolagem automática'
        };
      case 'de':
        return {
          title: 'Neueste Artikel',
          readMore: 'Mehr Lesen',
          viewAll: 'Alle Artikel Anzeigen',
          by: 'Von',
          on: 'am',
          scrollLeft: 'Nach links scrollen',
          scrollRight: 'Nach rechts scrollen',
          pauseAutoScroll: 'Auto-Scroll pausieren',
          resumeAutoScroll: 'Auto-Scroll fortsetzen'
        };
      case 'es':
        return {
          title: 'Últimos Artículos',
          readMore: 'Leer Más',
          viewAll: 'Ver Todos los Artículos',
          by: 'Por',
          on: 'el',
          scrollLeft: 'Desplazar a la izquierda',
          scrollRight: 'Desplazar a la derecha',
          pauseAutoScroll: 'Pausar auto-scroll',
          resumeAutoScroll: 'Reanudar auto-scroll'
        };
      case 'ar':
        return {
          title: 'أحدث المقالات',
          readMore: 'اقرأ المزيد',
          viewAll: 'عرض جميع المقالات',
          by: 'بواسطة',
          on: 'في',
          scrollLeft: 'انتقل لليسار',
          scrollRight: 'انتقل لليمين',
          pauseAutoScroll: 'إيقاف التمرير التلقائي مؤقتاً',
          resumeAutoScroll: 'استئناف التمرير التلقائي'
        };
      default:
        return {
          title: 'Latest Articles',
          readMore: 'Read More',
          viewAll: 'View All Articles',
          by: 'By',
          on: 'on',
          scrollLeft: 'Scroll left',
          scrollRight: 'Scroll right',
          pauseAutoScroll: 'Pause auto-scroll',
          resumeAutoScroll: 'Resume auto-scroll'
        };
    }
  };

  if (loading) {
    return (
      <section className="bg-gray-50 py-12 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-300 rounded w-48 mb-8"></div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="bg-white rounded-lg shadow-md p-6">
                  <div className="h-6 bg-gray-300 rounded mb-4"></div>
                  <div className="h-4 bg-gray-300 rounded mb-2"></div>
                  <div className="h-4 bg-gray-300 rounded mb-4 w-3/4"></div>
                  <div className="h-4 bg-gray-300 rounded w-1/2"></div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>
    );
  }

  if (error || posts.length === 0) {
    return null; // Don't show anything if there's an error or no posts
  }

  const texts = getTexts(lang);

  return (
    <section className="bg-gray-50 py-12 mt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between mb-12">
          <div className="text-center flex-1">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              {texts.title}
            </h2>
            <div className="w-20 h-1 bg-blue-600 mx-auto"></div>
          </div>
          
          {/* Auto-scroll Controls */}
          {posts.length > 3 && (
            <div className="flex items-center gap-3 ml-8">
              <button
                onClick={toggleAutoScroll}
                title={isAutoScrolling ? texts.pauseAutoScroll : texts.resumeAutoScroll}
                className={`p-2 rounded-full transition-colors duration-200 ${
                  isAutoScrolling 
                    ? 'bg-blue-600 text-white hover:bg-blue-700' 
                    : 'bg-gray-300 text-gray-600 hover:bg-gray-400'
                }`}
              >
                {isAutoScrolling ? (
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 9v6m4-6v6" />
                  </svg>
                ) : (
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h6v6M9 10l6 6M9 16l6-6" />
                  </svg>
                )}
              </button>
              
              <button
                onClick={scrollLeft}
                disabled={!canScrollLeft}
                title={texts.scrollLeft}
                className={`p-2 rounded-full transition-colors duration-200 ${
                  canScrollLeft 
                    ? 'bg-gray-200 text-gray-700 hover:bg-gray-300' 
                    : 'bg-gray-100 text-gray-400 cursor-not-allowed'
                }`}
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              
              <button
                onClick={scrollRight}
                disabled={!canScrollRight}
                title={texts.scrollRight}
                className={`p-2 rounded-full transition-colors duration-200 ${
                  canScrollRight 
                    ? 'bg-gray-200 text-gray-700 hover:bg-gray-300' 
                    : 'bg-gray-100 text-gray-400 cursor-not-allowed'
                }`}
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          )}
        </div>

        {/* Scrollable Cards Container */}
        <div className="relative">
          <div
            ref={scrollContainerRef}
            className="flex gap-6 overflow-x-auto scrollbar-hide scroll-smooth pb-4"
            style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
            onMouseEnter={() => setIsAutoScrolling(false)}
            onMouseLeave={() => posts.length > 3 && setTimeout(() => setIsAutoScrolling(true), 2000)}
          >
            {posts.map((post) => (
              <article key={post.id} className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden flex-shrink-0 w-80">
                {post.cover_image && (
                  <div className="relative h-48 overflow-hidden">
                    <img
                      src={post.cover_image}
                      alt={post.title}
                      className="w-full h-full object-cover"
                    />
                  </div>
                )}
                
                <div className="p-6">
                  <div className="flex items-center text-sm text-gray-500 mb-3">
                    <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                    <span className="mr-4">{texts.by} {post.author_name || 'Unknown Author'}</span>
                    <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    <span>{texts.on} {formatDate(post.published_at)}</span>
                  </div>

                  {post.category && (
                    <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full mb-3">
                      {post.category.name}
                    </span>
                  )}

                  <h3 className="text-xl font-semibold text-gray-900 mb-3 line-clamp-2">
                    {post.title}
                  </h3>

                  <p className="text-gray-600 mb-4 line-clamp-3">
                    {post.excerpt}
                  </p>

                  <Link
                    href={`/${lang}/blog/${post.slug}`}
                    className="inline-flex items-center text-blue-600 hover:text-blue-800 font-medium transition-colors duration-200"
                  >
                    {texts.readMore}
                    <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </Link>
                </div>
              </article>
            ))}
          </div>
        </div>

        <div className="text-center mt-12">
          <Link
            href={`/${lang}/blog`}
            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 transition-colors duration-200"
          >
            {texts.viewAll}
            <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </Link>
        </div>
      </div>
      
      {/* Custom CSS for hiding scrollbar */}
      <style jsx>{`
        .scrollbar-hide::-webkit-scrollbar {
          display: none;
        }
      `}</style>
    </section>
  );
}