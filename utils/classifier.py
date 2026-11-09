
import os
import joblib

# Lokasi model
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "symptom_classifier.pkl"
)


def load_model():
    """Memuat model klasifikasi gejala."""

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            "Model belum ditemukan. "
            "Pastikan symptom_classifier.pkl "
            "sudah diunggah ke folder model."
        )

    return joblib.load(MODEL_PATH)


def predict_symptom(symptoms):
    """Memprediksi kategori berdasarkan teks gejala."""

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
