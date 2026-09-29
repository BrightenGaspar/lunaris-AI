"use client";

import React, { useState } from "react";
import { Brain, ChevronDown, ChevronRight, Terminal, Search, FileText, Calculator, CheckCircle2 } from "lucide-react";

interface Step {
  step: number;
  thought?: string;
  action?: string;
  action_input?: string;
  observation?: string;
  type?: string;
  content?: string;
}

interface ReasoningTraceProps {
  steps: Step[];
}

export const ReasoningTrace: React.FC<ReasoningTraceProps> = ({ steps }) => {
  const [isOpen, setIsOpen] = useState(false);

  if (!steps || steps.length === 0) return null;

  const getToolIcon = (toolName?: string) => {
    switch (toolName) {
      case "search_documents":
        return <FileText className="w-3.5 h-3.5 text-emerald-400" />;
      case "web_search":
        return <Search className="w-3.5 h-3.5 text-cyan-400" />;
      case "execute_python_sandbox":
        return <Terminal className="w-3.5 h-3.5 text-amber-400" />;
      case "calculate_math":
        return <Calculator className="w-3.5 h-3.5 text-purple-400" />;
      default:
        return <Brain className="w-3.5 h-3.5 text-indigo-400" />;
    }
  };

  return (
    <div className="mb-3 rounded-lg border border-slate-800 bg-lunaris-800/80 overflow-hidden text-xs">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-3 py-2 flex items-center justify-between text-slate-300 hover:text-white bg-slate-900/60 transition-colors"
      >
        <div className="flex items-center space-x-2">
          <Brain className="w-4 h-4 text-indigo-400 animate-pulse" />
          <span className="font-medium text-slate-200">
            Autonomous ReAct Reasoning ({steps.length} {steps.length === 1 ? 'Step' : 'Steps'})
          </span>
        </div>
        <div className="flex items-center space-x-1.5 text-slate-400">
          <span className="text-[11px]">{isOpen ? "Hide trace" : "View reasoning trace"}</span>
          {isOpen ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronRight className="w-3.5 h-3.5" />}
        </div>
      </button>

      {isOpen && (
        <div className="p-3 space-y-2.5 divide-y divide-slate-800/60 bg-slate-950/40">
          {steps.map((st, idx) => (
            <div key={idx} className="pt-2 first:pt-0 space-y-1.5">
              {st.thought && (
                <div className="text-slate-300">
                  <span className="text-indigo-400 font-semibold uppercase text-[10px] tracking-wider">Thought: </span>
                  {st.thought.replace(/^Thought:\s*/i, "")}
                </div>
              )}

              {st.action && (
                <div className="flex items-start space-x-2 bg-slate-900/90 rounded p-2 border border-slate-800">
                  <div className="mt-0.5">{getToolIcon(st.action)}</div>
                  <div className="flex-1 overflow-hidden font-mono text-[11px]">
                    <div className="text-indigo-300 font-semibold flex items-center space-x-1">
                      <span>Action:</span>
                      <span className="text-cyan-400">{st.action}</span>
                    </div>
                    {st.action_input && (
                      <div className="text-slate-400 mt-0.5 break-words">
                        <span className="text-slate-500">Input: </span>
                        {st.action_input}
                      </div>
                    )}
                  </div>
                </div>
              )}

              {st.observation && (
                <div className="bg-slate-900/50 rounded p-2 text-slate-300 font-mono text-[11px] max-h-36 overflow-y-auto border border-slate-800/50">
                  <span className="text-emerald-400 font-semibold text-[10px] block uppercase mb-0.5">Observation:</span>
                  <pre className="whitespace-pre-wrap">{st.observation}</pre>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
