"use client";
import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";

const T = {
  en: { 
    placeholder: "Search businesses, e.g. 'florist in Porto'",
    searchButton: "Search"
  },
  nl: { 
    placeholder: "Zoek bedrijven, bijv. 'bloemist in Porto'",
    searchButton: "Zoeken"
  },
  pt: { 
    placeholder: "Pesquisar empresas, ex. 'florista no Porto'",
    searchButton: "Pesquisar"
  },
  fr: { 
    placeholder: "Rechercher des entreprises, par ex. 'fleuriste à Porto'",
    searchButton: "Rechercher"
  },
  de: { 
    placeholder: "Unternehmen suchen, z.B. 'Florist in Porto'",
    searchButton: "Suchen"
  },
  es: { 
    placeholder: "Buscar empresas, ej. 'floristería en Porto'",
    searchButton: "Buscar"
  }
} as const;

export default function SearchBox({ lang }: { lang: string }) {
  const t = T[lang as keyof typeof T] || T.en;
  const [q, setQ] = useState("");
  const [sug, setSug] = useState<string[]>([]);
  const [open, setOpen] = useState(false);
  const router = useRouter();
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const h = (e: MouseEvent) => { 
      if (!ref.current?.contains(e.target as Node)) setOpen(false); 
    };
    document.addEventListener("click", h); 
    return () => document.removeEventListener("click", h);
  }, []);

  useEffect(() => {
    const t = setTimeout(async () => {
      if (!q.trim()) { setSug([]); return; }
      try {
        const url = `http://127.0.0.1:8000/api/v1/search/businesses/?q=${encodeURIComponent(q)}&limit=5`;
        const r = await fetch(url); 
        const j = await r.json();
        setSug((j.results ?? []).map((x: any) => x.name));
        setOpen((j.results ?? []).length > 0);
      } catch (error) {
        setSug([]);
        setOpen(false);
      }
    }, 250);
    return () => clearTimeout(t);
  }, [q]);

  function go(text?: string) {
    const query = (text ?? q).trim(); 
    if (!query) return;
    router.push(`/${lang}/search?q=${encodeURIComponent(query)}`);
  }

  return (
    <div ref={ref} className="relative">
      <div className="flex gap-2">
        <input
          className="input"
          placeholder={t.placeholder}
          value={q}
          onChange={(e) => setQ(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && go()}
        />
                <button 
          className="btn btn-primary"
          onClick={() => go()}
        >
          {t.searchButton}
        </button>
      </div>

      {open && (
        <div className="absolute z-20 mt-2 w-full overflow-hidden rounded-xl border bg-white shadow-soft">
          {sug.map((s, i) => (
            <button
              key={i}
              className="block w-full px-4 py-2 text-left hover:bg-gray-50"
              onMouseDown={() => go(s)}
            >
              {s}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}