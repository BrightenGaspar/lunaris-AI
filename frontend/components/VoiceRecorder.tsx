"use client";

import React, { useState, useRef } from "react";
import { Mic, MicOff, Loader2, Volume2 } from "lucide-react";

interface VoiceRecorderProps {
  onTranscription: (text: string, response: string, audioUrl?: string) => void;
}

export const VoiceRecorder: React.FC<VoiceRecorderProps> = ({ onTranscription }) => {
  const [recording, setRecording] = useState(false);
  const [processing, setProcessing] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: "audio/webm" });
        await sendVoiceToBackend(audioBlob);
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorder.start();
      setRecording(true);
    } catch (err) {
      console.error("Microphone access error:", err);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && recording) {
      mediaRecorderRef.current.stop();
      setRecording(false);
      setProcessing(true);
    }
  };

  const sendVoiceToBackend = async (blob: Blob) => {
    const formData = new FormData();
    formData.append("file", blob, "user_voice.webm");

    try {
      const res = await fetch("http://localhost:8000/api/v1/voice/chat", {
        method: "POST",
        body: formData,
      });

      if (res.ok) {
        const data = await res.json();
        onTranscription(data.transcription, data.response, data.audio_url);
        if (data.audio_url) {
          const audio = new Audio(`http://localhost:8000${data.audio_url}`);
          audio.play();
        }
      }
    } catch (err) {
      console.error("Voice chat error:", err);
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className="flex items-center">
      {processing ? (
        <button disabled className="p-2.5 rounded-full bg-slate-800 text-indigo-400">
          <Loader2 className="w-5 h-5 animate-spin" />
        </button>
      ) : recording ? (
        <button
          onClick={stopRecording}
          className="p-2.5 rounded-full bg-rose-600 hover:bg-rose-500 text-white animate-pulse shadow-lg shadow-rose-500/30"
          title="Stop Recording"
        >
          <MicOff className="w-5 h-5" />
        </button>
      ) : (
        <button
          onClick={startRecording}
          className="p-2.5 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition-colors"
          title="Hold/Click to Speak"
        >
          <Mic className="w-5 h-5" />
        </button>
      )}
    </div>
  );
};
