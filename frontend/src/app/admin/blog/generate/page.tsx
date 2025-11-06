"use client";
import React, {useMemo, useState} from "react";

type OutlineSection = { h2: string; bullets: string[] };
type OutlineResp = {
  title: string;
  sections: OutlineSection[];
  candidate_faqs?: string[];
  sources?: {title:string; url:string; note?:string}[];
};
type DraftResp = {
  body_html: string;
  headings?: string[];
  toc?: {id:string; text:string}[];
  citations?: {title:string; url:string; note?:string}[];
  internal_links?: {href:string; anchor:string}[];
};
type SEOResp = {
  meta_title: string;
  meta_desc: string;
  slug: string;
  alt_texts?: {selector:string; alt:string}[];
  tags?: string[];
};

const api = {
  outline: "/api/v1/ai/generate/outline",
  draft: "/api/v1/ai/generate/draft",
  seo: "/api/v1/ai/generate/seo",
  posts: "/api/v1/posts"
};

function Label({children}:{children:React.ReactNode}) {
  return <label className="block text-sm font-medium text-gray-700 mb-1">{children}</label>;
}
function Input(props: React.InputHTMLAttributes<HTMLInputElement>) {
  return <input {...props} className={"w-full rounded-xl bg-white border border-gray-300 px-3 py-2 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 "+(props.className||"")} />;
}
function TextArea(props: React.TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return <textarea {...props} className={"w-full rounded-xl bg-white border border-gray-300 px-3 py-2 min-h-[120px] text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 "+(props.className||"")} />;
}
function Button({children, ...rest}: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return <button {...rest} className={"rounded-2xl px-4 py-2 font-medium shadow-sm border border-gray-700 hover:bg-gray-800 disabled:opacity-50 "+(rest.className||"")}>{children}</button>;
}

