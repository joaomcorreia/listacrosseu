"use client";
import { useEffect, useRef, useState } from "react";
import { sendAssistantMessage, createChatMessage, sanitizeMessageContent, type ChatMessage } from "../src/lib/assistant-api";

interface AssistantChatProps {
  className?: string;
  placeholder?: string;
  initialMessage?: string;
  compact?: boolean;
}

export default function AssistantChat({ 
  className = "", 
  placeholder = "Type your message...",
  initialMessage = "Hello! How can I help you today?",
  compact = false
}: AssistantChatProps) {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([
    createChatMessage("assistant", initialMessage)
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  async function handleSendMessage() {
    const userMessage = message.trim();
    if (!userMessage || isLoading) return;

    // Add user message immediately (optimistic UI)
    const userMsg = createChatMessage("user", userMessage);
    setMessages(prev => [...prev, userMsg]);
    setMessage("");
    setIsLoading(true);
    setIsTyping(true);

    try {
      const response = await sendAssistantMessage(userMessage);
      
      if (response.status === "ok") {
        const assistantMsg = createChatMessage("assistant", response.reply);
        setMessages(prev => [...prev, assistantMsg]);
      } else {
        const errorMsg = createChatMessage("error", "Sorry, I'm having trouble answering right now.");
        setMessages(prev => [...prev, errorMsg]);
      }
    } catch (error: any) {
      const errorMsg = createChatMessage("error", "Sorry, I'm having trouble answering right now.");
      setMessages(prev => [...prev, errorMsg]);
      
      // Log error in development
      if (process.env.NODE_ENV === 'development') {
        console.error('[AssistantChat] Send failed:', error);
      }
    } finally {
      setIsLoading(false);
      setIsTyping(false);
    }
  }

  function handleRetry() {
    // Find the last user message and resend it
    const lastUserMessage = [...messages].reverse().find(msg => msg.role === "user");
    if (lastUserMessage && !isLoading) {
      setMessage(lastUserMessage.content);
      inputRef.current?.focus();
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter") {
      if (e.shiftKey) {
        // Shift+Enter: allow newline (default behavior)
        return;
      } else {
        // Enter: submit
        e.preventDefault();
        handleSendMessage();
      }
    }
  }

  function renderMessage(msg: ChatMessage) {
    const isUser = msg.role === "user";
    const isError = msg.role === "error";
    
    return (
      <div key={msg.id} className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}>
        <div className={`max-w-[85%] ${isUser ? "order-2" : "order-1"}`}>
          <div className={`px-4 py-2 rounded-lg text-sm ${
            isUser 
              ? "bg-blue-600 text-white" 
              : isError 
              ? "bg-red-50 text-red-800 border border-red-200"
              : "bg-gray-100 text-gray-800"
          }`}>
            <div 
              dangerouslySetInnerHTML={{ 
                __html: sanitizeMessageContent(msg.content) 
              }} 
            />
          </div>
          {isError && (
            <div className="mt-2">
              <button 
                className="px-3 py-1 text-xs border rounded bg-white hover:bg-gray-50 text-gray-700 transition-colors"
                onClick={handleRetry}
                disabled={isLoading}
              >
                Retry
              </button>
            </div>
          )}
          <div className="text-xs text-gray-500 mt-1">
            {new Date(msg.ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </div>
        </div>
      </div>
    );
  }

  function renderTypingIndicator() {
    if (!isTyping) return null;
    
    return (
      <div className="flex justify-start mb-4">
        <div className="max-w-[85%]">
          <div className="px-4 py-2 rounded-lg text-sm bg-gray-100">
            <div className="flex items-center space-x-2">
              <span className="text-gray-600">Assistant is typing</span>
              <div className="flex space-x-1">
                <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const chatHeight = compact ? "h-64" : "h-96";
  
  return (
    <div className={`flex flex-col bg-white border rounded-lg shadow-sm ${className}`}>
      {/* Header */}
      <div className="px-4 py-3 border-b bg-gray-50 rounded-t-lg">
        <h3 className="font-semibold text-gray-800">Assistant Chat</h3>
      </div>

      {/* Messages */}
      <div className={`${chatHeight} overflow-y-auto p-4 space-y-2`} role="log" aria-live="polite" aria-label="Chat messages">
        {messages.map(renderMessage)}
        {renderTypingIndicator()}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t bg-gray-50 rounded-b-lg">
        <div className="flex space-x-3">
          <textarea
            ref={inputRef}
            className="flex-1 resize-none border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder={`${placeholder} (Enter to send, Shift+Enter for new line)`}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isLoading}
            rows={compact ? 1 : 2}
            aria-label="Type your message to the assistant"
          />
          <button
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors text-sm font-medium"
            onClick={handleSendMessage}
            disabled={isLoading || !message.trim()}
            aria-label="Send message to assistant"
          >
            {isLoading ? (
              <div className="flex items-center space-x-2">
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Sending</span>
              </div>
            ) : (
              "Send"
            )}
          </button>
        </div>
      </div>
    </div>
  );
}