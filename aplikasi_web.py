import streamlit as st
import re
import itertools

# --- JUDUL APLIKASI ---
st.set_page_config(page_title="Mahasewa BBFS Digital", layout="wide")
st.title("🚀 MAHASEWA BBFS DIGITAL")

# --- INPUT BBFS ---
input_bbfs = st.text_input("🔢 Masukkan Angka BBFS:", placeholder="Contoh: 12345", max_chars=10)

col1, col2, col3 = st.columns(3)
with col1:
    show_twin = st.checkbox("Twin (4D)", value=False)
with col2:
    show_triple = st.checkbox("Triple (4D)", value=False)
with col3:
    show_quad = st.checkbox("Quad (4D)", value=False)

tombol_proses = st.button("🚀 PROSES SEKARANG")

# --- LOGIKA MESIN BBFS MURNI ---
if tombol_proses:
    if input_bbfs:
        # 1. Bersihkan input (hanya ambil angka)
        angka = re.findall(r'\d', input_bbfs)
        angka_unik = sorted(list(set(angka)))
        
        if len(angka_unik) < 4:
            st.error("Masukkan minimal 4 digit angka yang berbeda!")
        else:
            # 2. Generate Kombinasi 4D Standar (Tanpa Kembar)
            kombinasi_4d = list(itertools.permutations(angka_unik, 4))
            hasil = ["".join(p) for p in kombinasi_4d]
            
            # 3. Logika Tambahan (Twin, Triple, Quad)
            if show_twin:
                # Tambah logika twin di sini jika Koh mau
                pass
            
            # 4. Tampilkan Hasil
            st.success(f"✅ Berhasil generate {len(hasil)} line 4D.")
            st.write(hasil)
    else:
        st.warning("Kotak input masih kosong, Koh!")

# --- FOOTER ---
st.markdown("---")
st.markdown('<p style="text-align: center; color: #888;">© 2026 Mahasewa BBFS Digital Team</p>', unsafe_allow_html=True)
