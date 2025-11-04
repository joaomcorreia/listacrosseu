"use client";
import { useEffect, useState } from "react";
import { listAssistantVersions, publishAssistant, rollbackAssistant } from "@/lib/assistant";

export default function AssistantPublishPanel() {
    const [versions, setVersions] = useState<Array<{ version: number, label: string, created_at: string }>>([]);
    const [label, setLabel] = useState("");
    const [loading, setLoading] = useState(false);
    const [msg, setMsg] = useState<string | null>(null);
    const [err, setErr] = useState<string | null>(null);

    async function refresh() {
        setErr(null);
        try {
            const data = await listAssistantVersions();
            setVersions(data.versions.map(v => ({ version: v.version, label: v.label, created_at: v.created_at })));
        } catch (e: any) {
            setErr(e.message || String(e));
        }
    }

    useEffect(() => { refresh(); }, []);

    async function onPublish(makeLive: boolean) {
        setLoading(true); setMsg(null); setErr(null);
        try {
            await publishAssistant(label, makeLive);
            setLabel("");
            await refresh();
            setMsg(makeLive ? "Published and set Live." : "Published (not live).");
        } catch (e: any) {
            setErr(e.message || String(e));
        } finally {
            setLoading(false);
            setTimeout(() => setMsg(null), 2000);
        }
    }

    async function onRestore(v: number, makeLive: boolean) {
        setLoading(true); setMsg(null); setErr(null);
        try {
            await rollbackAssistant(v, makeLive);
            await refresh();
            setMsg(makeLive ? `Restored v${v} and set Live.` : `Restored v${v} (draft).`);
        } catch (e: any) {
            setErr(e.message || String(e));
        } finally {
            setLoading(false);
            setTimeout(() => setMsg(null), 2000);
        }
    }

    return (
        <div className="max-w-4xl border rounded-xl p-4 space-y-4">
            <h2 className="text-lg font-semibold">Publish & Versions</h2>

            <div className="grid gap-2 md:grid-cols-3 items-end">
                <div className="md:col-span-2">
                    <label className="block text-sm font-medium mb-1">Version label (optional)</label>
                    <input className="w-full border rounded p-2 text-sm" value={label} onChange={(e) => setLabel(e.target.value)} placeholder="Post-launch tweaks" />
                </div>
                <div className="flex gap-2">
                    <button onClick={() => onPublish(true)} disabled={loading} className="px-3 py-2 border rounded bg-black text-white text-sm disabled:opacity-50">
                        Publish as Live
                    </button>
                    <button onClick={() => onPublish(false)} disabled={loading} className="px-3 py-2 border rounded text-sm disabled:opacity-50">
                        Publish (keep Draft)
                    </button>
                </div>
            </div>

            <div>
                <h3 className="font-medium mb-2">Versions</h3>
                <div className="border rounded">
                    <table className="w-full text-sm">
                        <thead>
                            <tr className="bg-gray-50 text-left">
                                <th className="p-2">Version</th>
                                <th className="p-2">Label</th>
                                <th className="p-2">Created</th>
                                <th className="p-2">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {versions.map(v => (
                                <tr key={v.version} className="border-t">
                                    <td className="p-2">v{v.version}</td>
                                    <td className="p-2">{v.label || "-"}</td>
                                    <td className="p-2">{new Date(v.created_at).toLocaleString()}</td>
                                    <td className="p-2 flex gap-2">
                                        <button onClick={() => onRestore(v.version, true)} disabled={loading} className="px-2 py-1 border rounded text-xs disabled:opacity-50">
                                            Restore as Live
                                        </button>
                                        <button onClick={() => onRestore(v.version, false)} disabled={loading} className="px-2 py-1 border rounded text-xs disabled:opacity-50">
                                            Restore as Draft
                                        </button>
                                    </td>
                                </tr>
                            ))}
                            {versions.length === 0 && (
                                <tr><td className="p-2 text-gray-500" colSpan={4}>No versions yet.</td></tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>

            {msg && <div className="text-green-700 text-sm">{msg}</div>}
            {err && <div className="text-red-700 text-sm">{err}</div>}
        </div>
    );
}