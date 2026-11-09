
import streamlit as st
from google import genai
from PIL import Image
from datetime import datetime

# =====================================================
# KONFIGURASI APLIKASI
# =====================================================

st.set_page_config(
    page_title="MediCess AI",
    page_icon="🏥",
    layout="wide"
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
# PROMPT KEAMANAN MEDIS
# =====================================================

MEDICAL_SAFETY = """
Anda adalah MediCess AI, asisten informasi kesehatan berbasis AI.

Aturan:
1. Anda bukan dokter dan tidak boleh mengaku sebagai dokter.
2. Jangan memberikan diagnosis pasti.
3. Berikan informasi untuk tujuan edukasi.
4. Jangan mengarang fakta medis.
5. Jika informasi tidak cukup, jelaskan keterbatasannya.
6. Jangan menyarankan menghentikan obat resep tanpa arahan dokter.
7. Jangan memberikan dosis obat personal.
8. Jika terdapat gejala darurat seperti sesak napas berat,
   nyeri dada berat, penurunan kesadaran, kejang, perdarahan berat,
   atau gejala stroke, sarankan segera mencari pertolongan medis darurat.
9. Gunakan bahasa Indonesia yang mudah dipahami.
"""


# =====================================================
# GEMINI API
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
# FUNGSI GENERATE AI
# =====================================================

def generate_ai(prompt, uploaded_image=None, feature_name="MediCess AI"):

    client = get_client()

    if client is None:
        st.error("API Key Gemini belum diisi.")
        return

    contents = [prompt]

    # Jika pengguna mengunggah gambar
    if uploaded_image is not None:

        try:
            image = Image.open(uploaded_image).convert("RGB")
            image.thumbnail((1024, 1024))
            contents.append(image)

        except Exception as e:
            st.error(f"Gagal membaca gambar: {e}")
            return

    response_placeholder = st.empty()
    full_response = ""

    try:

        with st.spinner("MediCess AI sedang memproses..."):

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

        # Simpan riwayat
        if full_response.strip():

            st.session_state.history.insert(0, {
                "feature": feature_name,
                "time": datetime.now().strftime("%d-%m-%Y %H:%M"),
                "prompt": prompt,
                "response": full_response
            })

    except Exception as e:

        st.error("Terjadi kesalahan saat menghubungi Gemini API.")
        st.code(str(e))


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🏥 MediCess AI")

    st.caption("Intelligent Healthcare Assistant")

    st.divider()

    st.subheader("Menu Utama")

    pages = [
        "Dashboard",
        "Medical Triage",
        "Drug Safety",
        "Recovery Planner",
        "History",
        "About"
    ]

    selected_page = st.radio(
        "Pilih halaman",
        pages,
        index=pages.index(st.session_state.selected_page),
        label_visibility="collapsed"
    )

    st.session_state.selected_page = selected_page

    st.divider()

    st.subheader("Pengaturan API")

    st.text_input(
        "Gemini API Key",
        type="password",
        key="api_key",
        placeholder="Masukkan API Key"
    )

    st.caption(
        "API Key digunakan untuk menghubungkan aplikasi dengan Gemini."
    )

    st.divider()

    st.caption("MediCess AI Version 1.0")


# =====================================================
# DASHBOARD
# =====================================================

if st.session_state.selected_page == "Dashboard":

    st.title("🏥 Welcome to MediCess AI")

    st.subheader("Your Health, Smarter.")

    st.write(
        "MediCess AI merupakan asisten informasi kesehatan "
        "berbasis Artificial Intelligence untuk membantu "
        "memahami informasi kesehatan secara lebih mudah."
    )

    st.divider()

    st.header("Selamat Datang 👋")

    st.write(
        "MediCess AI membantu Anda memahami informasi kesehatan "
        "melalui teknologi Artificial Intelligence."
    )

    st.divider()

    st.header("Fitur Utama")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🩺 Medical Triage")
        st.write(
            "Membantu memahami keluhan dan informasi tingkat urgensi gejala."
        )

    with col2:
        st.subheader("💊 Drug Safety")
        st.write(
            "Memberikan informasi umum mengenai obat dan hal yang perlu diperhatikan."
        )

    with col3:
        st.subheader("🌿 Recovery Planner")
        st.write(
            "Membantu menyusun rencana kebiasaan sehat dan pemulihan umum."
        )

    st.divider()

    st.header("Mulai Menggunakan Fitur")

    st.write("Pilih layanan MediCess AI sesuai kebutuhan Anda.")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🩺 Medical Triage", use_container_width=True):
            st.session_state.selected_page = "Medical Triage"
            st.rerun()

    with col2:
        if st.button("💊 Drug Safety", use_container_width=True):
            st.session_state.selected_page = "Drug Safety"
            st.rerun()

    with col3:
        if st.button("🌿 Recovery Planner", use_container_width=True):
            st.session_state.selected_page = "Recovery Planner"
            st.rerun()

    st.divider()

    st.info(
        "MediCess AI adalah alat bantu informasi kesehatan, "
        "bukan pengganti diagnosis dan konsultasi dengan dokter."
    )


# =====================================================
# MEDICAL TRIAGE
# =====================================================

elif st.session_state.selected_page == "Medical Triage":

    st.title("🩺 Medical Triage")

    st.write(
        "Masukkan keluhan yang sedang Anda alami untuk mendapatkan "
        "informasi kesehatan dari MediCess AI."
    )

    st.divider()

    with st.form("triage_form"):

        symptoms = st.text_area(
            "Gejala atau keluhan",
            placeholder="Contoh: Saya mengalami demam, batuk, dan sakit kepala...",
            height=150
        )

        duration = st.text_input(
            "Lama gejala dirasakan",
            placeholder="Contoh: 2 hari"
        )

        age = st.number_input(
            "Usia",
            min_value=0,
            max_value=120,
            value=20
        )

        uploaded_image = st.file_uploader(
            "Unggah gambar (opsional)",
            type=["jpg", "jpeg", "png"]
        )

        submitted = st.form_submit_button(
            "Analisis Keluhan",
            use_container_width=True
        )

    if uploaded_image is not None:
        st.image(
            uploaded_image,
            caption="Gambar yang diunggah",
            width=300
        )

    if submitted:

        if not symptoms.strip():

            st.warning("Silakan masukkan keluhan terlebih dahulu.")

        else:

            prompt = f"""
{MEDICAL_SAFETY}

Bantu pengguna memahami keluhan berikut.

Usia: {age}
Gejala: {symptoms}
Durasi: {duration if duration else "Tidak disebutkan"}

Jika terdapat gambar, jelaskan hanya hal yang terlihat.
Jangan memastikan penyakit berdasarkan gambar.

Buat jawaban dengan format:

## 1. Ringkasan Keluhan
## 2. Kemungkinan Penjelasan
## 3. Tingkat Urgensi
## 4. Hal yang Dapat Dilakukan
## 5. Kapan Harus ke Dokter
## 6. Pertanyaan Lanjutan

Jangan memberikan diagnosis pasti.
Jika informasi tidak cukup, jelaskan keterbatasannya.
"""

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
        "dan potensi interaksi yang perlu dikonsultasikan."
    )

    st.divider()

    with st.form("drug_form"):

        medicines = st.text_area(
            "Nama obat",
            placeholder="Contoh: Paracetamol, Amoxicillin...",
            height=120
        )

        allergies = st.text_area(
            "Riwayat alergi obat",
            placeholder="Contoh: Alergi terhadap obat tertentu."
        )

        conditions = st.text_area(
            "Kondisi kesehatan lain (opsional)",
            placeholder="Contoh: Asma, gangguan ginjal, sedang hamil..."
        )

        submitted = st.form_submit_button(
            "Periksa Informasi Obat",
            use_container_width=True
        )

    if submitted:

        if not medicines.strip():

            st.warning("Masukkan nama obat terlebih dahulu.")

        else:

            prompt = f"""
{MEDICAL_SAFETY}

Berikan informasi umum mengenai obat berikut.

Daftar obat:
{medicines}

Riwayat alergi:
{allergies if allergies else "Tidak disebutkan"}

Kondisi kesehatan:
{conditions if conditions else "Tidak disebutkan"}

Buat jawaban dengan format:

## 1. Informasi Umum Obat
## 2. Kegunaan Obat
## 3. Efek Samping yang Perlu Diperhatikan
## 4. Potensi Interaksi
## 5. Perhatian terhadap Alergi
## 6. Saran Keamanan

Jangan mengklaim telah memeriksa database obat resmi.
Jangan mengarang interaksi obat.
Jika tidak yakin, sarankan verifikasi kepada apoteker atau dokter.
Jangan memberikan dosis personal atau menyarankan menghentikan obat resep.
"""

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
        "Buat rencana kebiasaan sehat dan pemulihan secara umum."
    )

    st.divider()

    with st.form("recovery_form"):

        condition = st.text_area(
            "Kondisi yang sedang dialami",
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
            "Durasi tidur",
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
                "Menjaga kesehatan umum"
            ]
        )

        submitted = st.form_submit_button(
            "Buat Rencana",
            use_container_width=True
        )

    if submitted:

        if not condition.strip():

            st.warning("Silakan jelaskan kondisi terlebih dahulu.")

        else:

            prompt = f"""
{MEDICAL_SAFETY}

Buat rencana kebiasaan sehat dan pemulihan umum.

Kondisi:
{condition}

Aktivitas:
{activity}

Durasi tidur:
{sleep}

Fokus:
{goal}

Susun jawaban dengan format:

## 1. Ringkasan Kondisi
## 2. Rencana Aktivitas Harian
## 3. Pola Istirahat
## 4. Saran Makan dan Minum
## 5. Aktivitas yang Perlu Diperhatikan
## 6. Tanda Bahaya
## 7. Catatan Penting

Jangan memberikan terapi khusus atau menjanjikan kesembuhan.
"""

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
        "Berikut adalah riwayat analisis selama sesi aplikasi berlangsung."
    )

    st.divider()

    if not st.session_state.history:

        st.info("Belum ada riwayat analisis.")

    else:

        if st.button("Hapus Semua Riwayat"):

            st.session_state.history = []
            st.rerun()

        for index, item in enumerate(st.session_state.history):

            with st.expander(
                f"{item['feature']} - {item['time']}"
            ):

                st.subheader("Permintaan")
                st.write(item["prompt"])

                st.subheader("Hasil Analisis")
                st.markdown(item["response"])


