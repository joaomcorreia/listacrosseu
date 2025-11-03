"use client";
import { useState } from "react";
import { actionCreateListing, actionStartJCWBuild, actionStartPrintOrder } from "@/lib/assistant";

export default function AssistantToolsPanel() {
  const [msg, setMsg] = useState<string | null>(null);
  const [err, setErr] = useState<string | null>(null);

  // Forms
  const [biz, setBiz] = useState({ business_name: "", country: "PT", city: "" , email: "", phone: "" });
  const [jcw, setJCW] = useState({ tenant_id: "laeu-tenant-123", preferred_locales: "en,pt", template_id: "jcw-rest-01" });
  const [prt, setPRT] = useState({ product: "business_card_standard", quantity: 250 });

  async function run<T>(fn: ()=>Promise<T>) {
    setMsg(null); setErr(null);
    try {
      const out = await fn();
      setMsg(JSON.stringify(out));
      setTimeout(()=>setMsg(null), 4000);
    } catch (e:any) {
      setErr(e.message || String(e));
      setTimeout(()=>setErr(null), 5000);
    }
  }

  return (
    <div className="max-w-5xl border rounded-xl p-4 space-y-6">
      <h2 className="text-lg font-semibold">Tools tester</h2>

      {/* Create Listing */}
      <div className="border rounded p-3 space-y-2">
        <div className="font-medium">Create listing</div>
        <div className="grid md:grid-cols-3 gap-2">
          <input className="border rounded p-2 text-sm" placeholder="Business name" value={biz.business_name} onChange={(e)=>setBiz({...biz, business_name:e.target.value})}/>
          <input className="border rounded p-2 text-sm" placeholder="Country (PT)" value={biz.country} onChange={(e)=>setBiz({...biz, country:e.target.value})}/>
          <input className="border rounded p-2 text-sm" placeholder="City" value={biz.city} onChange={(e)=>setBiz({...biz, city:e.target.value})}/>
          <input className="border rounded p-2 text-sm" placeholder="Email (optional)" value={biz.email} onChange={(e)=>setBiz({...biz, email:e.target.value})}/>
          <input className="border rounded p-2 text-sm" placeholder="Phone (optional)" value={biz.phone} onChange={(e)=>setBiz({...biz, phone:e.target.value})}/>
        </div>
        <button className="px-3 py-2 border rounded text-sm" onClick={()=>run(()=>actionCreateListing(biz))}>Test create_listing</button>
      </div>

      {/* Start JCW build */}
      <div className="border rounded p-3 space-y-2">
        <div className="font-medium">Start JCW build</div>
        <div className="grid md:grid-cols-3 gap-2">
          <input className="border rounded p-2 text-sm" placeholder="Tenant ID" value={jcw.tenant_id} onChange={(e)=>setJCW({...jcw, tenant_id:e.target.value})}/>
          <input className="border rounded p-2 text-sm" placeholder="Preferred locales (comma)" value={jcw.preferred_locales} onChange={(e)=>setJCW({...jcw, preferred_locales:e.target.value})}/>
          <input className="border rounded p-2 text-sm" placeholder="Template ID" value={jcw.template_id} onChange={(e)=>setJCW({...jcw, template_id:e.target.value})}/>
        </div>
        <button className="px-3 py-2 border rounded text-sm" onClick={()=>run(()=>actionStartJCWBuild({
          tenant_id: jcw.tenant_id,
          preferred_locales: jcw.preferred_locales.split(",").map(s=>s.trim()).filter(Boolean),
          template_id: jcw.template_id
        }))}>Test start_jcw_build</button>
      </div>

      {/* Start Print order */}
      <div className="border rounded p-3 space-y-2">
        <div className="font-medium">Start print order</div>
        <div className="grid md:grid-cols-3 gap-2">
          <input className="border rounded p-2 text-sm" placeholder="Product code" value={prt.product} onChange={(e)=>setPRT({...prt, product:e.target.value})}/>
          <input className="border rounded p-2 text-sm" type="number" placeholder="Quantity" value={prt.quantity} onChange={(e)=>setPRT({...prt, quantity: Number(e.target.value || 0)})}/>
        </div>
        <button className="px-3 py-2 border rounded text-sm" onClick={()=>run(()=>actionStartPrintOrder(prt))}>Test start_print_order</button>
      </div>

      {msg && <div className="text-sm text-green-700 break-words">Result: {msg}</div>}
      {err && <div className="text-sm text-red-700">Error: {err}</div>}
    </div>
  );
}