# =========================================================
# PHINISI RECOMMENDATION SYSTEM
# Ultra-Modern Dark UI — Ocean Luxury Edition
# =========================================================

# pip install streamlit pandas pillow

import streamlit as st
import pandas as pd

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Phinisi — Luxury Voyage",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv("dataset_kapal_preprocessing.csv")

# =========================================================
# CUSTOM CSS — Ultra Modern Ocean Dark Theme
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── RESET & BASE ── */
*, *::before, *::after { box-sizing: border-box; }

.stApp {
    background: #050d1a;
    color: #e8edf5;
    font-family: 'DM Sans', sans-serif;
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #050d1a; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #1e40af, #0ea5e9);
    border-radius: 99px;
}

/* ── ANIMATED BACKGROUND MESH ── */
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 50% at 10% 0%, rgba(14,165,233,0.10) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 90% 100%, rgba(30,64,175,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 40% 30% at 50% 50%, rgba(6,182,212,0.04) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

/* ── HERO HEADER ── */
.hero-wrap {
    position: relative;
    padding: 52px 0 36px;
    margin-bottom: 8px;
    text-align: center;
}

.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(14,165,233,0.10);
    border: 1px solid rgba(14,165,233,0.25);
    border-radius: 99px;
    padding: 6px 18px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #38bdf8;
    margin-bottom: 20px;
}

.hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(36px, 5vw, 62px);
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #ffffff 0%, #93c5fd 50%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 14px;
}

.hero-sub {
    font-size: 16px;
    font-weight: 300;
    color: #7090b0;
    letter-spacing: 0.02em;
    max-width: 500px;
    margin: 0 auto 10px;
    line-height: 1.6;
}

