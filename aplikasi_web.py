import streamlit as st
import re
from collections import Counter
from itertools import permutations

# --- LOGIKA MESIN ---
def hitung_bb(angka):
    return "".join(sorted(angka))

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

# CSS KHUSUS AGAR TEKS TURUN KE BAWAH (WRAP)
st.markdown("""
    <style>
    code {
        white-space: pre-wrap !important;
        word-break: break-all !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 Mesin Analisa & BBFS Pro")
st.write("Selamat datang, Koh! Silakan racik angka keberuntungan di sini.")

# Sidebar untuk Upload
st.sidebar.header("📁 Pengaturan Data")
uploaded_file = st.sidebar.file_uploader("Upload data_keluaran.txt", type=['txt'])

if uploaded_file:
    teks = uploaded_file.read().decode("utf-8")
    semua_raw = re.findall(r'\b\d{4}\b', teks)
    data_ada = set(semua_raw)

    st.subheader("🎲 Masukkan Angka BBFS")
    input_bbfs = st.text_input("Contoh: 012345", max_chars=10)

    if input_bbfs:
        # Proses Kombinasi
        hasil_kombinasi = sorted(list(set("".join(p) for p in permutations(input_bbfs, 4))))
        
        bbfs_acak = [a for a in hasil_kombinasi if not is_berurutan(a)]
        bbfs_berurutan = [a for a in hasil_kombinasi if is_berurutan(a)]
        bbfs_panas = [a for a in hasil_kombinasi if a in data_ada]

        # Kolom Hasil
        col1, col2 = st.columns(2)
        
        with col1:
            st.success(f"✅ Kombinasi Utama ({len(bbfs_acak)})")
            for i in range(0, len(bbfs_acak), 300):
                blok = bbfs_acak[i:i+300]
                teks_hasil = "*".join(blok)
                st.write(f"**Paragraf {int(i/300)+1}**")
                st.code(teks_hasil, language="text") 
                st.divider()

        with col2:
            st.warning(f"⚠️ Pilihan Kedua: Berurutan ({len(bbfs_berurutan)})")
            if bbfs_berurutan:
                teks_urut = "*".join(bbfs_berurutan)
                st.code(teks_urut, language="text")
            else:
                st.write("Nihil")
            
            st.divider()
            st.error(f"🔥 Data Panas / Sudah Keluar ({len(bbfs_panas)})")
            if bbfs_panas:
                teks_panas = "*".join(bbfs_panas)
                st.code(teks_panas, language="text")
            else:
                st.write("Nihil")
else:
    st.info("Silakan upload file 'data_keluaran.txt' dulu di kiri, Koh.")