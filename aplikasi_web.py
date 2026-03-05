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
    # 1. Hasilkan semua permutasi unik
    hasil_raw = sorted(list(set("".join(p) for p in permutations(input_digits, digit_count))))
    
    # 2. Identifikasi angka yang sudah pernah keluar (Data Panas)
    panas = [a for a in hasil_raw if a in data_ada]
    
    # 3. Identifikasi angka berurutan
    berurutan = [a for a in hasil_raw if is_berurutan(a)]
    
    # 4. Filter 'acak' agar HANYA berisi angka yang TIDAK berurutan DAN TIDAK ada di data_ada
    acak = [a for a in hasil_raw if not is_berurutan(a) and a not in panas]
    
    return acak, berurutan, panas

def get_kembar_strict_v2(input_digits, tipe, data_ada):
    # Menghasilkan semua kombinasi 4 digit
    hasil_raw = ["".join(p) for p in itertools.product(input_digits, repeat=4)]
    
    semua_kembar = []
    for h in hasil_raw:
        counts = [h.count(d) for d in set(h)]
        max_c = max(counts)
        
        # Filter berdasarkan tipe kembar
        if (tipe == 2 and max_c == 2) or (tipe == 3 and max_c == 3) or (tipe == 4 and max_c == 4):
            semua_kembar.append(h)
    
    semua_kembar = sorted(list(set(semua_kembar)))
    
    # Pisahkan mana yang bersih (aman) dan mana yang panas
    aman = [a for a in semua_kembar if a not in data_ada]
    panas = [a for a in semua_kembar if a in data_ada]
    
    return aman, panas

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

def is_tereliminasi(angka, f_as, f_kop, f_kep, f_ekor):
    # Jika filter kosong, tidak ada yang dieliminasi
    if not (f_as or f_kop or f_kep or f_ekor):
        return False
    
    # Cek kecocokan posisi
    if f_as and angka[0] == f_as: return True
    if f_kop and angka[1] == f_kop: return True
    if f_kep and angka[2] == f_kep: return True
    if f_ekor and angka[3] == f_ekor: return True
    
    return False

# --- TAMPILAN WEB ---
st.set_page_config(page_title="Mahasewa BBFS Pro", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    code {
        white-space: pre-wrap !important; 
        word-break: break-all !important;
        background-color: #ffffff !important; 
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        display: block;
        padding: 25px !important;
        border-radius: 10px;
        border: 1px solid #eeeeee !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        line-height: 2.5 !important;
        min-height: fit-content !important;
        overflow: visible !important;
    }
    
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
show_twin = k1.checkbox("Twin Saja", value=False)
show_triple = k2.checkbox("Triple Saja", value=False)
show_quad = k3.checkbox("Quad Saja", value=False)

input_bbfs = st.text_input("🎲 Masukkan Angka BBFS:", placeholder="Contoh: 12345", max_chars=10)

st.write("🔍 **Filter Posisi (Eliminasi):**")
c_as, c_kop, c_kep, c_ekor = st.columns(4)
f_as = c_as.text_input("As", max_chars=1)
f_kop = c_kop.text_input("Kop", max_chars=1)
f_kep = c_kep.text_input("Kepala", max_chars=1)
f_ekor = c_ekor.text_input("Ekor", max_chars=1)

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
        # 1. Kumpulkan semua hasil ke dalam satu wadah
        data_hasil = []
        
        # Proses 4D (dengan filter eliminasi)
        if show_4d:
            a4, b4, p4 = get_kombinasi(input_bbfs, 4, data_ada)
            data_hasil.extend([a for a in a4 if not is_tereliminasi(a, f_as, f_kop, f_kep, f_ekor)])
            
        # Proses 3D
        if show_3d:
            a3, b3, p3 = get_kombinasi(input_bbfs, 3, data_ada)
            data_hasil.extend([a for a in a3 if not is_tereliminasi(a, f_as, f_kop, f_kep, f_ekor)])
            
        # Proses 2D
        if show_2d:
            a2, b2, p2 = get_kombinasi(input_bbfs, 2, data_ada)
            data_hasil.extend([a for a in a2 if not is_tereliminasi(a, f_as, f_kop, f_kep, f_ekor)])

        # 2. Tampilkan dengan TABS
        tab1, tab2 = st.tabs(["📋 Tampilan Per Blok (Default)", "📄 Tampilan List (Full)"])
        
        with tab1:
            if data_hasil:
                st.subheader(f"📊 HASIL AKHIR ({len(data_hasil)} Line)")
                for i in range(0, len(data_hasil), 300):
                    akhir = i + 300
                    with st.expander(f"📦 BLOK ({i+1} - {min(akhir, len(data_hasil))})"):
                        st.code("*".join(data_hasil[i:akhir]))
            else:
                st.warning("Tidak ada hasil yang cocok dengan filter.")

        with tab2:
            st.subheader("📝 LIST LENGKAP (Tanpa Blok)")
            st.code("*".join(data_hasil))

    # Ini adalah bagian yang menyebabkan error di foto tadi, pastikan sejajar dengan 'if' di atas
    elif tombol_proses and not input_bbfs:
        st.error("Isi angkanya dulu Koh!")

st.markdown("<p style='text-align: center; font-size: 0.8rem; color: #888;'>© 2026 Mahasewa BBFS Digital Team</p>", unsafe_allow_html=True)










