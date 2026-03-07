import streamlit as st

def tampilkan_hasil_tab(data_hasil, a4_final):
    # Membuat Tab
    tab1, tab2 = st.tabs(["Layar 1: Hasil Ringkas", "Layar 2: Full 4D Acak"])
    
    with tab1:
        # Memanggil fungsi cetak dari file utama
        from __main__ import cetak_hasil_blok
        cetak_hasil_blok("HASIL BBFS", data_hasil)
        
    with tab2:
        if a4_final:
            # Di sini kita tambahkan {len(a4_final)} ke judulnya
            st.subheader(f"SEMUA HASIL 4D ACAK ({len(a4_final)} Line)")
            st.code("*".join(a4_final))
        else:
            st.info("Tidak ada data 4D untuk ditampilkan.")
