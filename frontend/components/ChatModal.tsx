"use client";

import React, { useState, useRef, useEffect } from "react";
import { X, Send, Bot, User, Sparkles, Terminal } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { ReasoningTrace } from "./ReasoningTrace";
import { VoiceRecorder } from "./VoiceRecorder";

interface ChatModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialQuery?: string;
}

export const ChatModal: React.FC<ChatModalProps> = ({ isOpen, onClose, initialQuery = "" }) => {
  const [messages, setMessages] = useState<any[]>([
    {
      role: "assistant",
      content:
        "🌕 **Lunaris AI Sovereign Intelligence**\n\nI am ready. Ask me anything, request deep research across local documents, query live web metasearch, or run code in the sandbox.",
    },
  ]);
  const [input, setInput] = useState(initialQuery);
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);

  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (initialQuery && isOpen) {
      setInput(initialQuery);
    }
  }, [initialQuery, isOpen]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  if (!isOpen) return null;

  const handleSend = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!input.trim() || loading) return;

    const userText = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userText }]);
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/api/v1/agent/react", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          prompt: userText,
          session_id: sessionId,
          max_iterations: 5,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        setSessionId(data.session_id);
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: data.response,
            reasoning_steps: data.reasoning_steps,
          },
        ]);
      } else {
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: "⚠️ Error contacting Lunaris AI Gateway." },
        ]);
      }
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: `⚠️ Network error: ${err.message}` },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleVoiceTranscription = (text: string, response: string, audioUrl?: string) => {
    setMessages((prev) => [
      ...prev,
      { role: "user", content: text },
      { role: "assistant", content: response, audioUrl },
    ]);
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
      <div className="bg-[#0b080e] border border-red-500/30 rounded-2xl w-full max-w-3xl h-[85vh] flex flex-col overflow-hidden shadow-[0_25px_90px_rgba(0,0,0,0.9),0_0_40px_rgba(255,20,50,0.15)]">
        {/* Header */}
        <div className="h-14 px-5 border-b border-red-500/10 flex items-center justify-between bg-[#120d18]">
          <div className="flex items-center space-x-2.5">
            <div className="w-7 h-7 rounded-full bg-gradient-to-br from-red-600 to-amber-600 flex items-center justify-center shadow-[0_0_10px_rgba(255,30,50,0.6)]">
              <Bot className="w-4 h-4 text-white" />
            </div>
            <div>
              <h3 className="text-xs font-bold text-white tracking-wide">
                LUNARIS <span className="text-red-500">AI AGENT</span>
              </h3>
              <span className="text-[10px] text-slate-400 font-mono">Autonomous ReAct Loop</span>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-white/[0.05]"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Message Stream */}
        <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-4">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex space-x-3 ${
                msg.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              {msg.role === "assistant" && (
                <div className="w-7 h-7 rounded-lg bg-red-600/20 border border-red-500/30 flex items-center justify-center shrink-0 mt-0.5">
                  <Bot className="w-3.5 h-3.5 text-red-400" />
                </div>
              )}

              <div
                className={`max-w-[85%] rounded-xl px-4 py-3 text-xs shadow-sm ${
                  msg.role === "user"
                    ? "bg-gradient-to-r from-red-700 to-red-600 text-white rounded-tr-none"
                    : "bg-[#141019] border border-red-500/20 rounded-tl-none text-slate-200"
                }`}
              >
                {msg.reasoning_steps && msg.reasoning_steps.length > 0 && (
                  <ReasoningTrace steps={msg.reasoning_steps} />
                )}

                <div className="prose prose-invert prose-xs max-w-none break-words leading-relaxed">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {msg.content}
                  </ReactMarkdown>
                </div>
              </div>

              {msg.role === "user" && (
                <div className="w-7 h-7 rounded-lg bg-slate-800 flex items-center justify-center shrink-0 mt-0.5 font-bold text-xs text-white">
                  SB
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="flex items-center space-x-2 text-xs text-slate-400">
              <Sparkles className="w-4 h-4 text-red-500 animate-spin" />
              <span className="font-mono text-[11px]">ReAct reasoning across tools...</span>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Input Bar */}
        <div className="p-3.5 bg-[#0e0a12] border-t border-red-500/10">
          <form
            onSubmit={handleSend}
            className="flex items-center space-x-2 bg-[#17121d] border border-red-500/20 rounded-xl px-3 py-1.5 focus-within:border-red-500 transition-colors"
          >
            <VoiceRecorder onTranscription={handleVoiceTranscription} />
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask Lunaris AI anything (pgvector RAG, web search, code sandbox)..."
              disabled={loading}
              className="flex-1 bg-transparent text-xs text-white placeholder:text-slate-500 focus:outline-none"
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="p-2 rounded-lg bg-gradient-to-r from-red-600 to-orange-500 hover:from-red-500 hover:to-orange-400 text-white disabled:opacity-40 transition-all"
            >
              <Send className="w-3.5 h-3.5" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
