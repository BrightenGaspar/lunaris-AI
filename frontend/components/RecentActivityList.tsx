"use client";

import React from "react";

export const RecentActivityList: React.FC = () => {
  const activities = [
    { title: "Model training completed", time: "23:41", dot: "bg-red-500", glow: "#ff1638" },
    { title: "New data received", time: "23:41", dot: "bg-emerald-400", glow: "#34d399" },
    { title: "Analysis report generated", time: "23:28", dot: "bg-emerald-400", glow: "#34d399" },
    { title: "Backup successful", time: "23:15", dot: "bg-amber-400", glow: "#fbbf24" },
    { title: "System health check", time: "22:58", dot: "bg-red-500", glow: "#ff1638" },
  ];

  return (
    <div className="rounded-2xl bg-[#0f0b14] border border-red-500/20 p-5 shadow-[0_10px_30px_rgba(0,0,0,0.5)] flex flex-col justify-between">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-xs font-bold text-white tracking-wide">Recent Activity</h3>
        <button className="text-[11px] text-red-500 hover:text-orange-400 font-semibold transition-colors">
          View All
        </button>
      </div>

      <div className="space-y-3">
        {activities.map((act, i) => (
          <div key={i} className="flex items-center justify-between text-xs py-0.5">
            <div className="flex items-center space-x-2.5">
              <div
                className={`w-2 h-2 rounded-full ${act.dot}`}
                style={{ boxShadow: `0 0 6px ${act.glow}` }}
              />
              <span className="text-slate-300 font-medium text-[11px]">{act.title}</span>
            </div>
            <span className="text-slate-500 font-mono text-[10px]">{act.time}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
