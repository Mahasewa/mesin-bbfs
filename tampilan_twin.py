import streamlit as st

def proses_pilihan_twin(data_kelompok):
    st.subheader("📊 DAFTAR POLA TWIN 4D")
    
    # Inisialisasi state untuk menampung pilihan checkbox
    if 'pilihan_twin' not in st.session_state:
        st.session_state.pilihan_twin = {pola: False for pola in data_kelompok.keys()}

    # Tampilkan Pola dengan Checkbox di Sampingnya
    for pola, daftar in data_kelompok.items():
        # Membuat kolom: Sempit untuk checkbox, lebar untuk expander
        c1, c2 = st.columns([1, 10])
        
        # Checkbox di kolom 1
        is_checked = st.checkbox(f"Pilih", key=f"cb_{pola}", value=st.session_state.pilihan_twin[pola])
        st.session_state.pilihan_twin[pola] = is_checked
        
        # Expander di kolom 2
        with c2.expander(f"🔹 POLA {pola} ({len(daftar)} Line)"):
            st.code("*".join(daftar))
            
    st.divider()
    
    # Tombol Eksekusi
    if st.button("🚀 GABUNGKAN POLA TERPILIH"):
        hasil_gabung = []
        for pola, checked in st.session_state.pilihan_twin.items():
            if checked:
                hasil_gabung.extend(data_kelompok[pola])
            
        if hasil_gabung:
            st.subheader(f"📊 HASIL GABUNGAN ({len(hasil_gabung)} Line)")
            st.code("*".join(hasil_gabung))
        else:
            st.warning("Belum ada pola yang diceklis!")
