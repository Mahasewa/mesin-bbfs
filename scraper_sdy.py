import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

driver = webdriver.Chrome(options=options)

try:
    print("Membuka Sydney Pools...")
    driver.get("https://www.sydneypoolstoday.com/")
    time.sleep(15)
    
    # Mencari angka 6 digit di dalam semua baris tabel (td)
    elements = driver.find_elements(By.TAG_NAME, "td")
    found_data = None
    
    for el in elements:
        teks = el.text.strip().replace(" ", "")
        # Cari angka yang panjangnya 6 digit
        if len(teks) == 6 and teks.isdigit():
            found_data = teks
            break

    if found_data:
        hasil_4d = found_data[-4:]
        print(f"SDY Berhasil: {found_data} -> 4D: {hasil_4d}")
        with open("data_keluaran_sdy.txt", "a") as f:
            f.write(f"\n{hasil_4d}")
    else:
        print("SDY: Angka tidak ditemukan di tabel.")

except Exception as e:
    print(f"SDY Error: {e}")
finally:
    driver.quit()
