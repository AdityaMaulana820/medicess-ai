import streamlit as st
import google.generativeai as genai
from PIL import Image

# Config Halaman
st.set_page_config(page_title="MediCess AI - Agent Kesehatan", page_icon="🏥", layout="wide")

st.title("🏥 MediCess AI — Autonomous Healthcare Agent")
st.write("Agen AI Kesehatan Mandiri berbasis Gemini untuk Triase Medis, Analisis Visual, & Keamanan Obat.")

# Sidebar API Key
with st.sidebar:
    st.header("⚙️ Pengaturan")
    api_key = st.text_input("Masukkan Gemini API Key:", type="password")
    st.markdown("---")
    st.markdown("**Status Agen:** `Ready` 🟢")

if not api_key:
    st.warning("⚠️ Silakan masukkan Gemini API Key kamu di bilah samping (sidebar) kiri untuk memulai.")
    st.stop()

# Inisialisasi Model Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Tab Fitur Sesuai Proposal
tab1, tab2, tab3 = st.tabs([
    "🩺 F1: Triase Keluhan & Foto Gejala", 
    "💊 F2: Validator Keamanan & Interaksi Obat", 
    "📅 F3: Recovery & Lifestyle Planner"
])

# FITUR 1: Multimodal Triase Agent
with tab1:
    st.subheader("F1: Multimodal Symptom & Skin Visual Triaging Agent")
    st.write("Agen akan menganalisis teks keluhan serta foto fisik (seperti ruam/luka) untuk menentukan tingkat urgensi medis.")
    
    col1, col2 = st.columns(2)
    with col1:
        keluhan_text = st.text_area("Deskripsikan keluhan kesehatan kamu:", placeholder="Contoh: Ada ruam merah di tangan disertai rasa gatal dan demam ringan sejak kemarin...")
    with col2:
        uploaded_image = st.file_uploader("Unggah foto kondisi fisik / ruam kulit (Opsional):", type=["png", "jpg", "jpeg"])
        if uploaded_image:
            image = Image.open(uploaded_image)
            st.image(image, caption="Foto Gejala Ditingkatkan", use_container_width=True)

    if st.button("🚀 Jalankan Analisis Agen Triase"):
        if not keluhan_text and not uploaded_image:
            st.error("Masukkan deskripsi keluhan atau unggah foto terlebih dahulu!")
        else:
            with st.spinner("🤖 MediCess Agent sedang berpikir & mengevaluasi tingkat urgensi..."):
                prompt = f"""
                Kamu adalah MediCess AI, Agen Triase Medis Profesional.
                Tugasmu:
                1. Menganalisis keluhan berikut: "{keluhan_text}"
                2. Tentukan Tingkat Urgensi: [EMERGENCY / URGENT / NON-URGENT/SELF-CARE]
                3. Berikan saran langkah awal dan rekomendasi spesialis dokter yang relevan.
                4. Berikan disclaimer medis di akhir bahwa ini adalah pertolongan awal AI.
                """
                
                try:
                    if uploaded_image:
                        response = model.generate_content([prompt, image])
                    else:
                        response = model.generate_content(prompt)
                    
                    st.success("Analisis Agen Selesai!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")

# FITUR 2: Drug Safety Validator Agent
with tab2:
    st.subheader("F2: Drug Interaction & Safety Validator Agent")
    st.write("Agen akan mengecek potensi bahaya interaksi antara obat yang akan kamu konsumsi.")
    
    daftar_obat = st.text_area("Masukkan daftar nama obat yang sedang/akan dikonsumsi:", placeholder="Contoh: Paracetamol 500mg, Amoxicillin 500mg, Ibuprofen...")
    riwayat_alergi = st.text_input("Riwayat Alergi / Kondisi Medis (Opsional):", placeholder="Contoh: Alergi Penisilin, Memiliki Riwayat Maag")

    if st.button("🔍 Validasi Keamanan Obat"):
        if not daftar_obat:
            st.error("Masukkan setidaknya satu nama obat!")
        else:
            with st.spinner("🤖 Agen sedang mengecek basis data keamanan obat..."):
                prompt_obat = f"""
                Kamu adalah MediCess Drug Safety Agent.
                Analisis daftar obat ini: {daftar_obat}
                Riwayat Pasien: {riwayat_alergi}
                
                Tugasmu:
                1. Cek apakah ada potensi interaksi berbahaya antar obat tersebut.
                2. Cek apakah ada kontraindikasi dengan riwayat medis/alergi pasien.
                3. Berikan petunjuk aturan minum (sebelum/sesudah makan).
                """
                try:
                    response_obat = model.generate_content(prompt_obat)
                    st.success("Pengecekan Obat Selesai!")
                    st.markdown(response_obat.text)
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")

# FITUR 3: Lifestyle & Recovery Planner
with tab3:
    st.subheader("F3: Autonomous Lifestyle & Recovery Planner")
    st.write("Agen akan menyusun jadwal pemulihan dan pola hidup khusus berdasarkan kondisi kesehatanmu.")
    
    kondisi_pasien = st.text_input("Kondisi Kesehatan / Pemulihan:", placeholder="Contoh: Pemulihan Demam Berdarah (DBD) hari ke-4")
    
    if st.button("📋 Buatkan Rencana Pemulihan"):
        if not kondisi_pasien:
            st.error("Isi kondisi kesehatan kamu!")
        else:
            with st.spinner("🤖 Agen sedang merancang jadwal pemulihan harian..."):
                prompt_plan = f"""
                Buatkan rancangan jadwal harian pemulihan (*recovery plan*) untuk kondisi: {kondisi_pasien}.
                Sertakan rekomendasi asupan nutrisi/cairan, hal yang wajib dihindari, dan jadwal istirahat.
                """
                try:
                    response_plan = model.generate_content(prompt_plan)
                    st.success("Jadwal Pemulihan Berhasil Dibuat!")
                    st.markdown(response_plan.text)
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")
