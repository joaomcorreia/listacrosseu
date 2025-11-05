'use client';
import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import SeoPanel from '@/components/admin/SeoPanel';
import type { AdminPageWithSeo } from '@/types/page';
import type { SeoByLang } from '@/types/seo';

export default function EditPage() {
  const { id } = useParams<{ id: string }>();
  const [item, setItem] = useState<AdminPageWithSeo | null>(null);
  const [seo, setSeo] = useState<SeoByLang | null>(null);

  useEffect(() => {
    fetch(`/api/admin/pages/${id}`).then(r=>r.json()).then(setItem);
    fetch(`/api/admin/seo/page/${id}`).then(r=>r.json()).then(setSeo);
  }, [id]);

  async function saveSeo() {
    if (!seo) return;
    await fetch(`/api/admin/seo/page/${id}`, {
      method: 'PUT',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(seo)
    });
    alert('SEO saved');
  }

  if (!item || !seo) return <div className="p-6">Loading…</div>;

  return (
    <div className="p-6 space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Edit Page — {item.name}</h1>
        <div className="text-sm text-gray-500">Path: {item.path}</div>
      </div>

      {/* Content tab placeholder */}
      <div className="bg-white rounded-2xl border border-gray-100 p-5">
        <div className="text-sm text-gray-600">Content editor placeholder (add your page-specific fields here).</div>
      </div>

      {/* SEO tab */}
      <div className="bg-white rounded-2xl border border-gray-100 p-5">
        <SeoPanel valueByLang={seo} onChange={setSeo} baseUrl="https://listacross.eu" />
        <div className="flex items-center justify-end gap-3 mt-4">
          <button className="px-4 py-2 rounded-xl border" onClick={()=>location.reload()}>Discard</button>
          <button className="px-4 py-2 rounded-xl bg-blue-600 text-white" onClick={saveSeo}>Save SEO</button>
        </div>
      </div>
    </div>
  );
}