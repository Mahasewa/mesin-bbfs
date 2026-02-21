import streamlit as st
import re
import requests
import itertools
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

def get_kembar_strict(input_digits, tipe):
    hasil_raw = ["".join(p) for p in itertools.product(input_digits, repeat=4)]
    final = []
    for h in hasil_raw:
        counts = [h.count(d) for d in set(h)]
        max_c = max(counts)
        if tipe == 2 and max_c == 2: final.append(h) # Twin Murni
        elif tipe == 3 and max_c == 3: final.append(h) # Triple Murni
        elif tipe == 4 and max_c == 4: final.append(h) # Quad Murni
    return sorted(list(set(final)))
def kelompokkan_twin(daftar_angka):
    kelompok = {}
    for angka in daftar_angka:
        # Logika menentukan pola (A, B, C)
        mapping = {}
        pola = ""
        for char in angka:
            if char not in mapping:
                mapping[char] = chr(65 + len(mapping)) # Jadi A, B, atau C
            pola += mapping[char]
        
        if pola not in kelompok:
            kelompok[pola] = []
        kelompok[pola].append(angka)
    return kelompok
# --- TAMPILAN WEB ---
st.set_page_config(page_title="Mahasewa BBFS Pro", layout="wide")

# CSS KHUSUS: PAKSA HITAM & PUTIH
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Kotak angka: Latar Putih, Tulisan Hitam */
    code {
        white-space: pre-wrap !important; 
        word-break: break-all !important;
        background-color: #ffffff !important; /* PUTIH BERSIH */
        color: #000000 !important;           /* HITAM PEKAT */
        -webkit-text-fill-color: #000000 !important;
        
        display: block;
        padding: 20px !important;
       /* SOLUSI BIAR GAK TUMPANG TINDIH */
        line-height: 2.5 !important;      /* Kasih jarak baris yang lega */
        overflow: visible !important;     /* Biar teks gak kepotong garis */
        
        border: 1px solid #eeeeee !important; 
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }
    
    /* Tombol Proses */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(to right, #FF4B2B, #FF416C);
        color: white;
        font-weight: bold;
        padding: 15px;
        border-radius: 10px;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER LOGO ---
col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2:
    logo_url = "https://raw.githubusercontent.com/Mahasewa/mesin-bbfs/main/logo_mahasewa.png"
    st.image(logo_url, use_container_width=True)
    st.markdown("<h2 style='text-align: center; color: #FF4B4B;'>MAHASEWA BBFS</h2>", unsafe_allow_html=True)

st.divider()

# --- INPUT AREA ---
pasaran = st.selectbox("🎯 Pilih Pasaran:", ("Hong Kong (HK)", "Sydney (SDY)", "Singapore (SGP)"))

st.write("🔍 **Opsi Mode Utama:**")
c1, c2, c3 = st.columns(3)
show_4d = c1.checkbox("Mode 4D", value=True)
show_3d = c2.checkbox("Mode 3D", value=False)
show_2d = c3.checkbox("Mode 2D", value=False)

st.write("👯 **Opsi Angka Kembar:**")
k1, k2, k3 = st.columns(3)
show_twin = k1.checkbox("Twin (4D)", value=False)
show_triple = k2.checkbox("Triple (4D)", value=False)
show_quad = k3.checkbox("Quad (4D)", value=False)

input_bbfs = st.text_input("🎲 Masukkan Angka BBFS:", placeholder="Contoh: 12345", max_chars=10)
tombol_proses = st.button("🚀 PROSES SEKARANG")

# --- AMBIL DATA ---
file_map = {"Hong Kong (HK)": "data_keluaran_hk.txt", "Sydney (SDY)": "data_keluaran_sdy.txt", "Singapore (SGP)": "data_keluaran_sgp.txt"}
URL_DATA = f"https://raw.githubusercontent.com/Mahasewa/mesin-bbfs/main/{file_map[pasaran]}"
try:
    respon = requests.get(URL_DATA)
    data_ada = set(re.findall(r'\b\d{4}\b', respon.text)) if respon.status_code == 200 else set()
except:
    data_ada = set()

# --- EKSEKUSI ---
if tombol_proses and input_bbfs:
    def cetak_hasil_blok(label, daftar_angka):
        if daftar_angka:
            st.subheader(f"📊 HASIL {label} ({len(daftar_angka)} Line)")
            for i in range(0, len(daftar_angka), 300):
                st.code("*".join(daftar_angka[i:i+300]))

    # 1. Proses 4D
    if show_4d:
        a4, b4, p4 = get_kombinasi(input_bbfs, 4, data_ada)
        if a4:
            st.subheader(f"📊 HASIL 4D ACAK ({len(a4)} Line)")
            for i in range(0, len(a4), 300):
                akhir = i + 300
                with st.expander(f"📦 BLOK 4D (No. {i+1} - {min(akhir, len(a4))})"):
                    st.code("*".join(a4[i:akhir]))
            if b4: st.warning(f"⚠️ BERURUTAN (4D): {len(b4)} Line -> {', '.join(b4)}")
            if p4: st.error(f"🔥 DATA PANAS (4D): {len(p4)} Line -> {', '.join(p4)}")

    # 2. Proses 3D
    if show_3d:
        a3, b3, p3 = get_kombinasi(input_bbfs, 3, data_ada)
        if a3:
            st.subheader(f"📊 HASIL 3D ACAK ({len(a3)} Line)")
            for i in range(0, len(a3), 300):
                akhir = i + 300
                with st.expander(f"📦 BLOK 3D (No. {i+1} - {min(akhir, len(a3))})"):
                    st.code("*".join(a3[i:akhir]))
            if b3: st.warning(f"⚠️ BERURUTAN (3D): {len(b3)} Line -> {', '.join(b3)}")
            if p3: st.error(f"🔥 DATA PANAS (3D): {len(p3)} Line -> {', '.join(p3)}")

    # 3. Proses 2D
    if show_2d:
        a2, b2, p2 = get_kombinasi(input_bbfs, 2, data_ada)
        if a2:
            st.subheader(f"📊 HASIL 2D ACAK ({len(a2)} Line)")
            for i in range(0, len(a2), 300):
                akhir = i + 300
                with st.expander(f"📦 BLOK 2D (No. {i+1} - {min(akhir, len(a2))})"):
                    st.code("*".join(a2[i:akhir]))
            if b2: st.warning(f"⚠️ BERURUTAN (2D): {len(b2)} Line -> {', '.join(b2)}")
            if p2: st.error(f"🔥 DATA PANAS (2D): {len(p2)} Line -> {', '.join(p2)}")
    
   # 4. Proses Kembar (Strict) & Cek Data Panas
    if show_twin:
        res_twin = get_kembar_strict(input_bbfs, 2)
        if res_twin:
            st.subheader(f"📊 TOTAL TWIN 4D ({len(res_twin)} Line)")
            
            # Kita kelompokkan dulu
            data_kelompok = kelompokkan_twin(res_twin)
            
            # Tampilkan per pola
            for pola, daftar in data_kelompok.items():
                with st.expander(f"🔹 POLA {pola} ({len(daftar)} Line)"):
                    st.code("*".join(daftar))
                    
                    # Cek Data Panas per pola ini
                    p_twin = [a for a in daftar if a in data_ada]
                    if p_twin:
                        st.error(f"🔥 DATA PANAS DI POLA {pola}: {', '.join(p_twin)}")

    if show_triple:
        res_trip = get_kembar_strict(input_bbfs, 3)
        p_trip = [a for a in res_trip if a in data_ada]
        cetak_hasil_blok("TRIPLE 4D (MURNI)", res_trip)
        if p_trip: st.error(f"🔥 DATA PANAS TRIPLE: {', '.join(p_trip)}")

    if show_quad:
        res_quad = get_kembar_strict(input_bbfs, 4)
        p_quad = [a for a in res_quad if a in data_ada]
        cetak_hasil_blok("QUAD 4D (MURNI)", res_quad)
        if p_quad: st.error(f"🔥 DATA PANAS QUAD: {', '.join(p_quad)}")

elif tombol_proses and not input_bbfs:
    st.error("Isi angkanya dulu Koh!")

st.markdown("<p style='text-align: center; font-size: 0.8rem; color: #888;'>© 2026 Mahasewa BBFS Digital Team</p>", unsafe_allow_html=True)










