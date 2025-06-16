"use client";

import { useState, useRef, useEffect } from "react";
import { MicrophoneIcon, StopIcon } from "@heroicons/react/24/solid";

interface SymptomInputProps {
  onSubmit: (text: string) => void;
  isLoading: boolean;
}

export default function SymptomInput({
  onSubmit,
  isLoading,
}: SymptomInputProps) {
  const [text, setText] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [isSupported, setIsSupported] = useState(true);
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    // Check if browser supports speech recognition
    if (typeof window !== "undefined") {
      const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;
      if (SpeechRecognition) {
        recognitionRef.current = new SpeechRecognition();
        recognitionRef.current.continuous = true;
        recognitionRef.current.interimResults = true;
        recognitionRef.current.lang = "id-ID";

        recognitionRef.current.onresult = (event: any) => {
          const transcript = Array.from(event.results)
            .map((result: any) => result[0].transcript)
            .join("");
          setText(transcript);
        };

        recognitionRef.current.onerror = (event: any) => {
          console.error("Speech recognition error:", event.error);
          setIsRecording(false);
        };
      } else {
        setIsSupported(false);
      }
    }
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (text.trim()) {
      onSubmit(text.trim());
    }
  };

  const toggleRecording = () => {
    if (!recognitionRef.current) return;

    if (isRecording) {
      recognitionRef.current.stop();
    } else {
      recognitionRef.current.start();
    }
    setIsRecording(!isRecording);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="relative">
        <textarea
          rows={4}
          className="block w-full rounded-md border-0 py-1.5 text-gray-900 dark:text-gray-100 shadow-sm ring-1 ring-inset ring-gray-300 dark:ring-gray-700 placeholder:text-gray-400 dark:placeholder:text-gray-500 focus:ring-2 focus:ring-inset focus:ring-indigo-600 dark:focus:ring-indigo-500 sm:text-sm sm:leading-6 bg-white dark:bg-gray-900"
          placeholder="Jelaskan gejala yang Anda alami..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          disabled={isLoading}
        />
        {isSupported && (
          <button
            type="button"
            onClick={toggleRecording}
            className="absolute bottom-2 right-2 p-2 rounded-full text-gray-400 hover:text-gray-500 dark:hover:text-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            disabled={isLoading}
          >
            {isRecording ? (
              <StopIcon className="h-5 w-5 text-red-500" />
            ) : (
              <MicrophoneIcon className="h-5 w-5" />
            )}
          </button>
        )}
      </div>

      {!isSupported && (
        <p className="text-sm text-red-600 dark:text-red-400">
          Browser Anda tidak mendukung pengenalan suara.
        </p>
      )}

      <div className="flex justify-end">
        <button
          type="submit"
          disabled={!text.trim() || isLoading}
          className="rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? "Memproses..." : "Analisis Gejala"}
        </button>
      </div>
    </form>
  );
}
