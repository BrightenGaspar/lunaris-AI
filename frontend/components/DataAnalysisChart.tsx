"use client";

import React, { useState } from "react";
import { ChevronDown, Database, TrendingUp, RefreshCw } from "lucide-react";

export const DataAnalysisChart: React.FC = () => {
  const [filter, setFilter] = useState("This Week");

  const bars = [
    { day: "Mon", height: 35 },
    { day: "Tue", height: 50 },
    { day: "Wed", height: 75 },
    { day: "Thu", height: 60 },
    { day: "Fri", height: 90 },
    { day: "Sat", height: 70 },
    { day: "Sun", height: 100 },
  ];

  return (
    <div className="rounded-2xl bg-[#0f0b14] border border-red-500/20 p-5 shadow-[0_10px_30px_rgba(0,0,0,0.5)] flex flex-col justify-between">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-xs font-bold text-white tracking-wide">Data Analysis</h3>
        <div className="flex items-center space-x-1 text-[11px] text-slate-400 bg-[#16101c] px-2.5 py-1 rounded-lg border border-slate-800 cursor-pointer">
          <span>{filter}</span>
          <ChevronDown className="w-3 h-3" />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-center">
        {/* Bar Chart */}
        <div className="md:col-span-2">
          <div className="flex items-end justify-between h-28 pt-4 pb-1 px-2 border-b border-slate-800/80">
            {bars.map((b, i) => (
              <div key={i} className="flex flex-col items-center flex-1 space-y-1">
                <div className="w-full flex items-end justify-center h-full">
                  <div
                    style={{ height: `${b.height}%` }}
                    className="w-4 bg-gradient-to-t from-[#850820] to-[#ff1638] rounded-t-sm shadow-[0_0_8px_rgba(255,20,50,0.4)] hover:brightness-125 transition-all"
                  />
                </div>
                <span className="text-[10px] text-slate-400 font-mono">{b.day}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Side Metrics */}
        <div className="space-y-3 border-l border-slate-800/80 pl-3">
          <div className="flex items-center space-x-2.5">
            <div className="p-1.5 rounded-lg bg-red-600/10 text-red-500">
              <Database className="w-3.5 h-3.5" />
            </div>
            <div>
              <div className="text-xs font-bold text-white font-mono">125K</div>
              <div className="text-[10px] text-slate-400">Data Points</div>
            </div>
          </div>

          <div className="flex items-center space-x-2.5">
            <div className="p-1.5 rounded-lg bg-emerald-600/10 text-emerald-400">
              <TrendingUp className="w-3.5 h-3.5" />
            </div>
            <div>
              <div className="text-xs font-bold text-white font-mono">24.8%</div>
              <div className="text-[10px] text-slate-400">Growth</div>
            </div>
          </div>

          <div className="flex items-center space-x-2.5">
            <div className="p-1.5 rounded-lg bg-amber-600/10 text-amber-400">
              <RefreshCw className="w-3.5 h-3.5" />
            </div>
            <div>
              <div className="text-xs font-bold text-white font-mono">99.2%</div>
              <div className="text-[10px] text-slate-400">Uptime</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
