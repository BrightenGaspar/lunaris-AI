"use client";

import React from "react";
import { ArrowRight, Sparkles } from "lucide-react";

interface WelcomeBannerProps {
  onStartNewProject: () => void;
}

export const WelcomeBanner: React.FC<WelcomeBannerProps> = ({ onStartNewProject }) => {
  return (
    <div className="relative rounded-2xl bg-gradient-to-r from-[#140c17] via-[#100814] to-[#1c0812] border border-red-500/25 p-6 overflow-hidden flex flex-col justify-between min-h-[160px] shadow-[0_10px_40px_rgba(0,0,0,0.6)]">
      {/* Background Holographic Planet Art */}
      <div className="absolute right-0 top-0 bottom-0 w-1/2 pointer-events-none overflow-hidden flex items-center justify-end">
        <div className="relative w-64 h-64 -mr-10 opacity-80">
          {/* Glowing wireframe sphere effect */}
          <div className="absolute inset-0 rounded-full bg-gradient-to-l from-red-600/30 via-red-900/10 to-transparent blur-md" />
          <svg viewBox="0 0 200 200" className="w-full h-full text-red-500/60 animate-spin-slow">
            <circle cx="100" cy="100" r="80" fill="none" stroke="currentColor" strokeWidth="1" strokeDasharray="4 4" />
            <ellipse cx="100" cy="100" rx="80" ry="30" fill="none" stroke="currentColor" strokeWidth="1" />
            <ellipse cx="100" cy="100" rx="30" ry="80" fill="none" stroke="currentColor" strokeWidth="1" />
            <circle cx="100" cy="100" r="4" fill="#ff4b60" className="shadow-[0_0_10px_#ff1638]" />
            <circle cx="140" cy="80" r="3" fill="#ff7417" />
            <circle cx="70" cy="130" r="3" fill="#ff1638" />
            <circle cx="120" cy="140" r="3" fill="#ff1638" />
            <line x1="100" y1="100" x2="140" y2="80" stroke="rgba(255,50,70,0.4)" strokeWidth="1" />
            <line x1="100" y1="100" x2="70" y2="130" stroke="rgba(255,50,70,0.4)" strokeWidth="1" />
          </svg>
        </div>
      </div>

      {/* Quote at Top Right */}
      <div className="absolute right-6 top-5 text-right hidden md:block">
        <p className="text-[11px] text-slate-400 italic max-w-xs">
          &ldquo;Intelligence powers a brighter tomorrow.&rdquo;
        </p>
      </div>

      {/* Content */}
      <div className="relative z-10">
        <span className="text-xs text-slate-400 font-medium">Welcome back,</span>
        <h2 className="text-2xl font-bold text-white tracking-wide mt-0.5">
          Steve Brighton
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Let&apos;s build a smarter tomorrow with AI.
        </p>

        <button
          onClick={onStartNewProject}
          className="mt-4 px-4 py-2 bg-gradient-to-r from-[#d81333] to-[#ff4b2b] hover:from-red-600 hover:to-orange-500 text-white rounded-xl text-xs font-semibold flex items-center space-x-2 shadow-[0_4px_20px_rgba(255,20,50,0.4)] transition-all transform hover:-translate-y-0.5"
        >
          <span>Start a New Project</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
};
