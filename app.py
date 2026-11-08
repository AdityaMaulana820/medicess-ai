
import streamlit as st
from google import genai
from PIL import Image
import base64

# CONFIG HALAMAN
st.set_page_config(
    page_title="MediCess AI - Agent Kesehatan",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 MediCess AI — Autonomous Healthcare Agent")
st.write(
    "Agen AI Kesehatan Mandiri berbasis Gemini untuk "
    "Triase Medis, Analisis Visual, dan Keamanan Obat."
)

# SIDEBAR
with st.sidebar:
    st.header("⚙️ Pengaturan")
    api_key = st.text_input(
        "Masukkan Gemini API Key:",
        type="password"
    )
    st.markdown("---")
    st.markdown("**Status Agen:** 🟢 Ready")

if not api_key:
    st.warning("Masukkan Gemini API Key terlebih dahulu.")
    st.stop()

# INISIALISASI GEMINI
try:
    client = genai.Client(api_key=api_key)
    MODEL = "gemini-3.8-flash"
except Exception as e:
    st.error(f"Gagal menginisialisasi Gemini: {e}")
    st.stop()


# FUNGSI GENERATE TEKS
def generate_ai(prompt, image=None):
    if image:
        image_bytes = image.getvalue()
        mime_type = image.type

        image_base64 = base64.b64encode(
            image_bytes
        ).decode("utf-8")

        interaction = client.interactions.create(
            model=MODEL,
            input=[
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image",
                    "data": image_base64,
                    "mime_type": mime_type
                }
            ]
        )
    else:
        interaction = client.interactions.create(
            model=MODEL,
            input=prompt
        )

    return interaction.output_text


# TAB FITUR
tab1, tab2, tab3 = st.tabs([
    "🩺 F1: Triase Keluhan & Foto Gejala",
    "💊 F2: Validator Keamanan Obat",
    "📅 F3: Recovery & Lifestyle Planner"
])


# ==========================================
# FITUR 1: MEDICAL TRIAGE AGENT
# ==========================================
with tab1:

    st.subheader("F1: Multimodal Symptom & Skin Visual Triaging Agent")

    st.write(
        "Analisis keluhan kesehatan dan foto kondisi fisik "
        "untuk membantu memahami tingkat urgensi."
    )

    col1, col2 = st.columns(2)

    with col1:
        keluhan_text = st.text_area(
            "Deskripsikan keluhan kesehatan:",
            placeholder="Contoh: Ruam merah dan gatal sejak kemarin..."
        )

    with col2:
        uploaded_image = st.file_uploader(
            "Unggah foto kondisi fisik:",
            type=["png", "jpg", "jpeg"],
            key="triage_image"
        )

        if uploaded_image:
            st.image(
                uploaded_image,
                caption="Foto Kondisi Fisik",
                use_container_width=True
            )

    if st.button("🚀 Jalankan Analisis Agen Triase"):

        if not keluhan_text and not uploaded_image:
            st.error("Masukkan keluhan atau foto terlebih dahulu!")

        else:
            prompt = f"""
            Kamu adalah MediCess AI, asisten informasi kesehatan.

            Analisis keluhan berikut:
            {keluhan_text}

            Berikan hasil dengan struktur:

            1. Ringkasan Keluhan
            2. Kemungkinan Penyebab (bukan diagnosis pasti)
            3. Tingkat Urgensi:
               - EMERGENCY
               - URGENT
               - NON-URGENT / SELF-CARE
            4. Saran tindakan awal
            5. Rekomendasi tenaga medis yang relevan
            6. Tanda bahaya yang harus diperhatikan

            Jangan memberikan diagnosis pasti.
            Jika ditemukan tanda kondisi darurat,
            arahkan pasien segera ke IGD.

            Foto tidak boleh dianggap sebagai bukti
            diagnosis yang pasti.

            Berikan disclaimer medis.
            """

            try:
                with st.spinner("🤖 Agen sedang menganalisis..."):

                    hasil = generate_ai(
                        prompt,
                        uploaded_image
                    )

                st.success("Analisis berhasil!")
                st.markdown(hasil)

            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")


