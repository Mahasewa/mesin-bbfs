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
    driver.get("https://www.singaporepools.com.sg/en/product/pages/4d_results.aspx")
    time.sleep(25)
    
    try:
        element = driver.find_element(By.CLASS_NAME, "winning-number-1")
        hasil_4d = element.text.strip()
    except:
        # Cadangan jika elemen class tidak ketemu
        elements = driver.find_elements(By.TAG_NAME, "td")
        hasil_4d = next((el.text.strip() for el in elements if len(el.text.strip()) == 4 and el.text.strip().isdigit()), None)

    if hasil_4d:
        # LOGIKA ANTI-DUPLIKAT
        try:
            with open("data_keluaran_sgp.txt", "r") as f:
                lines = f.readlines()
                last_line = lines[-1].strip() if lines else ""
        except FileNotFoundError:
            last_line = ""

        if hasil_4d != last_line:
            with open("data_keluaran_sgp.txt", "a") as f:
                f.write(f"\n{hasil_4d}")
            print(f"SGP Berhasil Simpan: {hasil_4d}")
        else:
            print(f"SGP: Angka {hasil_4d} sudah ada, skip.")

except Exception as e:
    print(f"SGP Error: {e}")
finally:
    driver.quit()
