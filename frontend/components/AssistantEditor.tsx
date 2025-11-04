"use client";
import { useEffect, useState } from "react";
import { AssistantLive, fetchAssistantConfig, updateAssistantConfig } from "@/lib/assistant";

export default function AssistantEditor() {
    const [data, setData] = useState<AssistantLive | null>(null);
    const [saving, setSaving] = useState(false);
    const [msg, setMsg] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);

    // Form fields
    const [systemPrompt, setSystemPrompt] = useState("");
    const [defaultLang, setDefaultLang] = useState("en");
    const [supportedLangs, setSupportedLangs] = useState("en,nl,fr,es,pt");
    const [ctaText, setCtaText] = useState("{}");

    useEffect(() => {
        fetchAssistantConfig()
            .then((json) => {
                setData(json);
                setSystemPrompt(json.system_prompt || "");
                setDefaultLang(json.default_lang || "en");
                setSupportedLangs((json.supported_langs || []).join(","));
                setCtaText(JSON.stringify(json.cta_text || {}, null, 2));
            })
            .catch((e) => setError(String(e)));
    }, []);

    async function onSave() {
        setSaving(true);
        setMsg(null);
        setError(null);
        try {
            const langs = supportedLangs.split(",").map((s) => s.trim()).filter(Boolean);
            let cta: Record<string, Record<string, string>> = {};
            try {
                cta = JSON.parse(ctaText);
            } catch (e) {
                throw new Error("CTA Text must be valid JSON.");
            }
            const updated = await updateAssistantConfig({
                system_prompt: systemPrompt,
                default_lang: defaultLang,
                supported_langs: langs,
                cta_text: cta,
                // keep status as-is; or send {status:"draft"} explicitly
            } as any);
            setData(updated);
            setMsg("Saved.");
        } catch (e: any) {
            setError(e.message || String(e));
        } finally {
            setSaving(false);
            setTimeout(() => setMsg(null), 2000);
        }
    }

    if (error) return <div className="text-red-600">Error: {error}</div>;
    if (!data) return <div>Loading…</div>;

    return (
        <div className="max-w-4xl space-y-6">
            <div className="text-sm text-gray-500">Version: {data.version} • Status: {data.status}</div>

            <div>
                <label className="block text-sm font-medium mb-1">System Prompt</label>
                <textarea
                    className="w-full border rounded p-2 text-sm h-40"
                    value={systemPrompt}
                    onChange={(e) => setSystemPrompt(e.target.value)}
                />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                    <label className="block text-sm font-medium mb-1">Default Language</label>
                    <input
                        className="w-full border rounded p-2 text-sm"
                        value={defaultLang}
                        onChange={(e) => setDefaultLang(e.target.value)}
                        placeholder="en"
                    />
                </div>
                <div className="md:col-span-2">
                    <label className="block text-sm font-medium mb-1">Supported Languages (comma-separated)</label>
                    <input
                        className="w-full border rounded p-2 text-sm"
                        value={supportedLangs}
                        onChange={(e) => setSupportedLangs(e.target.value)}
                        placeholder="en,nl,fr,es,pt"
                    />
                </div>
            </div>

            <div>
                <label className="block text-sm font-medium mb-1">CTA Text (JSON)</label>
                <textarea
                    className="w-full border rounded p-2 text-sm font-mono h-48"
                    value={ctaText}
                    onChange={(e) => setCtaText(e.target.value)}
                />
                <p className="text-xs text-gray-500 mt-1">Example: {`{ "en": { "create_listing": "Advertise free" } }`}</p>
            </div>

            <div className="flex items-center gap-3">
                <button
                    onClick={onSave}
                    disabled={saving}
                    className="px-4 py-2 border rounded bg-black text-white text-sm disabled:opacity-50"
                >
                    {saving ? "Saving…" : "Save"}
                </button>
                {msg && <span className="text-green-700 text-sm">{msg}</span>}
                {error && <span className="text-red-700 text-sm">{error}</span>}
            </div>
        </div>
    );
}