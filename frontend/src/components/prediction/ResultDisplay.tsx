"use client";

import React from "react";
import {
  ChartBarIcon,
  ExclamationTriangleIcon,
} from "@heroicons/react/24/outline";
import "../styles/glass.css";

interface Prediction {
  disease: string;
  confidence: number;
  symptoms: string[];
  recommendations: string[];
}

interface ResultDisplayProps {
  prediction: Prediction | null;
  isLoading: boolean;
}

const ResultDisplay: React.FC<ResultDisplayProps> = ({
  prediction,
  isLoading,
}) => {
  if (isLoading) {
    return (
      <div className="glass-container p-6 max-w-2xl mx-auto">
        <div className="flex justify-center items-center h-32">
          <div className="glass-pulse w-8 h-8 rounded-full bg-gradient-to-r from-blue-400 to-blue-600 animate-spin" />
        </div>
      </div>
    );
  }

  if (!prediction) {
    return null;
  }

  return (
    <div className="glass-container p-6 max-w-2xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold text-gray-800">Hasil Analisis</h2>
        <div className="flex items-center space-x-2">
          <ChartBarIcon className="h-6 w-6 text-blue-500" />
          <span className="text-sm font-medium text-gray-600">
            {Math.round(prediction.confidence * 100)}% Akurasi
          </span>
        </div>
      </div>

      <div className="glass-card">
        <h3 className="text-xl font-medium text-gray-800 mb-2">
          Kemungkinan Penyakit
        </h3>
        <p className="text-2xl font-bold text-blue-600">{prediction.disease}</p>
      </div>

      <div className="glass-card">
        <h3 className="text-xl font-medium text-gray-800 mb-2">
          Gejala yang Terdeteksi
        </h3>
        <ul className="space-y-2">
          {prediction.symptoms.map((symptom, index) => (
            <li key={index} className="flex items-center space-x-2">
              <div className="w-2 h-2 rounded-full bg-blue-500" />
              <span className="text-gray-700">{symptom}</span>
            </li>
          ))}
        </ul>
      </div>

      <div className="glass-card">
        <h3 className="text-xl font-medium text-gray-800 mb-2">Rekomendasi</h3>
        <ul className="space-y-2">
          {prediction.recommendations.map((recommendation, index) => (
            <li key={index} className="flex items-start space-x-2">
              <ExclamationTriangleIcon className="h-5 w-5 text-yellow-500 mt-1" />
              <span className="text-gray-700">{recommendation}</span>
            </li>
          ))}
        </ul>
      </div>

      <div className="text-sm text-gray-500 italic">
        * Hasil ini hanya perkiraan. Silakan konsultasikan dengan dokter untuk
        diagnosis yang akurat.
      </div>
    </div>
  );
};

export default ResultDisplay;
