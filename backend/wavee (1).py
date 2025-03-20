import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog

# File selection dialog
Tk().withdraw()  # Hide the root window
image_path = filedialog.askopenfilename(title="Select a CTG Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])

if not image_path:
    print("No file selected. Exiting...")
    exit()

print("Selected file:", image_path)

def preprocess_ctg_image(image_path):
    """Load and preprocess the CTG image."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Convert to grayscale
    img = cv2.GaussianBlur(img, (5, 5), 0)  # Reduce noise
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY_INV, 11, 2)  # Thresholding
    return img

# Preprocess the uploaded image
processed_image = preprocess_ctg_image(image_path)
print("CTG Image Preprocessed Successfully!")

# Load original grayscale image
original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Display images
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(original_image, cmap="gray")
plt.title("Original Grayscale CTG")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(processed_image, cmap="gray")
plt.title("Processed CTG Image")
plt.axis("off")

plt.show()

def extract_waveform(image):
    """Extract waveform values from the processed CTG image."""
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    waveform_points = [(point[0][0], point[0][1]) for contour in contours for point in contour]
    return sorted(waveform_points, key=lambda x: x[0])

waveform_data = extract_waveform(processed_image)
print(f"Extracted {len(waveform_data)} waveform points!")

def compute_ctg_features(waveform_points):
    """Compute the 22 CTG features from the extracted waveform."""
    y_values = np.array([point[1] for point in waveform_points])
    features = {
        "Baseline Value (SisPorto)": np.mean(y_values),
        "Accelerations (SisPorto)": np.count_nonzero(np.diff(y_values) > 5),
        "Foetal Movement (SisPorto)": np.count_nonzero(np.diff(y_values) > 10),
        "Uterine Contractions (SisPorto)": np.count_nonzero(np.diff(y_values) < -10),
        "Abnormal Short-Term Variability (%)": np.var(y_values[:50]),
        "Mean Short-Term Variability": np.std(y_values[:50]),
        "Abnormal Long-Term Variability (%)": np.var(y_values[50:]),
        "Mean Long-Term Variability": np.std(y_values[50:]),
        "Light Decelerations": np.count_nonzero(y_values < np.percentile(y_values, 20)),
        "Severe Decelerations": np.count_nonzero(y_values < np.percentile(y_values, 10)),
        "Prolonged Decelerations": np.count_nonzero(y_values < np.percentile(y_values, 5)),
        "Repetitive Decelerations": np.count_nonzero(y_values < np.percentile(y_values, 3)),
        "Histogram Width": np.max(y_values) - np.min(y_values),
        "Low Freq. of Histogram": np.percentile(y_values, 5),
        "High Freq. of Histogram": np.percentile(y_values, 95),
        "Number of Histogram Peaks": len(np.unique(y_values)),
        "Number of Histogram Zeros": np.count_nonzero(y_values == 0),
        "Histogram Mode": np.argmax(np.bincount(y_values)),
        "Histogram Mean": np.mean(y_values),
        "Histogram Median": np.median(y_values),
        "Histogram Variance": np.var(y_values),
        "Histogram Tendency": 1 if np.mean(y_values) > np.median(y_values) else -1
    }
    return pd.DataFrame([features])
ctg_features_df = compute_ctg_features(waveform_data)
print("CTG Features Computed Successfully!")
pd.set_option("display.max_columns", None)  # Show all columns
# print(ctg_features_df)

print(ctg_features_df)
