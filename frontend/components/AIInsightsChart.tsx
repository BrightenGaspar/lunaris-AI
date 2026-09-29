"use client";

import React, { useState } from "react";
import { ChevronDown } from "lucide-react";

export const AIInsightsChart: React.FC = () => {
  const [filter, setFilter] = useState("Last 7 days");

  const dataPoints = [
    { label: "Sep 9", val: 50 },
    { label: "Sep 10", val: 80 },
    { label: "Sep 11", val: 120 },
    { label: "Sep 12", val: 70 },
    { label: "Sep 13", val: 140 },
    { label: "Sep 14", val: 110 },
    { label: "Sep 15", val: 180 },
  ];

  return (
    <div className="rounded-2xl bg-[#0f0b14] border border-red-500/20 p-5 shadow-[0_10px_30px_rgba(0,0,0,0.5)] flex flex-col justify-between">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-xs font-bold text-white tracking-wide">AI Insights</h3>
        <div className="flex items-center space-x-1 text-[11px] text-slate-400 bg-[#16101c] px-2.5 py-1 rounded-lg border border-slate-800 cursor-pointer">
          <span>{filter}</span>
          <ChevronDown className="w-3 h-3" />
        </div>
      </div>

      {/* SVG Line Chart */}
      <div className="relative h-28 my-2">
        <svg viewBox="0 0 300 100" className="w-full h-full overflow-visible">
          {/* Subtle Grid Lines */}
          <line x1="0" y1="20" x2="300" y2="20" stroke="rgba(255,255,255,0.05)" strokeDasharray="3 3" />
          <line x1="0" y1="50" x2="300" y2="50" stroke="rgba(255,255,255,0.05)" strokeDasharray="3 3" />
          <line x1="0" y1="80" x2="300" y2="80" stroke="rgba(255,255,255,0.05)" strokeDasharray="3 3" />

          {/* Area Glow */}
          <polygon
            fill="url(#redAreaGradient)"
            points="0,80 40,65 90,45 140,70 190,30 240,48 290,15 290,100 0,100"
          />

          {/* Glowing Red Line */}
          <polyline
            fill="none"
            stroke="#ff1638"
            strokeWidth="2.5"
            points="0,80 40,65 90,45 140,70 190,30 240,48 290,15"
            style={{ filter: "drop-shadow(0 0 6px #ff1638)" }}
          />

          {/* Data Points */}
          <circle cx="0" cy="80" r="3.5" fill="#ffffff" stroke="#ff1638" strokeWidth="2" />
          <circle cx="40" cy="65" r="3.5" fill="#ffffff" stroke="#ff1638" strokeWidth="2" />
          <circle cx="90" cy="45" r="3.5" fill="#ffffff" stroke="#ff1638" strokeWidth="2" />
          <circle cx="140" cy="70" r="3.5" fill="#ffffff" stroke="#ff1638" strokeWidth="2" />
          <circle cx="190" cy="30" r="3.5" fill="#ffffff" stroke="#ff1638" strokeWidth="2" />
          <circle cx="240" cy="48" r="3.5" fill="#ffffff" stroke="#ff1638" strokeWidth="2" />
          <circle cx="290" cy="15" r="4.5" fill="#ffffff" stroke="#ff1638" strokeWidth="2.5" style={{ filter: "drop-shadow(0 0 8px #ff1638)" }} />

          <defs>
            <linearGradient id="redAreaGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="rgba(255, 22, 56, 0.3)" />
              <stop offset="100%" stopColor="rgba(255, 22, 56, 0.0)" />
            </linearGradient>
          </defs>
        </svg>

        {/* X Axis Labels */}
        <div className="flex justify-between text-[9px] text-slate-500 mt-1 font-mono">
          {dataPoints.map((d, i) => (
            <span key={i}>{d.label}</span>
          ))}
        </div>
      </div>

      {/* Metric Pills at Bottom */}
      <div className="grid grid-cols-3 gap-2 pt-2 border-t border-slate-800/80 text-center">
        <div className="bg-[#16101c] p-1.5 rounded-lg border border-slate-800">
          <div className="text-xs font-bold text-white font-mono">1.2M</div>
          <div className="text-[9px] text-slate-400">Requests</div>
        </div>
        <div className="bg-[#16101c] p-1.5 rounded-lg border border-slate-800">
          <div className="text-xs font-bold text-white font-mono">98.6%</div>
          <div className="text-[9px] text-slate-400">Accuracy</div>
        </div>
        <div className="bg-[#16101c] p-1.5 rounded-lg border border-slate-800">
          <div className="text-xs font-bold text-white font-mono">0.8s</div>
          <div className="text-[9px] text-slate-400">Response</div>
        </div>
      </div>
    </div>
  );
};
