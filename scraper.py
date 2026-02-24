import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    print("Membuka HK Pools...")
    driver.get("https://www.hongkongpools.com/live.html")
    time.sleep(25) # Menunggu lebih lama agar angka muncul

    # AMBIL SELURUH TEKS DI HALAMAN (Agar tidak kena error 'no such element')
    page_content = driver.find_element(By.TAG_NAME, "body").text
    
    # Cari pola angka 6 digit menggunakan Regex
    all_numbers = re.findall(r'\d{6}', page_content)
    
    found_4d = None
    if all_numbers:
        # Ambil angka 6D pertama yang ditemukan (biasanya Prize 1)
        found_4d = all_numbers[0][-4:]
        print(f"Data ditemukan di teks halaman: {all_numbers[0]} -> 4D: {found_4d}")
    else:
        print("HK: Tidak menemukan pola angka 6D di halaman ini.")

    if found_4d:
        # LOGIKA ANTI-DUPLIKAT
        try:
            with open("data_keluaran_hk.txt", "r") as f:
                lines = f.readlines()
                last_line = lines[-1].strip() if lines else ""
        except FileNotFoundError:
            last_line = ""

        if found_4d != last_line:
            with open("data_keluaran_hk.txt", "a") as f:
                f.write(f"\n{found_4d}")
            print(f"HK Berhasil Simpan: {found_4d}")
        else:
            print(f"HK: Angka {found_4d} sudah ada di baris terakhir, skip.")

except Exception as e:
    print(f"HK Error Sistem: {e}")
finally:
    driver.quit()
