"use client";
import { useEffect, useState } from "react";
import { listIntents, saveIntent } from "@/lib/assistant";

const STYLES = [{v:"short",l:"Short"},{v:"detailed",l:"Detailed"}];
const CTAS = [
  {v:"none",l:"None"},
  {v:"create_listing",l:"Create Listing"},
  {v:"upgrade_plan",l:"Upgrade Plan"},
  {v:"start_jcw_build",l:"Start JCW Build"},
  {v:"start_print_order",l:"Start Print Order"}
];

export default function AssistantIntentsPanel() {
  const [items, setItems] = useState<any[]>([]);
  const [editing, setEditing] = useState<any|null>(null);
  const [err, setErr] = useState<string|null>(null);
  const [msg, setMsg] = useState<string|null>(null);
  const [loading, setLoading] = useState(false);

  async function refresh() {
    setErr(null);
    try { setItems((await listIntents()).items); } catch(e:any){ setErr(e.message||String(e)); }
  }
  useEffect(()=>{ refresh(); }, []);

  function newIntent() {
    setEditing({
      name: "", title: "", enabled: true, priority: 0,
      examples: [], keywords: [], answer_style: "short",
      primary_cta: "none", fallback_doc_slugs: []
    });
  }

  function listToCSV(arr:any[]) { return (arr||[]).join(","); }
  function csvToList(s:string) { return s.split(",").map(x=>x.trim()).filter(Boolean); }

  async function onSave() {
    if (!editing) return;
    setLoading(true); setErr(null); setMsg(null);
    try {
      const payload = {
        ...editing,
        examples: typeof editing.examples === "string" ? csvToList(editing.examples) : editing.examples,
        keywords: typeof editing.keywords === "string" ? csvToList(editing.keywords) : editing.keywords,
        fallback_doc_slugs: typeof editing.fallback_doc_slugs === "string"
          ? csvToList(editing.fallback_doc_slugs) : editing.fallback_doc_slugs,
      };
      await saveIntent(payload);
      setEditing(null);
      await refresh();
      setMsg("Saved.");
    } catch(e:any){ setErr(e.message||String(e)); }
    finally { setLoading(false); setTimeout(()=>setMsg(null),1500); }
  }

  return (
    <div className="max-w-5xl border rounded-xl p-4 space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">Intents</h2>
        <button onClick={newIntent} className="px-3 py-2 border rounded text-sm hover:bg-gray-50">Add intent</button>
      </div>

      <div className="border rounded overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-gray-50 text-left">
              <th className="p-2">Name</th>
              <th className="p-2">Title</th>
              <th className="p-2">Enabled</th>
              <th className="p-2">Priority</th>
              <th className="p-2">Primary CTA</th>
              <th className="p-2">Updated</th>
              <th className="p-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {items.map((it:any)=>(
              <tr key={it.id} className="border-t">
                <td className="p-2 font-mono">{it.name}</td>
                <td className="p-2">{it.title}</td>
                <td className="p-2">{it.enabled ? "yes":"no"}</td>
                <td className="p-2">{it.priority}</td>
                <td className="p-2">{it.primary_cta}</td>
                <td className="p-2">{new Date(it.updated_at).toLocaleString()}</td>
                <td className="p-2">
                  <button className="px-2 py-1 border rounded text-xs hover:bg-gray-50" onClick={()=>setEditing(it)}>Edit</button>
                </td>
              </tr>
            ))}
            {items.length===0 && <tr><td className="p-2 text-gray-500" colSpan={7}>No intents.</td></tr>}
          </tbody>
        </table>
      </div>

      {editing && (
        <div className="border rounded p-3 space-y-3">
          <div className="grid md:grid-cols-4 gap-3">
            <div>
              <label className="block text-sm font-medium mb-1">Name (slug)</label>
              <input className="w-full border rounded p-2 text-sm font-mono" value={editing.name||""} onChange={e=>setEditing({...editing,name:e.target.value})}/>
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium mb-1">Title</label>
              <input className="w-full border rounded p-2 text-sm" value={editing.title||""} onChange={e=>setEditing({...editing,title:e.target.value})}/>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Enabled</label>
              <select className="w-full border rounded p-2 text-sm" value={editing.enabled ? "1":"0"} onChange={e=>setEditing({...editing,enabled:e.target.value==="1"})}>
                <option value="1">Yes</option><option value="0">No</option>
              </select>
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-3">
            <div>
              <label className="block text-sm font-medium mb-1">Priority</label>
              <input type="number" className="w-full border rounded p-2 text-sm" value={editing.priority??0} onChange={e=>setEditing({...editing,priority:Number(e.target.value||0)})}/>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Answer Style</label>
              <select className="w-full border rounded p-2 text-sm" value={editing.answer_style} onChange={e=>setEditing({...editing,answer_style:e.target.value})}>
                {STYLES.map(s=><option key={s.v} value={s.v}>{s.l}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Primary CTA</label>
              <select className="w-full border rounded p-2 text-sm" value={editing.primary_cta} onChange={e=>setEditing({...editing,primary_cta:e.target.value})}>
                {CTAS.map(c=><option key={c.v} value={c.v}>{c.l}</option>)}
              </select>
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-3">
            <div className="md:col-span-1">
              <label className="block text-sm font-medium mb-1">Examples (comma)</label>
              <input className="w-full border rounded p-2 text-sm"
                     value={Array.isArray(editing.examples)?editing.examples.join(","):editing.examples||""}
                     onChange={e=>setEditing({...editing,examples:e.target.value})}/>
            </div>
            <div className="md:col-span-1">
              <label className="block text-sm font-medium mb-1">Keywords (comma)</label>
              <input className="w-full border rounded p-2 text-sm"
                     value={Array.isArray(editing.keywords)?editing.keywords.join(","):editing.keywords||""}
                     onChange={e=>setEditing({...editing,keywords:e.target.value})}/>
            </div>
            <div className="md:col-span-1">
              <label className="block text-sm font-medium mb-1">Fallback docs (comma slugs)</label>
              <input className="w-full border rounded p-2 text-sm"
                     value={Array.isArray(editing.fallback_doc_slugs)?editing.fallback_doc_slugs.join(","):editing.fallback_doc_slugs||""}
                     onChange={e=>setEditing({...editing,fallback_doc_slugs:e.target.value})}/>
            </div>
          </div>

          <div className="flex gap-2">
            <button 
              className="px-3 py-2 border rounded text-sm hover:bg-gray-50" 
              onClick={()=>setEditing(null)}
              disabled={loading}
            >
              Cancel
            </button>
            <button 
              className="px-3 py-2 border rounded bg-black text-white text-sm hover:bg-gray-800 disabled:opacity-50" 
              onClick={onSave}
              disabled={loading}
            >
              {loading ? "Saving..." : "Save"}
            </button>
          </div>
        </div>
      )}

      {msg && <div className="text-green-700 text-sm">{msg}</div>}
      {err && <div className="text-red-700 text-sm">{err}</div>}
    </div>
  );
}