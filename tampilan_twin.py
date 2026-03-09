import streamlit as st

def proses_pilihan_twin(data_kelompok):
    # Hitung total semua angka twin untuk judul utama
    total_semua = sum(len(daftar) for daftar in data_kelompok.values())
    
    st.subheader(f"📊 DAFTAR POLA TWIN 4D {total_semua} Line")
    
    # Inisialisasi memori pilihan jika belum ada
    if 'pilihan_twin' not in st.session_state:
        st.session_state.pilihan_twin = {pola: False for pola in data_kelompok.keys()}

    # Tampilkan daftar dengan pola yang diminta
    for pola, daftar in data_kelompok.items():
        col_check, col_exp = st.columns([1, 10])
        
        # Checkbox menempel di kiri
        with col_check:
            # Status dibaca dan disimpan ke session_state agar tidak hilang saat rerun
            status = st.checkbox("", key=f"cb_{pola}", value=st.session_state.pilihan_twin.get(pola, False))
            st.session_state.pilihan_twin[pola] = status
            
        # Expander (Tampilan Lama) di kanan
        with col_exp:
            with st.expander(f"🔹 Pola {pola} {len(daftar)} Line"):
                st.code("*".join(daftar))
                
    st.divider()
    
    # Tombol Aksi
    if st.button("🚀 GABUNGKAN POLA TERPILIH"):
        hasil_gabung = []
        for pola, terpilih in st.session_state.pilihan_twin.items():
            if terpilih:
                hasil_gabung.extend(data_kelompok[pola])
        
        if hasil_gabung:
            st.subheader(f"✅ HASIL GABUNGAN ({len(hasil_gabung)} Line)")
            st.code("*".join(hasil_gabung))
        else:
            st.warning("Pilih dulu pola yang mau digabung, Koh.")
