"use client";

import React from "react";
import { Plus, Upload, Cpu, BarChart2, ArrowRight } from "lucide-react";

interface QuickActionsProps {
  onNewProject: () => void;
  onUploadData: () => void;
  onTrainModel: () => void;
  onViewReports: () => void;
}

export const QuickActions: React.FC<QuickActionsProps> = ({
  onNewProject,
  onUploadData,
  onTrainModel,
  onViewReports,
}) => {
  const actions = [
    {
      title: "New Project",
      subtitle: "Create AI project",
      icon: Plus,
      action: onNewProject,
    },
    {
      title: "Upload Data",
      subtitle: "Import dataset",
      icon: Upload,
      action: onUploadData,
    },
    {
      title: "Train Model",
      subtitle: "Start training",
      icon: Cpu,
      action: onTrainModel,
    },
    {
      title: "View Reports",
      subtitle: "Analytics & insights",
      icon: BarChart2,
      action: onViewReports,
    },
  ];

  return (
    <div className="space-y-3">
      <h3 className="text-xs font-bold text-white tracking-wide">Quick Actions</h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {actions.map((act, i) => {
          const Icon = act.icon;
          return (
            <button
              key={i}
              onClick={act.action}
              className="rounded-2xl bg-[#0f0b14] border border-red-500/20 hover:border-red-500/50 p-3.5 flex items-center justify-between text-left transition-all group shadow-[0_8px_25px_rgba(0,0,0,0.4)] hover:-translate-y-0.5"
            >
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-red-600 to-red-800 text-white flex items-center justify-center shadow-[0_0_15px_rgba(255,20,50,0.4)] group-hover:scale-105 transition-transform">
                  <Icon className="w-5 h-5" />
                </div>
                <div>
                  <div className="text-xs font-bold text-white group-hover:text-red-400 transition-colors">
                    {act.title}
                  </div>
                  <div className="text-[10px] text-slate-400">{act.subtitle}</div>
                </div>
              </div>
              <ArrowRight className="w-4 h-4 text-red-500 opacity-60 group-hover:opacity-100 group-hover:translate-x-1 transition-all" />
            </button>
          );
        })}
      </div>
    </div>
  );
};
