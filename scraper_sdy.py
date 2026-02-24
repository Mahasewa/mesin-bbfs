import time
import re
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
    driver.get("https://www.sydneypoolstoday.com/")
    time.sleep(20)
    
    table_text = driver.find_element(By.TAG_NAME, "table").text
    all_numbers = re.findall(r'\d{6}', table_text)
    
    found_4d = None
    for num in all_numbers:
        if "2026" not in num: # Hindari ambil angka tahun
            found_4d = num[-4:]
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

except Exception as e:
    print(f"SDY Error: {e}")
finally:
    driver.quit()
