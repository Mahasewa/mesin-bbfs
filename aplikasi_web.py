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
    panas = [a for a in hasil_raw if any(a in d for d in data_ada)]
    return acak, berurutan, panas

# --- TAMPILAN WEB ---
st.set_page_config(page_title="Mahasewa BBFS Pro", layout="wide")

# CSS Custom untuk menghilangkan Header Streamlit dan merapikan UI
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stCodeBlock {white-space: pre-wrap !important; word-break: break-all !important;}
    div.block-container {padding-top: 1rem;}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER LOGO & NAMA ---
col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2:
    # Mengambil logo dari GitHub Koh
    logo_url = "https://raw.githubusercontent.com/Mahasewa/mesin-bbfs/main/logo_mahasewa.png"
    st.image(logo_url, use_container_width=True)
    st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>MAHASEWA BBFS</h1>", unsafe_allow_html=True)

st.divider()

# --- PILIHAN PASARAN & CEKLIST (DIBUAT RAPI) ---
col_set1, col_set2 = st.columns([1, 1])

with col_set1:
    pasaran = st.selectbox("🎯 Pilih Pasaran:", ("Hong Kong (HK)", "Sydney (SDY)", "Singapore (SGP)"))

with col_set2:
    st.write("🔍 **Opsi Tampilan:**")
    c1, c2, c3 = st.columns(3)
    show_4d = c1.checkbox("4D", value=True)
    show_3d = c2.checkbox("3D", value=False)
    show_2d = c3.checkbox("2D", value=False)

# Mapping file
file_map = {
    "Hong Kong (HK)": "data_keluaran_hk.txt", 
    "Sydney (SDY)": "data_keluaran_sdy.txt", 
    "Singapore (SGP)": "data_keluaran_sgp.txt"
}
URL_DATA = f"https://raw.githubusercontent.com/Mahasewa/mesin-bbfs/main/{file_map[pasaran]}"

# --- AMBIL DATA ---
try:
    respon = requests.get(URL_DATA)
    if respon.status_code == 200:
        data_ada = set(re.findall(r'\b\d{4}\b', respon.text))
        st.sidebar.success(f"✅ {pasaran} Connected")
    else:
        data_ada = set()
        st.sidebar.error("❌ Data tidak ditemukan")
except:
    data_ada = set()

# --- INPUT UTAMA ---
input_bbfs = st.text_input(f"🎲 Input Angka BBFS {pasaran}:", placeholder="Contoh: 12345", max_chars=10)

if input_bbfs:
    def tampilkan_hasil_keren(label, acak, berurutan, panas):
        with st.expander(f"📊 LIHAT HASIL {label}", expanded=True):
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.success(f"✅ {label} Utama ({len(acak)} Line)")
                if acak: st.code("*".join(acak))
            with res_col2:
                st.warning(f"⚠️ Berurutan ({len(berurutan)})")
                if berurutan: st.code("*".join(berurutan))
                st.error(f"🔥 Data Panas ({len(panas)})")
                if panas: st.code("*".join(panas))

    if show_4d:
        a4, b4, p4 = get_kombinasi(input_bbfs, 4, data_ada)
        tampilkan_hasil_keren("4D", a4, b4, p4)
    
    if show_3d:
        a3, b3, p3 = get_kombinasi(input_bbfs, 3, data_ada)
        tampilkan_hasil_keren("3D", a3, b3, p3)
        
    if show_2d:
        a2, b2, p2 = get_kombinasi(input_bbfs, 2, data_ada)
        tampilkan_hasil_keren("2D", a2, b2, p2)

st.markdown("<p style='text-align: center; font-size: 0.8rem;'>© 2026 Mahasewa BBFS Digital Team</p>", unsafe_allow_html=True)
