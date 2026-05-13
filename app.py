# =========================================================
# SISTEM REKOMENDASI PAKET WISATA KAPAL PHINISI
# Implementasi Sentence-BERT + Content-Based Filtering
# Labuan Bajo
# =========================================================
#
# pip install streamlit pandas sentence-transformers scikit-learn pillow torch
#
# Struktur CSV yang dibutuhkan:
#   nama_paket, nama_kapal, kategori, harga, durasi, kapasitas,
#   destinasi, fasilitas, layanan, deskripsi, image_url, link, content
#
# Kolom "content" = gabungan semua teks yang sudah di-preprocess
# (nama_paket + destinasi + fasilitas + layanan + deskripsi)
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Phinisi RekoSystem — Labuan Bajo",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# LOAD DATA & MODEL (cached)
# =========================================================

@st.cache_data
def load_data():
    df = pd.read_csv("dataset_kapal_preprocessing")
    df["content"] = df["content"].fillna("")
    return df

@st.cache_resource
def load_model():
    # Model multilingual ringan & akurat untuk B.Indonesia
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

@st.cache_data
def get_corpus_embeddings(_model, contents):
    return _model.encode(contents, show_progress_bar=False)

df = load_data()
model = load_model()
corpus_embeddings = get_corpus_embeddings(model, df["content"].tolist())

# =========================================================
# FUNGSI REKOMENDASI SENTENCE-BERT
# =========================================================

def get_recommendations(query: str, top_k: int = 5, kategori: str = "Semua"):
    """
    1. Encode query dengan SBERT
    2. Hitung cosine similarity vs semua dokumen
    3. Filter kategori (opsional)
    4. Return top_k hasil diurutkan by similarity
    """
    query_embedding = model.encode([query])
    similarities = cosine_similarity(query_embedding, corpus_embeddings)[0]

    result_df = df.copy()
    result_df["similarity_score"] = similarities

    if kategori != "Semua":
        result_df = result_df[result_df["kategori"] == kategori]

    result_df = result_df.sort_values("similarity_score", ascending=False)
    return result_df.head(top_k).reset_index(drop=True)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Outfit:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }

.stApp {
    background: #03080f;
    color: #dce8f5;
    font-family: 'Outfit', sans-serif;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #03080f; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #0369a1, #06b6d4);
    border-radius: 99px;
}

.stApp::before {
    content: "";
    position: fixed; inset: 0;
    background:
        radial-gradient(ellipse 90% 55% at 5% 0%,  rgba(3,105,161,0.13) 0%, transparent 55%),
        radial-gradient(ellipse 70% 45% at 95% 95%, rgba(6,182,212,0.09) 0%, transparent 55%);
    pointer-events: none; z-index: 0;
}

.block-container {
    padding: 0 2.5rem 5rem !important;
    max-width: 1320px !important;
}

[data-testid="column"] { padding: 0 10px !important; }