export default function Page() {
  const [topic, setTopic] = useState("");
  const [language, setLanguage] = useState("en");
  const [country, setCountry] = useState("");
  const [keywords, setKeywords] = useState("eu, small business, registration");
  const [tone, setTone] = useState("helpful, expert, approachable");
  const [loading, setLoading] = useState<null | "outline" | "draft" | "seo" | "save" | "publish">(null);

  const [outline, setOutline] = useState<OutlineResp | null>(null);
  const [draft, setDraft] = useState<DraftResp | null>(null);
  const [seo, setSeo] = useState<SEOResp | null>(null);

  const [postId, setPostId] = useState<string>("");
  const [messages, setMessages] = useState<string[]>([]);

  const reliability = useMemo(() => {
    const body = draft?.body_html || "";
    const hasMoneyOrDates = /\€\s?\d|\b\d{4}\b/.test(body);
    const hasCitations = (draft?.citations?.length || 0) > 0;
    const hasInternal = (draft?.internal_links?.length || 0) >= 2;
    return {
      hasMoneyOrDates, hasCitations, hasInternal,
      ok: (!hasMoneyOrDates || hasCitations) && hasInternal
    };
  }, [draft]);

  const pushMsg = (m:string) => setMessages(prev => [m, ...prev].slice(0,6));

  async function postJSON<T>(url: string, payload: any): Promise<T> {
    const res = await fetch(url, { method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(payload) });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(`${res.status} ${res.statusText}: ${text}`);
    }
    return res.json() as Promise<T>;
  }

  async function handleOutline() {
    setLoading("outline");
    setOutline(null); setDraft(null); setSeo(null); setPostId("");
    try {
      const payload = {
        topic: topic.trim(),
        language,
        country_code: country.trim(),
        keywords: keywords.split(",").map(k=>k.trim()).filter(Boolean),
        tone
      };
      const data = await postJSON<{outline: OutlineResp}>(api.outline, payload);
      setOutline(data.outline || (data as any));
      pushMsg("Outline generated.");
    } catch (e:any) { pushMsg("Outline error: "+e.message); }
    finally { setLoading(null); }
  }

  async function handleDraft() {
    if (!outline) { pushMsg("Generate an outline first."); return; }
    setLoading("draft"); setDraft(null);
    try {
      const data = await postJSON<{draft: DraftResp}>(api.draft, { outline });
      setDraft(data.draft || (data as any));
      pushMsg("Draft generated.");
    } catch (e:any) { pushMsg("Draft error: "+e.message); }
    finally { setLoading(null); }
  }

  async function handleSEO() {
    if (!outline) { pushMsg("Generate outline first."); return; }
    const title = outline.title || topic || "Post";
    setLoading("seo"); setSeo(null);
    try {
      const data = await postJSON<{seo: SEOResp}>(api.seo, {
        title,
        proposed_slug: title.toLowerCase().replace(/\s+/g,"-").replace(/[^a-z0-9\-]/g,"").slice(0,200),
        language,
        keywords: keywords.split(",").map(k=>k.trim()).filter(Boolean)
      });
      setSeo(data.seo || (data as any));
      pushMsg("SEO generated.");
    } catch (e:any) { pushMsg("SEO error: "+e.message); }
    finally { setLoading(null); }
  }

  async function handleSaveDraft() {
    if (!draft || !outline || !seo) { pushMsg("Run Outline, Draft and SEO first."); return; }
    setLoading("save");
    try {
      const content = {
        title: outline.title,
        summary: "",
        body_html: draft.body_html,
        headings: draft.headings || [],
        toc: draft.toc || [],
        images: [],
        meta: {
          title: seo.meta_title,
          description: seo.meta_desc,
          keywords: keywords.split(",").map(k=>k.trim()).filter(Boolean),
          slug: seo.slug
        },
        internal_links: draft.internal_links || [],
        external_citations: draft.citations || []
      };
      const payload = {
        canonical_lang: language,
        languages: [language],
        content_json: { [language]: content },
        tags: seo.tags || [],
        category: "",
        country_code: (country || "").toUpperCase()
      };
      const res = await postJSON<{id:string; slug:string}>(api.posts, payload);
      setPostId(res.id);
      pushMsg("Saved draft: "+res.slug);
    } catch (e:any) { pushMsg("Save error: "+e.message); }
    finally { setLoading(null); }
  }

  async function handlePublish() {
    if (!postId) { pushMsg("Save a draft first."); return; }
    if (!reliability.ok) { pushMsg("Reliability checks not met."); return; }
    setLoading("publish");
    try {
      const res = await postJSON<{ok:boolean; published_at?:string}>(`/api/v1/posts/${postId}/publish`, {});
      if ((res as any).error) throw new Error((res as any).error);
      pushMsg("Published ✔");
    } catch (e:any) { pushMsg("Publish error: "+e.message); }
    finally { setLoading(null); }
  }

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Listy → Blog Generator</h1>
        <div className="text-sm opacity-70">/admin/blog/generate</div>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        <div className="md:col-span-2 space-y-6">
          <div className="rounded-2xl border border-gray-800 p-4 space-y-4">
            <div className="grid sm:grid-cols-2 gap-4">
              <div>
                <Label>Topic</Label>
                <Input placeholder="Register a business in Portugal (2025)…" value={topic} onChange={e=>setTopic(e.target.value)} />
              </div>
              <div>
                <Label>Language</Label>
                <Input placeholder="en | nl | pt | fr | de | es" value={language} onChange={e=>setLanguage(e.target.value)} />
              </div>
              <div>
                <Label>Country focus (optional)</Label>
                <Input placeholder="PT, NL, FR…" value={country} onChange={e=>setCountry(e.target.value)} />
              </div>
              <div>
                <Label>Primary keywords (comma-sep)</Label>
                <Input value={keywords} onChange={e=>setKeywords(e.target.value)} />
              </div>
            </div>
            <div>
              <Label>Tone</Label>
              <TextArea value={tone} onChange={e=>setTone(e.target.value)} />
            </div>
            <div className="flex gap-3">
              <Button onClick={handleOutline} disabled={loading!==null}>{loading==="outline"?"…":"1) Get Outline"}</Button>
              <Button onClick={handleDraft} disabled={!outline || loading!==null}>{loading==="draft"?"…":"2) Generate Draft"}</Button>
              <Button onClick={handleSEO} disabled={!outline || loading!==null}>{loading==="seo"?"…":"3) Add SEO"}</Button>
            </div>
          </div>

          <div className="rounded-2xl border border-gray-800 p-4">
            <h2 className="text-lg font-semibold mb-3">Preview</h2>
            {!draft && <div className="text-sm opacity-70">No draft yet.</div>}
            {draft && (
              <div className="prose prose-invert max-w-none" dangerouslySetInnerHTML={{__html: draft.body_html}} />
            )}
          </div>
        </div>

        <div className="space-y-6">
          <div className="rounded-2xl border border-gray-800 p-4">
            <h3 className="font-semibold mb-3">Reliability checks</h3>
            <ul className="text-sm space-y-2">
              <li>• At least 2 internal links: <b>{(draft?.internal_links?.length||0) >= 2 ? "OK" : "Missing"}</b></li>
              <li>• Citations when € or years present: <b>{reliability.hasMoneyOrDates ? (reliability.hasCitations ? "OK" : "Missing") : "N/A"}</b></li>
            </ul>
          </div>

          <div className="rounded-2xl border border-gray-800 p-4 space-y-3">
            <div className="flex gap-3">
              <Button onClick={handleSaveDraft} disabled={!draft || !seo || loading!==null}>{loading==="save"?"…":"4) Save Draft"}</Button>
              <Button onClick={handlePublish} disabled={!postId || !reliability.ok || loading!==null} className="border-blue-500">{loading==="publish"?"…":"5) Publish"}</Button>
            </div>
            <div className="text-xs text-gray-400 space-y-1">
              {messages.map((m,i)=>(<div key={i}>• {m}</div>))}
            </div>
          </div>

          <div className="rounded-2xl border border-gray-800 p-4">
            <h3 className="font-semibold mb-2">Outline & SEO</h3>
            <div className="text-xs">
              {outline && (
                <details open className="mb-2">
                  <summary className="cursor-pointer">Outline</summary>
                  <pre className="whitespace-pre-wrap">{JSON.stringify(outline, null, 2)}</pre>
                </details>
              )}
              {seo && (
                <details>
                  <summary className="cursor-pointer">SEO</summary>
                  <pre className="whitespace-pre-wrap">{JSON.stringify(seo, null, 2)}</pre>
                </details>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}