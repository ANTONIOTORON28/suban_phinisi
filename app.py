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
# LOAD DATA
# ==========================================
@st.cache_data
def load_data():
    df = pd.read_csv("dataset_kapal_preprocessing.csv")
    df.columns = df.columns.str.strip()
    return df


df = load_data()


# ==========================================
# CREATE TEXT REPRESENTATION (WAJIB)
# ==========================================
def build_text(row):
    return " ".join([
        str(row.get("nama_paket", "")),
        str(row.get("nama_kapal", "")),
        str(row.get("kategori", "")),
        str(row.get("tipe_trip", "")),
        str(row.get("durasi", "")),
        str(row.get("fasilitas", "")),
        str(row.get("layanan", "")),
        str(row.get("destinasi", "")),
        str(row.get("deskripsi", ""))
    ])


df["processed_text"] = df.apply(build_text, axis=1)


# ==========================================
# LOAD MODEL
# ==========================================
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


model = load_model()


# ==========================================
# EMBEDDINGS
# ==========================================
@st.cache_resource
def create_embeddings(texts):
    return model.encode(list(texts), show_progress_bar=False)


embeddings = create_embeddings(df["processed_text"])


# ==========================================
# RECOMMENDATION FUNCTION
# ==========================================
def recommend(query, top_n):
    query_vec = model.encode([query])

    scores = cosine_similarity(query_vec, embeddings)[0]

    top_idx = np.argsort(scores)[::-1][:top_n]

    result = df.iloc[top_idx].copy()
    result["score"] = scores[top_idx]

    return result


# ==========================================
# UI
# ==========================================
st.title("🚢 Sistem Rekomendasi Paket Wisata Kapal Phinisi (SBERT)")
st.write("Rekomendasi berbasis kemiripan paket wisata, bukan keyword biasa.")


# ==========================================
# INPUT (FOKUS PAKET, BUKAN DESKRIPSI)
# ==========================================
kategori = st.selectbox(
    "Pilih Kategori Paket",
    df["kategori"].dropna().unique()
)

top_n = st.slider("Top-N Rekomendasi", 1, 10, 5)

user_desc = st.text_area(
    "Tambahan kebutuhan (opsional)",
    placeholder="contoh: snorkeling, jacuzzi, sunset dinner, private chef"
)


# ==========================================
# SEARCH
# ==========================================
if st.button("🔍 Cari Rekomendasi"):

    # 🔥 FIX KONSEP UTAMA: PAKET ADALAH UTAMA
    if user_desc.strip() == "":
        query = kategori
    else:
        query = f"{kategori} {user_desc}"


    results = recommend(query, top_n)


    st.subheader("✨ Hasil Rekomendasi Terbaik")


    for _, row in results.iterrows():

        col_img, col_info = st.columns([1, 3])

        # ================= IMAGE =================
        with col_img:
            img = str(row.get("image_url", ""))

            if img.startswith("http"):
                st.image(img, use_container_width=True)
            else:
                st.image("https://via.placeholder.com/300x200")


        # ================= INFO =================
        with col_info:
            st.markdown(f"""
## {row.get('nama_paket','-')}

**Kapal:** {row.get('nama_kapal','-')}  
**Kategori:** {row.get('kategori','-')}  
**Tipe Trip:** {row.get('tipe_trip','-')}  
**Harga:** {row.get('harga','-')}  
**Durasi:** {row.get('durasi','-')}  

**Destinasi:** {row.get('destinasi','-')}  
**Fasilitas:** {row.get('fasilitas','-')}  
**Layanan:** {row.get('layanan','-')}  

**Similarity Score:** {row['score']:.4f}
""")

        st.divider()
