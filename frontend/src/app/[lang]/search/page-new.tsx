import SearchBoxNew from "@/components/SearchBoxNew";

async function fetchResults(q: string) {
  if (!q) return { total: 0, results: [] as any[] };
  const url = `http://127.0.0.1:8000/api/v1/search/businesses/?q=${encodeURIComponent(q)}&limit=50`;
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
    <div className="space-y-8">
      <section className="rounded-2xl bg-brand-light p-6">
        <div className="grid gap-4 md:grid-cols-3 md:items-center">
          <div className="md:col-span-2">
            <h1 className="text-2xl font-bold mb-2">Find businesses across Europe</h1>
            <p className="text-gray-600">Type a category, service, or city. Results update instantly.</p>
          </div>
          <div className="md:col-span-1">
            <SearchBoxNew lang={lang} />
          </div>
        </div>
      </section>

      <section className="space-y-3">
        <div className="flex items-baseline justify-between">
          <h2 className="text-xl font-semibold">{q ? `Results for "${q}"` : "Start searching"}</h2>
          <div className="text-sm text-gray-600">{q ? `${data.total} found` : ""}</div>
        </div>

        {data.total === 0 ? (
          <div className="rounded-xl border p-8 text-gray-600">
            {q ? "No results found. Try another term or check spelling." : "Enter a search term above to find businesses across Europe."}
          </div>
        ) : (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {data.results.map((b: any) => (
              <article key={b.id ?? `${b.name}-${b.city}`} className="card">
                <div className="card-body">
                  <div className="mb-1 text-base font-semibold">{b.name}</div>
                  <div className="text-sm text-gray-600">
                    {b.category?.name || b.category} · {b.city}, {b.country}
                  </div>
                  {b.address && <div className="mt-2 text-sm">{b.address}</div>}
                  {(b.phone || b.website) && (
                    <div className="mt-3 flex gap-2 text-xs">
                      {b.phone && (
                        <a href={`tel:${b.phone}`} className="text-brand hover:underline">
                          📞 {b.phone}
                        </a>
                      )}
                      {b.website && (
                        <a href={b.website} target="_blank" rel="noopener noreferrer" className="text-brand hover:underline">
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
      </section>
    </div>
  );
}