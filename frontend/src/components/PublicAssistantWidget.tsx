"use client";
import { useEffect, useRef, useState } from "react";
import { publicAsk } from "@/lib/assistant";

type Msg = { role: "user" | "assistant"; text: string; cta?: { code: string; label: string }; payload?: any };

export default function PublicAssistantWidget({ initialLang = "en", isLoggedIn = false }: { initialLang?: string; isLoggedIn?: boolean }) {
  const [lang, setLang] = useState(initialLang);
  const [q, setQ] = useState("");
  const [busy, setBusy] = useState(false);
  const [chat, setChat] = useState<Msg[]>([
    {
      role: "assistant",
      text:
        isLoggedIn
          ? "Hi! Ask me anything about ListAcross EU, plans, or building your website. I'll show one next step when you're ready."
          : "Welcome! You can explore freely. To publish or save progress, you'll need a free ListAcross EU account."
    }
  ]);

  const boxRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    boxRef.current?.scrollTo({ top: boxRef.current.scrollHeight, behavior: "smooth" });
  }, [chat]);

  async function send() {
    if (!q.trim() || busy) return;
    const userMsg: Msg = { role: "user", text: q.trim() };
    setChat((c) => [...c, userMsg]);
    setQ("");
    setBusy(true);
    try {
      const resp = await publicAsk(userMsg.text, lang);
      const next: Msg = {
        role: "assistant",
        text: resp.answer || "…",
        cta: resp.cta?.code && resp.cta.code !== "none" ? resp.cta : undefined,
        payload: resp.tool_payload_template || {}
      };
      setChat((c) => [...c, next]);
    } catch (e: any) {
      setChat((c) => [...c, { role: "assistant", text: "I couldn't reach the assistant right now. Please try again." }]);
    } finally {
      setBusy(false);
    }
  }

  function renderCTA(m: Msg) {
    if (!m.cta) return null;
    const needsAccount = !isLoggedIn && ["create_listing", "start_jcw_build", "start_print_order", "upgrade_plan"].includes(m.cta.code);
    const label = needsAccount ? `${m.cta.label} (sign in required)` : m.cta.label;
    return (
      <button
        className="px-3 py-2 border rounded text-sm"
        onClick={() => {
          if (needsAccount) {
            window.location.href = "/account/register?next=/dashboard";
          } else if (m.cta) {
            // Public pages: just navigate to the dashboard or action URL
            if (m.cta.code === "upgrade_plan") {
              window.location.href = m.payload?.upgrade_url || "/dashboard/billing/upgrade";
            } else if (m.cta.code === "start_print_order") {
              window.location.href = "/dashboard/print";
            } else if (m.cta.code === "start_jcw_build") {
              window.location.href = "/dashboard/build-website";
            } else if (m.cta.code === "create_listing") {
              window.location.href = "/dashboard/advertise";
            }
          }
        }}
      >
        {label}
      </button>
    );
  }

  return (
    <div className="fixed bottom-6 right-6 w-[320px] rounded-2xl shadow-lg border bg-white flex flex-col">
      <div className="px-3 py-2 border-b flex items-center justify-between">
        <div className="font-medium text-sm">Ask ListAcross</div>
        <select className="text-xs border rounded px-1 py-0.5" value={lang} onChange={(e)=>setLang(e.target.value)}>
          <option value="en">EN</option><option value="nl">NL</option>
          <option value="fr">FR</option><option value="es">ES</option><option value="pt">PT</option>
        </select>
      </div>

      <div ref={boxRef} className="h-72 overflow-y-auto p-3 space-y-2">
        {chat.map((m, i) => (
          <div key={i} className={m.role === "user" ? "text-right" : "text-left"}>
            <div className={`inline-block px-3 py-2 rounded-xl text-sm ${m.role==="user" ? "bg-black text-white" : "bg-gray-100"}`}>
              {m.text}
            </div>
            {m.role === "assistant" && m.cta && <div className="mt-2">{renderCTA(m)}</div>}
          </div>
        ))}
      </div>

      {!isLoggedIn && (
        <div className="px-3 pb-1 text-[11px] text-gray-500">
          To publish websites or listings, please register (free) and you'll continue where you left off.
        </div>
      )}

      <div className="p-3 border-t flex gap-2">
        <input
          className="flex-1 border rounded px-2 py-2 text-sm"
          placeholder="Ask about plans, websites, printing…"
          value={q}
          onChange={(e)=>setQ(e.target.value)}
          onKeyDown={(e)=>{ if (e.key === "Enter") send(); }}
        />
        <button className="px-3 py-2 border rounded text-sm" disabled={busy} onClick={send}>
          {busy ? "…" : "Send"}
        </button>
      </div>
    </div>
  );
}