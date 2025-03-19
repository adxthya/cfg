"use client";

import { useSearchParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

const getFetalHealthStatus = (baseline) => {
  if (baseline < 100) return "Normal";
  if (baseline >= 100 && baseline <= 200) return "Suspect";
  return "Pathological";
};

const getStatusColor = (status) => {
  switch (status) {
    case "Normal":
      return "text-green-700 bg-green-100";
    case "Suspect":
      return "text-orange-700 bg-orange-100";
    case "Pathological":
      return "text-red-700 bg-red-100";
    default:
      return "text-gray-700 bg-gray-100";
  }
};

export default function ResultsClient() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [baselineValue, setBaselineValue] = useState(null);

  useEffect(() => {
    const baseline = parseFloat(searchParams.get("baseline") || "0");
    setBaselineValue(baseline);
  }, [searchParams]);

  if (baselineValue === null) {
    return <p className="text-center text-gray-600">Loading...</p>;
  }

  const fetalHealth = getFetalHealthStatus(baselineValue);

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#e5c6e4] p-6">
      <div className="max-w-2xl w-full p-6 bg-white rounded-lg shadow-lg">
        <h2 className="text-2xl font-semibold text-center text-[#a14c9c] mb-4">
          Fetal Health Analysis Results
        </h2>

        <div className="bg-gray-100 p-4 rounded-md">
          <h3 className="text-lg font-medium text-[#7b387a] text-center">
            Analysis Complete
          </h3>
          <p className="text-gray-700 text-center">
            Data Source: Manual Data Entry
          </p>
        </div>

        <div className="mt-6 text-center">
          <h4 className="text-lg font-medium text-gray-800">
            Fetal Health Status:
          </h4>
          <div
            className={`inline-block px-6 py-2 mt-2 rounded-md text-lg font-semibold ${getStatusColor(
              fetalHealth
            )}`}
          >
            {fetalHealth}
          </div>
        </div>

        <div className="mt-4 text-center text-gray-700">
          <p className="mt-2">
            This analysis is based on the CTG data provided. Please consult with
            a medical professional for clinical interpretation.
          </p>
        </div>

        <div className="flex justify-between mt-6">
          <button
            className="px-4 py-2 bg-[#a14c9c] hover:bg-[#7b387a] rounded text-white transition"
            onClick={() => router.back()}
          >
            Back
          </button>
          <button
            className="px-4 py-2 bg-[#a14c9c] hover:bg-[#7b387a] rounded text-white transition"
            onClick={() => router.push("/")}
          >
            Home
          </button>
        </div>
      </div>
    </div>
  );
}
