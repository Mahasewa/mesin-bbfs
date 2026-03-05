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
    driver.get("https://www.hongkongpools.com")
    
    # Tunggu lebih lama agar JavaScript selesai loading
    time.sleep(20) 

    # Mencari angka 6 digit di dalam tabel
    elements = driver.find_elements(By.TAG_NAME, "td")
    
    found_data = None
    for el in elements:
        teks = el.text.strip().replace(" ", "")
        # Mencari teks yang panjangnya 6 angka
        if len(teks) == 6 and teks.isdigit():
            found_data = teks
            break # Ambil yang pertama (Prize 1)

    if found_data:
        hasil_4d = found_data[-4:]
        
        # --- LOGIKA ANTI-DUPLIKAT ---
        try:
            with open("data_keluaran_hk.txt", "r") as f:
                lines = f.readlines()
                # Ambil baris terakhir dan hilangkan spasi/enter
                last_line = lines[-1].strip() if lines else ""
        except FileNotFoundError:
            last_line = ""

        # Hanya tulis jika angka baru tidak sama dengan angka terakhir di file
        if hasil_4d != last_line:
            with open("data_keluaran_hk.txt", "a") as f:
                f.write(f"\n{hasil_4d}")
            print(f"Data Berhasil Ditarik: {found_data} -> 4D: {hasil_4d} (Disimpan)")
        else:
            print(f"Angka {hasil_4d} sudah ada di baris terakhir. Skip simpan.")
        # ----------------------------
        
    else:
        print("Gagal menemukan angka 6D. Website mungkin sedang update.")

except Exception as e:
    print(f"Terjadi Error: {e}")

finally:
    driver.quit()
