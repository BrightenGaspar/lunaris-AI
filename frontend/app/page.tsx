"use client";

import React, { useState } from "react";
import { Sidebar } from "@/components/Sidebar";
import { Header } from "@/components/Header";
import { WelcomeBanner } from "@/components/WelcomeBanner";
import { ClockWeatherWidget } from "@/components/ClockWeatherWidget";
import { MetricCards } from "@/components/MetricCards";
import { SystemOverview } from "@/components/SystemOverview";
import { GlobalActivityMap } from "@/components/GlobalActivityMap";
import { AIInsightsChart } from "@/components/AIInsightsChart";
import { DataAnalysisChart } from "@/components/DataAnalysisChart";
import { RecentActivityList } from "@/components/RecentActivityList";
import { QuickActions } from "@/components/QuickActions";

import { ChatModal } from "@/components/ChatModal";
import { UploadModal } from "@/components/UploadModal";
import { SandboxRunner } from "@/components/SandboxRunner";

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState("dashboard");
  const [searchQuery, setSearchQuery] = useState("");
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [isUploadOpen, setIsUploadOpen] = useState(false);
  const [isSandboxOpen, setIsSandboxOpen] = useState(false);
  const [chatInitialQuery, setChatInitialQuery] = useState("");

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      setChatInitialQuery(searchQuery.trim());
      setIsChatOpen(true);
    }
  };

  const handleStartNewProject = () => {
    setChatInitialQuery("Start a new AI project plan and outline architecture.");
    setIsChatOpen(true);
  };

  return (
    <div className="flex min-h-screen bg-[#070509] text-white font-sans selection:bg-red-600 selection:text-white overflow-x-hidden">
      {/* Sidebar Navigation */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onOpenUpload={() => setIsUploadOpen(true)}
        onOpenChat={() => setIsChatOpen(true)}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        <Header
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
          onSearchSubmit={handleSearchSubmit}
        />

        <main className="flex-1 p-5 md:p-6 space-y-5 max-w-[1600px] w-full mx-auto">
          {/* Row 1: Welcome Banner & Clock/Weather Widget */}
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-5 items-stretch">
            <div className="lg:col-span-3">
              <WelcomeBanner onStartNewProject={handleStartNewProject} />
            </div>
            <div className="lg:col-span-1">
              <ClockWeatherWidget />
            </div>
          </div>

          {/* Row 2: 4 Metric Cards */}
          <MetricCards />

          {/* Row 3: System Overview, Global Activity Map, AI Insights Chart */}
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-12 gap-5 items-stretch">
            <div className="lg:col-span-3">
              <SystemOverview />
            </div>
            <div className="lg:col-span-5">
              <GlobalActivityMap />
            </div>
            <div className="lg:col-span-4">
              <AIInsightsChart />
            </div>
          </div>

          {/* Row 4: Data Analysis & Recent Activity */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-stretch">
            <div className="lg:col-span-7">
              <DataAnalysisChart />
            </div>
            <div className="lg:col-span-5">
              <RecentActivityList />
            </div>
          </div>

          {/* Row 5: Quick Actions Bar */}
          <QuickActions
            onNewProject={() => {
              setChatInitialQuery("");
              setIsChatOpen(true);
            }}
            onUploadData={() => setIsUploadOpen(true)}
            onTrainModel={() => setIsSandboxOpen(true)}
            onViewReports={() => {
              setChatInitialQuery("Generate an analytics report summarizing system performance.");
              setIsChatOpen(true);
            }}
          />
        </main>
      </div>

      {/* Interactive Modals */}
      <ChatModal
        isOpen={isChatOpen}
        onClose={() => setIsChatOpen(false)}
        initialQuery={chatInitialQuery}
      />
      <UploadModal
        isOpen={isUploadOpen}
        onClose={() => setIsUploadOpen(false)}
      />
      <SandboxRunner
        isOpen={isSandboxOpen}
        onClose={() => setIsSandboxOpen(false)}
      />
    </div>
  );
}
