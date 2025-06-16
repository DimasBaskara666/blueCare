"use client";

import { useState } from "react";
import SymptomInput from "@/components/prediction/SymptomInput";
import Chatbot from "@/components/chatbot/Chatbot";
import ResultDisplay from "@/components/prediction/ResultDisplay";

export default function Home() {
  const [predictions, setPredictions] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (text: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch("http://localhost:5000/api/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error("Gagal mendapatkan prediksi");
      }

      const data = await response.json();
      setPredictions(data.predictions);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Terjadi kesalahan");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="space-y-6">
        <div className="bg-white dark:bg-gray-800 shadow sm:rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h2 className="text-lg font-medium text-gray-900 dark:text-gray-100">
              Masukkan Gejala
            </h2>
            <div className="mt-2 max-w-xl text-sm text-gray-500 dark:text-gray-400">
              <p>
                Jelaskan gejala yang Anda alami dalam Bahasa Indonesia. Anda
                dapat menggunakan input teks atau suara.
              </p>
            </div>
            <div className="mt-5">
              <SymptomInput onSubmit={handleSubmit} isLoading={isLoading} />
            </div>
          </div>
        </div>

        {error && (
          <div className="rounded-md bg-red-50 dark:bg-red-900/50 p-4">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800 dark:text-red-200">
                  Error
                </h3>
                <div className="mt-2 text-sm text-red-700 dark:text-red-300">
                  <p>{error}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {predictions.length > 0 && <ResultDisplay predictions={predictions} />}
      </div>

      <div className="bg-white dark:bg-gray-800 shadow sm:rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h2 className="text-lg font-medium text-gray-900 dark:text-gray-100">
            Asisten Kesehatan
          </h2>
          <div className="mt-2 max-w-xl text-sm text-gray-500 dark:text-gray-400">
            <p>
              Tanyakan apapun tentang kesehatan Anda. Asisten akan membantu
              memberikan informasi dan saran.
            </p>
          </div>
          <div className="mt-5">
            <Chatbot />
          </div>
        </div>
      </div>
    </div>
  );
}