.hero-line {
    width: 80px;
    height: 2px;
    background: linear-gradient(90deg, transparent, #0ea5e9, transparent);
    margin: 24px auto 0;
    border-radius: 99px;
}

/* ── SEARCH BAR ── */
.stTextInput > div > div {
    background: rgba(8,20,40,0.80) !important;
    border: 1px solid rgba(14,165,233,0.20) !important;
    border-radius: 16px !important;
    color: white !important;
    padding: 4px 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    transition: border-color 0.25s, box-shadow 0.25s;
    backdrop-filter: blur(12px);
}
.stTextInput > div > div:focus-within {
    border-color: rgba(14,165,233,0.60) !important;
    box-shadow: 0 0 0 3px rgba(14,165,233,0.12), 0 8px 24px rgba(0,0,0,0.3) !important;
}
.stTextInput input {
    color: white !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput input::placeholder { color: #506070 !important; }
.stTextInput label {
    color: #7090b0 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── SELECTBOX ── */
.stSelectbox > div > div {
    background: rgba(8,20,40,0.80) !important;
    border: 1px solid rgba(14,165,233,0.20) !important;
    border-radius: 16px !important;
    color: white !important;
    font-family: 'DM Sans', sans-serif !important;
    backdrop-filter: blur(12px);
    transition: border-color 0.25s;
}
.stSelectbox > div > div:hover {
    border-color: rgba(14,165,233,0.40) !important;
}
.stSelectbox label {
    color: #7090b0 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── FILTER PANEL ── */
.filter-wrap {
    background: rgba(6,15,30,0.70);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 24px;
    padding: 24px 28px;
    margin-bottom: 32px;
    backdrop-filter: blur(20px);
    display: flex;
    align-items: flex-end;
    gap: 16px;
}

/* ── RESULT COUNT ── */
.result-count {
    font-size: 13px;
    color: #506070;
    font-weight: 400;
    letter-spacing: 0.04em;
    margin-bottom: 24px;
    padding-left: 2px;
}
.result-count span {
    color: #38bdf8;
    font-weight: 700;
}

/* ── VESSEL CARD ── */
.vessel-card {
    position: relative;
    background: linear-gradient(
        135deg,
        rgba(8,18,35,0.98) 0%,
        rgba(6,14,28,0.98) 100%
    );
    border-radius: 32px;
    border: 1px solid rgba(255,255,255,0.06);
    overflow: hidden;
    margin-bottom: 28px;
    transition: transform 0.35s cubic-bezier(.22,.68,0,1.2), box-shadow 0.35s;
    box-shadow:
        0 4px 6px rgba(0,0,0,0.3),
        0 20px 60px rgba(0,0,0,0.5),
        inset 0 1px 0 rgba(255,255,255,0.04);
}

.vessel-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #0ea5e9 40%, #38bdf8 60%, transparent);
    opacity: 0;
    transition: opacity 0.35s;
}

.vessel-card:hover {
    transform: translateY(-4px);
    box-shadow:
        0 8px 12px rgba(0,0,0,0.4),
        0 32px 80px rgba(0,0,0,0.6),
        0 0 0 1px rgba(14,165,233,0.15),
        inset 0 1px 0 rgba(255,255,255,0.06);
}
.vessel-card:hover::before { opacity: 1; }

.card-inner {
    padding: 32px;
}

/* ── IMAGE WRAPPER ── */
.img-wrap {
    position: relative;
    border-radius: 20px;
    overflow: hidden;
}
.img-wrap::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(
        135deg,
        rgba(14,165,233,0.08) 0%,
        transparent 50%,
        rgba(0,0,0,0.30) 100%
    );
    pointer-events: none;
}

/* ── KATEGORI PILL ── */
.kategori-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 5px 14px;
    border-radius: 99px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 14px;
}
.pill-vvip {
    background: rgba(250,204,21,0.12);
    border: 1px solid rgba(250,204,21,0.30);
    color: #facc15;
}
.pill-vip {
    background: rgba(167,139,250,0.12);
    border: 1px solid rgba(167,139,250,0.30);
    color: #a78bfa;
}
.pill-standard {
    background: rgba(52,211,153,0.12);
    border: 1px solid rgba(52,211,153,0.30);
    color: #34d399;
}
.pill-default {
    background: rgba(14,165,233,0.12);
    border: 1px solid rgba(14,165,233,0.30);
    color: #38bdf8;
}

/* ── VESSEL NAME ── */
.vessel-name {
    font-family: 'Cormorant Garamond', serif;
    font-size: 30px;
    font-weight: 700;
    line-height: 1.15;
    color: #ffffff;
    margin-bottom: 6px;
    letter-spacing: -0.01em;
}

.vessel-ship {
    font-size: 13px;
    color: #4a6a8a;
    font-weight: 400;
    margin-bottom: 24px;
    letter-spacing: 0.02em;
}
.vessel-ship span { color: #7090b0; }

/* ── INFO GRID ── */
.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 22px;
}

.info-item {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 12px 16px;
    transition: background 0.2s;
}
.info-item:hover { background: rgba(255,255,255,0.05); }

.info-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #3a5a7a;
    margin-bottom: 4px;
}

.info-value {
    font-size: 15px;
    font-weight: 600;
    color: #e2eaf5;
    line-height: 1.3;
}

.info-value.accent { color: #38bdf8; }
.info-value.gold { color: #facc15; }
.info-value.emerald { color: #34d399; }

/* ── DIVIDER ── */
.slim-divider {
    height: 1px;
    background: linear-gradient(90deg, rgba(14,165,233,0.15), rgba(255,255,255,0.04), transparent);
    margin: 20px 0;
    border: none;
}

/* ── SECTION LABEL ── */
.section-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #3a5a7a;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-label::after {
    content: "";
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.05);
}

/* ── BADGE CHIPS ── */
.chips-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
    margin-bottom: 16px;
}

.chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 6px 13px;
    border-radius: 10px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    font-size: 12px;
    font-weight: 500;
    color: #8aaccc;
    transition: all 0.2s;
    white-space: nowrap;
}
.chip:hover {
    background: rgba(14,165,233,0.10);
    border-color: rgba(14,165,233,0.25);
    color: #93c5fd;
}
.chip-icon { font-size: 11px; }

/* ── DESTINASI ── */
.destinasi-wrap {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 20px;
}
.dest-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #0ea5e9;
    flex-shrink: 0;
}
.dest-text {
    font-size: 13px;
    color: #7090b0;
    font-weight: 400;
    letter-spacing: 0.03em;
}

/* ── DESCRIPTION ── */
.desc-text {
    font-size: 13.5px;
    color: #5a7a9a;
    line-height: 1.85;
    font-weight: 300;
    border-left: 2px solid rgba(14,165,233,0.25);
    padding-left: 14px;
    margin-top: 4px;
}

