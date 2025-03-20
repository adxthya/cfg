import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.neural_network import MLPClassifier
import joblib
import numpy as np
import xgboost as xgb

# Load dataset
df = pd.read_excel(r'"C:\Users\user\Desktop\Anly\ctg-management-app\CTG.xls"', header=0, sheet_name=2, skipfooter=3)
df.dropna(axis=0, thresh=10, inplace=True)
df.drop(columns=['FileName', 'Date', 'SegFile', 'A', 'B', 'C', 'D', 'E', 'AD', 'DE', 'LD', 'FS', 'SUSP', 'CLASS', 'DR'], inplace=True)
df.columns = df.columns.str.strip()
df = df.drop(columns=['FileName', 'Date', 'b', 'e'], errors='ignore')

# Features and Target
X = df.drop(columns=['NSP'])
y = df['NSP']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Label Encoding
le = LabelEncoder()
y_train = le.fit_transform(y_train)
y_test = le.transform(y_test)

# Feature Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define models
models = {
    "Logistic Regression": LogisticRegression(),
    "KNN": KNeighborsClassifier(),
    "Random Forest": RandomForestClassifier(),
    "Gradient Boosting": GradientBoostingClassifier(),
    "SVM": SVC(),
    "Decision Tree": DecisionTreeClassifier(),
    "Extra Trees": ExtraTreesClassifier(),
    "XGBoost": XGBClassifier(),
    "LightGBM": LGBMClassifier(),
    "Naive Bayes": GaussianNB(),
    "MLP (Neural Network)": MLPClassifier(hidden_layer_sizes=(100,), max_iter=500)
}

# Train and Evaluate models
accuracy_scores = {}
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    accuracy_scores[name] = accuracy_score(y_test, y_pred)
    
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Normal", "Suspect", "Pathological"], yticklabels=["Normal", "Suspect", "Pathological"])
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title(f"Confusion Matrix - {name}")
    plt.show()

# Get the best-performing model
best_model_name = max(accuracy_scores, key=accuracy_scores.get)
final_model = models[best_model_name]

# Save scaler
joblib.dump(scaler, "scaler.pkl")

# ✅ Fix for XGBoost Saving Issue
if best_model_name == "XGBoost":
    final_model.get_booster().save_model("fetal_health_model.json")  # Save XGBoost model in correct format
else:
    joblib.dump(final_model, "fetal_health_model.pkl")  # Save other models normally

# ✅ Load model correctly
scaler = joblib.load("scaler.pkl")

if best_model_name == "XGBoost":
    model = xgb.Booster()
    model.load_model("fetal_health_model.json")
else:
    model = joblib.load("fetal_health_model.pkl")

def predict_fetal_health(features):
    features = np.array(features).reshape(1, -1)
    features_scaled = scaler.transform(features)
    
    if best_model_name == "XGBoost":
        dmatrix = xgb.DMatrix(features_scaled)  # Convert to DMatrix for XGBoost
        prediction = model.predict(dmatrix)
        prediction = np.round(prediction).astype(int)  # Convert probabilities to class labels
    else:
        prediction = model.predict(features_scaled)
    
    return {0: "Normal", 1: "Suspect", 2: "Pathological"}.get(prediction[0], "Unknown")

# Example Usage
sample_input = [120, 0.002, 0.000, 0.004, 0.000, 0.000, 0.000, 54, 0.5, 50, 0.003, 0.008, 0.003, 0.000, 0.000, 0.000, 61, 0.5, 38, 0, 1.5, 0]
result = predict_fetal_health(sample_input)
print(f"Predicted Fetal Health: {result}")
