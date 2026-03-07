import streamlit as st

def proses_pilihan_twin(data_kelompok):
    st.subheader("📊 DAFTAR POLA TWIN 4D")
    
    # 1. Tampilkan pola (statis)
    for pola, daftar in data_kelompok.items():
        with st.expander(f"🔹 POLA {pola} ({len(daftar)} Line)"):
            st.code("*".join(daftar))
            
    st.divider()
    
    # 2. Panel Pilihan dengan SESSION STATE agar tidak hilang saat di-klik
    st.subheader("🛠️ Panel Gabung Pola Twin")
    
    if 'pilihan_checkbox' not in st.session_state:
        st.session_state.pilihan_checkbox = {}

    col_check = st.columns(4)
    for i, pola in enumerate(data_kelompok.keys()):
        # Menyimpan status checkbox ke session_state
        is_checked = st.session_state.pilihan_checkbox.get(pola, False)
        if col_check[i % 4].checkbox(f"Pola {pola}", value=is_checked, key=f"check_{pola}"):
            st.session_state.pilihan_checkbox[pola] = True
        else:
            st.session_state.pilihan_checkbox[pola] = False

    # 3. Tombol Eksekusi
    if st.button("🚀 GABUNGKAN POLA TERPILIH"):
        hasil_gabung = []
        for pola, checked in st.session_state.pilihan_checkbox.items():
            if checked:
                hasil_gabung.extend(data_kelompok[pola])
            
        # 4. Hasil Gabungan
        st.divider()
        st.subheader(f"📊 HASIL GABUNGAN ({len(hasil_gabung)} Line)")
        st.code("*".join(hasil_gabung))
