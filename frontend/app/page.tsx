"use client";

import React, { useState, useEffect, useRef } from "react";
import { Send, Bot, User, Sparkles, Terminal, Database, Shield, Radio } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { DocumentManager } from "@/components/DocumentManager";
import { ReasoningTrace } from "@/components/ReasoningTrace";
import { SandboxRunner } from "@/components/SandboxRunner";
import { VoiceRecorder } from "@/components/VoiceRecorder";

interface Message {
  role: "user" | "assistant";
  content: string;
  reasoning_steps?: any[];
  audioUrl?: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "🌕 **Lunaris AI Initialized**\n\nI am your private sovereign intelligence engine. I can perform autonomous **ReAct multi-step reasoning**, query your local documents via **pgvector**, search the live web via **SearXNG**, run untrusted scripts in the **Docker Sandbox**, or interact via voice.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [showSandbox, setShowSandbox] = useState(false);
  const [showSidebar, setShowSidebar] = useState(true);
  const [systemHealth, setSystemHealth] = useState<string>("checking");

  const chatBottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  useEffect(() => {
    // Check backend health
    fetch("http://localhost:8000/api/v1/health")
      .then((res) => res.json())
      .then((data) => setSystemHealth(data.status === "online" ? "online" : "offline"))
      .catch(() => setSystemHealth("offline"));
  }, []);

  const handleSend = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!input.trim() || loading) return;

    const userQuery = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userQuery }]);
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/api/v1/agent/react", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          prompt: userQuery,
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
          {
            role: "assistant",
            content: "⚠️ Error connecting to Lunaris AI Agent Gateway.",
          },
        ]);
      }
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `⚠️ Failed to fetch response from gateway: ${err.message}`,
        },
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
    <div className="flex h-screen w-full bg-lunaris-900 text-slate-100 overflow-hidden font-sans">
      {/* Sidebar Knowledge Manager */}
      {showSidebar && <DocumentManager />}

      {/* Main Chat View */}
      <div className="flex-1 flex flex-col h-full overflow-hidden">
        {/* Top Navigation Bar */}
        <header className="h-14 border-b border-slate-800/80 bg-lunaris-800/50 backdrop-blur px-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <button
              onClick={() => setShowSidebar(!showSidebar)}
              className="p-1.5 text-slate-400 hover:text-white rounded-md hover:bg-slate-800 transition-colors"
              title="Toggle Knowledge Base Sidebar"
            >
              <Database className="w-4 h-4 text-indigo-400" />
            </button>
            <div className="flex items-center space-x-2">
              <div className="w-2.5 h-2.5 rounded-full bg-indigo-500 animate-ping" />
              <h1 className="font-bold text-slate-100 tracking-tight text-sm flex items-center space-x-1.5">
                <span>LUNARIS AI</span>
                <span className="text-[10px] uppercase font-mono px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                  Sovereign Core
                </span>
              </h1>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={() => setShowSandbox(true)}
              className="flex items-center space-x-1.5 px-2.5 py-1.5 rounded-md bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-mono transition-colors border border-slate-700"
            >
              <Terminal className="w-3.5 h-3.5 text-amber-400" />
              <span>Sandbox Console</span>
            </button>

            <div className="flex items-center space-x-1.5 text-xs px-2.5 py-1 rounded-full bg-slate-900 border border-slate-800">
              <span
                className={`w-2 h-2 rounded-full ${
                  systemHealth === "online" ? "bg-emerald-400" : "bg-rose-400"
                }`}
              />
              <span className="text-[11px] font-mono text-slate-400 capitalize">
                {systemHealth}
              </span>
            </div>
          </div>
        </header>

        {/* Message Stream */}
        <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6">
          <div className="max-w-3xl mx-auto space-y-6">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex space-x-3 ${
                  msg.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                {msg.role === "assistant" && (
                  <div className="w-8 h-8 rounded-lg bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center shrink-0 mt-0.5">
                    <Bot className="w-4 h-4 text-indigo-400" />
                  </div>
                )}

                <div
                  className={`max-w-[85%] rounded-xl px-4 py-3 text-sm shadow-sm ${
                    msg.role === "user"
                      ? "bg-indigo-600 text-white rounded-tr-none"
                      : "bg-lunaris-800 border border-slate-800/80 rounded-tl-none text-slate-200"
                  }`}
                >
                  {/* Reasoning Trace if Available */}
                  {msg.reasoning_steps && msg.reasoning_steps.length > 0 && (
                    <ReasoningTrace steps={msg.reasoning_steps} />
                  )}

                  <div className="prose prose-invert prose-sm max-w-none break-words">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {msg.content}
                    </ReactMarkdown>
                  </div>
                </div>

                {msg.role === "user" && (
                  <div className="w-8 h-8 rounded-lg bg-slate-800 flex items-center justify-center shrink-0 mt-0.5">
                    <User className="w-4 h-4 text-slate-300" />
                  </div>
                )}
              </div>
            ))}

            {loading && (
              <div className="flex items-center space-x-3 text-slate-400 text-xs">
                <div className="w-8 h-8 rounded-lg bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center shrink-0">
                  <Sparkles className="w-4 h-4 text-indigo-400 animate-spin" />
                </div>
                <div className="flex items-center space-x-2 bg-lunaris-800 border border-slate-800 rounded-lg px-3 py-2">
                  <span className="font-mono">ReAct Agent reasoning across tools...</span>
                </div>
              </div>
            )}
            <div ref={chatBottomRef} />
          </div>
        </div>

        {/* Input Bar */}
        <div className="p-4 bg-lunaris-900 border-t border-slate-800/80">
          <form
            onSubmit={handleSend}
            className="max-w-3xl mx-auto flex items-center space-x-2 bg-lunaris-800 border border-slate-700/80 rounded-xl px-3 py-2 focus-within:border-indigo-500 transition-colors"
          >
            <VoiceRecorder onTranscription={handleVoiceTranscription} />

            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask Lunaris AI anything (search docs, web, execute code, reason)..."
              disabled={loading}
              className="flex-1 bg-transparent text-slate-100 text-sm focus:outline-none placeholder:text-slate-500"
            />

            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="p-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 text-white transition-colors"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
          <div className="text-center text-[10px] text-slate-500 mt-2 font-mono">
            Lunaris AI Sovereign Intelligence • Air-Gapped & Zero Cloud Telemetry
          </div>
        </div>
      </div>

      {/* Sandbox Runner Modal */}
      <SandboxRunner isOpen={showSandbox} onClose={() => setShowSandbox(false)} />
    </div>
  );
}
