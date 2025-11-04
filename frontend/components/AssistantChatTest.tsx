"use client";
import { useState } from "react";
import { askAssistant, actionCreateListing, actionStartJCWBuild, actionStartPrintOrder } from "@/lib/assistant";

export default function AssistantChatTest() {
    const [q, setQ] = useState("");
    const [lang, setLang] = useState("en");
    const [resp, setResp] = useState<any>(null);
    const [err, setErr] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [payload, setPayload] = useState<any>({});

    async function onAsk() {
        setLoading(true); setErr(null);
        try {
            const r = await askAssistant(q, lang);
            setResp(r);
            setPayload(r.tool_payload_template || {});
        } catch (e: any) { setErr(e.message || String(e)); }
        finally { setLoading(false); }
    }

    async function runCTA() {
        if (!resp) return;
        const code = resp.cta?.code;
        if (code === "create_listing") {
            await actionCreateListing(payload);
        } else if (code === "start_jcw_build") {
            const pl = { ...payload };
            if (typeof pl.preferred_locales === "string") {
                pl.preferred_locales = pl.preferred_locales.split(",").map((s: string) => s.trim()).filter(Boolean);
            }
            await actionStartJCWBuild(pl);
        } else if (code === "start_print_order") {
            await actionStartPrintOrder(payload);
        } else if (code === "upgrade_plan") {
            window.location.href = payload.upgrade_url || "/dashboard/billing/upgrade";
        }
    }

    return (
        <div className="max-w-3xl border rounded-xl p-4 space-y-4">
            <div className="flex gap-2">
                <input className="border rounded p-2 flex-1 text-sm" value={q} onChange={e => setQ(e.target.value)} placeholder="Ask something…" />
                <input className="border rounded p-2 w-24 text-sm" value={lang} onChange={e => setLang(e.target.value)} placeholder="en" />
                <button className="px-3 py-2 border rounded text-sm" onClick={onAsk} disabled={loading}>{loading ? "Thinking…" : "Ask"}</button>
            </div>

            {resp && (
                <div className="space-y-3">
                    <div className="whitespace-pre-wrap text-sm">{resp.answer}</div>
                    <div className="text-xs text-gray-500">Intent: {resp.intent || "-"}</div>

                    {resp.cta?.code && resp.cta.code !== "none" && (
                        <div className="space-y-2">
                            <div className="font-medium text-sm">Action</div>
                            <div className="grid gap-2">
                                <textarea className="border rounded p-2 text-sm font-mono h-28"
                                    value={JSON.stringify(payload, null, 2)}
                                    onChange={e => { try { setPayload(JSON.parse(e.target.value)); } catch { /* ignore */ } }} />
                                <button className="px-3 py-2 border rounded bg-black text-white text-sm" onClick={runCTA}>
                                    {resp.cta.label || "Proceed"}
                                </button>
                            </div>
                        </div>
                    )}

                    {resp.used_kb?.length > 0 && (
                        <div className="text-xs text-gray-500">
                            Context: {resp.used_kb.map((d: any) => d.slug).join(", ")}
                        </div>
                    )}
                </div>
            )}

            {err && <div className="text-red-700 text-sm">{err}</div>}
        </div>
    );
}