
import streamlit as st
from datetime import datetime

from utils.classifier import predict_symptom
from utils.drug_safety import analyze_medicines
from utils.recovery import create_recovery_plan


# ==========================================
# KONFIGURASI APLIKASI
# ==========================================

st.set_page_config(
    page_title="MediCess AI",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 MediCess AI")
st.caption("Asisten edukasi kesehatan berbasis Machine Learning")


# ==========================================
# SESSION STATE
# ==========================================

if "history" not in st.session_state:
    st.session_state.history = []

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# ==========================================
# FUNGSI BANTUAN
# ==========================================

def save_history(feature, prompt, response):
    st.session_state.history.insert(
        0,
        {
            "feature": feature,
            "time": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "prompt": prompt,
            "response": str(response)
        }
    )


def show_disclaimer():
    st.info(
        "MediCess AI merupakan aplikasi edukasi dan eksperimen "
        "Machine Learning. Hasilnya bukan diagnosis, resep, atau "
        "pengganti konsultasi tenaga medis."
    )


def show_error(error):
    st.error(
        f"Terjadi kesalahan: {type(error).__name__}: {error}"
    )
    with st.expander("Lihat detail error untuk perbaikan"):
        st.exception(error)


# ==========================================
# SIDEBAR NAVIGASI
# ==========================================

with st.sidebar:

    st.title("🩺 MediCess AI")
    st.caption("Health Education Assistant")

    selected_page = st.radio(
        "Menu Navigasi",
        [
            "Dashboard",
            "Medical Triage",
            "Drug Safety",
            "Recovery Planner",
            "History",
            "About"
        ],
        key="page"
    )

    st.divider()
    st.caption("MediCess AI v2.0")
    st.caption("Powered by Machine Learning")


# ==========================================
# DASHBOARD
# ==========================================

if selected_page == "Dashboard":

    st.header("Dashboard")

    st.write(
        "Selamat datang di MediCess AI. "
        "Gunakan fitur berikut untuk mendapatkan informasi "
        "dan edukasi kesehatan umum."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Medical Triage", "ML")
        st.caption("Klasifikasi teks gejala")

    with col2:
        st.metric("Drug Safety", "Local")
        st.caption("Informasi dasar obat")

    with col3:
        st.metric("Recovery Planner", "Guide")
        st.caption("Panduan kebiasaan sehat")

    st.divider()

    st.subheader("Fitur Aplikasi")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 🔎 Medical Triage")

        st.write(
            "Mengklasifikasikan deskripsi gejala berdasarkan "
            "pola teks dari dataset menggunakan Machine Learning."
        )

        st.markdown("### 💊 Drug Safety")

        st.write(
            "Memberikan informasi dasar mengenai beberapa obat "
            "dan catatan kehati-hatian."
        )

    with col2:

        st.markdown("### 🌱 Recovery Planner")

        st.write(
            "Menyusun rekomendasi kebiasaan sehat berdasarkan "
            "aktivitas, tidur, dan tujuan pengguna."
        )

        st.markdown("### 📋 History")

        st.write(
            "Melihat riwayat penggunaan fitur selama sesi aplikasi."
        )

    st.divider()

    st.subheader("Penting untuk Diketahui")

    st.warning(
        "Jika mengalami nyeri dada berat, sesak napas berat, "
        "kejang, penurunan kesadaran, atau kondisi darurat lainnya, "
        "segera cari pertolongan medis."
    )

    show_disclaimer()


# ==========================================
# MEDICAL TRIAGE
# ==========================================

elif selected_page == "Medical Triage":

    st.header("🔎 Medical Triage")

    st.write(
        "Masukkan deskripsi gejala untuk mendapatkan hasil "
        "klasifikasi berdasarkan model Machine Learning."
    )

    st.info(
        "Dataset model menggunakan bahasa Inggris. "
        "Untuk eksperimen ini, masukkan deskripsi gejala "
        "dalam bahasa Inggris."
    )

    with st.form("triage_form"):

        symptoms = st.text_area(
            "Deskripsi Gejala",
            placeholder=(
                "Example: I have a headache, fever, "
                "and feel tired."
            ),
            height=150
        )

        col1, col2 = st.columns(2)

        with col1:

            duration = st.text_input(
                "Sudah berapa lama mengalami gejala?",
                placeholder="Contoh: 2 hari"
            )

        with col2:

            age = st.number_input(
                "Usia",
                min_value=1,
                max_value=120,
                value=20
            )

        submitted = st.form_submit_button(
            "Analisis Gejala",
            use_container_width=True
        )

    if submitted:

        if not symptoms.strip():

            st.error(
                "Silakan masukkan deskripsi gejala terlebih dahulu."
            )

        else:

            try:

                with st.spinner(
                    "Model sedang menganalisis teks..."
                ):

                    result = predict_symptom(symptoms)

                prediction = result["prediction"]

                st.success(
                    "Klasifikasi berhasil dilakukan."
                )

                st.subheader("Hasil Klasifikasi")

                st.info(
                    f"Kategori yang diprediksi: **{prediction}**"
                )

                st.caption(
                    f"Usia: {age} tahun | Durasi gejala: "
                    f"{duration if duration else 'Tidak disebutkan'}"
                )

                st.warning(
                    "Hasil ini hanya prediksi kategori berdasarkan "
                    "pola teks dataset. Hasil bukan diagnosis medis "
                    "dan tidak menentukan tingkat kegawatan penyakit."
                )

                save_history(
                    "Medical Triage",
                    symptoms,
                    f"Prediksi kategori: {prediction}"
                )

            except FileNotFoundError as error:

                st.error(str(error))

                st.info(
                    "Pastikan file model tersedia di "
                    "folder model/symptom_classifier.pkl "
                    "pada repository."
                )

            except Exception as error:

                show_error(error)

    st.divider()

    show_disclaimer()


# ==========================================
# DRUG SAFETY
# ==========================================

elif selected_page == "Drug Safety":

    st.header("💊 Drug Safety")

    st.write(
        "Fitur ini memberikan informasi dasar untuk beberapa "
        "obat yang tersedia dalam referensi lokal aplikasi."
    )

    with st.form("drug_form"):

        medicines = st.text_area(
            "Nama Obat",
            placeholder=(
                "Contoh:\nParacetamol\nIbuprofen"
            ),
            height=120
        )

        allergies = st.text_input(
            "Riwayat Alergi",
            placeholder="Contoh: Alergi penisilin"
        )

        conditions = st.text_area(
            "Kondisi Kesehatan",
            placeholder="Contoh: Memiliki riwayat maag"
        )

        submitted = st.form_submit_button(
            "Periksa Informasi Obat",
            use_container_width=True
        )

    if submitted:

        if not medicines.strip():

            st.error("Masukkan minimal satu nama obat.")

        else:

            try:

                medicine_list = [
                    item.strip()
                    for item in medicines.replace(",", "\n").splitlines()
                    if item.strip()
                ]

                result = analyze_medicines(
                    medicine_list,
                    allergies,
                    conditions
                )

                st.subheader(
                    "Hasil Pemeriksaan Informasi"
                )

                for item in result.get("results", []):

                    if isinstance(item, dict):

                        st.markdown(
                            f"### {item.get('name', 'Informasi Obat')}"
                        )

                        for key, value in item.items():

                            if key != "name":

                                st.write(
                                    f"**{key.replace('_', ' ').title()}:** "
                                    f"{value}"
                                )

                    else:

                        st.write(item)

                for warning in result.get("warnings", []):

                    st.warning(warning)

                if result.get("interaction_note"):

                    st.info(result["interaction_note"])

                if result.get("disclaimer"):

                    st.caption(result["disclaimer"])

                save_history(
                    "Drug Safety",
                    ", ".join(medicine_list),
                    "Pemeriksaan informasi obat telah dilakukan."
                )

            except Exception as error:

                show_error(error)

    st.divider()

    st.warning(
        "Referensi obat dalam aplikasi masih terbatas. "
        "Fitur ini bukan pemeriksa interaksi obat yang tervalidasi. "
        "Jangan menggunakan hasilnya untuk menentukan dosis atau "
        "menghentikan obat tanpa berkonsultasi dengan tenaga medis."
    )

    show_disclaimer()


# ==========================================
# RECOVERY PLANNER
# ==========================================

elif selected_page == "Recovery Planner":

    st.header("🌱 Recovery Planner")

    st.write(
        "Buat panduan kebiasaan sehat berdasarkan kondisi "
        "dan aktivitas sehari-hari."
    )

    with st.form("recovery_form"):

        condition = st.text_input(
            "Kondisi saat ini",
            placeholder="Contoh: Sedang dalam masa pemulihan"
        )

        activity = st.selectbox(
            "Tingkat Aktivitas",
            [
                "Rendah / banyak istirahat",
                "Sedang",
                "Aktif"
            ]
        )

        sleep = st.selectbox(
            "Durasi Tidur",
            [
                "Kurang dari 5 jam",
                "5–6 jam",
                "7–8 jam",
                "Lebih dari 8 jam"
            ]
        )

        goal = st.selectbox(
            "Tujuan Kesehatan",
            [
                "Pemulihan kondisi tubuh",
                "Meningkatkan kualitas tidur",
                "Menjaga pola makan",
                "Meningkatkan kebugaran",
                "Menjaga kesehatan umum"
            ]
        )

        submitted = st.form_submit_button(
            "Buat Recovery Plan",
            use_container_width=True
        )

    if submitted:

        if not condition.strip():

            st.error("Silakan isi kondisi saat ini.")

        else:

            try:

                result = create_recovery_plan(
                    condition,
                    activity,
                    sleep,
                    goal
                )

                st.success(
                    "Recovery Plan berhasil dibuat."
                )

                st.subheader(
                    "📋 Rencana Kebiasaan Sehat"
                )

                st.markdown("### Kondisi")
                st.write(result["condition"])

                st.markdown("### Aktivitas")
                st.write(result["activity"])

                st.markdown("### Istirahat dan Tidur")
                st.write(result["sleep"])

                st.markdown("### Nutrisi")
                st.write(result["nutrition"])

                st.markdown("### Rekomendasi Tujuan")
                st.write(result["goal"])

                st.warning(result["warning"])

                st.caption(result["disclaimer"])

                save_history(
                    "Recovery Planner",
                    condition,
                    "Recovery Plan berhasil dibuat."
                )

            except Exception as error:

                show_error(error)

    st.divider()

    show_disclaimer()


# ==========================================
# HISTORY
# ==========================================

elif selected_page == "History":

    st.header("📋 History")

    st.write(
        "Riwayat penggunaan fitur selama sesi aplikasi ini."
    )

    history = st.session_state.history

    if not history:

        st.info("Belum ada riwayat penggunaan.")

    else:

        st.metric(
            "Total Aktivitas",
            len(history)
        )

        if st.button("Hapus Semua Riwayat"):

            st.session_state.history = []

            st.rerun()

        for item in history:

            with st.expander(
                f"{item['feature']} — {item['time']}"
            ):

                st.write("**Input:**")
                st.write(item["prompt"])

                st.write("**Hasil:**")
                st.write(item["response"])


# ==========================================
# ABOUT
# ==========================================

elif selected_page == "About":

    st.header("ℹ️ About MediCess AI")

    st.write(
        "MediCess AI merupakan aplikasi edukasi kesehatan "
        "yang menggabungkan klasifikasi teks berbasis "
        "Machine Learning dengan referensi informasi kesehatan lokal."
    )

    st.subheader("Teknologi yang Digunakan")

    technologies = [
        "Python",
        "Streamlit",
        "Scikit-learn",
        "TF-IDF Vectorization",
        "Machine Learning Classification",
        "Joblib"
    ]

    for technology in technologies:

        st.write(f"• {technology}")

    st.subheader("Dataset")

    st.write(
        "Model Medical Triage menggunakan dataset Symptom2Disease "
        "yang berisi deskripsi gejala berbahasa Inggris dan label kategori."
    )

    st.markdown(
        "[Lihat Dataset Symptom2Disease]"
        "(https://huggingface.co/datasets/NeuronZero/Symptom2Disease)"
    )

    st.subheader("Tujuan Pengembangan")

    st.write(
        "Mengembangkan prototipe aplikasi edukasi kesehatan "
        "berbasis Machine Learning yang dapat diakses melalui browser "
        "tanpa memerlukan API Key layanan AI eksternal."
    )

    st.warning(
        "MediCess AI masih merupakan prototipe penelitian "
        "dan belum divalidasi untuk penggunaan klinis."
    )

    st.divider()

    st.caption(
        "MediCess AI — Machine Learning Health Education Prototype"
    )
