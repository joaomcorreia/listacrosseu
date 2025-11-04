"use client";
import { useEffect, useState } from "react";
import { fetchAssistantLive, AssistantLive } from "@/lib/assistant";

export default function AssistantPanel() {
    const [data, setData] = useState<AssistantLive | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchAssistantLive()
            .then(setData)
            .catch((e) => setError(String(e)))
            .finally(() => setLoading(false));
    }, []);

    if (loading) return (
        <div className="flex items-center justify-center p-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <span className="ml-2 text-gray-600">Loading assistant configuration...</span>
        </div>
    );

    if (error) return (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="text-red-800 font-medium">Error loading assistant configuration</div>
            <div className="text-red-600 text-sm mt-1">{error}</div>
        </div>
    );

    if (!data) return (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <div className="text-yellow-800">No assistant configuration found.</div>
        </div>
    );

    return (
        <div className="max-w-3xl border rounded-xl p-4 space-y-4">
            <div className="text-sm text-gray-500">Version: {data.version} • Status: {data.status}</div>
            <div>
                <h2 className="text-lg font-semibold mb-2">System Prompt</h2>
                <pre className="whitespace-pre-wrap text-sm bg-gray-50 p-3 rounded">{data.system_prompt || "(empty)"}</pre>
            </div>
            <div>
                <h2 className="text-lg font-semibold mb-2">Languages</h2>
                <div className="text-sm">Default: {data.default_lang}</div>
                <div className="text-sm">Supported: {data.supported_langs.join(", ")}</div>
            </div>
            <div>
                <h2 className="text-lg font-semibold mb-2">CTA Text</h2>
                <div className="grid gap-2">
                    {Object.entries(data.cta_text).map(([lang, entries]) => (
                        <div key={lang} className="border rounded p-2">
                            <div className="font-medium mb-1">{lang}</div>
                            <ul className="list-disc pl-5 text-sm">
                                {Object.entries(entries).map(([k, v]) => (
                                    <li key={k}><span className="font-mono">{k}</span>: {v}</li>
                                ))}
                            </ul>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}