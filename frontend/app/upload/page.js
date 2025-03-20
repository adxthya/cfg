"use client";
import React, { useState } from "react";

function ImageUploadPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [error, setError] = useState(null);
  const [isUploaded, setIsUploaded] = useState(false);
  const [prediction, setPrediction] = useState(null);

  const handleFileSelect = (event) => {
    const file = event.target.files?.[0];
    setError(null);
    setIsUploaded(false);
    setPrediction(null);

    if (!file) return;

    if (!file.type.startsWith("image/")) {
      setError("Please select an image file");
      setSelectedFile(null);
      setPreview(null);
      return;
    }

    setSelectedFile(file);

    const reader = new FileReader();
    reader.onloadend = () => {
      setPreview(reader.result);
    };
    reader.readAsDataURL(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError("Please select a file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch("http://127.0.0.1:5000/predict/image", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Error uploading file");
      }

      const data = await response.json();
      setPrediction(data.prediction);
      setIsUploaded(true);
    } catch (error) {
      setError("Error uploading file. Please try again.");
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreview(null);
    setError(null);
    setIsUploaded(false);
    setPrediction(null);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-6">
      <div className="bg-white shadow-lg rounded-lg p-6 h-2/3 w-3/4">
        <h2 className="text-2xl font-semibold text-center text-purple-700 mb-4">
          Upload CTG Waveform Image
        </h2>

        <div className="flex flex-col items-center">
          {preview ? (
            <div className="w-fit h-64 border rounded-lg overflow-hidden shadow-md">
              <img
                src={preview}
                alt="Preview"
                className="w-full h-full object-cover"
              />
            </div>
          ) : (
            <label
              htmlFor="file-input"
              className="w-3/4 h-64 border-2 border-dashed border-purple-400 rounded-lg flex flex-col items-center justify-center cursor-pointer hover:bg-purple-50 transition p-4"
            >
              <p className="text-gray-500 text-sm">
                Click to select or drag an image here
              </p>
              <span className="text-3xl mt-2">📁</span>
            </label>
          )}

          <input
            type="file"
            id="file-input"
            accept="image/*"
            onChange={handleFileSelect}
            className="hidden"
          />
        </div>

        {error && (
          <div className="mt-4 text-red-500 text-sm text-center">{error}</div>
        )}

        <div className="mt-6 flex justify-center gap-4">
          <button
            className="px-4 py-2 bg-gray-400 text-white rounded-lg hover:bg-gray-500 transition"
            onClick={handleReset}
          >
            Reset
          </button>
          <button
            className={`px-4 py-2 rounded-lg text-white transition ${
              selectedFile && !isUploaded
                ? "bg-purple-600 hover:bg-purple-700"
                : "bg-gray-400 cursor-not-allowed"
            }`}
            onClick={handleUpload}
            disabled={!selectedFile || isUploaded}
          >
            {isUploaded ? "Uploaded" : "Upload"}
          </button>
        </div>

        {prediction && (
          <div className="mt-6 text-center bg-gray-100 p-4 rounded-lg shadow-md">
            <h3 className="text-lg font-medium text-purple-700">
              Prediction: {prediction}
            </h3>
          </div>
        )}
      </div>
    </div>
  );
}

export default ImageUploadPage;
