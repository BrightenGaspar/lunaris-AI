"use client";

import React, { useState } from "react";
import { ChevronDown } from "lucide-react";

export const GlobalActivityMap: React.FC = () => {
  const [filter, setFilter] = useState("Last 24 hours");

  const stats = [
    { label: "Active", count: "1,284", color: "bg-red-500", glow: "#ff1638" },
    { label: "Processing", count: "320", color: "bg-amber-400", glow: "#fbbf24" },
    { label: "Completed", count: "5,921", color: "bg-emerald-400", glow: "#34d399" },
    { label: "Errors", count: "12", color: "bg-red-600", glow: "#dc2626" },
  ];

  return (
    <div className="rounded-2xl bg-[#0f0b14] border border-red-500/20 p-5 shadow-[0_10px_30px_rgba(0,0,0,0.5)] flex flex-col justify-between">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-xs font-bold text-white tracking-wide">Global Activity</h3>
        <div className="flex items-center space-x-1 text-[11px] text-slate-400 bg-[#16101c] px-2.5 py-1 rounded-lg border border-slate-800 cursor-pointer">
          <span>{filter}</span>
          <ChevronDown className="w-3 h-3" />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-center">
        {/* World Map Vector Illustration */}
        <div className="md:col-span-2 relative h-36 flex items-center justify-center overflow-hidden">
          <svg viewBox="0 0 400 180" className="w-full h-full opacity-60">
            {/* World continents outline silhouette */}
            <path
              fill="rgba(255,255,255,0.06)"
              d="M60,40 Q90,30 110,50 Q130,70 100,100 Q80,120 70,80 Z M180,35 Q220,30 240,60 Q260,90 230,120 Q190,140 180,80 Z M300,50 Q340,40 360,70 Q370,110 330,120 Q300,90 300,50 Z M120,130 Q140,120 150,150 Q130,170 120,130 Z"
            />
            {/* Glowing Interconnected Network Lines */}
            <polyline
              points="75,55 190,65 240,80 320,60"
              fill="none"
              stroke="#ff1638"
              strokeWidth="1.5"
              strokeDasharray="3 3"
              style={{ filter: "drop-shadow(0 0 6px #ff1638)" }}
            />
            <polyline
              points="100,85 190,65 140,140 230,110 330,110"
              fill="none"
              stroke="#ff7417"
              strokeWidth="1"
              strokeDasharray="2 2"
            />

            {/* Glowing Map Node Pins */}
            <circle cx="75" cy="55" r="4" fill="#ff1638" style={{ filter: "drop-shadow(0 0 8px #ff1638)" }} />
            <circle cx="190" cy="65" r="5" fill="#ff1638" style={{ filter: "drop-shadow(0 0 10px #ff1638)" }} />
            <circle cx="240" cy="80" r="4" fill="#ff7417" />
            <circle cx="320" cy="60" r="4" fill="#ff1638" />
            <circle cx="140" cy="140" r="3" fill="#ff1638" />
            <circle cx="330" cy="110" r="3" fill="#34d399" />
          </svg>
        </div>

        {/* Legend Numbers */}
        <div className="space-y-2 border-l border-slate-800/80 pl-3">
          {stats.map((st, i) => (
            <div key={i} className="flex items-center justify-between text-xs">
              <div className="flex items-center space-x-2">
                <div className={`w-2 h-2 rounded-full ${st.color}`} style={{ boxShadow: `0 0 6px ${st.glow}` }} />
                <span className="text-slate-400 text-[11px]">{st.label}</span>
              </div>
              <span className="font-bold text-white font-mono text-[11px]">{st.count}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