/* ── HERO ── */
.hero {
    text-align: center;
    padding: 56px 20px 0;
    margin-bottom: 40px;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(6,182,212,0.08);
    border: 1px solid rgba(6,182,212,0.22);
    border-radius: 99px;
    padding: 7px 20px;
    font-size: 11px; font-weight: 600;
    letter-spacing: 0.14em; text-transform: uppercase;
    color: #22d3ee; margin-bottom: 22px;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(30px, 4.5vw, 58px);
    font-weight: 700; line-height: 1.12;
    background: linear-gradient(140deg, #f0f8ff 0%, #7dd3fc 45%, #22d3ee 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 10px;
}
.hero-subtitle {
    font-size: 13px; color: #3a6080;
    letter-spacing: 0.08em; text-transform: uppercase;
    margin-bottom: 14px;
}
.hero-desc {
    font-size: 15px; font-weight: 300;
    color: #4a7090; line-height: 1.75;
    max-width: 560px; margin: 0 auto;
}
.hero-divider {
    width: 100px; height: 1px;
    background: linear-gradient(90deg, transparent, #0ea5e9 50%, transparent);
    margin: 28px auto 0;
}

/* ── QUERY PANEL ── */
.query-panel {
    background: rgba(4,12,24,0.75);
    border: 1px solid rgba(6,182,212,0.14);
    border-radius: 28px;
    padding: 32px 36px;
    margin-bottom: 12px;
    backdrop-filter: blur(24px);
    box-shadow: 0 8px 40px rgba(0,0,0,0.40);
}
.query-heading {
    font-size: 11px; font-weight: 700;
    letter-spacing: 0.16em; text-transform: uppercase;
    color: #22d3ee; margin-bottom: 6px;
}
.query-hint {
    font-size: 13px; color: #2a5070; font-weight: 300;
    margin-bottom: 22px; line-height: 1.6;
}

/* ── TEXTAREA ── */
.stTextArea textarea {
    background: rgba(2,8,18,0.85) !important;
    border: 1px solid rgba(6,182,212,0.18) !important;
    border-radius: 18px !important;
    color: #dce8f5 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 15px !important;
    line-height: 1.7 !important;
    padding: 16px 20px !important;
    transition: border-color 0.25s, box-shadow 0.25s;
}
.stTextArea textarea:focus {
    border-color: rgba(6,182,212,0.50) !important;
    box-shadow: 0 0 0 3px rgba(6,182,212,0.10) !important;
}
.stTextArea textarea::placeholder { color: #2a4560 !important; }
.stTextArea label { display: none !important; }

/* ── SELECTBOX ── */
.stSelectbox > div > div {
    background: rgba(2,8,18,0.85) !important;
    border: 1px solid rgba(6,182,212,0.18) !important;
    border-radius: 16px !important;
    color: #dce8f5 !important;
    font-family: 'Outfit', sans-serif !important;
}
.stSelectbox label {
    color: #2a5070 !important;
    font-size: 11px !important; font-weight: 700 !important;
    letter-spacing: 0.14em !important; text-transform: uppercase !important;
    font-family: 'Outfit', sans-serif !important;
}

/* ── NUMBER INPUT ── */
.stNumberInput > div > div {
    background: rgba(2,8,18,0.85) !important;
    border: 1px solid rgba(6,182,212,0.18) !important;
    border-radius: 16px !important;
    color: #dce8f5 !important;
    font-family: 'Outfit', sans-serif !important;
}
.stNumberInput label {
    color: #2a5070 !important;
    font-size: 11px !important; font-weight: 700 !important;
    letter-spacing: 0.14em !important; text-transform: uppercase !important;
    font-family: 'Outfit', sans-serif !important;
}

/* ── BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #0369a1 0%, #0284c7 60%, #0ea5e9 100%) !important;
    color: white !important; border: none !important;
    border-radius: 16px !important; padding: 13px 32px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important; font-size: 15px !important;
    letter-spacing: 0.05em !important; width: 100% !important;
    box-shadow: 0 4px 24px rgba(14,165,233,0.30) !important;
    transition: all 0.25s !important;
}
.stButton > button:hover {
    box-shadow: 0 6px 32px rgba(14,165,233,0.45) !important;
    transform: translateY(-2px) !important;
}

/* ── RESULT HEADER ── */
.result-header {
    display: flex; align-items: center;
    justify-content: space-between;
    margin: 36px 0 20px;
    padding-bottom: 14px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    flex-wrap: wrap; gap: 10px;
}
.result-title {
    font-family: 'Playfair Display', serif;
    font-size: 22px; font-weight: 600;
    color: #bdd8f0;
}
.result-qtag {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(6,182,212,0.08);
    border: 1px solid rgba(6,182,212,0.20);
    border-radius: 10px; padding: 6px 14px;
    font-size: 13px; color: #22d3ee; font-weight: 500;
    max-width: 420px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}

/* ── VESSEL CARD ── */
.vessel-card {
    position: relative;
    background: linear-gradient(140deg,
        rgba(5,14,28,0.97) 0%, rgba(3,9,20,0.97) 100%
    );
    border-radius: 28px;
    border: 1px solid rgba(255,255,255,0.05);
    overflow: hidden; margin-bottom: 24px;
    transition: transform 0.32s cubic-bezier(.22,.68,0,1.15), box-shadow 0.32s;
    box-shadow: 0 2px 4px rgba(0,0,0,0.30), 0 16px 48px rgba(0,0,0,0.50);
}
.vessel-card::before {
    content: ""; position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #0ea5e9 40%, #22d3ee 60%, transparent);
    opacity: 0; transition: opacity 0.32s;
}
.vessel-card:hover { transform: translateY(-5px); }
.vessel-card:hover::before { opacity: 1; }
.card-inner { padding: 28px 30px; }

/* ── IMAGE ── */
.img-container {
    position: relative;
    border-radius: 18px; overflow: hidden;
}
.img-container::after {
    content: ""; position: absolute; inset: 0;
    background: linear-gradient(135deg,
        rgba(6,182,212,0.06) 0%, transparent 45%, rgba(0,0,0,0.25) 100%
    );
    pointer-events: none;
}

/* ── RANK BADGE ── */
.rank-badge {
    position: absolute; top: 14px; left: 14px;
    width: 38px; height: 38px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Playfair Display', serif;
    font-size: 16px; font-weight: 700;
    z-index: 10; border: 2px solid;
}
.rank-1 { background: rgba(250,204,21,0.18); border-color: rgba(250,204,21,0.55); color: #facc15; }
.rank-2 { background: rgba(203,213,225,0.14); border-color: rgba(203,213,225,0.40); color: #cbd5e1; }
.rank-3 { background: rgba(234,179,8,0.12); border-color: rgba(234,179,8,0.35); color: #eab308; }
.rank-n { background: rgba(6,182,212,0.10); border-color: rgba(6,182,212,0.28); color: #22d3ee; }

/* ── SIMILARITY METER ── */
.sim-wrap { margin-top: 14px; }
.sim-label {
    display: flex; justify-content: space-between; align-items: center;
    font-size: 11px; font-weight: 600;
    letter-spacing: 0.10em; text-transform: uppercase;
    color: #2a5070; margin-bottom: 6px;
}
.sim-label span { color: #22d3ee; font-size: 14px; font-weight: 700; letter-spacing: 0; }
.sim-bar-bg {
    height: 5px; background: rgba(255,255,255,0.05);
    border-radius: 99px; overflow: hidden;
}
.sim-bar-fill {
    height: 100%; border-radius: 99px;
    background: linear-gradient(90deg, #0369a1, #0ea5e9, #22d3ee);
}

/* ── KATEGORI PILL ── */
.kategori-pill {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 4px 13px; border-radius: 99px;
    font-size: 10px; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    margin-bottom: 12px;
}
.pill-vvip  { background: rgba(250,204,21,0.10); border: 1px solid rgba(250,204,21,0.28); color: #facc15; }
.pill-vip   { background: rgba(167,139,250,0.10); border: 1px solid rgba(167,139,250,0.28); color: #a78bfa; }
.pill-std   { background: rgba(52,211,153,0.10); border: 1px solid rgba(52,211,153,0.28); color: #34d399; }
.pill-other { background: rgba(6,182,212,0.10); border: 1px solid rgba(6,182,212,0.28); color: #22d3ee; }

/* ── VESSEL NAME ── */
.vessel-name {
    font-family: 'Playfair Display', serif;
    font-size: 26px; font-weight: 700;
    line-height: 1.18; color: #f0f8ff;
    margin-bottom: 4px;
}
.vessel-ship {
    font-size: 12.5px; color: #2a5070;
    letter-spacing: 0.04em; margin-bottom: 20px;
}
.vessel-ship b { color: #4a7090; font-weight: 500; }

/* ── INFO GRID ── */
.info-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 10px; margin-bottom: 18px;
}
.info-item {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.045);
    border-radius: 13px; padding: 11px 14px;
    transition: background 0.2s;
}
.info-item:hover { background: rgba(6,182,212,0.06); }
.info-lbl {
    font-size: 9.5px; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: #1e4060; margin-bottom: 4px;
}
.info-val { font-size: 14px; font-weight: 600; color: #c8dff0; }
.info-val.gold    { color: #fbbf24; }
.info-val.sky     { color: #38bdf8; }
.info-val.emerald { color: #34d399; }

/* ── SECTION TAG ── */
.sec-tag {
    font-size: 9.5px; font-weight: 700;
    letter-spacing: 0.14em; text-transform: uppercase;
    color: #1e4060; margin-bottom: 9px;
    display: flex; align-items: center; gap: 8px;
}
.sec-tag::after {
    content: ""; flex: 1; height: 1px;
    background: rgba(255,255,255,0.04);
}

/* ── CHIPS ── */
.chips { display: flex; flex-wrap: wrap; gap: 7px; margin-bottom: 14px; }
.chip {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 5px 12px; border-radius: 9px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    font-size: 12px; font-weight: 500; color: #5a8aaa;
    transition: all 0.2s; white-space: nowrap;
}
.chip:hover { background: rgba(6,182,212,0.09); border-color: rgba(6,182,212,0.22); color: #7dd3fc; }

/* ── DESTINASI ── */
.dest-row { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 16px; }
.dest-dot { width: 5px; height: 5px; border-radius: 50%; background: #0ea5e9; flex-shrink: 0; }
.dest-txt { font-size: 13px; color: #4a7090; }

/* ── DESCRIPTION ── */
.sdiv {
    height: 1px; margin: 16px 0;
    background: linear-gradient(90deg, rgba(6,182,212,0.12), rgba(255,255,255,0.03), transparent);
    border: none;
}
.desc-box {
    background: rgba(3,105,161,0.05);
    border-left: 2px solid rgba(14,165,233,0.22);
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
    font-size: 13px; color: #3a6080;
    line-height: 1.85; font-weight: 300;
    margin-bottom: 20px;
}

/* ── LINK BUTTON ── */
.stLinkButton a {
    background: linear-gradient(135deg, #0369a1, #0284c7, #0ea5e9) !important;
    color: white !important; border: none !important;
    border-radius: 13px !important; padding: 11px 26px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important; font-size: 13px !important;
    box-shadow: 0 4px 20px rgba(14,165,233,0.28) !important;
    text-decoration: none !important;
}

/* ── EMPTY STATE ── */
.empty-state { text-align: center; padding: 80px 20px; }
.empty-icon { font-size: 52px; margin-bottom: 18px; }
.empty-title {
    font-family: 'Playfair Display', serif;
    font-size: 26px; color: #2a4a6a; margin-bottom: 10px;
}
.empty-sub { font-size: 14px; color: #1e3a5a; line-height: 1.7; }

/* ── FOOTER ── */
.footer {
    text-align: center; padding: 52px 20px 24px;
    border-top: 1px solid rgba(255,255,255,0.03);
    margin-top: 60px;
}
.footer-title {
    font-family: 'Playfair Display', serif;
    font-size: 18px; color: #1e3a5a; margin-bottom: 6px;
}
.footer-sub { font-size: 11px; color: #102030; letter-spacing: 0.10em; text-transform: uppercase; }

</style>
""", unsafe_allow_html=True)

# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">
    <div class="hero-badge">⚓ &nbsp; Content-Based Filtering · Sentence-BERT</div>
    <div class="hero-title">Sistem Rekomendasi<br>Paket Wisata Phinisi</div>
    <div class="hero-subtitle">Labuan Bajo · Nusa Tenggara Timur</div>
    <div class="hero-desc">
        Deskripsikan wisata impian Anda, sistem akan menemukan kapal phinisi
        terbaik menggunakan kecerdasan semantik Sentence-BERT
    </div>
    <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# QUERY PANEL
# =========================================================

st.markdown('<div class="query-panel">', unsafe_allow_html=True)

st.markdown("""
<div class="query-heading">🔍 &nbsp; Deskripsikan Wisata Impian Anda</div>
<div class="query-hint">
    Tulis deskripsi wisata yang Anda inginkan — tujuan, aktivitas, fasilitas, durasi, atau anggaran.
    Semakin detail, semakin relevan rekomendasinya.
</div>
""", unsafe_allow_html=True)

query_input = st.text_area(
    "query",
    placeholder="Contoh: Saya ingin berlayar 3 hari di Komodo, snorkeling di Pink Beach, dengan kapal mewah berkapasitas keluarga...",
    height=110,
    key="query_main"
)

st.markdown("""
<div style="font-size:11px;color:#1e4060;letter-spacing:0.10em;text-transform:uppercase;font-weight:700;margin-bottom:10px;">
    💡 Contoh Query
</div>
<div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:4px;">
    <span style="padding:6px 13px;background:rgba(6,182,212,0.06);border:1px solid rgba(6,182,212,0.16);border-radius:10px;font-size:12px;color:#4a8aaa;">🤿 Snorkeling &amp; diving Komodo</span>
    <span style="padding:6px 13px;background:rgba(6,182,212,0.06);border:1px solid rgba(6,182,212,0.16);border-radius:10px;font-size:12px;color:#4a8aaa;">🏝️ Island hopping 5 hari keluarga</span>
    <span style="padding:6px 13px;background:rgba(6,182,212,0.06);border:1px solid rgba(6,182,212,0.16);border-radius:10px;font-size:12px;color:#4a8aaa;">👑 Kapal VVIP honeymoon mewah</span>
    <span style="padding:6px 13px;background:rgba(6,182,212,0.06);border:1px solid rgba(6,182,212,0.16);border-radius:10px;font-size:12px;color:#4a8aaa;">🐉 Trekking Pulau Komodo dragon</span>
    <span style="padding:6px 13px;background:rgba(6,182,212,0.06);border:1px solid rgba(6,182,212,0.16);border-radius:10px;font-size:12px;color:#4a8aaa;">📸 Sunset cruise Labuan Bajo</span>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# FILTER ROW
# =========================================================

col_kat, col_topk, col_btn = st.columns([1.8, 0.9, 1.0])

with col_kat:
    kategori_list = ["Semua"] + sorted(df["kategori"].dropna().unique().tolist())
    kategori_filter = st.selectbox("FILTER KATEGORI", kategori_list)

with col_topk:
    top_k = st.number_input("JUMLAH REKOMENDASI", min_value=1, max_value=20, value=5, step=1)

with col_btn:
    st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
    cari_btn = st.button("🔍  Cari Rekomendasi", use_container_width=True)

# =========================================================
# HELPERS
# =========================================================

def get_pill(kategori):
    k = str(kategori).upper()
    if "VVIP" in k: return f'<div class="kategori-pill pill-vvip">👑&nbsp;{kategori}</div>'
    if "VIP"  in k: return f'<div class="kategori-pill pill-vip">💎&nbsp;{kategori}</div>'
    if "STANDARD" in k or "STD" in k: return f'<div class="kategori-pill pill-std">⚡&nbsp;{kategori}</div>'
    return f'<div class="kategori-pill pill-other">🚢&nbsp;{kategori}</div>'

def rank_class(i):
    return ["rank-1","rank-2","rank-3"][i] if i < 3 else "rank-n"

# =========================================================
# SESSION STATE
# =========================================================

if "results" not in st.session_state:
    st.session_state.results = None
    st.session_state.last_query = ""

# =========================================================
# PROSES REKOMENDASI
# =========================================================

if cari_btn:
    if not query_input.strip():
        st.warning("⚠️  Silakan masukkan deskripsi wisata terlebih dahulu.")
    else:
        with st.spinner("🧠  Memproses embedding Sentence-BERT dan menghitung cosine similarity..."):
            results = get_recommendations(query_input.strip(), top_k=int(top_k), kategori=kategori_filter)
        st.session_state.results = results
        st.session_state.last_query = query_input.strip()

# =========================================================
# TAMPILKAN HASIL
# =========================================================

results     = st.session_state.results
last_query  = st.session_state.last_query

if results is not None and len(results) > 0:

    q_display = last_query[:65] + ("..." if len(last_query) > 65 else "")
    st.markdown(f"""
    <div class="result-header">
        <div class="result-title">✦ &nbsp;{len(results)} Rekomendasi Terbaik</div>
        <div class="result-qtag">🔍 &nbsp;"{q_display}"</div>
    </div>
    """, unsafe_allow_html=True)

    for i, row in results.iterrows():
        score     = float(row.get("similarity_score", 0))
        score_pct = min(score * 100, 100)

        st.markdown('<div class="vessel-card"><div class="card-inner">', unsafe_allow_html=True)

        col_img, col_detail = st.columns([1.05, 1.40])

        with col_img:
            st.markdown('<div class="img-container" style="position:relative">', unsafe_allow_html=True)
            st.image(row["image_url"], use_container_width=True)
            st.markdown(f"""
            <div class="rank-badge {rank_class(i)}" style="position:absolute;top:14px;left:14px;">
                {i+1}
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Similarity meter
            st.markdown(f"""
            <div class="sim-wrap">
                <div class="sim-label">
                    Skor Kesamaan Semantik
                    <span>{score:.4f}</span>
                </div>
                <div class="sim-bar-bg">
                    <div class="sim-bar-fill" style="width:{score_pct:.1f}%"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_detail:
            st.markdown(
                get_pill(row['kategori']) +
                f'<div class="vessel-name">{row["nama_paket"]}</div>' +
                f'<div class="vessel-ship">Kapal: <b>{row["nama_kapal"]}</b></div>',
                unsafe_allow_html=True
            )

            st.markdown(f"""
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-lbl">💰 Harga</div>
                    <div class="info-val gold">{row['harga']}</div>
                </div>
                <div class="info-item">
                    <div class="info-lbl">⏱ Durasi</div>
                    <div class="info-val sky">{row['durasi']}</div>
                </div>
                <div class="info-item">
                    <div class="info-lbl">👥 Kapasitas</div>
                    <div class="info-val emerald">{row['kapasitas']}</div>
                </div>
                <div class="info-item">
                    <div class="info-lbl">🏷 Kategori</div>
                    <div class="info-val">{row['kategori']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Destinasi
            st.markdown(f"""
            <div class="sec-tag">📍 Destinasi</div>
            <div class="dest-row">
                <div class="dest-dot"></div>
                <div class="dest-txt">{row['destinasi']}</div>
            </div>
            """, unsafe_allow_html=True)

            # Fasilitas
            fac_items = [f.strip() for f in str(row["fasilitas"]).split(",") if f.strip()]
            fac_html  = '<div class="sec-tag">✨ Fasilitas</div><div class="chips">'
            for f in fac_items:
                fac_html += f'<span class="chip">✦ {f}</span>'
            fac_html += '</div>'
            st.markdown(fac_html, unsafe_allow_html=True)

            # Layanan
            lay_items = [l.strip() for l in str(row["layanan"]).split(",") if l.strip()]
            lay_html  = '<div class="sec-tag">🏝️ Layanan</div><div class="chips">'
            for l in lay_items:
                lay_html += f'<span class="chip">◈ {l}</span>'
            lay_html += '</div>'
            st.markdown(lay_html, unsafe_allow_html=True)

        # Deskripsi
        st.markdown(f"""
        <div style="padding:0 4px 4px;">
            <div class="sdiv"></div>
            <div class="sec-tag">📋 Deskripsi Paket</div>
            <div class="desc-box">{row['deskripsi']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.link_button("⚓  Lihat Detail Kapal", row["link"])
        st.markdown("</div></div><div style='height:6px'></div>", unsafe_allow_html=True)

elif results is not None and len(results) == 0:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">⚓</div>
        <div class="empty-title">Tidak Ada Hasil Ditemukan</div>
        <div class="empty-sub">
            Tidak ada kapal yang cocok dengan query dan filter yang Anda pilih.<br>
            Coba gunakan kata kunci berbeda atau ubah filter kategori.
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    # Landing state — belum ada query
    st.markdown("""
    <div style="text-align:center; padding:72px 20px 48px;">
        <div style="font-size:56px;margin-bottom:20px;opacity:0.4">🚢</div>
        <div style="font-family:'Playfair Display',serif;font-size:26px;color:#2a4a6a;margin-bottom:12px;">
            Mulai Temukan Kapal Impian Anda
        </div>
        <div style="font-size:14px;color:#1e3a5a;line-height:1.8;max-width:480px;margin:0 auto;">
            Ketikkan deskripsi wisata yang Anda inginkan di atas,<br>
            lalu klik <strong style="color:#0ea5e9">Cari Rekomendasi</strong> untuk mendapatkan<br>
            hasil berbasis kecerdasan semantik Sentence-BERT.
        </div>
        <div style="margin-top:32px;display:flex;justify-content:center;gap:20px;flex-wrap:wrap;">
            <div style="text-align:center;padding:20px 22px;background:rgba(6,182,212,0.05);border:1px solid rgba(6,182,212,0.10);border-radius:16px;min-width:140px;">
                <div style="font-size:28px;margin-bottom:10px;">🧠</div>
                <div style="font-size:11px;color:#1e4060;font-weight:700;letter-spacing:0.10em;text-transform:uppercase;">Sentence-BERT</div>
                <div style="font-size:12px;color:#1a3050;margin-top:4px;">Pemahaman semantik</div>
            </div>
            <div style="text-align:center;padding:20px 22px;background:rgba(6,182,212,0.05);border:1px solid rgba(6,182,212,0.10);border-radius:16px;min-width:140px;">
                <div style="font-size:28px;margin-bottom:10px;">📐</div>
                <div style="font-size:11px;color:#1e4060;font-weight:700;letter-spacing:0.10em;text-transform:uppercase;">Cosine Similarity</div>
                <div style="font-size:12px;color:#1a3050;margin-top:4px;">Pengukuran relevansi</div>
            </div>
            <div style="text-align:center;padding:20px 22px;background:rgba(6,182,212,0.05);border:1px solid rgba(6,182,212,0.10);border-radius:16px;min-width:140px;">
                <div style="font-size:28px;margin-bottom:10px;">🎯</div>
                <div style="font-size:11px;color:#1e4060;font-weight:700;letter-spacing:0.10em;text-transform:uppercase;">Content-Based</div>
                <div style="font-size:12px;color:#1a3050;margin-top:4px;">Filter berbasis konten</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    <div class="footer-title">⚓ Phinisi Recommendation System</div>
    <div class="footer-sub">
        Implementasi Sentence-BERT · Content-Based Filtering · Labuan Bajo
    </div>
</div>
""", unsafe_allow_html=True)
