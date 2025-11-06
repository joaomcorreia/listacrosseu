import SearchBoxNew from "@/components/SearchBoxNew";

async function fetchResults(q: string) {
  if (!q) return { total: 0, results: [] as any[] };
  // Use direct Django API for server-side rendering, proxy for client-side
  const isDev = process.env.NODE_ENV === 'development';
  const baseUrl = isDev ? 'http://127.0.0.1:8000' : process.env.NEXT_PUBLIC_API_URL || '';
  const url = `${baseUrl}/api/v1/search/businesses/?q=${encodeURIComponent(q)}&limit=50`;
  
  try {
    const r = await fetch(url, { cache: "no-store" });
    if (!r.ok) return { total: 0, results: [] as any[] };
    return await r.json();
  } catch (error) {
    console.error('API fetch error:', error);
    return { total: 0, results: [] as any[] };
  }
}

export async function generateMetadata({ searchParams }: { searchParams: { q?: string } }) {
  const q = searchParams.q || '';
  return {
    title: q ? `Results for "${q}" | ListAcross EU` : 'Search | ListAcross EU',
    robots: { index: false, follow: true },
  };
}

export default async function Page({ searchParams, params }: any) {
  const lang = params.lang ?? "en";
  const q = (searchParams?.q ?? "").toString();
  const data = await fetchResults(q);

  return (
    <div className="min-h-screen">
      {/* Hero Search Section */}
      <section className="bg-gradient-to-br from-brand via-purple-600 to-indigo-800 relative overflow-hidden pt-24 pb-16">
        {/* Animated Background Elements */}
        <div className="absolute inset-0">
          <div className="absolute top-20 left-10 w-32 h-32 bg-white/10 rounded-full animate-pulse"></div>
          <div className="absolute top-40 right-20 w-24 h-24 bg-white/5 rounded-full animate-bounce" style={{ animationDelay: '1s' }}></div>
          <div className="absolute bottom-20 left-1/4 w-40 h-40 bg-white/5 rounded-full animate-pulse" style={{ animationDelay: '2s' }}></div>
        </div>
        
        <div className="container mx-auto px-4 py-16 relative z-10 text-center text-white">
          <div className="inline-flex items-center bg-white/20 backdrop-blur-sm border border-white/30 rounded-full px-6 py-3 mb-8 animate-fade-in-up">
            <span className="text-sm text-white/90">🔍 Search across 30+ European countries</span>
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold mb-6 animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
            Find Businesses 
            <span className="block bg-gradient-to-r from-yellow-300 via-white to-blue-300 bg-clip-text text-transparent">
              Across Europe
            </span>
          </h1>
          
          <p className="text-xl text-white/90 mb-12 max-w-3xl mx-auto animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
            Type a category, service, or city. Results update instantly with live suggestions.
          </p>
          
          <div className="max-w-3xl mx-auto animate-fade-in-up" style={{ animationDelay: '0.6s' }}>
            <div className="bg-white/95 backdrop-blur-lg p-6 rounded-3xl shadow-2xl border border-white/50">
              <SearchBoxNew lang={lang} />
            </div>
          </div>
        </div>
      </section>

      {/* Results Section */}
      <section className="py-20 bg-white relative">
        <div className="absolute top-0 left-0 w-full h-32 bg-gradient-to-b from-brand/5 to-transparent"></div>
        <div className="container mx-auto px-4">
          <div className="flex items-baseline justify-between mb-8 animate-fade-in-up">
            <h2 className="text-3xl font-bold text-gray-900">
              {q ? `Results for "${q}"` : "Start searching"}
            </h2>
            <div className="text-lg text-brand font-semibold">
              {q ? `${data.total} found` : ""}
            </div>
          </div>

          {data.total === 0 ? (
            <div className="rounded-2xl border-2 border-dashed border-gray-300 p-12 text-center text-gray-600 animate-fade-in-up bg-gray-50">
              <div className="text-6xl mb-4">🔍</div>
              <div className="text-xl font-semibold mb-2">
                {q ? "No results found" : "Enter a search term"}
              </div>
              <div>
                {q ? "Try another term or check spelling." : "Find businesses across Europe by typing above."}
              </div>
            </div>
          ) : (
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {data.results.map((b: any, index: number) => (
                <article 
                  key={b.id ?? `${b.name}-${b.city}`} 
                  className="card group hover:shadow-2xl transition-all duration-300 transform hover:scale-105 animate-fade-in-up"
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  <div className="card-body">
                    <div className="flex items-start justify-between mb-3">
                      <h3 className="text-lg font-bold text-gray-900 group-hover:text-brand transition-colors">
                        {b.name}
                      </h3>
                      <div className="text-2xl">🏢</div>
                    </div>
                    
                    <div className="text-sm text-gray-600 mb-3 flex items-center gap-2">
                      <span className="bg-brand/10 text-brand px-2 py-1 rounded-full text-xs font-medium">
                        {b.category?.name || b.category}
                      </span>
                      <span>•</span>
                      <span>📍 {b.city}, {b.country}</span>
                    </div>
                    
                    {b.address && (
                      <div className="text-sm text-gray-500 mb-4 flex items-center gap-2">
                        📍 {b.address}
                      </div>
                    )}
                    
                    {(b.phone || b.website) && (
                      <div className="flex gap-3 pt-3 border-t border-gray-100">
                        {b.phone && (
                          <a 
                            href={`tel:${b.phone}`} 
                            className="flex items-center gap-2 text-brand hover:text-brand-dark transition-colors text-sm font-medium"
                          >
                            📞 Call
                          </a>
                        )}
                        {b.website && (
                          <a 
                            href={b.website} 
                            target="_blank" 
                            rel="noopener noreferrer" 
                            className="flex items-center gap-2 text-brand hover:text-brand-dark transition-colors text-sm font-medium"
                          >
                            🌐 Website
                          </a>
                        )}
                      </div>
                    )}
                  </div>
                </article>
              ))}
            </div>
          )}
        </div>
      </section>
    </div>
  );
}