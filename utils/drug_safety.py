
# ==========================================
# MEDICESS AI - DRUG SAFETY
# Referensi informasi obat sederhana
# ==========================================

DRUG_DATABASE = {
    "paracetamol": {
        "category": "Analgesik dan antipiretik",
        "information": "Digunakan untuk membantu meredakan nyeri dan demam.",
        "caution": (
            "Penggunaan berlebihan dapat menyebabkan kerusakan hati. "
            "Periksa kandungan obat lain agar tidak terjadi penggunaan "
            "paracetamol ganda."
        )
    },
    "ibuprofen": {
        "category": "Obat antiinflamasi nonsteroid (NSAID)",
        "information": "Digunakan untuk membantu meredakan nyeri dan peradangan.",
        "caution": (
            "Perlu perhatian khusus pada orang dengan riwayat tukak lambung, "
            "gangguan ginjal, alergi NSAID, atau kondisi kehamilan tertentu."
        )
    },
    "amoxicillin": {
        "category": "Antibiotik golongan penisilin",
        "information": "Antibiotik untuk infeksi bakteri tertentu berdasarkan resep.",
        "caution": (
            "Tidak digunakan untuk infeksi virus. Perhatikan riwayat alergi "
            "penisilin dan gunakan sesuai instruksi tenaga medis."
        )
    },
    "cetirizine": {
        "category": "Antihistamin",
        "information": "Digunakan untuk membantu meredakan gejala alergi.",
        "caution": (
            "Dapat menyebabkan kantuk pada sebagian orang. "
            "Perhatikan respons tubuh sebelum berkendara."
        )
    },
    "omeprazole": {
        "category": "Penghambat pompa proton (PPI)",
        "information": "Digunakan untuk mengurangi produksi asam lambung.",
        "caution": (
            "Penggunaan jangka panjang perlu dievaluasi oleh tenaga medis."
        )
    }
}


def analyze_medicines(medicines, allergies="", conditions=""):
    """
    Memberikan informasi dasar obat dari referensi lokal.
    Tidak melakukan pemeriksaan interaksi klinis.
    """

    if not medicines or not medicines.strip():
        return "Silakan masukkan nama obat terlebih dahulu."

    medicine_names = [
        item.strip().lower()
        for item in medicines.replace("\n", ",").split(",")
        if item.strip()
    ]

    results = []

    for name in medicine_names:
        drug = DRUG_DATABASE.get(name)

        if drug:
            results.append({
                "name": name.title(),
                "status": "Ditemukan dalam referensi lokal",
                "category": drug["category"],
                "information": drug["information"],
                "caution": drug["caution"]
            })
        else:
            results.append({
                "name": name.title(),
                "status": "Belum tersedia dalam referensi lokal",
                "category": "Tidak diketahui",
                "information": (
                    "Informasi obat ini belum tersedia dalam basis data "
                    "MediCess AI."
                ),
                "caution": (
                    "Jangan menyimpulkan keamanan atau kegunaan obat. "
                    "Verifikasi nama dan informasi obat kepada apoteker "
                    "atau dokter."
                )
            })

    warnings = []

    if allergies.strip():
        warnings.append(
            "PENGINGAT ALERGI: Anda menyebutkan riwayat alergi. "
            "Pastikan setiap obat diverifikasi oleh dokter atau apoteker "
            "sebelum digunakan."
        )

    if conditions.strip():
        warnings.append(
            "PENGINGAT KONDISI KESEHATAN: Kondisi kesehatan, kehamilan, "
            "dan penyakit penyerta dapat memengaruhi keamanan obat. "
            "Mintalah pemeriksaan tenaga medis."
        )

    return {
        "results": results,
        "warnings": warnings,
        "interaction_note": (
            "MediCess AI belum memiliki database interaksi obat yang "
            "tervalidasi. Hasil ini bukan pemeriksaan interaksi obat."
        ),
        "disclaimer": (
            "Informasi hanya untuk edukasi, bukan rekomendasi penggunaan "
            "obat atau pengganti konsultasi tenaga medis."
        )
    }