# ==========================================
# FITUR 2: DRUG SAFETY VALIDATOR
# ==========================================
with tab2:

    st.subheader("F2: Drug Interaction & Safety Validator Agent")

    st.write(
        "Menganalisis potensi interaksi dan risiko penggunaan obat."
    )

    daftar_obat = st.text_area(
        "Masukkan daftar obat:",
        placeholder="Paracetamol 500mg, Amoxicillin 500mg..."
    )

    riwayat_alergi = st.text_input(
        "Riwayat Alergi / Kondisi Medis:",
        placeholder="Contoh: Alergi penisilin, maag..."
    )

    if st.button("🔍 Validasi Keamanan Obat"):

        if not daftar_obat:
            st.error("Masukkan setidaknya satu nama obat!")

        else:

            prompt_obat = f"""
            Kamu adalah MediCess Drug Safety Agent.

            Daftar obat:
            {daftar_obat}

            Riwayat pasien:
            {riwayat_alergi}

            Analisis:

            1. Potensi interaksi antarobat.
            2. Risiko alergi dan kontraindikasi.
            3. Efek samping yang perlu diperhatikan.
            4. Informasi penggunaan berdasarkan sumber
               medis yang dapat diverifikasi.
            5. Hal yang perlu dikonsultasikan kepada apoteker
               atau dokter.

            Jangan mengarang interaksi obat.
            Jika data tidak cukup, nyatakan bahwa informasi
            perlu diverifikasi oleh tenaga kesehatan.

            Jangan menentukan dosis personal tanpa
            informasi klinis yang memadai.

            Berikan disclaimer medis.
            """

            try:
                with st.spinner("🤖 Agen mengevaluasi keamanan obat..."):

                    hasil_obat = generate_ai(prompt_obat)

                st.success("Analisis obat selesai!")
                st.markdown(hasil_obat)

            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")


# ==========================================
# FITUR 3: RECOVERY & LIFESTYLE PLANNER
# ==========================================
with tab3:

    st.subheader("F3: Autonomous Lifestyle & Recovery Planner")

    st.write(
        "Menyusun panduan aktivitas dan pemulihan "
        "berdasarkan kondisi kesehatan."
    )

    kondisi_pasien = st.text_input(
        "Kondisi kesehatan:",
        placeholder="Contoh: Pemulihan demam hari ke-3..."
    )

    if st.button("📋 Buatkan Rencana Pemulihan"):

        if not kondisi_pasien:
            st.error("Masukkan kondisi kesehatan!")

        else:

            prompt_plan = f"""
            Kamu adalah MediCess Recovery Planning Agent.

            Kondisi pasien:
            {kondisi_pasien}

            Buat panduan pemulihan harian meliputi:

            1. Jadwal aktivitas harian.
            2. Rekomendasi nutrisi.
            3. Kebutuhan cairan secara umum.
            4. Jadwal istirahat.
            5. Aktivitas yang sebaiknya dihindari.
            6. Tanda bahaya yang memerlukan pemeriksaan medis.

            Sesuaikan rekomendasi dengan kondisi pasien.
            Jangan memberikan dosis obat atau menggantikan
            instruksi dokter.

            Berikan disclaimer medis.
            """

            try:
                with st.spinner("🤖 Agen menyusun rencana pemulihan..."):

                    hasil_plan = generate_ai(prompt_plan)

                st.success("Rencana pemulihan berhasil dibuat!")
                st.markdown(hasil_plan)

            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")


# FOOTER
st.markdown("---")
st.caption(
    "MediCess AI | Healthcare Assistant | "
    "Bukan pengganti diagnosis dan konsultasi dokter."
)
