import streamlit as st
import re
import requests
import itertools
from itertools import permutations
from bs4 import beautifulSoup
import datetime
import os
import base64
import json

# --- LOGIKA MESIN: UPDATE KE GITHUB ---
def update_dan_tata_kolom(pasaran, angka_baru):
    try:
        # Mengambil Token dari Secrets Streamlit
        token = st.secrets["github_token"]
        repo = "Mahasewa/mesin-bbfs"
        path = f"data_keluaran_{pasaran.lower()}.txt"
        url = f"https://api.github.com/repos/{repo}/contents/{path}"
        headers = {"Authorization": f"token {token}"}

        # 1. Ambil file lama dari GitHub
        res = requests.get(url, headers=headers)
        if res.status_code != 200: 
            return False
        
        file_data = res.json()
        content = base64.b64decode(file_data['content']).decode('utf-8')
        lines = content.splitlines(keepends=True)

        # 2. Cek data terakhir agar tidak double
        baris_terakhir_isi = lines[-1].strip().split() if lines else []
        if baris_terakhir_isi and baris_terakhir_isi[-1] == angka_baru:
            return False

        # 3. Logika 7 Kolom
        if not lines or len(baris_terakhir_isi) >= 7:
            # Buat baris baru di bawah
            new_content = content.rstrip() + f"\n{angka_baru}"
        else:
            # Tambah ke samping dengan jarak 4 spasi
            lines[-1] = lines[-1].rstrip() + f"    {angka_baru}"
            new_content = "".join(lines)

        # 4. Kirim kembali ke GitHub
        payload = {
            "message": f"Update {pasaran} otomatis",
            "content": base64.b64encode(new_content.encode('utf-8')).decode('utf-8'),
            "sha": file_data['sha']
        }
        requests.put(url, headers=headers, json=payload)
        return True
    except:
        return False

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
        if tipe == 2 and max_c == 2: final.append(h)
        elif tipe == 3 and max_c == 3: final.append(h)
        elif tipe == 4 and max_c == 4: final.append(h)
    return sorted(list(set(final)))

def kelompokkan_twin(daftar_angka):
    kelompok = {}
    for angka in daftar_angka:
        mapping = {}
        pola = ""
        for char in angka:
            if char not in mapping:
                mapping[char] = chr(65 + len(mapping))
            pola += mapping[char]
        if pola not in kelompok:
            kelompok[pola] = []
        kelompok[pola].append(angka)
    return kelompok

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
        padding: 20px !important;
        line-height: 2.5 !important;      
        overflow: visible !important;      
        border: 1px solid #eeeeee !important; 
        font-weight: bold !important;
        font-size: 1.1rem !important;
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

col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2:
    logo_url = "https://raw.githubusercontent.com/Mahasewa/mesin-bbfs/main/logo_mahasewa.png"
    st.image(logo_url, use_container_width=True)
    st.markdown("<h2 style='text-align: center; color: #FF4B4B;'>MAHASEWA BBFS</h2>", unsafe_allow_html=True)

st.divider()

pasaran_pilih = st.selectbox("🎯 Pilih Pasaran:", ("Hong Kong (HK)", "Sydney (SDY)", "Singapore (SGP)"))

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

file_map = {"Hong Kong (HK)": "data_keluaran_hk.txt", "Sydney (SDY)": "data_keluaran_sdy.txt", "Singapore (SGP)": "data_keluaran_sgp.txt"}
URL_DATA = f"https://raw.githubusercontent.com/Mahasewa/mesin-bbfs/main/{file_map[pasaran_pilih]}"
try:
    respon = requests.get(URL_DATA)
    data_ada = set(re.findall(r'\b\d{4}\b', respon.text

