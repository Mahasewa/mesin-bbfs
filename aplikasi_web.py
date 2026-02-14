import streamlit as st
import re
import requests
from itertools import permutations

# --- LOGIKA MESIN ---
def is_berurutan(angka):
    try:
        n = [int(d) for d in angka]
        naik = all(n[i] + 1 == n[i+1] for i in range(len(n)-1))
        turun = all(n[i] - 1 == n[i+1] for i in range(len(n)-1))
        return naik or turun
    except:
        return False

def get_kombinasi(input_digits, digit_count, data_ada):
    hasil_raw = sorted(list(set("".join(p) for p in permutations(input_digits, digit_count))))
    acak = [a for a in hasil_raw if not is_berurutan(a)]
    berurutan = [a for a in hasil_raw if is_berurutan(a)]
    # Cek apakah angka (atau bagian dari angka) ada di database
    panas = [a for a in hasil_raw if any(a in d for d in data_ada)]
    return acak, berurutan, panas

# --- TAMPILAN WEB ---
st.set_page_config(page_title="Mahasewa BBFS Pro", layout="wide")

# CSS MAGIC: Agar tulisan otomatis turun ke bawah (wrap) dan tombol jadi cantik
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Agar hasil angka tidak memanjang ke samping tapi turun ke bawah */
    code {
        white-space: pre-wrap !important; 
        word-break: break-all !important;
        background-color: **#FFFFFF** !important; 
        color: **#000000** !important;
        display: block;
        padding: 15px !important;
        border-radius: 10px;
        border: 1px solid #d1d3d8 !important;
        font-weight: bold;
        ***-webkit-text-fill-color: #000000 !important;***
    }
    
    /* Gaya Tombol Proses */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(to right, #4facfe 0%, #00f2fe 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2:
    logo_url = "https://raw.githubusercontent.com/Mahasewa/mesin-bbfs/main/logo_mahasewa.png"
    st.image(logo_url, use_container_width=True)
    st.markdown("<h2 style='text-align: center; color: #FF4B4B;'>MAHASEWA BBFS</h2>", unsafe_allow_html=True)

st.divider()

# --- INPUT AREA ---
pasaran = st.selectbox("🎯 Pilih Pasaran:", ("Hong Kong (HK)", "Sydney (SDY)", "Singapore (SGP)"))

col_chk1, col_chk2, col_chk3 = st.columns(3)
show_4d = col_chk1.checkbox("Mode 4D", value=True)
show_3d = col_chk2.checkbox("Mode 3D", value=False)
show_2d = col_chk3.checkbox("Mode 2D", value=False)

input_bbfs = st.text_input("🎲 Masukkan Angka (0-9):", placeholder="Contoh: 12345", max_chars=10)

# TOMBOL PROSES (Sesuai gambar)
tombol_proses = st.button("🚀 PROSES SEKARANG")

# --- PROSES DATA ---
file_map = {"Hong Kong (HK)": "data_keluaran_hk.txt", "Sydney (SDY)": "data_keluaran_sdy.txt", "Singapore (SGP)": "data_keluaran_sgp.txt"}
URL_DATA = f"https://raw.githubusercontent.com/Mahasewa/mesin-bbfs/main/{file_map[pasaran]}"

try:
    respon = requests.get(URL_DATA)
    data_ada = set(re.findall(r'\b\d{4}\b', respon.text)) if respon.status_code == 200 else set()
except:
    data_ada = set()

# Jalankan hanya jika tombol diklik
if tombol_proses and input_bbfs:
    def cetak_hasil(label, acak, berurutan, panas):
        st.subheader(f"📊 HASIL {label}")
        
        st.success(f"✅ {label} UTAMA (ACAK) - {len(acak)} Line")
        # --- BAGIAN REVISI: POTONG TIAP 300 ---
        if acak:
            for i in range(0, len(acak), 300):
                st.code("*".join(acak[i:i+300]))
        # -------------------------------------
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.warning(f"⚠️ BERURUTAN ({len(berurutan)})")
            if berurutan: st.code("*".join(berurutan))
        with col_res2:
            st.error(f"🔥 DATA PANAS ({len(panas)})")
            if panas: st.code("*".join(panas))
        st.divider()

    if show_4d:
        a4, b4, p4 = get_kombinasi(input_bbfs, 4, data_ada)
        cetak_hasil("4D", a4, b4, p4)
    
    if show_3d:
        a3, b3, p3 = get_kombinasi(input_bbfs, 3, data_ada)
        cetak_hasil("3D", a3, b3, p3)
        
    if show_2d:
        a2, b2, p2 = get_kombinasi(input_bbfs, 2, data_ada)
        cetak_hasil("2D", a2, b2, p2)
elif tombol_proses and not input_bbfs:
    st.error("Masukkan angkanya dulu, Koh!")

st.markdown("<p style='text-align: center; font-size: 0.8rem; color: #888;'>© 2026 Mahasewa BBFS Digital Team</p>", unsafe_allow_html=True)




