import streamlit as st

def proses_pilihan_twin(data_kelompok):
    st.subheader("📊 DAFTAR POLA TWIN 4D")
    
    # 1. Tampilkan tampilan lama (seperti expander) agar Koh tahu pilihannya
    for pola, daftar in data_kelompok.items():
        with st.expander(f"🔹 POLA {pola} ({len(daftar)} Line)"):
            st.code("*".join(daftar))
            
    st.divider()
    
    # 2. Panel Pilihan (Checkbox)
    st.subheader("🛠️ Panel Gabung Pola Twin")
    pilihan_pola = list(data_kelompok.keys())
    terpilih = []
    
    col_check = st.columns(4)
    for i, pola in enumerate(pilihan_pola):
        if col_check[i % 4].checkbox(f"Pola {pola}"):
            terpilih.append(pola)
            
    # 3. Tombol Eksekusi
    if st.button("🚀 GABUNGKAN POLA TERPILIH"):
        hasil_gabung = []
        for pola in terpilih:
            hasil_gabung.extend(data_kelompok[pola])
            
        # 4. Layar 3: Hasil Gabungan
        st.divider()
        st.subheader(f"📊 HASIL GABUNGAN ({len(hasil_gabung)} Line)")
        st.code("*".join(hasil_gabung))
