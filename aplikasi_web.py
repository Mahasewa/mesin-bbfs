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

# --- TAMPILAN WEB ---
st.set_page_config(page_title="Mesin BBFS Koh", layout="wide")

# CSS AGAR TEKS TURUN KE BAWAH
st.markdown("""<style>code {white-space: pre-wrap !important; word-break: break-all !important;}</style>""", unsafe_allow_html=True)

st.title("🎯 Mesin Analisa & BBFS Pro")

# --- AMBIL DATA OTOMATIS DARI GITHUB KOH ---
# Ini alamat file data_keluaran.txt punya Koh di GitHub
URL_DATA = "https://raw.githubusercontent.com/Mahasewa/mesin-bbfs/main/data_keluaran.txt"

try:
    respon = requests.get(URL_DATA)
    if respon.status_code == 200:
        teks = respon.text
        semua_raw = re.findall(r'\b\d{4}\b', teks)
        data_ada = set(semua_raw)
        st.sidebar.success(f"✅ Data Terhubung: {len(semua_raw)} angka")
    else:
        st.sidebar.error("❌ Gagal mengambil data. Pastikan file 'data_keluaran.txt' sudah diupload ke GitHub.")
        data_ada = set()
except:
    st.sidebar.error("❌ Koneksi Error")
    data_ada = set()

# --- INPUT BBFS ---
st.subheader("🎲 Masukkan Angka BBFS")
input_bbfs = st.text_input("Contoh: 012345", max_chars=10)

if input_bbfs:
    hasil_kombinasi = sorted(list(set("".join(p) for p in permutations(input_bbfs, 4))))
    bbfs_acak = [a for a in hasil_kombinasi if not is_berurutan(a)]
    bbfs_berurutan = [a for a in hasil_kombinasi if is_berurutan(a)]
    bbfs_panas = [a for a in hasil_kombinasi if a in data_ada]

    col1, col2 = st.columns(2)
    with col1:
        st.success(f"✅ Kombinasi Utama ({len(bbfs_acak)})")
        for i in range(0, len(bbfs_acak), 300):
            st.code("*".join(bbfs_acak[i:i+300]), language="text")
    with col2:
        st.warning(f"⚠️ Pilihan Kedua: Berurutan ({len(bbfs_berurutan)})")
        if bbfs_berurutan: st.code("*".join(bbfs_berurutan), language="text")
        
        st.divider()
        st.error(f"🔥 Data Panas / Sudah Keluar ({len(bbfs_panas)})")
        if bbfs_panas: st.code("*".join(bbfs_panas), language="text")
        else: st.write("Belum ada angka yang sama dengan database.")
