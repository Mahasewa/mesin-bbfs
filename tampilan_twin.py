import streamlit as st

def proses_pilihan_twin(data_kelompok):
    st.subheader("📊 KATALOG POLA TWIN 4D")
    
    # 1. Tampilkan katalog (Hanya label dan expander)
    # Gunakan session_state untuk menyimpan pilihan tanpa memicu aksi
    for pola, daftar in data_kelompok.items():
        # Kolom untuk checkmark dan label
        col1, col2 = st.columns([1, 10])
        
        # Checkbox di sini cuma mengubah nilai di memori, TIDAK memicu aksi apa pun
        key_pola = f"cb_{pola}"
        st.session_state[key_pola] = col1.checkbox(f"Pilih", key=key_pola)
        
        # Expander hanya untuk melihat isi data
        with col2.expander(f"🔹 POLA {pola} ({len(daftar)} Line)"):
            st.code("*".join(daftar))
            
    st.divider()
    
    # 2. Tombol Aksi (Hanya di sini terjadi proses gabung data)
    if st.button("🚀 GABUNGKAN POLA TERPILIH"):
        hasil_gabung = []
        
        # Baru sekarang kita cek mana saja yang dicentang
        for pola in data_kelompok.keys():
            if st.session_state[f"cb_{pola}"]:
                hasil_gabung.extend(data_kelompok[pola])
        
        # Tampilkan Hasil di bawah
        if hasil_gabung:
            st.subheader(f"📊 HASIL GABUNGAN ({len(hasil_gabung)} Line)")
            st.code("*".join(hasil_gabung))
        else:
            st.warning("Belum ada pola yang dipilih, Koh!")
