"use client";

import React, { useState } from "react";
import { MicrophoneIcon, PaperAirplaneIcon } from "@heroicons/react/24/solid";
import "../styles/glass.css";

interface SymptomInputProps {
  onSubmit: (symptoms: string) => void;
  onVoiceInput: () => void;
  isLoading?: boolean;
}

const SymptomInput: React.FC<SymptomInputProps> = ({
  onSubmit,
  onVoiceInput,
  isLoading = false,
}) => {
  const [symptoms, setSymptoms] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (symptoms.trim()) {
      onSubmit(symptoms.trim());
      setSymptoms("");
    }
  };

  return (
    <div className="glass-container p-6 max-w-2xl mx-auto">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="relative">
          <textarea
            className="glass-input w-full h-32 resize-none"
            value={symptoms}
            onChange={(e) => setSymptoms(e.target.value)}
            placeholder="Jelaskan gejala yang Anda alami..."
            disabled={isLoading}
          />
          <div className="absolute bottom-4 right-4 flex space-x-2">
            <button
              type="button"
              onClick={onVoiceInput}
              className="glass-button p-2 rounded-full"
              disabled={isLoading}
            >
              <MicrophoneIcon className="h-6 w-6 text-gray-600" />
            </button>
            <button
              type="submit"
              className="glass-button p-2 rounded-full"
              disabled={isLoading || !symptoms.trim()}
            >
              <PaperAirplaneIcon className="h-6 w-6 text-gray-600" />
            </button>
          </div>
        </div>
        {isLoading && (
          <div className="flex justify-center">
            <div className="glass-pulse w-8 h-8 rounded-full bg-gradient-to-r from-blue-400 to-blue-600 animate-spin" />
          </div>
        )}
      </form>
    </div>
  );
};

export default SymptomInput;
