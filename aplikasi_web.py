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
st.set_page_config(page_title="Mesin BBFS Super Pro", layout="wide")
st.markdown("""<style>code {white-space: pre-wrap !important; word-break: break-all !important;}</style>""", unsafe_allow_html=True)

st.title("🎯 Mesin Analisa BBFS Multi-Pasaran")

# --- SIDEBAR PENGATURAN ---
st.sidebar.header("⚙️ Pengaturan")
pasaran = st.sidebar.selectbox("Pilih Pasaran:", ("Hong Kong (HK)", "Sydney (SDY)", "Singapore (SGP)"))
st.sidebar.subheader("🔍 Tampilkan Kombinasi:")
show_4d = st.sidebar.checkbox("Tampilkan 4D", value=True)
show_3d = st.sidebar.checkbox("Tampilkan 3D", value=False)
show_2d = st.sidebar.checkbox("Tampilkan 2D", value=False)

# Mapping file
file_map = {"Hong Kong (HK)": "data_keluaran_hk.txt", "Sydney (SDY)": "data_keluaran_sdy.txt", "Singapore (SGP)": "data_keluaran_sgp.txt"}
nama_file = file_map[pasaran]
URL_DATA = f"https://raw.githubusercontent.com/Mahasewa/mesin-bbfs/main/{nama_file}"

# --- AMBIL DATA ---
try:
    respon = requests.get(URL_DATA)
    if respon.status_code == 200:
        teks = respon.text
        data_ada = set(re.findall(r'\b\d{4}\b', teks))
        st.sidebar.success(f"✅ {pasaran} Terhubung")
        st.sidebar.info(f"📊 Total Data: {len(data_ada)} angka")
    else:
        st.sidebar.error(f"❌ File {nama_file} tidak ditemukan")
        data_ada = set()
except:
    st.sidebar.error("❌ Koneksi Error")
    data_ada = set()

# --- INPUT & HASIL ---
input_bbfs = st.text_input(f"🎲 Masukkan Angka BBFS ({pasaran}):", max_chars=10)

if input_bbfs:
    # Fungsi untuk menampilkan hasil per kategori
    def tampilkan_hasil(label, acak, berurutan, panas):
        st.header(f"--- Hasil {label} ---")
        c1, c2 = st.columns(2)
        with c1:
            st.success(f"✅ {label} Utama (Acak) - {len(acak)} Line")
            if acak: 
                for i in range(0, len(acak), 300): st.code("*".join(acak[i:i+300]))
        with c2:
            st.warning(f"⚠️ {label} Berurutan - {len(berurutan)} Line")
            if berurutan: st.code("*".join(berurutan))
            st.error(f"🔥 Data Panas {label} (Sudah Keluar) - {len(panas)} Line")
            if panas: st.code("*".join(panas))
            else: st.write("Belum ada yang pernah keluar.")

    if show_4d:
        a4, b4, p4 = get_kombinasi(input_bbfs, 4, data_ada)
        tampilkan_hasil("4D", a4, b4, p4)
    
    if show_3d:
        a3, b3, p3 = get_kombinasi(input_bbfs, 3, data_ada)
        tampilkan_hasil("3D", a3, b3, p3)
        
    if show_2d:
        a2, b2, p2 = get_kombinasi(input_bbfs, 2, data_ada)
        tampilkan_hasil("2D", a2, b2, p2)
