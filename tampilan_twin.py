import streamlit as st

def proses_pilihan_twin(data_kelompok):
    # 1. Simpan daftar pola ke dalam session_state agar tidak hilang
    if 'pola_terpilih' not in st.session_state:
        st.session_state.pola_terpilih = []

    st.subheader("🛠️ Panel Gabung Pola Twin")
    
    # 2. Tampilkan Checkbox untuk setiap pola yang tersedia
    pilihan_pola = list(data_kelompok.keys())
    terpilih = []
    
    col_check = st.columns(4)
    for i, pola in enumerate(pilihan_pola):
        if col_check[i % 4].checkbox(f"Pola {pola}", key=f"check_{pola}"):
            terpilih.append(pola)
            
    # 3. Tombol untuk eksekusi gabung
    if st.button("🚀 GABUNGKAN POLA TERPILIH"):
        st.session_state.pola_terpilih = terpilih
        
    # 4. Layar 3: Menampilkan hasil gabungan
    if st.session_state.pola_terpilih:
        hasil_gabung = []
        for pola in st.session_state.pola_terpilih:
            hasil_gabung.extend(data_kelompok[pola])
            
        st.divider()
        st.subheader(f"📊 HASIL GABUNGAN ({len(hasil_gabung)} Line)")
        st.code("*".join(hasil_gabung))
    else:
        st.info("Pilih pola di atas lalu klik tombol gabung untuk melihat hasil.")
