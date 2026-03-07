import streamlit as st

def tampilkan_hasil_tab(data_hasil, a4_final):
    # Membuat Tab
    tab1, tab2 = st.tabs(["Layar 1: Hasil Ringkas", "Layar 2: Full 4D Acak"])
    
    with tab1:
        # Panggil fungsi cetak_hasil_blok yang sudah ada di file utama
        # Jika cetak_hasil_blok masih pakai loop 300, itu akan memecah per 300 angka
        from __main__ import cetak_hasil_blok
        cetak_hasil_blok("HASIL BBFS", data_hasil)
        
    with tab2:
        if a4_final:
            st.subheader("SEMUA HASIL 4D ACAK (FULL LIST)")
            # PENTING: Gunakan "*".join(a4_final) agar muncul bintang antar angka
            # TANPA spasi, dan st.code akan membuat blok kode rapi
            st.code("*".join(a4_final))
        else:
            st.info("Tidak ada data 4D untuk ditampilkan.")
