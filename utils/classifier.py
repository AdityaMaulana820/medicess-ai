import os
import sys
import hashlib
import joblib
import sklearn
import numpy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "symptom_classifier.pkl"
)


def load_model():
    print("=== MODEL DI STREAMLIT ===")
    print("Python:", sys.version)
    print("Scikit-learn:", sklearn.__version__)
    print("Joblib:", joblib.__version__)
    print("NumPy:", numpy.__version__)

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("File model tidak ditemukan!")

    with open(MODEL_PATH, "rb") as f:
        data = f.read()

    print("Ukuran model:", len(data))
    print("SHA256:", hashlib.sha256(data).hexdigest())
    print("16 byte pertama:", data[:16])

    return joblib.load(MODEL_PATH)


def predict_symptom(symptoms):
    if not symptoms or not symptoms.strip():
        raise ValueError("Gejala tidak boleh kosong.")

    model = load_model()
    prediction = model.predict([symptoms.strip()])[0]

    return {
        "prediction": str(prediction),
        "input": symptoms.strip(),
        "disclaimer": (
            "Hasil ini merupakan klasifikasi pola teks "
            "berdasarkan dataset penelitian, bukan diagnosis medis."
        )
    }
