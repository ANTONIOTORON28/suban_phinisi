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
# LOAD DATA (FIX FINAL)
# ==========================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("dataset_kapal_preprocessing.csv")  # ✅ FIX FINAL KAMU
        df.columns = df.columns.str.strip()
        return df
    except FileNotFoundError:
        st.error("❌ dataset_kapal_preprocessing.csv tidak ditemukan!")
        st.stop()


df = load_data()


# ==========================================
# TEXT FEATURE
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
# MODEL SBERT
# ==========================================
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


model = load_model()


# ==========================================
# EMBEDDINGS
# ==========================================
@st.cache_resource
def create_embeddings(dataframe):
    return model.encode(
        dataframe["text"].astype(str).tolist(),
        show_progress_bar=False
    )


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
st.write("Cari paket wisata sesuai kebutuhan Anda")


kategori = st.selectbox(
    "Pilih Kategori Trip",
    df["kategori"].dropna().unique()
)

user_input = st.text_area(
    "Deskripsi perjalanan",
    placeholder="contoh: private trip, snorkeling, jacuzzi, sunset dinner"
)

top_n = st.slider("Top-N Rekomendasi", 1, 10, 5)


# ==========================================
# SEARCH
# ==========================================
if st.button("🔍 Cari Rekomendasi"):

    if user_input.strip() == "":
        st.warning("Isi deskripsi dulu ya")
        st.stop()

    query = f"{kategori} {user_input}"

    results = recommend(query, top_n)

    st.subheader("✨ Hasil Rekomendasi")

    for _, row in results.iterrows():

        col1, col2 = st.columns([1, 3])

        with col1:
            img = str(row.get("image_url", ""))
            if img.startswith("http"):
                st.image(img, use_container_width=True)

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
