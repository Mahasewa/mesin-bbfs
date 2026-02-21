import streamlit as st
import re
import itertools

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="MAHASEWA BBFS DIGITAL", page_icon="🚀", layout="wide")

# --- CSS CUSTOM (BIAR TAMPILAN KEREN SEPERTI DULU) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background: linear-gradient(45deg, #ff4b4b, #ff814b);
        color: white;
        font-weight: bold;
        border: none;
        height: 3em;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
        text-align: center;
        font-size: 20px;
    }
    .header-text {
        text-align: center;
        color: #ff4b4b;
        font-family: 'Arial Black';
        text-shadow: 2px 2px #000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGO DAN JUDUL (Tampilan Jadul Koh) ---
st.markdown("<h1 class='header-text'>🚀 MAHASEWA BBFS DIGITAL</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Solusi Cerdas BBFS 4D/3D/2D</p>", unsafe_allow_html=True)

# --- INPUT AREA ---
input_bbfs = st.text_input("🔢 MASUKKAN ANGKA BBFS (Max 10 Digit):", placeholder="Contoh: 12345")

# Kolom Twin, Triple, Quad
k1, k2, k3 = st.columns(3)
with k1:
    show_twin = st.checkbox("Twin (4D)", value=False)
with k2:
    show_triple = st.checkbox("Triple (4D)", value=False)
with k3:
    show_quad = st.checkbox("Quad (4D)", value=False)

tombol_proses = st.button("🚀 PROSES SEKARANG")

# --- MESIN UTAMA BBFS ---
if tombol_proses:
    if input_bbfs:
        # Hanya ambil angka
        angka_raw = re.findall(r'\d', input_bbfs)
        angka_unik = sorted(list(set(angka_raw)))
        
        if len(angka_unik) < 2:
            st.error("❌ Masukkan minimal 2 digit angka!")
        else:
            # Fungsi BBFS Murni
            def bbfs_generate(n):
                return ["".join(p) for p in itertools.permutations(angka_unik, n)]

            # Menampilkan hasil dalam kolom yang rapi
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.markdown("### 🔴 4D")
                hasil_4d = bbfs_generate(4)
                st.write(f"Total: {len(hasil_4d)}")
                st.text_area("Hasil 4D", value=", ".join(hasil_4d), height=200)

            with col_b:
                st.markdown("### 🟡 3D")
                hasil_3d = bbfs_generate(3)
                st.write(f"Total: {len(hasil_3d)}")
                st.text_area("Hasil 3D", value=", ".join(hasil_3d), height=200)

            with col_c:
                st.markdown("### 🟢 2D")
                hasil_2d = bbfs_generate(2)
                st.write(f"Total: {len(hasil_2d)}")
                st.text_area("Hasil 2D", value=", ".join(hasil_2d), height=200)
            
            st.success("✅ Angka Berhasil Diolah!")
    else:
        st.warning("⚠️ Kotak input masih kosong, Koh!")

# --- FOOTER ---
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 0.8rem; color: #888;">© 2026 Mahasewa BBFS Digital Team</p>', unsafe_allow_html=True)
