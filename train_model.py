
import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

# ==========================================
# 1. MEMBACA DATASET
# ==========================================

DATA_PATH = "data/Symptom2Disease.csv"

df = pd.read_csv(DATA_PATH)

# Membersihkan nama kolom
df.columns = df.columns.str.strip().str.lower()

if not {"text", "label"}.issubset(df.columns):
    raise ValueError(
        f"Kolom text dan label tidak ditemukan. "
        f"Kolom tersedia: {df.columns.tolist()}"
    )

df = df[["text", "label"]].dropna()
df["text"] = df["text"].astype(str).str.strip()
df["label"] = df["label"].astype(str).str.strip()
df = df[(df["text"] != "") & (df["label"] != "")]

print("Jumlah data:", len(df))
print("Jumlah kategori:", df["label"].nunique())

# ==========================================
# 2. MEMBAGI DATA
# ==========================================

X = df["text"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ==========================================
# 3. MODEL YANG DIBANDINGKAN
# ==========================================

models = {
    "Naive Bayes": MultinomialNB(),

    "SVM": LinearSVC(
        class_weight="balanced",
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )
}

results = []
best_model = None
best_score = -1
best_name = ""

# ==========================================
# 4. TRAINING DAN EVALUASI
# ==========================================

for name, classifier in models.items():

    print("\nMelatih:", name)

    pipeline = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                ngram_range=(1, 2),
                max_features=20000,
                sublinear_tf=True
            )
        ),
        ("classifier", classifier)
    ])

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    precision = precision_score(
        y_test,
        predictions,
        average="macro",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        average="macro",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        average="macro",
        zero_division=0
    )

    results.append({
        "Model": name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "Macro F1": f1
    })

    print("Accuracy:", round(accuracy, 4))
    print("Precision:", round(precision, 4))
    print("Recall:", round(recall, 4))
    print("Macro F1:", round(f1, 4))

    if f1 > best_score:
        best_score = f1
        best_model = pipeline
        best_name = name
        best_predictions = predictions

# ==========================================
# 5. HASIL PERBANDINGAN
# ==========================================

results_df = pd.DataFrame(results)

print("\nHASIL PERBANDINGAN MODEL")
print(results_df.to_string(index=False))

print("\nMODEL TERBAIK:", best_name)

print("\nCLASSIFICATION REPORT")
print(classification_report(
    y_test,
    best_predictions,
    zero_division=0
))

# ==========================================
# 6. SIMPAN MODEL
# ==========================================

os.makedirs("model", exist_ok=True)

joblib.dump(
    best_model,
    "model/symptom_classifier.pkl"
)

print("\nModel berhasil disimpan!")
print("Lokasi: model/symptom_classifier.pkl")
