
MEDICINE_INFO = {
    "paracetamol": {
        "description": "Obat untuk meredakan nyeri dan demam.",
        "warning": "Perhatikan dosis dan hindari penggunaan berlebihan karena dapat merusak hati."
    },
    "ibuprofen": {
        "description": "Obat antiinflamasi nonsteroid untuk nyeri dan peradangan.",
        "warning": "Perlu kehati-hatian pada penderita gangguan lambung, ginjal, atau kondisi tertentu."
    },
    "amoxicillin": {
        "description": "Antibiotik golongan penisilin.",
        "warning": "Gunakan hanya berdasarkan resep tenaga medis. Perhatikan riwayat alergi penisilin."
    },
    "cetirizine": {
        "description": "Antihistamin untuk membantu meredakan gejala alergi.",
        "warning": "Dapat menyebabkan kantuk pada sebagian orang."
    },
    "omeprazole": {
        "description": "Obat untuk mengurangi produksi asam lambung.",
        "warning": "Gunakan sesuai petunjuk tenaga medis."
    }
}


def analyze_medicines(medicines, allergies="", conditions=""):

    # Mendukung input berupa list maupun string
    if isinstance(medicines, str):
        medicine_list = [
            item.strip().lower()
            for item in medicines.split(",")
            if item.strip()
        ]

    elif isinstance(medicines, list):
        medicine_list = [
            str(item).strip().lower()
            for item in medicines
            if str(item).strip()
        ]

    else:
        medicine_list = []

    if not medicine_list:
        raise ValueError("Masukkan minimal satu nama obat.")

    allergy_text = str(allergies or "").strip().lower()
    condition_text = str(conditions or "").strip().lower()

    results = []
    warnings = []

    for medicine in medicine_list:

        info = MEDICINE_INFO.get(medicine)

        if info:
            results.append({
                "medicine": medicine,
                "description": info["description"],
                "warning": info["warning"]
            })
            warnings.append(f"{medicine}: {info['warning']}")

            if medicine == "amoxicillin" and any(
                word in allergy_text
                for word in ["penicillin", "penisilin", "amoxicillin"]
            ):
                warnings.append(
                    "PERINGATAN: Riwayat alergi yang disebutkan mungkin "
                    "berkaitan dengan amoxicillin. Jangan gunakan sebelum "
                    "berkonsultasi dengan tenaga medis."
                )

        else:
            results.append({
                "medicine": medicine,
                "description": "Informasi obat belum tersedia dalam database.",
                "warning": "Tidak dapat dilakukan analisis untuk obat ini."
            })
            warnings.append(
                f"Informasi {medicine} belum tersedia."
            )

    return {
        "results": results,
        "warnings": warnings,
        "interaction_note": (
            "Pemeriksaan interaksi antarobat belum tersedia. "
            "Jangan menganggap kombinasi obat aman berdasarkan hasil ini."
        ),
        "disclaimer": (
            "Informasi ini bersifat edukasi dan bukan pengganti "
            "konsultasi dokter atau apoteker."
        )
    }
