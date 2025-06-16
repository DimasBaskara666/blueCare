"use client";

interface Prediction {
  disease: string;
  confidence: number;
  symptoms: string[];
}

interface ResultDisplayProps {
  predictions: Prediction[];
}

export default function ResultDisplay({ predictions }: ResultDisplayProps) {
  return (
    <div className="bg-white dark:bg-gray-800 shadow sm:rounded-lg">
      <div className="px-4 py-5 sm:p-6">
        <h3 className="text-base font-semibold leading-6 text-gray-900 dark:text-gray-100">
          Hasil Analisis
        </h3>
        <div className="mt-4 space-y-4">
          {predictions.map((prediction, index) => (
            <div
              key={index}
              className="rounded-lg border border-gray-200 dark:border-gray-700 p-4"
            >
              <div className="flex items-center justify-between">
                <h4 className="text-lg font-medium text-gray-900 dark:text-gray-100">
                  {prediction.disease}
                </h4>
                <span className="inline-flex items-center rounded-md bg-blue-50 dark:bg-blue-900/50 px-2 py-1 text-xs font-medium text-blue-700 dark:text-blue-300">
                  {Math.round(prediction.confidence * 100)}% kemungkinan
                </span>
              </div>
              <div className="mt-2">
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  Gejala yang terdeteksi:
                </p>
                <ul className="mt-1 list-disc list-inside text-sm text-gray-600 dark:text-gray-300">
                  {prediction.symptoms.map((symptom, idx) => (
                    <li key={idx}>{symptom.replace("_", " ")}</li>
                  ))}
                </ul>
              </div>
              <div className="mt-4">
                <div className="relative pt-1">
                  <div className="overflow-hidden h-2 text-xs flex rounded bg-gray-200 dark:bg-gray-700">
                    <div
                      style={{ width: `${prediction.confidence * 100}%` }}
                      className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-indigo-500"
                    />
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
        <div className="mt-6">
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Catatan: Hasil ini hanya bersifat prediksi awal. Konsultasikan
            dengan profesional kesehatan untuk diagnosis yang akurat.
          </p>
        </div>
      </div>
    </div>
  );
}
