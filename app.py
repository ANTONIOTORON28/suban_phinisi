# =========================================================
# PROFESSIONAL STREAMLIT UI
# PHINISI RECOMMENDATION SYSTEM
# FINAL FIX VERSION
# =========================================================

# pip install streamlit pandas pillow

import streamlit as st
import pandas as pd


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(

    page_title="Phinisi Recommendation System",

    page_icon="🚢",

    layout="wide"
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv("dataset_kapal_preprocessing.csv")

    # =====================================================
    # AUTO CREATE CONTENT COLUMN
    # =====================================================

    if "content" not in df.columns:

        df["content"] = (

            df["nama_paket"].fillna("") + " " +

            df["kategori"].fillna("") + " " +

            df["fasilitas"].fillna("") + " " +

            df["layanan"].fillna("") + " " +

            df["destinasi"].fillna("")
        )

    # =====================================================
    # DEFAULT COLUMNS
    # =====================================================

    default_columns = [

        "nama_paket",
        "nama_kapal",
        "kategori",
        "harga",
        "durasi",
        "kapasitas",
        "destinasi",
        "fasilitas",
        "layanan",
        "deskripsi",
        "image_url",
        "link",
        "content"
    ]

    for col in default_columns:

        if col not in df.columns:

            df[col] = "-"

        df[col] = df[col].fillna("-")

    return df


df = load_data()


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""

<style>

/* =====================================================
BACKGROUND
===================================================== */

.stApp {

    background:
        linear-gradient(
            135deg,
            #020617,
            #071426,
            #0b1220
        );

    color: white;
}


/* =====================================================
TITLE
===================================================== */

.main-title {

    font-size: 42px;

    font-weight: 800;

    color: white;

    margin-bottom: 30px;
}


/* =====================================================
CARD
===================================================== */

.card {

    background: rgba(8, 15, 30, 0.95);

    border-radius: 28px;

    padding: 30px;

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow:
        0 10px 30px rgba(0,0,0,0.4);

    margin-bottom: 35px;
}


/* =====================================================
IMAGE
===================================================== */

.card img {

    border-radius: 18px;
}


/* =====================================================
LABEL
===================================================== */

.label {

    color: white;

    font-weight: 700;

    font-size: 17px;

    margin-top: 8px;
}


/* =====================================================
VALUE
===================================================== */

.value {

    color: #dbeafe;

    font-size: 16px;
}


/* =====================================================
HIGHLIGHT
===================================================== */

.highlight {

    color: #facc15;

    font-weight: 700;
}


/* =====================================================
SECTION TITLE
===================================================== */

.section-title {

    margin-top: 20px;

    margin-bottom: 12px;

    color: white;

    font-weight: 700;

    font-size: 18px;
}


/* =====================================================
BADGE
===================================================== */

.badge {

    display: inline-block;

    padding: 8px 14px;

    border-radius: 999px;

    background: rgba(255,255,255,0.06);

    border: 1px solid rgba(255,255,255,0.08);

    margin: 4px;

    color: white;

    font-size: 14px;
}


/* =====================================================
DESCRIPTION
===================================================== */

.desc {

    color: #cbd5e1;

    line-height: 1.8;

    margin-top: 10px;

    font-size: 15px;
}


/* =====================================================
SEARCH
===================================================== */

.stTextInput input {

    border-radius: 14px !important;

    background: rgba(255,255,255,0.05) !important;

    color: white !important;
}


/* =====================================================
SELECTBOX
===================================================== */

.stSelectbox div[data-baseweb="select"] {

    background: rgba(255,255,255,0.05);

    border-radius: 14px;
}


/* =====================================================
BUTTON
===================================================== */

.stButton button {

    background:
        linear-gradient(
            90deg,
            #2563eb,
            #1d4ed8
        );

    color: white;

    border-radius: 12px;

    border: none;

    padding: 10px 22px;

    font-weight: 700;
}

</style>

""", unsafe_allow_html=True)


# =========================================================
# TITLE
# =========================================================

st.markdown(

    """
    <div class="main-title">
        🚢 Phinisi Recommendation System
    </div>
    """,

    unsafe_allow_html=True
)


# =========================================================
# SEARCH & FILTER
# =========================================================

col1, col2 = st.columns([2,1])

with col1:

    search = st.text_input(

        "Cari kapal, fasilitas, destinasi..."
    )

with col2:

    kategori_filter = st.selectbox(

        "Kategori",

        ["Semua"] +

        sorted(df["kategori"].unique().tolist())
    )


# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df.copy()

if kategori_filter != "Semua":

    filtered_df = filtered_df[

        filtered_df["kategori"] == kategori_filter
    ]


if search:

    filtered_df = filtered_df[

        filtered_df["content"].str.contains(
            search,
            case=False,
            na=False
        )
    ]


# =========================================================
# RESULT COUNT
# =========================================================

st.write(f"Total Kapal: {len(filtered_df)}")


# =========================================================
# CARD UI
# =========================================================

for _, row in filtered_df.iterrows():

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1.1, 1.4])

    # =====================================================
    # IMAGE
    # =====================================================

    with col1:

        if row["image_url"] != "-":

            st.image(

                row["image_url"],

                use_container_width=True
            )

        else:

            st.warning("Gambar tidak tersedia")


    # =====================================================
    # DETAIL
    # =====================================================

    with col2:

        st.markdown(

            f"""
            <div style="
                font-size:34px;
                font-weight:800;
                color:white;
                margin-bottom:18px;
            ">
                {row['nama_paket']}
            </div>
            """,

            unsafe_allow_html=True
        )

        st.markdown(

            f"""
            <div class="label">
                Kapal:
                <span class="value">
                    {row['nama_kapal']}
                </span>
            </div>

            <hr>

            <div class="label">
                Kategori:
                <span class="highlight">
                    {row['kategori']}
                </span>
            </div>

            <hr>

            <div class="label">
                Harga:
                <span class="highlight">
                    {row['harga']}
                </span>
            </div>

            <hr>

            <div class="label">
                Durasi:
                <span class="highlight">
                    {row['durasi']}
                </span>
            </div>

            <hr>

            <div class="label">
                Kapasitas:
                <span class="highlight">
                    {row['kapasitas']}
                </span>
            </div>

            <hr>

            <div class="label">
                Destinasi:
                <span class="value">
                    {row['destinasi']}
                </span>
            </div>
            """,

            unsafe_allow_html=True
        )

        # =================================================
        # FASILITAS
        # =================================================

        st.markdown(

            '<div class="section-title">Fasilitas:</div>',

            unsafe_allow_html=True
        )

        fasilitas_html = ""

        fasilitas_list = str(
            row["fasilitas"]
        ).split(",")

        for item in fasilitas_list:

            item = item.strip()

            if item and item != "-":

                fasilitas_html += f"""

                <span class="badge">
                    ✨ {item}
                </span>

                """

        st.markdown(
            fasilitas_html,
            unsafe_allow_html=True
        )

        # =================================================
        # LAYANAN
        # =================================================

        st.markdown(

            '<div class="section-title">Layanan:</div>',

            unsafe_allow_html=True
        )

        layanan_html = ""

        layanan_list = str(
            row["layanan"]
        ).split(",")

        for item in layanan_list:

            item = item.strip()

            if item and item != "-":

                layanan_html += f"""

                <span class="badge">
                    🏝️ {item}
                </span>

                """

        st.markdown(
            layanan_html,
            unsafe_allow_html=True
        )

    # =====================================================
    # DESCRIPTION
    # =====================================================

    st.markdown(

        f"""
        <div class="section-title">
            Deskripsi:
        </div>

        <div class="desc">
            {row['deskripsi']}
        </div>
        """,

        unsafe_allow_html=True
    )

    # =====================================================
    # BUTTON LINK
    # =====================================================

    if row["link"] != "-":

        st.link_button(

            "🔗 Lihat Detail Kapal",

            row["link"]
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )
