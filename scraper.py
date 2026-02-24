import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# Menyamarkan bot agar terlihat seperti browser Chrome biasa
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)

try:
    print("Sedang menyambung ke Hongkong Pools...")
    driver.get("https://www.hongkongpools.com/live.html")
    
    # Tunggu lebih lama (20 detik) agar JavaScript selesai loading
    time.sleep(20) 

    # Mengambil semua teks di halaman untuk cadangan jika elemen spesifik gagal
    page_text = driver.find_element(By.TAG_NAME, "body").text
    
    # Mencari angka 6 digit di dalam tabel
    # Kita cari elemen <td> yang isinya angka
    elements = driver.find_elements(By.TAG_NAME, "td")
    
    found_data = None
    for el in elements:
        teks = el.text.strip().replace(" ", "")
        # Jika ketemu teks yang panjangnya 6 angka
        if len(teks) == 6 and teks.isdigit():
            found_data = teks
            break # Ambil yang pertama ketemu (biasanya Prize 1)

    if found_data:
        hasil_4d = found_data[-4:]
        print(f"Data Berhasil Ditarik: {found_data} -> 4D: {hasil_4d}")
        
        with open("data_keluaran_hk.txt", "a") as f:
            f.write(f"\n{hasil_4d}")
    else:
        print("Gagal menemukan angka 6D. Website mungkin sedang maintenance atau proteksi aktif.")
        # Cetak sedikit isi halaman untuk diagnosa
        print("Isi halaman (potongan):", page_text[:200])

except Exception as e:
    print(f"Terjadi Error: {e}")

finally:
    driver.quit()
