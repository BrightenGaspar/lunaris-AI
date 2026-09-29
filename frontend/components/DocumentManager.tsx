"use client";

import React, { useState, useEffect } from "react";
import { Upload, FileText, Trash2, RefreshCw, CheckCircle2, AlertCircle, Database } from "lucide-react";

interface DocumentItem {
  title: string;
  file_type: string;
  file_path: string;
  file_hash: string;
  chunk_count: number;
  last_indexed: string;
}

export const DocumentManager: React.FC = () => {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  const fetchDocuments = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/v1/documents/list");
      if (res.ok) {
        const data = await res.json();
        setDocuments(data.documents || []);
      }
    } catch (e) {
      console.error("Failed to fetch documents", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    setUploading(true);
    setStatusMessage(null);

    const formData = new FormData();
    formData.append("file", files[0]);

    try {
      const res = await fetch("http://localhost:8000/api/v1/documents/upload", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (res.ok) {
        setStatusMessage(`Successfully indexed: ${files[0].name}`);
        fetchDocuments();
      } else {
        setStatusMessage(`Error: ${data.detail || "Upload failed"}`);
      }
    } catch (err: any) {
      setStatusMessage(`Upload failed: ${err.message}`);
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (title: string) => {
    try {
      const res = await fetch(`http://localhost:8000/api/v1/documents/${encodeURIComponent(title)}`, {
        method: "DELETE",
      });
      if (res.ok) {
        fetchDocuments();
      }
    } catch (err) {
      console.error("Failed to delete document", err);
    }
  };

  return (
    <div className="flex flex-col h-full bg-lunaris-900 border-r border-slate-800 p-4 w-80 text-sm">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div className="flex items-center space-x-2">
          <Database className="w-4 h-4 text-indigo-400" />
          <h2 className="font-semibold text-slate-200">Knowledge Base</h2>
        </div>
        <button
          onClick={fetchDocuments}
          disabled={loading}
          className="p-1.5 text-slate-400 hover:text-white rounded-md hover:bg-slate-800 transition-colors"
          title="Refresh document list"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      {/* Upload Zone */}
      <div className="mt-4">
        <label className="flex flex-col items-center justify-center p-4 border border-dashed border-slate-700 hover:border-indigo-500 rounded-lg cursor-pointer bg-slate-900/50 hover:bg-slate-900 transition-all">
          <Upload className="w-6 h-6 text-indigo-400 mb-1" />
          <span className="text-xs font-medium text-slate-300">
            {uploading ? "Indexing into pgvector..." : "Upload Document / Code"}
          </span>
          <span className="text-[10px] text-slate-500 mt-0.5">PDF, DOCX, CSV, TXT, MD, Python</span>
          <input
            type="file"
            onChange={handleFileUpload}
            disabled={uploading}
            className="hidden"
            accept=".pdf,.docx,.csv,.json,.txt,.md,.py,.js,.ts,.html,.css"
          />
        </label>
      </div>

      {statusMessage && (
        <div className="mt-2 text-[11px] p-2 rounded bg-slate-800/80 text-indigo-300 border border-indigo-500/20">
          {statusMessage}
        </div>
      )}

      {/* Document List */}
      <div className="mt-4 flex-1 overflow-y-auto space-y-2 pr-1">
        <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
          Indexed Documents ({documents.length})
        </div>

        {documents.length === 0 ? (
          <div className="text-center py-6 text-slate-500 text-xs">
            No documents indexed yet. Drop a file above to add to memory.
          </div>
        ) : (
          documents.map((doc, idx) => (
            <div
              key={idx}
              className="p-2.5 rounded-lg bg-slate-900/60 border border-slate-800/80 hover:border-slate-700 flex items-start justify-between group transition-colors"
            >
              <div className="flex items-start space-x-2 overflow-hidden">
                <FileText className="w-4 h-4 text-cyan-400 mt-0.5 shrink-0" />
                <div className="overflow-hidden">
                  <div className="font-medium text-slate-200 text-xs truncate" title={doc.title}>
                    {doc.title}
                  </div>
                  <div className="text-[10px] text-slate-500 flex items-center space-x-2 mt-0.5">
                    <span className="uppercase">{doc.file_type.replace('.', '')}</span>
                    <span>•</span>
                    <span>{doc.chunk_count} chunks</span>
                  </div>
                </div>
              </div>
              <button
                onClick={() => handleDelete(doc.title)}
                className="opacity-0 group-hover:opacity-100 p-1 text-slate-500 hover:text-red-400 transition-opacity"
                title="Delete document"
              >
                <Trash2 className="w-3.5 h-3.5" />
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
