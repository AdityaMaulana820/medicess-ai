
import streamlit as st
import time
import base64
from io import BytesIO
from PIL import Image
from google import genai
from datetime import datetime

# =====================================================
# 1. CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="MediCess AI | Healthcare Agent",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

MODEL = "gemini-3.8-flash"

# =====================================================
# 2. CUSTOM CSS
# =====================================================

st.markdown("""
<style>

/* GLOBAL */
.stApp {
    background: #f4f7fb;
    color: #172b4d;
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #102b46;
}

section[data-testid="stSidebar"] * {
    color: #ffffff;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: 8px 5px;
}

/* HERO */
.hero {
    background: linear-gradient(120deg, #102b46, #087f8c);
    padding: 35px;
    border-radius: 20px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 8px 25px rgba(16,43,70,0.12);
}

.hero h1 {
    color: white;
    font-size: 36px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero p {
    color: #d8edf0;
    font-size: 15px;
    line-height: 1.7;
}

.hero-tag {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    padding: 6px 13px;
    border-radius: 20px;
    font-size: 12px;
    margin-bottom: 15px;
}

/* SECTION */
.section-title {
    font-size: 24px;
    font-weight: 750;
    color: #102b46;
    margin-bottom: 5px;
}

.section-desc {
    color: #718096;
    font-size: 14px;
    margin-bottom: 22px;
}

/* FEATURE CARDS */
.feature-card {
    background: white;
    padding: 23px;
    border-radius: 17px;
    border: 1px solid #e5edf5;
    min-height: 175px;
    box-shadow: 0 4px 15px rgba(16,43,70,0.04);
}

.feature-icon {
    font-size: 30px;
    margin-bottom: 12px;
}

.feature-card h3 {
    color: #102b46;
    font-size: 18px;
    margin-bottom: 8px;
}

.feature-card p {
    color: #718096;
    font-size: 13px;
    line-height: 1.6;
}

/* INPUT */
.stTextArea textarea,
.stTextInput input {
    background: white;
    border: 1px solid #dce6ef;
    border-radius: 10px;
    color: #172b4d;
}

/* BUTTON */
.stButton > button {
    background: linear-gradient(120deg, #087f8c, #086b78);
    color: white;
    border: none;
    border-radius: 10px;
    min-height: 45px;
    font-weight: 700;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #075d69;
    color: white;
    border: none;
}

/* CONTAINER */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: white;
    border: 1px solid #e5edf5;
    border-radius: 15px;
}

/* METRIC */
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e5edf5;
    padding: 17px;
    border-radius: 14px;
}

/* FOOTER */
.footer {
    text-align: center;
    color: #718096;
    font-size: 12px;
    padding: 25px;
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] {
    background: #f9fbfd;
    border-radius: 12px;
}

/* ALERT */
.stAlert {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. SESSION STATE
# =====================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "api_client" not in st.session_state:
    st.session_state.api_client = None

if "client_key" not in st.session_state:
    st.session_state.client_key = None


# =====================================================
# 4. SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("""
    <div style="padding:15px 0 25px 0;">
        <h2 style="color:white;margin-bottom:0;">
            🏥 MediCess
        </h2>
        <p style="color:#9bbbc9;font-size:12px;">
            INTELLIGENT HEALTHCARE AGENT
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### NAVIGATION")

    page = st.radio(
        "Menu",
        [
            "🏠 Dashboard",
            "🩺 Medical Triage",
            "💊 Drug Safety",
            "📅 Recovery Planner",
            "📂 Riwayat Analisis",
            "ℹ️ Tentang MediCess"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown("### ⚙️ API SETTINGS")

    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="Masukkan API Key..."
    )

    if api_key:

        try:
            if st.session_state.client_key != api_key:

                st.session_state.api_client = genai.Client(
                    api_key=api_key
                )

                st.session_state.client_key = api_key

            st.success("Gemini API Connected")

        except Exception:
            st.error("Gagal menginisialisasi Gemini.")
            st.session_state.api_client = None

    else:
        st.warning("API Key belum dimasukkan.")

    st.markdown("---")

    st.caption("MediCess AI v2.0")
    st.caption("Powered by Google Gemini")


# =====================================================
# 5. GEMINI CLIENT
# =====================================================

def get_client():

    client = st.session_state.api_client

    if client is None:
        st.error("Masukkan Gemini API Key pada sidebar.")
        return None

    return client


# =====================================================
# 6. AI GENERATION WITH STREAMING
# =====================================================

def generate_ai(prompt, uploaded_image=None):

    client = get_client()

    if client is None:
        return None, 0

    input_data = prompt

    # IMAGE OPTIMIZATION
    if uploaded_image is not None:

        image = Image.open(
            BytesIO(uploaded_image.getvalue())
        ).convert("RGB")

        image.thumbnail((1024, 1024))

        buffer = BytesIO()

        image.save(
            buffer,
            format="JPEG",
            quality=80,
            optimize=True
        )

        image_base64 = base64.b64encode(
            buffer.getvalue()
        ).decode("utf-8")

        input_data = [
            {
                "type": "text",
                "text": prompt
            },
            {
                "type": "image",
                "data": image_base64,
                "mime_type": "image/jpeg"
            }
        ]

    # STREAMING RESPONSE
    start_time = time.time()

    response_placeholder = st.empty()

    full_response = ""

    stream = client.interactions.create(
        model=MODEL,
        input=input_data,
        generation_config={
            "thinking_level": "low",
            "max_output_tokens": 700
        },
        stream=True
    )

    for event in stream:

        if event.event_type == "step.delta":

            text_delta = getattr(
                event.delta,
                "text",
                None
            )

            if text_delta:

                full_response += text_delta

                response_placeholder.markdown(
                    full_response + " ▌"
                )

    elapsed = time.time() - start_time

    if not full_response.strip():

        raise RuntimeError(
            "Gemini tidak menghasilkan jawaban teks."
        )

    response_placeholder.markdown(full_response)

    return full_response, elapsed


# =====================================================
# 7. SAVE HISTORY
# =====================================================

def save_history(feature, question, answer, elapsed):

    st.session_state.history.insert(
        0,
        {
            "feature": feature,
            "question": question,
            "answer": answer,
            "time": datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            ),
            "duration": round(elapsed, 2)
        }
    )


# =====================================================
# 8. RESULT DISPLAY
# =====================================================

def display_result(result, elapsed, filename):

    st.success("Analisis berhasil diselesaikan!")

    st.caption(
        f"⏱️ Waktu pemrosesan: {elapsed:.2f} detik"
    )

    with st.container(border=True):

        st.markdown("### 📋 Hasil Analisis")

        st.markdown(result)

    st.download_button(
        label="📥 Unduh Hasil Analisis",
        data=result,
        file_name=filename,
        mime="text/plain"
    )


# =====================================================
# 9. DASHBOARD
# =====================================================

if page == "🏠 Dashboard":

    st.markdown("""
    <div class="hero">

        <span class="hero-tag">
            ✦ AI HEALTHCARE PLATFORM
        </span>

        <h1>Welcome to MediCess AI</h1>

        <p>
            Your Health, Smarter.<br>
            Asisten kesehatan cerdas berbasis Artificial Intelligence
            untuk membantu memahami informasi kesehatan.
        </p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Healthcare Services</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-desc">'
        'Pilih layanan kesehatan yang ingin kamu gunakan.'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🩺</div>
            <h3>Medical Triage</h3>
            <p>
                Analisis keluhan kesehatan dan foto kondisi fisik
                untuk membantu memahami tingkat urgensi.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💊</div>
            <h3>Drug Safety</h3>
            <p>
                Analisis potensi interaksi obat, alergi,
                dan risiko penggunaan obat.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📅</div>
            <h3>Recovery Planner</h3>
            <p>
                Membantu menyusun panduan aktivitas,
                nutrisi, dan jadwal pemulihan.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    st.markdown("### 📊 Dashboard Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Analisis Sesi Ini",
            len(st.session_state.history)
        )

    with col2:
        st.metric(
            "Healthcare AI Features",
            "3"
        )

    st.markdown("---")

    st.markdown("### 🛡️ Medical Information Notice")

    st.info(
        "MediCess AI merupakan asisten informasi kesehatan. "
        "Hasil analisis tidak menggantikan diagnosis, pemeriksaan, "
        "atau keputusan tenaga kesehatan profesional."
    )


# =====================================================
# 10. FEATURE 1 - MEDICAL TRIAGE
# =====================================================

elif page == "🩺 Medical Triage":

    st.markdown("""
    <div class="hero">
        <span class="hero-tag">FEATURE 01</span>
        <h1>🩺 AI Medical Triage</h1>
        <p>
            Intelligent Symptom & Visual Analysis
            <br>
            Analisis keluhan kesehatan dan foto kondisi fisik.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):

        st.markdown("### Informasi Keluhan")

        col1, col2 = st.columns(2)

        with col1:

            keluhan_text = st.text_area(
                "Deskripsikan keluhan kesehatan:",
                placeholder=(
                    "Contoh: Ruam merah di tangan, "
                    "terasa gatal sejak kemarin..."
                ),
                height=160
            )

        with col2:

            uploaded_image = st.file_uploader(
                "Unggah foto kondisi fisik (opsional):",
                type=["png", "jpg", "jpeg"],
                key="triage_image"
            )

            if uploaded_image:

                st.image(
                    uploaded_image,
                    caption="Foto kondisi fisik",
                    use_container_width=True
                )

        st.caption(
            "Hindari mengunggah foto yang memuat informasi "
            "identitas pribadi."
        )

        if st.button(
            "🚀 Mulai Analisis Keluhan",
            type="primary",
            use_container_width=True
        ):

            if not keluhan_text.strip() and uploaded_image is None:

                st.warning(
                    "Masukkan keluhan atau unggah foto terlebih dahulu."
                )

            else:

                prompt = f"""
Kamu adalah MediCess AI, asisten informasi kesehatan.

Keluhan pasien:
{keluhan_text if keluhan_text.strip() else "Tidak ada deskripsi teks."}

Jika foto tersedia, gunakan sebagai informasi pendukung.

Berikan hasil dengan struktur:

1. RINGKASAN KELUHAN
2. KEMUNGKINAN PENYEBAB
   Jelaskan sebagai kemungkinan, bukan diagnosis.
3. TINGKAT URGENSI
   - EMERGENCY
   - URGENT
   - NON-URGENT / SELF-CARE
4. SARAN TINDAKAN AWAL YANG AMAN
5. REKOMENDASI TENAGA MEDIS
6. TANDA BAHAYA

Jika ditemukan tanda kondisi darurat,
arahkan pasien segera ke IGD.

Jangan memastikan diagnosis hanya berdasarkan foto.
Jangan mengarang informasi medis.

Gunakan bahasa Indonesia yang sederhana,
ringkas, dan mudah dipahami.

Akhiri dengan disclaimer medis.
"""

                try:

                    with st.spinner(
                        "MediCess sedang menganalisis keluhan..."
                    ):

                        result, elapsed = generate_ai(
                            prompt,
                            uploaded_image
                        )

                    if result:

                        save_history(
                            "Medical Triage",
                            keluhan_text or "Analisis foto gejala",
                            result,
                            elapsed
                        )

                        display_result(
                            result,
                            elapsed,
                            "medicess_medical_triage.txt"
                        )

                except Exception as e:

                    st.error(
                        f"Terjadi kesalahan saat analisis: {e}"
                    )


# =====================================================
# 11. FEATURE 2 - DRUG SAFETY
# =====================================================

elif page == "💊 Drug Safety":

    st.markdown("""
    <div class="hero">
        <span class="hero-tag">FEATURE 02</span>
        <h1>💊 Medication Safety Checker</h1>
        <p>
            Drug Interaction & Safety Analysis
            <br>
            Membantu memahami potensi risiko penggunaan obat.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):

        st.markdown("### Informasi Penggunaan Obat")

        daftar_obat = st.text_area(
            "Masukkan daftar obat:",
            placeholder=(
                "Contoh:\n"
                "Paracetamol 500mg\n"
                "Amoxicillin 500mg\n"
                "Ibuprofen 200mg"
            ),
            height=150
        )

        riwayat_alergi = st.text_input(
            "Riwayat alergi atau kondisi medis:",
            placeholder=(
                "Contoh: Alergi penisilin, "
                "memiliki riwayat maag..."
            )
        )

        if st.button(
            "🔍 Periksa Keamanan Obat",
            type="primary",
            use_container_width=True
        ):

            if not daftar_obat.strip():

                st.warning(
                    "Masukkan setidaknya satu nama obat."
                )

            else:

                prompt_obat = f"""
Kamu adalah MediCess Drug Safety Agent.

Daftar obat:
{daftar_obat}

Riwayat alergi dan kondisi medis:
{riwayat_alergi if riwayat_alergi.strip() else "Tidak diberikan."}

Analisis dengan struktur:

1. IDENTIFIKASI OBAT
2. POTENSI INTERAKSI ANTAROBAT
3. RISIKO ALERGI DAN KONTRAINDIKASI
4. EFEK SAMPING PENTING
5. SARAN KEAMANAN
6. HAL YANG PERLU DITANYAKAN KEPADA APOTEKER

PENTING:
- Jangan mengarang interaksi obat.
- Bedakan informasi diketahui dan belum terverifikasi.
- Jangan mengklaim telah memeriksa database obat langsung.
- Jangan menentukan dosis personal.
- Jangan menyarankan penghentian obat resep sendiri.
- Jika data tidak cukup, jelaskan keterbatasannya.

Gunakan bahasa Indonesia sederhana dan ringkas.
Akhiri dengan disclaimer medis.
"""

                try:

                    with st.spinner(
                        "MediCess sedang mengevaluasi keamanan obat..."
                    ):

                        result, elapsed = generate_ai(
                            prompt_obat
                        )

                    if result:

                        save_history(
                            "Drug Safety",
                            daftar_obat,
                            result,
                            elapsed
                        )

                        display_result(
                            result,
                            elapsed,
                            "medicess_drug_safety.txt"
                        )

                except Exception as e:

                    st.error(
                        f"Terjadi kesalahan: {e}"
                    )


# =====================================================
# 12. FEATURE 3 - RECOVERY PLANNER
# =====================================================

elif page == "📅 Recovery Planner":

    st.markdown("""
    <div class="hero">
        <span class="hero-tag">FEATURE 03</span>
        <h1>📅 Personal Recovery Planner</h1>
        <p>
            Intelligent Lifestyle & Recovery Planning
            <br>
            Panduan aktivitas dan pemulihan berdasarkan kondisi kesehatan.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):

        st.markdown("### Informasi Kondisi Pasien")

        kondisi_pasien = st.text_area(
            "Kondisi kesehatan atau pemulihan:",
            placeholder=(
                "Contoh: Sedang dalam pemulihan demam, "
                "hari ketiga setelah sakit..."
            ),
            height=130
        )

        if st.button(
            "📋 Buat Rencana Pemulihan",
            type="primary",
            use_container_width=True
        ):

            if not kondisi_pasien.strip():

                st.warning(
                    "Masukkan kondisi kesehatan terlebih dahulu."
                )

            else:

                prompt_plan = f"""
Kamu adalah MediCess Recovery Planning Agent.

Kondisi pasien:
{kondisi_pasien}

Buat panduan pemulihan harian dengan struktur:

1. TUJUAN PEMULIHAN
2. JADWAL AKTIVITAS HARIAN

Gunakan tabel:
- Waktu
- Aktivitas
- Keterangan

3. REKOMENDASI NUTRISI
4. KEBUTUHAN CAIRAN SECARA UMUM
5. AKTIVITAS YANG SEBAIKNYA DIHINDARI
6. TANDA BAHAYA YANG MEMERLUKAN PEMERIKSAAN DOKTER

Sesuaikan dengan kondisi pasien.
Jangan memberikan dosis obat personal.
Jangan menggantikan instruksi dokter.
Jika kondisi berisiko tinggi, utamakan pemeriksaan medis.

Gunakan bahasa Indonesia yang sederhana,
ringkas, dan mudah dipahami.
"""

                try:

                    with st.spinner(
                        "MediCess sedang menyusun rencana pemulihan..."
                    ):

                        result, elapsed = generate_ai(
                            prompt_plan
                        )

                    if result:

                        save_history(
                            "Recovery Planner",
                            kondisi_pasien,
                            result,
                            elapsed
                        )

                        display_result(
                            result,
                            elapsed,
                            "medicess_recovery_plan.txt"
                        )

                except Exception as e:

                    st.error(
                        f"Terjadi kesalahan: {e}"
                    )


# =====================================================
# 13. ANALYSIS HISTORY
# =====================================================

elif page == "📂 Riwayat Analisis":

    st.markdown("""
    <div class="hero">
        <span class="hero-tag">USER ACTIVITY</span>
        <h1>📂 Riwayat Analisis</h1>
        <p>
            Daftar hasil analisis MediCess AI
            selama sesi aplikasi berlangsung.
        </p>
    </div>
    """, unsafe_allow_html=True)

    history = st.session_state.history

    if not history:

        st.info(
            "Belum ada riwayat analisis. "
            "Silakan gunakan salah satu fitur MediCess."
        )

    else:

        st.markdown(
            f"### Total {len(history)} Analisis"
        )

        if st.button("🗑️ Hapus Semua Riwayat"):

            st.session_state.history = []

            st.rerun()

        for index, item in enumerate(history):

            with st.expander(
                f"{item['feature']} | {item['time']}"
            ):

                st.markdown(
                    f"**Pertanyaan:** {item['question']}"
                )

                st.markdown(
                    f"**Waktu analisis:** {item['duration']} detik"
                )

                st.markdown("---")

                st.markdown(item["answer"])

                st.download_button(
                    "📥 Unduh Hasil",
                    data=item["answer"],
                    file_name=f"medicess_history_{index + 1}.txt",
                    mime="text/plain",
                    key=f"history_download_{index}"
                )


# =====================================================
# 14. ABOUT PAGE
# =====================================================

elif page == "ℹ️ Tentang MediCess":

    st.markdown("""
    <div class="hero">
        <span class="hero-tag">ABOUT THE PROJECT</span>
        <h1>🏥 About MediCess AI</h1>
        <p>
            Intelligent Healthcare Agent
            <br>
            Artificial Intelligence for Healthcare Information.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Tentang Aplikasi")

    st.write("""
    MediCess AI merupakan aplikasi asisten informasi kesehatan
    berbasis Artificial Intelligence yang menggunakan teknologi
    Google Gemini.

    Aplikasi ini dirancang untuk membantu pengguna memahami
    informasi awal terkait keluhan kesehatan, keamanan obat,
    serta perencanaan pemulihan.
    """)

    st.markdown("### Teknologi yang Digunakan")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        - Python
        - Streamlit
        - Google Gemini API
        """)

    with col2:

        st.markdown("""
        - Google Gen AI SDK
        - Pillow
        - Image Processing
        """)

    st.markdown("### Fitur Utama")

    st.markdown("""
    **F1 – Medical Triage**

    Analisis keluhan kesehatan dan foto kondisi fisik.

    **F2 – Drug Safety**

    Analisis awal potensi interaksi dan risiko obat.

    **F3 – Recovery Planner**

    Pembuatan panduan aktivitas dan pemulihan.
    """)

    st.info(
        "MediCess AI merupakan proyek asisten informasi kesehatan, "
        "bukan alat diagnosis medis atau pengganti tenaga kesehatan."
    )


# =====================================================
# 15. FOOTER
# =====================================================

st.markdown("---")

st.markdown("""
<div class="footer">

    <h3 style="color:#087f8c;">🏥 MediCess AI</h3>

    <p>
        Intelligent Healthcare Agent
    </p>

    <p>
        Powered by Google Gemini
    </p>

    <p>
        © 2026 MediCess AI. All Rights Reserved.
    </p>

    <small>
        Informasi AI bukan pengganti diagnosis dan konsultasi
        dengan dokter atau tenaga kesehatan profesional.
    </small>

</div>
""", unsafe_allow_html=True)
