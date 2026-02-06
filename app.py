import streamlit as st
import time

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="💬 JomKecek: Chatbot Dialek Kelantan",
    page_icon="🌾",
    layout="centered"
)

# ================= CUSTOM CSS (Elegant Theme) =================
st.markdown("""
<style>
.main { background-color: #FFF9F0; }
section[data-testid="stSidebar"] { background-color: #800000; color: white; }
section[data-testid="stSidebar"] * { color: white; }
.chat-user {
    background:#800000; color:white; padding:12px 16px;
    border-radius:18px 18px 2px 18px; max-width:80%;
    float:right; clear:both; margin:8px 0;
}
.chat-bot {
    background:#F5DEB3; color:#3E2723; padding:12px 16px;
    border-radius:18px 18px 18px 2px; max-width:80%;
    float:left; clear:both; margin:8px 0;
    border: 1px solid #D2B48C;
}
[data-testid="stMetricValue"] { color: #FFD700 !important; font-weight: bold; } /* Warna Emas untuk Skor */
</style>
""", unsafe_allow_html=True)

# ================= DUMMY LOGIC =================
def dummy_chatbot_pipeline(user_input, mode, more_info=False):
    query = user_input.lower().strip()

    # ===== TERJEMAHAN DIALEK =====
    if mode == "Terjemahan Dialek":

        if more_info:
            return (
                "🔍 **Analisis Token & Contoh Ayat:**\n\n"
                "1. **Demo (Kamu)**: *Demo tok sey makey ko?* (Kamu tak nak makan ke?)\n"
                "2. **Nok (Nak)**: *Ambo nok gi spital* (Saya nak pergi hospital)\n"
                "3. **Makey (Makan)**: *Demo tok sey makey ko?* (Kamu tak nak makan ke?)\n"
                "4. **Gapo (Apa)**: *Gapo hok dio nok?* (Apa yang dia nak?)"
            )

        # Dialek → Bahasa Melayu
        if "demo nok makey gapo" in query:
            return "📝 **Terjemahan BM:** Kamu nak makan apa?"

        # Bahasa Melayu → Dialek
        if "kamu nak makan apa" in query:
            return "📝 **Terjemahan Dialek:** Demo nok makey gapo?"

        # Default fallback
        return "📝 **Terjemahan:** " + user_input

    # ===== PELANCONGAN / TOUR GUIDE =====
    elif mode == "Pelancongan / Tour Guide":

        # --- Tempat Menarik ---
        if any(x in query for x in ["tempat menarik", "destinasi"]):
            return (
                "📌 **Antara tempat menarik di negeri Kelantan ialah:**\n\n"
                "1. **Pasar Siti Khadijah** – Syurga makanan dan kraftangan tempatan.\n"
                "2. **Pantai Cahaya Bulan** – Destinasi popular untuk berkeluarga.\n"
                "3. **Masjid Muhammadi** – Landmark bersejarah di Kota Bharu."
            )

        # --- Budaya ---
        elif any(x in query for x in ["budaya", "kesenian", "tradisi"]):
            return (
                "🎭 **Budaya Tradisional Kelantan:**\n\n"
                "1. **Dikir Barat** – Persembahan nyanyian dan puisi rakyat.\n"
                "2. **Mak Yong** – Teater tradisional Melayu (Warisan UNESCO).\n"
                "3. **Wayang Kulit** – Seni penceritaan berunsur legenda."
            )

        # --- Makanan ---
        elif any(x in query for x in ["makanan", "makan", "makanan tradisional"]):
            return (
                "🍽️ **Makanan Tradisional Kelantan:**\n\n"
                "1. **Nasi Kerabu** – Hidangan ikonik berwarna biru dengan budu.\n"
                "2. **Budu** – Sos ikan fermentasi identiti Kelantan.\n"
                "3. **Akok** – Kuih tradisional berasaskan telur dan santan."
            )

        # --- Default ---
        return "Jawapan Pelancongan untuk: " + user_input

# ================= SIDEBAR (METRICS SECTION) =================
with st.sidebar:
    st.markdown("# 🌾 Jom Kecek")
    mode = st.radio("Fungsi:", ["Terjemahan Dialek", "Pelancongan / Tour Guide"])

    st.divider()

    # --- EVALUATION METRICS PANEL ---
    st.markdown("### 📊 Prestasi Model (D3)")

    # ROUGE-L (Traditional NLP)
    st.metric(label="ROUGE-L Score", value="0.8562", delta="Tinggi")

    st.markdown("---")

    # RAG Triad (DeepEval)
    st.markdown("**Triad RAG (DeepEval)**")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Faithfulness", value="0.92")
    with col2:
        st.metric(label="Relevancy", value="0.88")

    st.metric(label="Contextual Precision", value="0.90")

    st.divider()
    if st.button("🧹 Reset Sembang"):
        st.session_state.messages = []
        st.rerun()

# ================= MAIN UI =================
st.title("💬 JomKecek")
st.caption("Visual Demo: LLM + RAG System 🌾")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Gapo dio kito buleh tulung hari ni? 😊"}]

for msg in st.session_state.messages:
    cls = "chat-user" if msg["role"] == "user" else "chat-bot"
    st.markdown(f"<div class='{cls}'>{msg['content']}</div>", unsafe_allow_html=True)

# Input chat
if prompt := st.chat_input("Taip di sini..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Menjana..."):
        time.sleep(0.5)
        response = dummy_chatbot_pipeline(prompt, mode)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.last_response = response  # SIMPAN respons terbaru
    st.rerun()

# ================= Tombol "Lebih Informasi" =================
# Hanya muncul jika mode Terjemahan dan jawapan mengandungi BM/Dialek
last_resp = st.session_state.get("last_response", "")
if mode == "Terjemahan Dialek" and ("Terjemahan BM" in last_resp or "Terjemahan Dialek" in last_resp):
    if st.button("🔍 Lebih Informasi"):
        st.info(dummy_chatbot_pipeline("", mode, more_info=True))
