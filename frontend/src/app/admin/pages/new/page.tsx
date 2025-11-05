'use client';
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import type { Lang } from '@/types/seo';

const ALL_LANGS: Lang[] = ['NL','PT','EN','FR','DE','ES'];

export default function CreatePage() {
  const router = useRouter();
  const [name, setName] = useState('');
  const [path, setPath] = useState('');
  const [type, setType] = useState<'static'|'dynamic'>('static');
  const [langs, setLangs] = useState<Lang[]>(ALL_LANGS);

  async function onCreate() {
    const res = await fetch('/api/admin/pages', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ name, path, type, langs })
    });
    const page = await res.json();
    router.push(`/admin/pages/${page.id}`);
  }

  function toggleLang(l: Lang) {
    setLangs(prev => prev.includes(l) ? prev.filter(x => x !== l) : [...prev, l]);
  }

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-semibold">Create Page</h1>

      <div className="bg-white rounded-2xl border border-gray-100 p-5 space-y-4">
        <div>
          <label className="block text-sm font-medium">Name</label>
          <input className="mt-1 w-full rounded-xl border border-gray-300 px-3 py-2" value={name} onChange={e=>setName(e.target.value)} placeholder="About, Countries, City PT, etc."/>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium">Path</label>
            <input className="mt-1 w-full rounded-xl border border-gray-300 px-3 py-2" value={path} onChange={e=>setPath(e.target.value)} placeholder="/about"/>
          </div>
          <div>
            <label className="block text-sm font-medium">Type</label>
            <select className="mt-1 w-full rounded-xl border border-gray-300 px-3 py-2" value={type} onChange={e=>setType(e.target.value as any)}>
              <option value="static">Static</option>
              <option value="dynamic">Dynamic</option>
            </select>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Languages</label>
          <div className="flex flex-wrap gap-2">
            {ALL_LANGS.map(l => (
              <label key={l} className={`px-3 py-1 rounded-full border cursor-pointer ${langs.includes(l) ? 'bg-blue-600 text-white border-blue-600' : 'bg-white text-gray-700 border-gray-300'}`}>
                <input type="checkbox" checked={langs.includes(l)} onChange={()=>toggleLang(l)} className="hidden"/>{l}
              </label>
            ))}
          </div>
        </div>

        <div className="flex items-center justify-end gap-3">
          <button className="px-4 py-2 rounded-xl border" onClick={()=>history.back()}>Cancel</button>
          <button className="px-4 py-2 rounded-xl bg-blue-600 text-white" onClick={onCreate} disabled={!name || !path}>Create</button>
        </div>
      </div>
    </div>
  );
}