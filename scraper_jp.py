from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_japan_pools():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        url = "https://japanpools.online/apps/resultv2"
        driver.get(url)
        time.sleep(5) # Waktu tunggu dimuatnya tabel
        
        # Mengambil elemen baris pertama dari tabel hasil (asumsi struktur tabel)
        # Menyesuaikan dengan data terbaru di baris pertama
        row = driver.find_element(By.CSS_SELECTOR, "table tbody tr")
        cols = row.find_elements(By.TAG_NAME, "td")
        
        if len(cols) >= 3:
            # Mengambil 6 digit, lalu memotong menjadi 4 digit terakhir
            full_number = cols[2].text.strip()
            data_baru_4d = full_number[-4:] 
            
            # --- LOGIKA ANTI-DUPLIKAT ---
            file_path = "data_keluaran_jp.txt"
            try:
                with open(file_path, "r") as f:
                    lines = f.readlines()
                    last_line = lines[-1].strip() if lines else ""
            except FileNotFoundError:
                last_line = ""

            if data_baru_4d != last_line:
                with open(file_path, "a") as f:
                    # Menambahkan data baru jika belum ada
                    f.write(f"\n{data_baru_4d}")
                print(f"JP Berhasil Simpan: {data_baru_4d}")
            else:
                print(f"JP: Angka {data_baru_4d} sudah ada, skip.")
                
    except Exception as e:
        print(f"JP Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_japan_pools()
