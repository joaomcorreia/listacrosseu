"use client";
import { useEffect, useRef, useState } from "react";
import { sendAssistantMessage, createChatMessage, sanitizeMessageContent, type ChatMessage } from "../src/lib/assistant-api";

export default function PublicAssistantWidget({ initialLang = "en", isLoggedIn = false }: { initialLang?: string; isLoggedIn?: boolean }) {
    const [lang, setLang] = useState(initialLang);
    const [q, setQ] = useState("");
    const [busy, setBusy] = useState(false);
    const [isTyping, setIsTyping] = useState(false);
    const [isOpen, setIsOpen] = useState(true);
    const [chat, setChat] = useState<ChatMessage[]>([
        createChatMessage("assistant", 
            isLoggedIn
                ? "Hi! Ask me anything about ListAcross EU, plans, or building your website. I'll show one next step when you're ready."
                : "Welcome! You can explore freely. To publish or save progress, you'll need a free ListAcross EU account."
        )
    ]);

    const boxRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLInputElement>(null);

    // Auto-scroll to newest message
    useEffect(() => {
        boxRef.current?.scrollTo({ top: boxRef.current.scrollHeight, behavior: "smooth" });
    }, [chat, isTyping]);

    async function send() {
        const message = q.trim();
        if (!message || busy) return;
        
        // Add user message immediately (optimistic UI)
        const userMsg = createChatMessage("user", message);
        setChat(prev => [...prev, userMsg]);
        setQ("");
        setBusy(true);
        setIsTyping(true);

        try {
            const response = await sendAssistantMessage(message);
            
            if (response.status === "ok") {
                const assistantMsg = createChatMessage("assistant", response.reply);
                setChat(prev => [...prev, assistantMsg]);
            } else {
                const errorMsg = createChatMessage("error", "Sorry, I'm having trouble answering right now.");
                setChat(prev => [...prev, errorMsg]);
            }
        } catch (error: any) {
            const errorMsg = createChatMessage("error", "Sorry, I'm having trouble answering right now.");
            setChat(prev => [...prev, errorMsg]);
            
            // Log error in development
            if (process.env.NODE_ENV === 'development') {
                console.error('[PublicAssistantWidget] Send failed:', error);
            }
        } finally {
            setBusy(false);
            setIsTyping(false);
        }
    }

    function retryLastMessage() {
        // Find the last user message and resend it
        const lastUserMessage = [...chat].reverse().find(msg => msg.role === "user");
        if (lastUserMessage && !busy) {
            setQ(lastUserMessage.content);
            inputRef.current?.focus();
        }
    }

    function handleKeyDown(e: React.KeyboardEvent) {
        if (e.key === "Enter") {
            if (e.shiftKey) {
                // Shift+Enter: allow newline (default behavior)
                return;
            } else {
                // Enter: submit
                e.preventDefault();
                send();
            }
        }
    }

    function renderMessage(message: ChatMessage) {
        const isUser = message.role === "user";
        const isError = message.role === "error";
        
        return (
            <div key={message.id} className={isUser ? "text-right" : "text-left"}>
                <div className={`inline-block px-3 py-2 rounded-xl text-sm max-w-[85%] ${
                    isUser 
                        ? "bg-black text-white" 
                        : isError 
                        ? "bg-red-100 text-red-800 border border-red-200"
                        : "bg-gray-100"
                }`}>
                    <div 
                        dangerouslySetInnerHTML={{ 
                            __html: sanitizeMessageContent(message.content) 
                        }} 
                    />
                </div>
                {isError && (
                    <div className="mt-2">
                        <button 
                            className="px-2 py-1 text-xs border rounded bg-white hover:bg-gray-50 text-gray-700"
                            onClick={retryLastMessage}
                            disabled={busy}
                        >
                            Retry
                        </button>
                    </div>
                )}
            </div>
        );
    }

    return (
        <div className="fixed bottom-6 right-6 z-50">
            {/* Minimized state - show small chat bubble */}
            {!isOpen && (
                <button
                    onClick={() => setIsOpen(true)}
                    className="w-14 h-14 bg-blue-500 hover:bg-blue-600 text-white rounded-full shadow-2xl border-2 border-blue-500 flex items-center justify-center transition-all duration-200 hover:scale-105"
                    aria-label="Open assistant chat"
                >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                    </svg>
                </button>
            )}
            
            {/* Expanded state - show full chat widget */}
            {isOpen && (
                <div className="w-[320px] rounded-2xl shadow-2xl border-2 border-blue-500 bg-white flex flex-col">
                    <div className="px-3 py-2 border-b flex items-center justify-between bg-blue-50">
                        <div className="font-medium text-sm text-blue-800">Ask ListAcross</div>
                        <div className="flex items-center space-x-2">
                            <select className="text-xs border rounded px-1 py-0.5" value={lang} onChange={(e) => setLang(e.target.value)}>
                                <option value="en">EN</option><option value="nl">NL</option>
                                <option value="fr">FR</option><option value="es">ES</option><option value="pt">PT</option>
                            </select>
                            <button
                                onClick={() => setIsOpen(false)}
                                className="p-1 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded transition-colors"
                                aria-label="Close assistant chat"
                            >
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                                </svg>
                            </button>
                        </div>
                    </div>

            <div ref={boxRef} className="h-72 overflow-y-auto p-3 space-y-2" role="log" aria-live="polite" aria-label="Chat messages">
                {chat.map(message => renderMessage(message))}
                {isTyping && (
                    <div className="text-left">
                        <div className="inline-block px-3 py-2 rounded-xl text-sm bg-gray-100">
                            <div className="flex items-center space-x-1">
                                <span>Assistant is typing</span>
                                <div className="flex space-x-1">
                                    <div className="w-1 h-1 bg-gray-500 rounded-full animate-bounce"></div>
                                    <div className="w-1 h-1 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                                    <div className="w-1 h-1 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {!isLoggedIn && (
                <div className="px-3 pb-1 text-[11px] text-gray-500">
                    To publish websites or listings, please register (free) and you'll continue where you left off.
                </div>
            )}

            <div className="p-3 border-t flex gap-2">
                <input
                    ref={inputRef}
                    className="flex-1 border rounded px-2 py-2 text-sm"
                    placeholder="Ask about plans, websites, printing… (Enter to send, Shift+Enter for new line)"
                    value={q}
                    onChange={(e) => setQ(e.target.value)}
                    onKeyDown={handleKeyDown}
                    disabled={busy}
                    aria-label="Type your message to the assistant"
                />
                <button 
                    className="px-3 py-2 border rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed" 
                    disabled={busy || !q.trim()} 
                    onClick={send}
                    aria-label="Send message to assistant"
                >
                    {busy ? "…" : "Send"}
                </button>
            </div>
                </div>
            )}
        </div>
    );
}