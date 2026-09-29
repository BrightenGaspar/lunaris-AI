"use client";

import React, { useState, useEffect } from "react";
import { X, Upload, FileText, Trash2, RefreshCw, CheckCircle2, AlertCircle } from "lucide-react";

interface UploadModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const UploadModal: React.FC<UploadModalProps> = ({ isOpen, onClose }) => {
  const [documents, setDocuments] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [statusMsg, setStatusMsg] = useState<string | null>(null);

  const fetchDocs = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/v1/documents/list");
      if (res.ok) {
        const data = await res.json();
        setDocuments(data.documents || []);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchDocs();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    setUploading(true);
    setStatusMsg(null);

    const formData = new FormData();
    formData.append("file", files[0]);

    try {
      const res = await fetch("http://localhost:8000/api/v1/documents/upload", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (res.ok) {
        setStatusMsg(`Indexed: ${files[0].name}`);
        fetchDocs();
      } else {
        setStatusMsg(`Failed: ${data.detail}`);
      }
    } catch (err: any) {
      setStatusMsg(`Upload error: ${err.message}`);
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (title: string) => {
    try {
      await fetch(`http://localhost:8000/api/v1/documents/${encodeURIComponent(title)}`, {
        method: "DELETE",
      });
      fetchDocs();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
      <div className="bg-[#0b080e] border border-red-500/30 rounded-2xl w-full max-w-xl max-h-[85vh] flex flex-col overflow-hidden shadow-[0_25px_90px_rgba(0,0,0,0.9)]">
        {/* Header */}
        <div className="h-14 px-5 border-b border-red-500/10 flex items-center justify-between bg-[#120d18]">
          <div className="flex items-center space-x-2">
            <Upload className="w-4 h-4 text-red-500" />
            <h3 className="text-xs font-bold text-white tracking-wide">Knowledge Base & Vector Ingestion</h3>
          </div>
          <button onClick={onClose} className="p-1 text-slate-400 hover:text-white">
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content */}
        <div className="p-5 space-y-4 overflow-y-auto">
          {/* Dropzone */}
          <label className="flex flex-col items-center justify-center p-6 border-2 border-dashed border-red-500/30 hover:border-red-500 rounded-xl cursor-pointer bg-[#141019] hover:bg-[#1a1522] transition-all">
            <Upload className="w-8 h-8 text-red-500 mb-2" />
            <span className="text-xs font-semibold text-white">
              {uploading ? "Ingesting & Embedding..." : "Click or Drag Documents to Ingest"}
            </span>
            <span className="text-[10px] text-slate-400 mt-1">PDF, DOCX, CSV, TXT, Markdown, Python, JSON</span>
            <input
              type="file"
              onChange={handleUpload}
              disabled={uploading}
              className="hidden"
              accept=".pdf,.docx,.csv,.json,.txt,.md,.py,.js,.ts,.html,.css"
            />
          </label>

          {statusMsg && (
            <div className="text-xs p-2.5 rounded-lg bg-red-600/10 border border-red-500/30 text-red-300">
              {statusMsg}
            </div>
          )}

          {/* List */}
          <div className="space-y-2">
            <div className="flex items-center justify-between text-xs font-semibold text-slate-400 uppercase tracking-wider">
              <span>Indexed Documents ({documents.length})</span>
              <button onClick={fetchDocs} className="text-slate-400 hover:text-white">
                <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
              </button>
            </div>

            {documents.length === 0 ? (
              <div className="text-center py-6 text-slate-500 text-xs">
                No documents indexed in pgvector yet.
              </div>
            ) : (
              documents.map((d, i) => (
                <div
                  key={i}
                  className="p-2.5 rounded-xl bg-[#141019] border border-slate-800 flex items-center justify-between text-xs"
                >
                  <div className="flex items-center space-x-2.5 overflow-hidden">
                    <FileText className="w-4 h-4 text-red-400 shrink-0" />
                    <div className="truncate">
                      <div className="font-medium text-white truncate">{d.title}</div>
                      <div className="text-[10px] text-slate-500">
                        {d.file_type} • {d.chunk_count} chunks
                      </div>
                    </div>
                  </div>
                  <button
                    onClick={() => handleDelete(d.title)}
                    className="p-1 text-slate-500 hover:text-red-400"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