/* ── BUTTON ── */
.stLinkButton a {
    background: linear-gradient(135deg, #0369a1 0%, #0284c7 50%, #0ea5e9 100%) !important;
    color: white !important;
    border-radius: 14px !important;
    border: none !important;
    padding: 12px 28px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    letter-spacing: 0.04em !important;
    box-shadow: 0 4px 20px rgba(14,165,233,0.30) !important;
    transition: all 0.25s !important;
    text-decoration: none !important;
}
.stLinkButton a:hover {
    background: linear-gradient(135deg, #075985 0%, #0369a1 50%, #0284c7 100%) !important;
    box-shadow: 0 6px 28px rgba(14,165,233,0.45) !important;
    transform: translateY(-1px);
}

/* ── SCORE BADGE ── */
.score-badge {
    position: absolute;
    top: 20px;
    right: 20px;
    background: rgba(5,13,26,0.85);
    border: 1px solid rgba(14,165,233,0.25);
    border-radius: 12px;
    padding: 8px 14px;
    backdrop-filter: blur(12px);
    text-align: center;
    z-index: 10;
}
.score-num {
    font-family: 'Cormorant Garamond', serif;
    font-size: 20px;
    font-weight: 700;
    color: #38bdf8;
    line-height: 1;
}
.score-lbl {
    font-size: 9px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #3a5a7a;
    font-weight: 600;
}

/* ── NO RESULT ── */
.no-result {
    text-align: center;
    padding: 80px 20px;
    color: #3a5a7a;
}
.no-result .icon { font-size: 48px; margin-bottom: 16px; }
.no-result h3 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 24px;
    color: #506070;
    margin-bottom: 8px;
}
.no-result p { font-size: 14px; }

/* ── MAIN BLOCK PADDING ── */
.block-container {
    padding: 0 2rem 4rem !important;
    max-width: 1280px !important;
}

/* ── COLUMN GAP FIX ── */
[data-testid="column"] { padding: 0 12px !important; }

</style>
""", unsafe_allow_html=True)


# =========================================================
# HERO HEADER
# =========================================================

st.markdown("""
<div class="hero-wrap">
    <div class="hero-eyebrow">⚓ &nbsp; Luxury Maritime Voyages</div>
    <div class="hero-title">Phinisi Recommendation<br>System</div>
    <div class="hero-sub">Temukan kapal phinisi terbaik untuk petualangan<br>bahari tak terlupakan di nusantara</div>
    <div class="hero-line"></div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# FILTER PANEL
# =========================================================

col_search, col_filter = st.columns([2.2, 1])

with col_search:
    search = st.text_input(
        "CARI KAPAL",
        placeholder="🔍  Cari nama kapal, destinasi, atau fasilitas..."
    )

with col_filter:
    kategori_filter = st.selectbox(
        "KATEGORI",
        ["Semua"] + sorted(df["kategori"].unique().tolist())
    )


# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df.copy()

if kategori_filter != "Semua":
    filtered_df = filtered_df[filtered_df["kategori"] == kategori_filter]

if search:
    filtered_df = filtered_df[
        filtered_df["content"].str.contains(search, case=False, na=False)
    ]

# =========================================================
# RESULT COUNT
# =========================================================

total = len(filtered_df)
st.markdown(
    f'<div class="result-count">Menampilkan <span>{total}</span> kapal phinisi</div>',
    unsafe_allow_html=True
)


# =========================================================
# HELPER: KATEGORI PILL
# =========================================================

def get_pill(kategori):
    k = str(kategori).upper()
    if "VVIP" in k:
        css = "pill-vvip"; icon = "👑"
    elif "VIP" in k:
        css = "pill-vip"; icon = "💎"
    elif "STANDARD" in k:
        css = "pill-standard"; icon = "⚡"
    else:
        css = "pill-default"; icon = "🚢"
    return f'<div class="kategori-pill {css}">{icon}&nbsp;{kategori}</div>'


def value_class(field):
    f = field.lower()
    if "harga" in f: return "gold"
    if "durasi" in f: return "accent"
    if "kapasitas" in f: return "emerald"
    return "accent"


# =========================================================
# CARDS
# =========================================================

if total == 0:
    st.markdown("""
    <div class="no-result">
        <div class="icon">⚓</div>
        <h3>Kapal Tidak Ditemukan</h3>
        <p>Coba ubah filter atau kata kunci pencarian Anda</p>
    </div>
    """, unsafe_allow_html=True)

else:
    for _, row in filtered_df.iterrows():

        # ── CARD OPEN ──
        st.markdown('<div class="vessel-card"><div class="card-inner">', unsafe_allow_html=True)

        col_img, col_info = st.columns([1.05, 1.35])

        # ── IMAGE ──
        with col_img:
            st.markdown('<div class="img-wrap">', unsafe_allow_html=True)
            st.image(row["image_url"], use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Score if exists
            if "score" in row and pd.notna(row["score"]):
                try:
                    score_val = float(row["score"])
                    st.markdown(f"""
                    <div style="
                        display:inline-flex; align-items:center; gap:8px;
                        background:rgba(14,165,233,0.08); border:1px solid rgba(14,165,233,0.20);
                        border-radius:12px; padding:8px 16px; margin-top:14px;
                        font-size:12px; color:#38bdf8; font-weight:600;
                        letter-spacing:0.06em;
                    ">
                        ✦ Score Relevansi: <strong>{score_val:.4f}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                except:
                    pass

        # ── DETAILS ──
        with col_info:

            # Pill + Name
            st.markdown(
                get_pill(row['kategori']) +
                f'<div class="vessel-name">{row["nama_paket"]}</div>' +
                f'<div class="vessel-ship">Kapal: <span>{row["nama_kapal"]}</span></div>',
                unsafe_allow_html=True
            )

            # Info Grid
            st.markdown(f"""
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">💰 Harga</div>
                    <div class="info-value gold">{row['harga']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">⏱ Durasi</div>
                    <div class="info-value accent">{row['durasi']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">👥 Kapasitas</div>
                    <div class="info-value emerald">{row['kapasitas']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">🧭 Kategori</div>
                    <div class="info-value">{row['kategori']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Destinasi
            st.markdown(f"""
            <div class="section-label">📍 Destinasi</div>
            <div class="destinasi-wrap">
                <div class="dest-dot"></div>
                <div class="dest-text">{row['destinasi']}</div>
            </div>
            """, unsafe_allow_html=True)

            # Fasilitas
            fasilitas_items = [f.strip() for f in str(row["fasilitas"]).split(",") if f.strip()]
            fasilitas_html = '<div class="section-label">✨ Fasilitas</div><div class="chips-wrap">'
            for f in fasilitas_items:
                fasilitas_html += f'<span class="chip"><span class="chip-icon">✦</span>{f}</span>'
            fasilitas_html += '</div>'
            st.markdown(fasilitas_html, unsafe_allow_html=True)

            # Layanan
            layanan_items = [l.strip() for l in str(row["layanan"]).split(",") if l.strip()]
            layanan_html = '<div class="section-label">🏝️ Layanan</div><div class="chips-wrap">'
            for l in layanan_items:
                layanan_html += f'<span class="chip"><span class="chip-icon">◈</span>{l}</span>'
            layanan_html += '</div>'
            st.markdown(layanan_html, unsafe_allow_html=True)

        # ── DESCRIPTION ──
        st.markdown(f"""
        <div style="padding:0 4px 8px;">
            <div class="slim-divider"></div>
            <div class="section-label">📋 Deskripsi</div>
            <div class="desc-text">{row['deskripsi']}</div>
        </div>
        """, unsafe_allow_html=True)

        # ── BUTTON ──
        st.link_button("⚓  Lihat Detail Kapal", row["link"])

        # ── CARD CLOSE ──
        st.markdown("</div></div>", unsafe_allow_html=True)

        # Spacer
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div style="
    text-align:center;
    padding: 48px 20px 24px;
    border-top: 1px solid rgba(255,255,255,0.04);
    margin-top: 48px;
">
    <div style="
        font-family: 'Cormorant Garamond', serif;
        font-size: 20px;
        color: #2a4a6a;
        letter-spacing: 0.08em;
        margin-bottom: 8px;
    ">⚓ PHINISI</div>
    <div style="font-size:12px; color:#1e3a5a; letter-spacing:0.08em; text-transform:uppercase;">
        Luxury Maritime Voyage Recommendation
    </div>
</div>
""", unsafe_allow_html=True)
