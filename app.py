import streamlit as st
import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# ==========================================
# CONFIG
# ==========================================
st.set_page_config(
    page_title="Rekomendasi Paket Wisata Phinisi",
    page_icon="🚢",
    layout="wide"
)


# ==========================================
# LOAD DATA (FIX: suban.csv)
# ==========================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("suban.csv")  # ✅ FIX UTAMA KAMU
        df.columns = df.columns.str.strip()
        return df
    except FileNotFoundError:
        st.error("❌ File suban.csv tidak ditemukan di repository!")
        st.stop()


df = load_data()


# ==========================================
# BUILD TEXT FEATURE (WAJIB SBERT)
# ==========================================
def build_text(row):
    return " ".join([
        str(row.get("nama_paket", "")),
        str(row.get("nama_kapal", "")),
        str(row.get("kategori", "")),
        str(row.get("durasi", "")),
        str(row.get("fasilitas", "")),
        str(row.get("layanan", "")),
        str(row.get("destinasi", "")),
        str(row.get("deskripsi", ""))
    ])


df["text"] = df.apply(build_text, axis=1)


# ==========================================
# LOAD MODEL SBERT
# ==========================================
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


model = load_model()


# ==========================================
# CREATE EMBEDDINGS
# ==========================================
@st.cache_resource
def create_embeddings(dataframe):
    texts = dataframe["text"].astype(str).tolist()
    return model.encode(texts, show_progress_bar=False)


embeddings = create_embeddings(df)


# ==========================================
# RECOMMENDATION ENGINE
# ==========================================
def recommend(query, top_n=5):

    query_vec = model.encode([query])

    scores = cosine_similarity(query_vec, embeddings)[0]

    top_idx = np.argsort(scores)[::-1][:top_n]

    results = df.iloc[top_idx].copy()
    results["score"] = scores[top_idx]

    return results


# ==========================================
# UI
# ==========================================
st.title("🚢 Sistem Rekomendasi Paket Wisata Phinisi (SBERT)")
st.write("Cari paket wisata terbaik berdasarkan preferensi Anda")


kategori = st.selectbox(
    "Pilih Kategori Trip",
    df["kategori"].dropna().unique()
)

user_input = st.text_area(
    "Deskripsi kebutuhan wisata",
    placeholder="contoh: private trip, snorkeling, jacuzzi, sunset dinner"
)

top_n = st.slider("Jumlah Rekomendasi", 1, 10, 5)


# ==========================================
# SEARCH BUTTON
# ==========================================
if st.button("🔍 Cari Rekomendasi"):

    if user_input.strip() == "":
        st.warning("Silakan isi deskripsi perjalanan.")
        st.stop()

    query = f"{kategori} {user_input}"

    results = recommend(query, top_n)

    st.subheader("✨ Hasil Rekomendasi Terbaik")

    for i, row in results.iterrows():

        col1, col2 = st.columns([1, 3])

        # ================= IMAGE =================
        with col1:
            img = str(row.get("image_url", ""))

            if img.startswith("http"):
                st.image(img, use_container_width=True)

        # ================= INFO =================
        with col2:
            st.markdown(f"""
            ## {row.get('nama_paket','-')}

            **Kapal:** {row.get('nama_kapal','-')}  
            **Kategori:** {row.get('kategori','-')}  
            **Harga:** {row.get('harga','-')}  
            **Durasi:** {row.get('durasi','-')}  

            **Destinasi:** {row.get('destinasi','-')}  
            **Fasilitas:** {row.get('fasilitas','-')}  
            **Layanan:** {row.get('layanan','-')}  

            **Similarity Score:** {row['score']:.4f}
            """)

        st.divider()
