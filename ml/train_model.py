import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

import joblib


# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("dataset/irrigation_dataset.csv")

print("Dataset loaded successfully!")
print("Shape:", df.shape)


# ==========================================
# 2. FEATURES AND TARGET
# ==========================================

X = df[
    [
        "temperature",
        "humidity",
        "soil_moisture"
    ]
]

y = df["water_needed"]


# ==========================================
# 3. TRAIN-TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==========================================
# 4. CREATE MODELS
# ==========================================

models = {
    "Logistic Regression": LogisticRegression(
        max_iter=1000
    ),

    "Decision Tree": DecisionTreeClassifier(
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )
}


# ==========================================
# 5. TRAIN AND EVALUATE
# ==========================================

results = {}

print("\n==============================")
print("MODEL RESULTS")
print("==============================")

for name, model in models.items():

    # Train
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)

    # Accuracy
    accuracy = accuracy_score(y_test, y_pred)

    results[name] = accuracy

    print(f"\n{name}")
    print(f"Accuracy: {accuracy:.4f}")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            y_pred,
            target_names=[
                "No Water Needed",
                "Water Needed"
            ]
        )
    )


# ==========================================
# 6. FIND BEST MODEL
# ==========================================

best_model_name = max(
    results,
    key=results.get
)

best_model = models[best_model_name]

print("\n==============================")
print("BEST MODEL")
print("==============================")

print("Model:", best_model_name)
print(f"Accuracy: {results[best_model_name]:.4f}")


# ==========================================
# 7. SAVE BEST MODEL
# ==========================================

model_path = "irrigation_model.pkl"

joblib.dump(
    best_model,
    model_path
)

print("\nModel saved successfully!")
print("Saved as:", model_path)