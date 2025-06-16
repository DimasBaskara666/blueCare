"use client";

import { useState, useRef, useEffect } from "react";
import { PaperAirplaneIcon } from "@heroicons/react/24/solid";

interface Message {
  text: string;
  isUser: boolean;
  suggestions?: string[];
}

export default function Chatbot() {
  const [messages, setMessages] = useState<Message[]>([
    {
      text: "Halo! Saya asisten kesehatan Anda. Apa yang bisa saya bantu?",
      isUser: false,
      suggestions: [
        "Bagaimana cara mengatasi demam?",
        "Apa gejala COVID-19?",
        "Kapan harus ke dokter?",
      ],
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { text: userMessage, isUser: true }]);
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:5000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: userMessage,
          context: {
            medical_terms: extractMedicalTerms(messages),
          },
        }),
      });

      if (!response.ok) {
        throw new Error("Gagal mendapatkan respons");
      }

      const data = await response.json();
      setMessages((prev) => [
        ...prev,
        {
          text: data.response,
          isUser: false,
          suggestions: data.suggestions,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          text: "Maaf, terjadi kesalahan. Silakan coba lagi.",
          isUser: false,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInput(suggestion);
  };

  // Simple function to extract medical terms from conversation
  const extractMedicalTerms = (messages: Message[]): string[] => {
    const terms = new Set<string>();
    const medicalTerms = [
      "demam",
      "batuk",
      "pilek",
      "sakit kepala",
      "mual",
      "muntah",
      "diare",
      "sesak nafas",
    ];

    messages.forEach((message) => {
      if (message.isUser) {
        const text = message.text.toLowerCase();
        medicalTerms.forEach((term) => {
          if (text.includes(term)) {
            terms.add(term);
          }
        });
      }
    });

    return Array.from(terms);
  };

  return (
    <div className="flex flex-col h-[600px]">
      <div className="flex-1 overflow-y-auto space-y-4 p-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${
              message.isUser ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-[80%] rounded-lg px-4 py-2 ${
                message.isUser
                  ? "bg-indigo-600 text-white"
                  : "bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100"
              }`}
            >
              <p className="whitespace-pre-wrap">{message.text}</p>
              {message.suggestions && message.suggestions.length > 0 && (
                <div className="mt-2 space-y-1">
                  {message.suggestions.map((suggestion, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleSuggestionClick(suggestion)}
                      className="block w-full text-left text-sm text-indigo-600 dark:text-indigo-400 hover:text-indigo-500 dark:hover:text-indigo-300"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <form
        onSubmit={handleSubmit}
        className="p-4 border-t border-gray-200 dark:border-gray-700"
      >
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ketik pesan Anda..."
            className="flex-1 rounded-md border-0 py-1.5 text-gray-900 dark:text-gray-100 shadow-sm ring-1 ring-inset ring-gray-300 dark:ring-gray-700 placeholder:text-gray-400 dark:placeholder:text-gray-500 focus:ring-2 focus:ring-inset focus:ring-indigo-600 dark:focus:ring-indigo-500 sm:text-sm sm:leading-6 bg-white dark:bg-gray-900"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <PaperAirplaneIcon className="h-5 w-5" />
          </button>
        </div>
      </form>
    </div>
  );
}
