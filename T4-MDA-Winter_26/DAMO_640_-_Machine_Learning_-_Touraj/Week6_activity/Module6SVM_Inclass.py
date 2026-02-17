# ===============================================================
# In-Class Assignment: Predicting Diabetes using Support Vector Machines
# ===============================================================

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.svm import SVC, SVR
from sklearn import datasets
import pandas as pd

# === Step 1: Load Dataset ===

df = pd.read_csv("diabetes.csv")


print("Dataset Loaded ✅")
print(df.head())

# === Step 2: Prepare Data ===
X = df.drop(columns=["Outcome"])
y = df["Outcome"]

# Split into train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# === Step 3: Feature Scaling ===
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# === Step 4: Train Linear SVM ===
print("\nTraining Linear SVM...")
linear_svm = SVC(kernel="linear", C=1.0)
linear_svm.fit(X_train_scaled, y_train)
y_pred_linear = linear_svm.predict(X_test_scaled)

print("\n--- Linear SVM Results ---")
print("Accuracy:", accuracy_score(y_test, y_pred_linear))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_linear))
print(classification_report(y_test, y_pred_linear))

# === Step 5: Train RBF SVM ===
print("\nTraining RBF Kernel SVM...")
rbf_svm = SVC(kernel="rbf", C=1.0, gamma="scale")
rbf_svm.fit(X_train_scaled, y_train)
y_pred_rbf = rbf_svm.predict(X_test_scaled)

print("\n--- RBF SVM Results ---")
print("Accuracy:", accuracy_score(y_test, y_pred_rbf))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_rbf))
print(classification_report(y_test, y_pred_rbf))

print("\nOptional: Running Support Vector Regression Example...")
X_r, y_r = datasets.load_diabetes(return_X_y=True)
X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_r, y_r, test_size=0.3, random_state=42)

scaler_r = StandardScaler()
X_train_r = scaler_r.fit_transform(X_train_r)
X_test_r = scaler_r.transform(X_test_r)

svr_model = SVR(kernel="rbf", C=1.0, epsilon=0.2)
svr_model.fit(X_train_r, y_train_r)
y_pred_r = svr_model.predict(X_test_r)

from sklearn.metrics import mean_squared_error, r2_score
print("SVR MSE:", mean_squared_error(y_test_r, y_pred_r))
print("SVR R²:", r2_score(y_test_r, y_pred_r))
