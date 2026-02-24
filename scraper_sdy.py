import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def scrape_sdy(url, name):
    driver = get_driver()
    try:
        print(f"Mencoba mengambil data dari {name}...")
        driver.get(url)
        time.sleep(25)
        
        page_content = driver.find_element(By.TAG_NAME, "body").text
        
        # Cari pola 6 angka
        all_6d = re.findall(r'\d{6}', page_content)
        for num in all_6d:
            if "2026" not in num:
                return num[-4:]
        
        # Cari pola 4 angka (Backup)
        all_4d = re.findall(r'\b\d{4}\b', page_content)
        for num in all_4d:
            if num != "2026":
                return num
                
        return None
    except Exception as e:
        print(f"Error di {name}: {e}")
        return None
    finally:
        driver.quit()

# --- MAIN PROGRAM ---
# Link 1: Utama, Link 2: Backup
targets = [
    {"name": "SydneyPoolsToday", "url": "https://www.sydneypoolstoday.com/"},
    {"name": "Link IP Backup", "url": "http://188.166.180.129/live-draw-sdy.php"}
]

hasil_4d = None
for target in targets:
    hasil_4d = scrape_sdy(target['url'], target['name'])
    if hasil_4d:
        print(f"Berhasil mendapatkan data dari {target['name']}: {hasil_4d}")
        break
    else:
        print(f"Gagal mendapatkan data dari {target['name']}, mencoba link berikutnya...")

if hasil_4d:
    # LOGIKA ANTI-DUPLIKAT
    try:
        with open("data_keluaran_sdy.txt", "r") as f:
            lines = f.readlines()
            last_line = lines[-1].strip() if lines else ""
    except FileNotFoundError:
        last_line = ""

    if hasil_4d != last_line:
        with open("data_keluaran_sdy.txt", "a") as f:
            f.write(f"\n{hasil_4d}")
        print(f"SDY Sukses Simpan: {hasil_4d}")
    else:
        print(f"SDY: Angka {hasil_4d} sudah ada, skip.")
else:
    print("SDY: Semua link gagal memberikan data.")
