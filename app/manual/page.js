"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

function ManualEntryPage() {
  const router = useRouter();

  const ctgFields = [
    "Baseline value (SisPorto)",
    "Accelerations (SisPorto)",
    "Fetal movement (SisPorto)",
    "Uterine contractions (SisPorto)",
    "Percentage of time with abnormal short-term variability (SisPorto)",
    "Mean value of short-term variability (SisPorto)",
    "Percentage of time with abnormal long-term variability (SisPorto)",
    "Mean value of long-term variability (SisPorto)",
    "Light decelerations",
    "Severe decelerations",
    "Prolonged decelerations",
    "Repetitive decelerations",
    "Histogram width",
    "Low frequency of the histogram",
    "High frequency of the histogram",
    "Number of histogram peaks",
    "Number of histogram zeros",
    "Histogram mode",
    "Histogram mean",
    "Histogram median",
    "Histogram variance",
    "Histogram tendency (-1=left asymmetric; 0=symmetric; 1=right asymmetric)",
  ];

  const initialFormState = ctgFields.reduce(
    (acc, field) => ({ ...acc, [field]: "" }),
    {}
  );

  const [formData, setFormData] = useState(initialFormState);

  const handleInputChange = (field, value) => {
    setFormData({ ...formData, [field]: value });
  };

  const handleSubmit = () => {
    const baselineValue =
      parseFloat(formData["Baseline value (SisPorto)"]) || 0;
    router.push(`/results?baseline=${baselineValue}`);
  };

  // Check if all fields are filled
  const isFormComplete = Object.values(formData).every(
    (value) => value.trim() !== ""
  );

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#e5c6e4] p-6">
      <div className="max-w-2xl w-full p-6 bg-white rounded-lg shadow-lg">
        <h2 className="text-2xl font-semibold text-center text-[#a14c9c] mb-4">
          Manual CTG Data Entry
        </h2>

        <form className="space-y-4">
          {ctgFields.map((field, index) => (
            <div
              key={index}
              className="flex flex-col"
            >
              <label
                htmlFor={`field-${index}`}
                className="text-sm font-medium text-[#7b387a]"
              >
                {field}
              </label>
              <input
                id={`field-${index}`}
                type="number"
                step="any"
                value={formData[field]}
                onChange={(e) => handleInputChange(field, e.target.value)}
                className="mt-1 p-2 border border-[#a14c9c] rounded bg-white focus:outline-none focus:ring focus:ring-[#a14c9c] text-gray-800"
                placeholder={`Enter ${field}`}
              />
            </div>
          ))}

          <div className="flex justify-between mt-6">
            <button
              type="button"
              className="px-4 py-2 bg-[#a14c9c] hover:bg-[#7b387a] rounded text-white transition"
              onClick={() => setFormData(initialFormState)}
            >
              Reset
            </button>
            <button
              type="button"
              className={`px-4 py-2 rounded text-white transition ${
                isFormComplete
                  ? "bg-[#a14c9c] hover:bg-[#7b387a]"
                  : "bg-gray-400 cursor-not-allowed"
              }`}
              onClick={handleSubmit}
              disabled={!isFormComplete}
            >
              Submit
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default ManualEntryPage;
