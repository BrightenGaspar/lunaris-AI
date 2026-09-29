"use client";

import React from "react";

export const SystemOverview: React.FC = () => {
  const gauges = [
    { label: "CPU", percentage: 72 },
    { label: "Memory", percentage: 54 },
    { label: "Storage", percentage: 81 },
  ];

  return (
    <div className="rounded-2xl bg-[#0f0b14] border border-red-500/20 p-5 shadow-[0_10px_30px_rgba(0,0,0,0.5)] flex flex-col justify-between">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xs font-bold text-white tracking-wide">System Overview</h3>
        <div className="w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_8px_#34d399]" />
      </div>

      <div className="grid grid-cols-3 gap-2 text-center py-2">
        {gauges.map((g, idx) => {
          const radius = 30;
          const circumference = 2 * Math.PI * radius;
          const strokeDashoffset = circumference - (g.percentage / 100) * circumference;

          return (
            <div key={idx} className="flex flex-col items-center">
              <div className="relative w-20 h-20 flex items-center justify-center">
                <svg className="w-full h-full -rotate-90">
                  {/* Background Track */}
                  <circle
                    cx="40"
                    cy="40"
                    r={radius}
                    stroke="rgba(255,255,255,0.08)"
                    strokeWidth="6"
                    fill="transparent"
                  />
                  {/* Progress Glow Gauge */}
                  <circle
                    cx="40"
                    cy="40"
                    r={radius}
                    stroke="#ff1638"
                    strokeWidth="6"
                    strokeDasharray={circumference}
                    strokeDashoffset={strokeDashoffset}
                    strokeLinecap="round"
                    fill="transparent"
                    className="transition-all duration-1000 ease-out"
                    style={{ filter: "drop-shadow(0 0 6px #ff1638)" }}
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center font-bold text-xs text-white font-mono">
                  {g.percentage}%
                </div>
              </div>
              <span className="text-[11px] text-slate-400 font-medium mt-1">{g.label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
