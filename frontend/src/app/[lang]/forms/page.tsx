'use client';
import { UI, type Lang, FORMS_SLUG } from '@/i18n/forms';
import { useState } from 'react';

function langFrom(param?: string): Lang {
  const m = (param||'en').toLowerCase();
  if (m==='nl') return 'NL';
  if (m==='pt') return 'PT';
  if (m==='fr') return 'FR';
  if (m==='de') return 'DE';
  if (m==='es') return 'ES';
  return 'EN';
}

type TabKey = 'free'|'claim'|'upgrade';

export default function FormsPage({ params }: { params: { lang: string }}) {
  const L = langFrom(params.lang);
  const t = UI[L];
  const [tab, setTab] = useState<TabKey>('free');

  return (
    <main className="px-6 py-8 space-y-8">
      {/* Hero */}
      <section className="text-center max-w-4xl mx-auto">
        <h1 className="text-3xl md:text-4xl font-semibold">{t.heroTitle}</h1>
        <p className="mt-3 text-gray-600">{t.heroSubtitle}</p>
      </section>

      {/* Tabs */}
      <div className="max-w-5xl mx-auto">
        <div className="flex flex-wrap gap-2 justify-center">
          {(['free','claim','upgrade'] as TabKey[]).map(k => (
            <button key={k}
              onClick={()=>setTab(k)}
              className={`px-4 py-2 rounded-full border text-sm ${tab===k ? 'bg-blue-600 text-white border-blue-600' : 'bg-white text-gray-700 border-gray-300'}`}>
              {t.tabs[k]}
            </button>
          ))}
        </div>
      </div>

      {/* Panels */}
      <section className="max-w-5xl mx-auto">
        {tab === 'free' && <FreeForm L={L}/>}
        {tab === 'claim' && <ClaimForm L={L}/>}
        {tab === 'upgrade' && <UpgradeForm L={L}/>}
      </section>
    </main>
  );
}

// ---------- UI helpers ----------
function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="block">
      <span className="block text-sm font-medium mb-1">{label}</span>
      {children}
    </label>
  );
}
function Input(props: React.InputHTMLAttributes<HTMLInputElement>) {
  return <input {...props} className={`w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 ${props.className||''}`} />;
}
function Textarea(props: React.TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return <textarea {...props} className={`w-full rounded-xl border border-gray-300 px-3 py-2 h-28 resize-y focus:outline-none focus:ring-2 focus:ring-blue-500 ${props.className||''}`} />;
}
function Card({ title, subtitle, children }: { title:string; subtitle:string; children:React.ReactNode }) {
  return (
    <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
      <div className="mb-4">
        <div className="text-lg font-semibold">{title}</div>
        <div className="text-sm text-gray-600">{subtitle}</div>
      </div>
      <div className="space-y-4">{children}</div>
    </div>
  );
}
function SubmitButton({ sending, label, sendingLabel }: { sending:boolean; label:string; sendingLabel:string }) {
  return (
    <button disabled={sending} className={`px-5 py-2 rounded-xl text-white ${sending?'bg-gray-400':'bg-blue-600'} `}>
      {sending ? sendingLabel : label}
    </button>
  );
}

