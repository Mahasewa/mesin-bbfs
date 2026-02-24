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
    print("Membuka Sydney Pools...")
    driver.get("https://www.sydneypoolstoday.com/")
    time.sleep(30) # Tunggu 30 detik agar semua angka muncul sempurna

    # Ambil semua teks yang ada di halaman web
    page_content = driver.find_element(By.TAG_NAME, "body").text
    print("Menganalisa teks halaman...")

    # Strategi 1: Cari pola angka 6 digit (abaikan yang ada 2026)
    all_6d = re.findall(r'\d{6}', page_content)
    found_4d = None
    
    for num in all_6d:
        if "2026" not in num:
            found_4d = num[-4:]
            break

    # Strategi 2: Jika 6 digit tidak ketemu, cari angka 4 digit yang bukan 2026
    if not found_4d:
        print("Mencoba Strategi 2 (Cari 4 Digit)...")
        all_4d = re.findall(r'\b\d{4}\b', page_content)
        for num in all_4d:
            if num != "2026":
                found_4d = num
                break

    if found_4d:
        # LOGIKA ANTI-DUPLIKAT
        try:
            with open("data_keluaran_sdy.txt", "r") as f:
                lines = f.readlines()
                last_line = lines[-1].strip() if lines else ""
        except FileNotFoundError:
            last_line = ""

        if found_4d != last_line:
            with open("data_keluaran_sdy.txt", "a") as f:
                f.write(f"\n{found_4d}")
            print(f"SDY Berhasil Simpan: {found_4d}")
        else:
            print(f"SDY: Angka {found_4d} sudah ada, skip.")
    else:
        print("SDY: Benar-benar tidak ada angka yang cocok di halaman ini.")
        # Cetak 200 karakter pertama teks halaman untuk diagnosa jika masih gagal
        print("Cuplikan teks web:", page_content[:200])

except Exception as e:
    print(f"SDY Error Sistem: {e}")
finally:
    driver.quit()
