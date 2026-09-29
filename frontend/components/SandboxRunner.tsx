"use client";

import React, { useState } from "react";
import { Terminal, Play, CheckCircle2, AlertTriangle, X } from "lucide-react";

interface SandboxRunnerProps {
  isOpen: boolean;
  onClose: () => void;
}

export const SandboxRunner: React.FC<SandboxRunnerProps> = ({ isOpen, onClose }) => {
  const [code, setCode] = useState<string>(
    "# Test Untrusted Python in Docker Sandbox\nimport math\n\nprimes = [n for n in range(2, 50) if all(n % d != 0 for d in range(2, int(math.sqrt(n)) + 1))]\nprint(f'Primes up to 50: {primes}')"
  );
  const [output, setOutput] = useState<string | null>(null);
  const [running, setRunning] = useState(false);
  const [status, setStatus] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleExecute = async () => {
    setRunning(true);
    setOutput(null);
    setStatus(null);

    try {
      const res = await fetch("http://localhost:8000/api/v1/sandbox/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });
      const data = await res.json();
      setStatus(data.status);
      setOutput(data.output || "No output returned.");
    } catch (err: any) {
      setStatus("error");
      setOutput(`Failed to communicate with sandbox API: ${err.message}`);
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-lunaris-800 border border-slate-700 rounded-xl w-full max-w-2xl overflow-hidden shadow-2xl flex flex-col max-h-[85vh]">
        {/* Header */}
        <div className="px-4 py-3 bg-slate-900 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Terminal className="w-5 h-5 text-amber-400" />
            <h3 className="font-semibold text-slate-100 text-sm">Docker Python Sandbox Terminal</h3>
            <span className="text-[10px] bg-amber-500/10 text-amber-400 border border-amber-500/30 px-2 py-0.5 rounded-full font-mono">
              Air-gapped (No Network)
            </span>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white p-1 rounded">
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Code Editor */}
        <div className="p-4 flex-1 flex flex-col space-y-3 overflow-hidden">
          <div className="flex-1 flex flex-col">
            <label className="text-xs text-slate-400 font-mono mb-1">Python Script:</label>
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              className="w-full h-44 bg-slate-950 border border-slate-800 rounded-lg p-3 text-emerald-400 font-mono text-xs focus:outline-none focus:border-indigo-500 resize-none"
              spellCheck={false}
            />
          </div>

          <div className="flex justify-end">
            <button
              onClick={handleExecute}
              disabled={running}
              className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 text-white rounded-lg text-xs font-medium transition-colors"
            >
              <Play className={`w-3.5 h-3.5 ${running ? 'animate-spin' : ''}`} />
              <span>{running ? "Executing in Container..." : "Run Code in Sandbox"}</span>
            </button>
          </div>

          {/* Output Terminal */}
          {output !== null && (
            <div className="space-y-1">
              <div className="flex items-center space-x-2">
                <span className="text-xs text-slate-400 font-mono">Execution Log:</span>
                {status === "success" && (
                  <span className="text-[10px] text-emerald-400 flex items-center space-x-1 font-mono">
                    <CheckCircle2 className="w-3 h-3" /> <span>Success</span>
                  </span>
                )}
                {status === "runtime_error" && (
                  <span className="text-[10px] text-rose-400 flex items-center space-x-1 font-mono">
                    <AlertTriangle className="w-3 h-3" /> <span>Runtime Error</span>
                  </span>
                )}
              </div>
              <pre className="p-3 bg-black/90 border border-slate-800 text-slate-200 font-mono text-xs rounded-lg max-h-40 overflow-y-auto whitespace-pre-wrap">
                {output}
              </pre>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