# =====================================================
# ABOUT
# =====================================================

elif st.session_state.selected_page == "About":

    st.title("ℹ️ Tentang MediCess AI")

    st.divider()

    st.header("MediCess AI")

    st.write(
        "MediCess AI merupakan aplikasi asisten informasi kesehatan "
        "berbasis Artificial Intelligence yang dikembangkan menggunakan "
        "Python, Streamlit, dan Google Gemini."
    )

    st.subheader("Fitur Aplikasi")

    st.markdown("""
    1. **Medical Triage**

       Membantu memahami keluhan dan informasi tingkat urgensi gejala.

    2. **Drug Safety**

       Memberikan informasi umum mengenai obat dan hal yang perlu diperhatikan.

    3. **Recovery Planner**

       Membantu menyusun rencana kebiasaan sehat dan pemulihan umum.

    4. **History**

       Menampilkan riwayat analisis selama sesi aplikasi.
    """)

    st.subheader("Teknologi yang Digunakan")

    st.markdown("""
    - Python
    - Streamlit
    - Google Gemini API
    - Pillow
    """)

    st.subheader("Disclaimer")

    st.warning(
        "MediCess AI bukan alat diagnosis medis dan tidak menggantikan "
        "pemeriksaan dokter. Informasi obat harus diverifikasi oleh "
        "dokter atau apoteker."
    )


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption("🏥 MediCess AI | Intelligent Healthcare Assistant")

st.caption("Powered by Google Gemini")

st.caption(
    "© 2026 MediCess AI. Informasi AI bukan pengganti konsultasi medis."
)
