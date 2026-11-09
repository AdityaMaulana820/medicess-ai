
# ==========================================
# MEDICESS AI - RECOVERY PLANNER
# Rekomendasi kebiasaan sehat umum
# ==========================================

def create_recovery_plan(condition, activity, sleep, goal):

    if not condition or not condition.strip():
        raise ValueError("Kondisi harus diisi.")

    # Rekomendasi aktivitas
    activity_recommendations = {
        "Rendah / banyak istirahat": (
            "Lakukan aktivitas ringan sesuai kemampuan. "
            "Jangan memaksakan aktivitas jika tubuh terasa lemah."
        ),
        "Sedang": (
            "Pertahankan aktivitas sehari-hari sesuai toleransi tubuh "
            "dan berikan waktu istirahat yang cukup."
        ),
        "Aktif": (
            "Atur keseimbangan aktivitas dan istirahat. "
            "Kurangi intensitas jika merasa tidak nyaman."
        )
    }

    # Rekomendasi tidur
    sleep_recommendations = {
        "Kurang dari 5 jam": (
            "Usahakan memperbaiki jadwal tidur secara bertahap. "
            "Orang dewasa umumnya membutuhkan setidaknya 7 jam tidur."
        ),
        "5–6 jam": (
            "Coba tingkatkan waktu tidur secara bertahap menuju "
            "setidaknya 7 jam jika memungkinkan."
        ),
        "7–8 jam": (
            "Pertahankan jadwal tidur yang teratur."
        ),
        "Lebih dari 8 jam": (
            "Perhatikan kualitas tidur dan bagaimana kondisi tubuh "
            "saat bangun. Tidur lebih lama tidak selalu berarti masalah."
        )
    }

    # Rekomendasi berdasarkan tujuan
    goal_recommendations = {
        "Pemulihan kondisi tubuh": (
            "Prioritaskan istirahat, asupan makanan seimbang, "
            "dan aktivitas sesuai kemampuan."
        ),
        "Meningkatkan kualitas tidur": (
            "Pertahankan waktu tidur dan bangun yang konsisten. "
            "Kurangi penggunaan layar menjelang tidur."
        ),
        "Menjaga pola makan": (
            "Konsumsi makanan beragam dan bergizi seimbang. "
            "Perhatikan kecukupan cairan."
        ),
        "Meningkatkan kebugaran": (
            "Mulai dari aktivitas ringan dan tingkatkan secara bertahap "
            "sesuai kemampuan dan kondisi kesehatan."
        ),
        "Menjaga kesehatan umum": (
            "Bangun kebiasaan tidur teratur, makan seimbang, "
            "aktivitas fisik, dan pengelolaan stres."
        )
    }

    return {
        "condition": condition.strip(),

        "activity": activity_recommendations.get(
            activity,
            "Sesuaikan aktivitas dengan kemampuan tubuh."
        ),

        "sleep": sleep_recommendations.get(
            sleep,
            "Usahakan menjaga jadwal tidur yang teratur."
        ),

        "nutrition": (
            "Pilih makanan beragam dan bergizi seimbang, "
            "serta cukupi kebutuhan cairan sesuai kondisi kesehatan."
        ),

        "goal": goal_recommendations.get(
            goal,
            "Pertahankan kebiasaan hidup sehat secara bertahap."
        ),

        "warning": (
            "Hentikan aktivitas dan cari pertolongan medis jika "
            "muncul sesak napas berat, nyeri dada berat, penurunan "
            "kesadaran, kejang, atau kondisi darurat lainnya."
        ),

        "disclaimer": (
            "Rencana ini merupakan edukasi kebiasaan sehat umum, "
            "bukan terapi atau pengganti saran dokter."
        )
    }