// ---------- Forms ----------
function FreeForm({ L }: { L: Lang }) {
  const t = UI[L];
  const [sending, setSending] = useState(false);
  const [ok, setOk] = useState<string|undefined>(undefined);
  const [err, setErr] = useState<string|undefined>(undefined);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSending(true); setOk(undefined); setErr(undefined);
    const form = e.target as HTMLFormElement;
    const data = Object.fromEntries(new FormData(form) as any);
    try {
      const r = await fetch('/api/public/forms/free', { method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify(data) });
      if (!r.ok) throw new Error('fail');
      setOk(t.actions.success);
      form.reset();
    } catch {
      setErr(t.actions.error);
    } finally {
      setSending(false);
    }
  }

  return (
    <Card title={t.freeTitle} subtitle={t.freeIntro}>
      <form onSubmit={onSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Field label={t.fields.businessName}><Input name="businessName" required /></Field>
          <Field label={t.fields.category}><Input name="category" required /></Field>
          <Field label={t.fields.country}><Input name="country" required /></Field>
          <Field label={t.fields.city}><Input name="city" required /></Field>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Field label={t.fields.address}><Input name="address" /></Field>
          <Field label={t.fields.website}><Input name="website" placeholder="https://"/></Field>
          <Field label={t.fields.email}><Input type="email" name="email" required /></Field>
          <Field label={t.fields.phone}><Input name="phone" /></Field>
        </div>
        <Field label={t.fields.description}><Textarea name="description" /></Field>

        <div className="flex items-center gap-3">
          <SubmitButton sending={sending} label={t.actions.submit} sendingLabel={t.actions.submitting} />
          {ok && <span className="text-green-600 text-sm">{ok}</span>}
          {err && <span className="text-red-600 text-sm">{err}</span>}
        </div>
      </form>
    </Card>
  );
}

function ClaimForm({ L }: { L: Lang }) {
  const t = UI[L];
  const [sending, setSending] = useState(false);
  const [ok, setOk] = useState<string|undefined>(undefined);
  const [err, setErr] = useState<string|undefined>(undefined);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSending(true); setOk(undefined); setErr(undefined);
    const form = e.target as HTMLFormElement;
    const data = Object.fromEntries(new FormData(form) as any);
    try {
      const r = await fetch('/api/public/forms/claim', { method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify(data) });
      if (!r.ok) throw new Error('fail');
      setOk(t.actions.success);
      form.reset();
    } catch {
      setErr(t.actions.error);
    } finally {
      setSending(false);
    }
  }

  return (
    <Card title={t.claimTitle} subtitle={t.claimIntro}>
      <form onSubmit={onSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Field label={t.fields.listingId}><Input name="listingId" required /></Field>
          <Field label={t.fields.claimantEmail}><Input type="email" name="claimantEmail" required /></Field>
        </div>
        <Field label={t.fields.message}><Textarea name="message" /></Field>

        <div className="flex items-center gap-3">
          <SubmitButton sending={sending} label={t.actions.submit} sendingLabel={t.actions.submitting} />
          {ok && <span className="text-green-600 text-sm">{ok}</span>}
          {err && <span className="text-red-600 text-sm">{err}</span>}
        </div>
      </form>
    </Card>
  );
}

function UpgradeForm({ L }: { L: Lang }) {
  const t = UI[L];
  const [sending, setSending] = useState(false);
  const [ok, setOk] = useState<string|undefined>(undefined);
  const [err, setErr] = useState<string|undefined>(undefined);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSending(true); setOk(undefined); setErr(undefined);
    const form = e.target as HTMLFormElement;
    const data = Object.fromEntries(new FormData(form) as any);
    try {
      const r = await fetch('/api/public/forms/upgrade', { method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify(data) });
      if (!r.ok) throw new Error('fail');
      setOk(t.actions.success);
      form.reset();
    } catch {
      setErr(t.actions.error);
    } finally {
      setSending(false);
    }
  }

  return (
    <Card title={t.upgradeTitle} subtitle={t.upgradeIntro}>
      <form onSubmit={onSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Field label={t.fields.listingId}><Input name="listingId" required /></Field>
          <Field label={t.fields.targetPlan}>
            <select name="targetPlan" className="w-full rounded-xl border border-gray-300 px-3 py-2">
              <option value="growth">{t.plans.growth}</option>
              <option value="premium">{t.plans.premium}</option>
            </select>
          </Field>
          <Field label={t.fields.contactEmail}><Input type="email" name="contactEmail" required /></Field>
        </div>
        <Field label={t.fields.notes}><Textarea name="notes" /></Field>

        <div className="flex items-center gap-3">
          <SubmitButton sending={sending} label={t.actions.submit} sendingLabel={t.actions.submitting} />
          {ok && <span className="text-green-600 text-sm">{ok}</span>}
          {err && <span className="text-red-600 text-sm">{err}</span>}
        </div>
      </form>
    </Card>
  );
}