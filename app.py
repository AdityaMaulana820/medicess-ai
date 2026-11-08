
import streamlit as st
from google import genai
from PIL import Image
from datetime import datetime

# =====================================================
# KONFIGURASI
# =====================================================

st.set_page_config(
    page_title="MediCess AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

MODEL = "gemini-3.8-flash"

# =====================================================
# SESSION STATE
# =====================================================

if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Dashboard"

if "history" not in st.session_state:
    st.session_state.history = []

if "api_client" not in st.session_state:
    st.session_state.api_client = None

if "client_key" not in st.session_state:
    st.session_state.client_key = None


# =====================================================
# CSS GLOBAL
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f5f8fc;
}

[data-testid="stSidebar"] {
    background: #102b46;
}

[data-testid="stSidebar"] * {
    color: #ffffff;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    color: #ffffff;
}

h1, h2, h3 {
    color: #102b46;
}

.stButton > button {
    border-radius: 10px;
    border: none;
    background: #087f8c;
    color: white;
    font-weight: 600;
    padding: 10px 18px;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #066b75;
    color: white;
    border: none;
}

.stTextInput input,
.stTextArea textarea {
    border-radius: 10px;
}

div[data-testid="stFileUploader"] {
    border-radius: 12px;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

hr {
    border-color: #e2e8f0;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# HERO
# =====================================================

def show_hero():

    st.html("""
    <div style="
        background: linear-gradient(120deg, #102b46, #087f8c);
        padding: 42px;
        border-radius: 22px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(16,43,70,0.12);
    ">

        <span style="
            display: inline-block;
            background: rgba(255,255,255,0.17);
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 1px;
        ">
            ✦ AI HEALTHCARE PLATFORM
        </span>

        <h1 style="
            color: #ffffff !important;
            font-size: 38px;
            font-weight: 800;
            margin: 20px 0 12px 0;
        ">
            Welcome to MediCess AI
        </h1>

        <p style="
            color: #e0f2f3 !important;
            font-size: 16px;
            line-height: 1.8;
            margin-bottom: 0;
        ">
            Your Health, Smarter.<br>
            Asisten informasi kesehatan berbasis Artificial Intelligence
            untuk membantu memahami informasi kesehatan secara lebih mudah.
        </p>

    </div>
    """)


# =====================================================
# WELCOME SECTION
# =====================================================

def show_welcome():

    st.html("""
    <div style="
        margin: 30px 0 20px 0;
        background: #ffffff;
        padding: 22px 25px;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(16,43,70,0.03);
    ">

        <h2 style="
            color: #102b46 !important;
            font-size: 25px;
            font-weight: 800;
            margin: 0 0 10px 0;
        ">
            Selamat Datang 👋
        </h2>

        <p style="
            color: #475569 !important;
            font-size: 15px;
            line-height: 1.8;
            margin: 0;
        ">
            MediCess AI membantu Anda memahami informasi kesehatan
            melalui teknologi Artificial Intelligence.
        </p>

    </div>
    """)


# =====================================================
# FEATURE CARDS
# =====================================================

def show_feature_cards():

    st.html("""
    <div style="
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
        gap: 16px;
        margin: 15px 0 20px 0;
    ">

        <div style="
            background: #ffffff;
            padding: 23px;
            border-radius: 16px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 14px rgba(16,43,70,0.04);
        ">
            <div style="font-size: 30px;">🩺</div>

            <h3 style="
                color: #102b46 !important;
                font-size: 18px;
                font-weight: 700;
            ">
                Medical Triage
            </h3>

            <p style="
                color: #475569 !important;
                font-size: 13px;
                line-height: 1.7;
            ">
                Membantu memahami keluhan dan tingkat urgensi gejala.
            </p>
        </div>

        <div style="
            background: #ffffff;
            padding: 23px;
            border-radius: 16px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 14px rgba(16,43,70,0.04);
        ">
            <div style="font-size: 30px;">💊</div>

            <h3 style="
                color: #102b46 !important;
                font-size: 18px;
                font-weight: 700;
            ">
                Drug Safety
            </h3>

            <p style="
                color: #475569 !important;
                font-size: 13px;
                line-height: 1.7;
            ">
                Informasi umum mengenai obat, alergi, dan hal yang perlu
                ditanyakan kepada apoteker.
            </p>
        </div>

        <div style="
            background: #ffffff;
            padding: 23px;
            border-radius: 16px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 14px rgba(16,43,70,0.04);
        ">
            <div style="font-size: 30px;">🌿</div>

            <h3 style="
                color: #102b46 !important;
                font-size: 18px;
                font-weight: 700;
            ">
                Recovery Planner
            </h3>

            <p style="
                color: #475569 !important;
                font-size: 13px;
                line-height: 1.7;
            ">
                Saran umum mengenai istirahat, aktivitas, dan kebiasaan sehat.
            </p>
        </div>

    </div>
    """)


# =====================================================
# MULAI MENGGUNAKAN FITUR
# =====================================================

def show_start_section():

    st.html("""
    <div style="
        margin: 30px 0 15px 0;
        background: #ffffff;
        padding: 22px 25px;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(16,43,70,0.03);
    ">

        <h2 style="
            color: #102b46 !important;
            font-size: 23px;
            font-weight: 800;
            margin: 0 0 10px 0;
        ">
            Mulai Menggunakan Fitur
        </h2>

        <p style="
            color: #475569 !important;
            font-size: 14px;
            margin: 0;
            line-height: 1.7;
        ">
            Pilih layanan MediCess AI sesuai kebutuhan Anda.
        </p>

    </div>
    """)


# =====================================================
# FOOTER
# =====================================================

def show_footer():

    st.divider()

    st.html("""
    <div style="
        text-align: center;
        color: #475569;
        font-size: 13px;
        padding: 22px 10px;
        line-height: 1.8;
    ">

        <h3 style="
            color: #087f8c !important;
            font-size: 22px;
            margin-bottom: 5px;
        ">
            🏥 MediCess AI
        </h3>

        <p>Intelligent Healthcare Assistant</p>
        <p>Powered by Google Gemini</p>
        <p>© 2026 MediCess AI. All Rights Reserved.</p>

        <small>
            Informasi dari AI bukan pengganti diagnosis,
            pemeriksaan, atau konsultasi dengan dokter
            dan tenaga kesehatan profesional.
        </small>

    </div>
    """)


# =====================================================
# GEMINI CLIENT
# =====================================================

def get_client():

    api_key = st.session_state.get("api_key", "").strip()

    if not api_key:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY", "").strip()
        except Exception:
            api_key = ""

    if not api_key:
        return None

    if (
        st.session_state.api_client is None
        or st.session_state.client_key != api_key
    ):
        st.session_state.api_client = genai.Client(
            api_key=api_key
        )

        st.session_state.client_key = api_key

    return st.session_state.api_client


# =====================================================
# GENERATE AI STREAMING
# =====================================================

def generate_ai(prompt, uploaded_image=None, feature_name="MediCess AI"):

    client = get_client()

    if client is None:
        st.error("API Key Gemini belum diisi.")
        return None

    contents = [prompt]

    if uploaded_image is not None:

        try:
            image = Image.open(uploaded_image).convert("RGB")
            image.thumbnail((1024, 1024))
            contents.append(image)

        except Exception as e:
            st.error(f"Gagal membaca gambar: {e}")
            return None

    response_placeholder = st.empty()
    full_response = ""

    try:

        stream = client.models.generate_content_stream(
            model=MODEL,
            contents=contents
        )

        for chunk in stream:

            if chunk.text:

                full_response += chunk.text

                response_placeholder.markdown(
                    full_response + " ▌"
                )

        response_placeholder.markdown(full_response)

        if full_response.strip():

            st.session_state.history.insert(0, {
                "feature": feature_name,
                "time": datetime.now().strftime("%d-%m-%Y %H:%M"),
                "prompt": prompt,
                "response": full_response
            })

        return full_response

    except Exception as e:

        st.error("Terjadi kesalahan ketika menghubungi Gemini API.")
        st.code(str(e))

        return None


# =====================================================
# PROMPT KEAMANAN MEDIS
# =====================================================

MEDICAL_SAFETY = """
Anda adalah asisten informasi kesehatan berbasis AI bernama MediCess AI.

Aturan penting:

1. Anda bukan dokter dan tidak boleh mengaku sebagai dokter.
2. Jangan memberikan diagnosis pasti.
3. Informasi bersifat edukasi, bukan pengganti pemeriksaan medis.
4. Jangan mengarang fakta medis.
5. Jika informasi tidak cukup, katakan bahwa informasi belum cukup.
6. Jangan menyarankan pengguna menghentikan obat resep tanpa arahan dokter.
7. Jangan memberikan dosis obat personal.
8. Jika terdapat tanda darurat seperti sesak napas berat, nyeri dada berat,
   penurunan kesadaran, kejang, perdarahan berat, atau gejala stroke,
   sarankan segera mencari pertolongan medis darurat.
9. Gunakan bahasa Indonesia yang jelas dan mudah dipahami.
"""


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("""
    <div style="text-align:center; padding:15px 5px 25px 5px;">

        <div style="font-size:42px;">🏥</div>

        <h2 style="color:white; margin:5px 0;">
            MediCess AI
        </h2>

        <p style="color:#b8d5e2; font-size:12px;">
            Intelligent Healthcare Assistant
        </p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### MENU UTAMA")

    pages = [
        "Dashboard",
        "Medical Triage",
        "Drug Safety",
        "Recovery Planner",
        "History",
        "About"
    ]

    selected = st.radio(
        "Navigasi",
        pages,
        index=pages.index(st.session_state.selected_page)
        if st.session_state.selected_page in pages else 0,
        label_visibility="collapsed"
    )

    st.session_state.selected_page = selected

    st.markdown("---")
    st.markdown("### ⚙️ API Configuration")

    st.text_input(
        "Gemini API Key",
        type="password",
        key="api_key",
        placeholder="Masukkan API Key..."
    )

    st.caption(
        "API Key digunakan untuk menghubungkan aplikasi ke Gemini."
    )

    st.markdown("---")
    st.caption("MediCess AI • Version 1.0")


# =====================================================
# DASHBOARD
# =====================================================

if st.session_state.selected_page == "Dashboard":

    show_hero()

    show_welcome()

    show_feature_cards()

    show_start_section()

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "🩺 Medical Triage",
            use_container_width=True
        ):

            st.session_state.selected_page = "Medical Triage"
            st.rerun()

    with col2:

        if st.button(
            "💊 Drug Safety",
            use_container_width=True
        ):

            st.session_state.selected_page = "Drug Safety"
            st.rerun()

    with col3:

        if st.button(
            "🌿 Recovery Planner",
            use_container_width=True
        ):

            st.session_state.selected_page = "Recovery Planner"
            st.rerun()

    st.info(
        "MediCess AI merupakan alat bantu informasi kesehatan, "
        "bukan sistem diagnosis atau pengganti tenaga medis."
    )


# =====================================================
# MEDICAL TRIAGE
# =====================================================

elif st.session_state.selected_page == "Medical Triage":

    st.title("🩺 Medical Triage")

    st.write(
        "Ceritakan keluhan yang sedang Anda alami."
    )

    with st.form("triage_form"):

        symptoms = st.text_area(
            "Apa gejala atau keluhan yang Anda alami?",
            placeholder="Contoh: Saya mengalami demam, batuk, dan sakit kepala sejak kemarin...",
            height=150
        )

        duration = st.text_input(
            "Sudah berapa lama gejala dirasakan?",
            placeholder="Contoh: 2 hari"
        )

        age = st.number_input(
            "Usia",
            min_value=0,
            max_value=120,
            value=20
        )

        uploaded_image = st.file_uploader(
            "Unggah foto jika relevan (opsional)",
            type=["jpg", "jpeg", "png"]
        )

        submitted = st.form_submit_button(
            "Analisis Keluhan",
            use_container_width=True
        )

    if uploaded_image:
        st.image(
            uploaded_image,
            caption="Gambar yang diunggah",
            width=300
        )

    if submitted:

        if not symptoms.strip():

            st.warning(
                "Silakan masukkan gejala terlebih dahulu."
            )

        else:

            prompt = f"""
{MEDICAL_SAFETY}

Bantu pengguna memahami keluhannya secara informatif dan berhati-hati.

Data pengguna:
- Usia: {age} tahun
- Keluhan: {symptoms}
- Durasi: {duration if duration else "Tidak disebutkan"}

Jika ada gambar, jelaskan hanya hal yang tampak secara visual.
Jangan memastikan penyakit berdasarkan gambar.

Susun jawaban:

## 1. Ringkasan Keluhan
Rangkum informasi pengguna.

## 2. Kemungkinan Penjelasan
Berikan beberapa kemungkinan umum jika relevan.
Tegaskan bahwa ini bukan diagnosis.

## 3. Tingkat Urgensi
Jelaskan apakah keluhan memerlukan:
- Pertolongan darurat
- Pemeriksaan dokter secepatnya
- Konsultasi medis terjadwal
- Pemantauan mandiri dengan hati-hati

Jangan menetapkan tingkat urgensi secara pasti jika data tidak cukup.

## 4. Hal yang Dapat Dilakukan
Berikan saran umum yang aman.

## 5. Kapan Harus ke Dokter
Jelaskan tanda bahaya yang perlu diperhatikan.

## 6. Pertanyaan Lanjutan
Berikan pertanyaan yang dapat membantu memperjelas keluhan.
"""

            with st.spinner(
                "MediCess AI sedang menganalisis keluhan..."
            ):

                generate_ai(
                    prompt,
                    uploaded_image,
                    "Medical Triage"
                )


# =====================================================
# DRUG SAFETY
# =====================================================

elif st.session_state.selected_page == "Drug Safety":

    st.title("💊 Drug Safety")

    st.write(
        "Dapatkan informasi umum mengenai obat, alergi, "
        "dan hal yang perlu dikonsultasikan kepada apoteker."
    )

    with st.form("drug_form"):

        medicines = st.text_area(
            "Nama obat yang sedang digunakan",
            placeholder="Contoh: Paracetamol, Amoxicillin...",
            height=120
        )

        allergies = st.text_area(
            "Apakah memiliki alergi obat?",
            placeholder="Tuliskan alergi yang diketahui."
        )

        conditions = st.text_area(
            "Kondisi kesehatan lain (opsional)",
            placeholder="Contoh: Asma, gangguan ginjal, sedang hamil..."
        )

        drug_submitted = st.form_submit_button(
            "Periksa Informasi Obat",
            use_container_width=True
        )

    if drug_submitted:

        if not medicines.strip():

            st.warning(
                "Masukkan nama obat terlebih dahulu."
            )

        else:

            prompt = f"""
{MEDICAL_SAFETY}

Pengguna meminta informasi umum mengenai obat.

Daftar obat:
{medicines}

Riwayat alergi:
{allergies if allergies else "Tidak disebutkan"}

Kondisi kesehatan:
{conditions if conditions else "Tidak disebutkan"}

Berikan jawaban:

## 1. Informasi Umum Obat
Jelaskan kegunaan umum masing-masing obat jika diketahui.

## 2. Hal yang Perlu Diperhatikan
Jelaskan efek samping umum dan peringatan yang relevan.

## 3. Potensi Interaksi
Sebutkan potensi interaksi hanya jika memiliki dasar informasi memadai.
Jika tidak yakin, katakan bahwa interaksi perlu diverifikasi oleh apoteker atau dokter.
Jangan mengklaim telah memeriksa database obat resmi.

## 4. Alergi dan Kondisi Khusus
Jelaskan hal yang perlu diperhatikan.

## 5. Saran Keamanan
Sarankan pengguna memeriksa kemasan dan berkonsultasi dengan apoteker/dokter.

Jangan memberikan dosis personal.
Jangan menyarankan menghentikan obat resep sendiri.
Jangan menyatakan kombinasi obat pasti aman hanya berdasarkan tebakan.
"""

            with st.spinner(
                "Memeriksa informasi obat..."
            ):

                generate_ai(
                    prompt,
                    feature_name="Drug Safety"
                )


# =====================================================
# RECOVERY PLANNER
# =====================================================

elif st.session_state.selected_page == "Recovery Planner":

    st.title("🌿 Recovery Planner")

    st.write(
        "Buat rencana pemulihan dan kebiasaan sehat secara umum."
    )

    with st.form("recovery_form"):

        recovery_condition = st.text_area(
            "Kondisi atau keluhan yang sedang dialami",
            placeholder="Contoh: Sedang dalam masa pemulihan setelah flu..."
        )

        activity = st.selectbox(
            "Tingkat aktivitas sehari-hari",
            [
                "Rendah / banyak istirahat",
                "Sedang",
                "Aktif"
            ]
        )

        sleep = st.selectbox(
            "Durasi tidur rata-rata",
            [
                "Kurang dari 5 jam",
                "5–6 jam",
                "7–8 jam",
                "Lebih dari 8 jam"
            ]
        )

        goal = st.selectbox(
            "Fokus utama",
            [
                "Pemulihan kondisi tubuh",
                "Meningkatkan kualitas tidur",
                "Menjaga pola makan",
                "Meningkatkan kebugaran",
                "Menjaga kesehatan secara umum"
            ]
        )

        recovery_submitted = st.form_submit_button(
            "Buat Rencana",
            use_container_width=True
        )

    if recovery_submitted:

        if not recovery_condition.strip():

            st.warning(
                "Silakan jelaskan kondisi terlebih dahulu."
            )

        else:

            prompt = f"""
{MEDICAL_SAFETY}

Buat rencana pemulihan dan kebiasaan sehat yang bersifat umum.

Kondisi:
{recovery_condition}

Aktivitas:
{activity}

Durasi tidur:
{sleep}

Fokus:
{goal}

Susun jawaban:

## 1. Ringkasan Kondisi
## 2. Rencana Harian
Buat tabel sederhana pagi, siang, sore, dan malam.
## 3. Pola Istirahat
## 4. Saran Makan dan Minum
## 5. Aktivitas yang Perlu Diperhatikan
## 6. Tanda Bahaya
## 7. Catatan Penting

Jangan memberikan terapi khusus atau menjanjikan kesembuhan.
Jika kondisi membutuhkan pengawasan medis, sarankan konsultasi dokter.
"""

            with st.spinner(
                "Menyusun rencana..."
            ):

                generate_ai(
                    prompt,
                    feature_name="Recovery Planner"
                )


# =====================================================
# HISTORY
# =====================================================

elif st.session_state.selected_page == "History":

    st.title("📚 Riwayat Analisis")

    st.write(
        "Riwayat analisis selama sesi aplikasi ini."
    )

    if not st.session_state.history:

        st.info(
            "Belum ada riwayat analisis."
        )

    else:

        if st.button("Hapus Semua Riwayat"):

            st.session_state.history = []
            st.rerun()

        for item in st.session_state.history:

            with st.expander(
                f"{item['feature']} — {item['time']}"
            ):

                st.markdown("**Permintaan:**")
                st.write(item["prompt"])

                st.markdown("**Hasil AI:**")
                st.markdown(item["response"])


# =====================================================
# ABOUT
# =====================================================

elif st.session_state.selected_page == "About":

    st.title("ℹ️ Tentang MediCess AI")

    st.markdown("""
    ## MediCess AI

    MediCess AI merupakan aplikasi asisten informasi kesehatan
    berbasis Artificial Intelligence yang dikembangkan menggunakan
    Streamlit dan Google Gemini.

    ### Fitur Utama

    - **Medical Triage:** Membantu memahami keluhan dan informasi urgensi.
    - **Drug Safety:** Memberikan informasi umum terkait obat dan keamanannya.
    - **Recovery Planner:** Membantu menyusun rencana kebiasaan sehat.
    - **History:** Menampilkan riwayat analisis selama sesi aplikasi.

    ### Teknologi

    - Python
    - Streamlit
    - Google Gemini API
    - Pillow

    ### Batasan Sistem

    MediCess AI bukan alat diagnosis medis, bukan pengganti dokter,
    dan tidak menjamin ketepatan informasi interaksi obat.
    Informasi penting harus diverifikasi melalui tenaga kesehatan profesional.
    """)


# =====================================================
# FOOTER
# =====================================================

show_footer()
