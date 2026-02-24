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
    print("Membuka Singapore Pools...")
    # Menggunakan link mobile/result yang lebih ringan
    driver.get("https://www.singaporepools.com.sg/en/product/pages/4d_results.aspx")
    time.sleep(20)
    
    # SGP biasanya punya class 'winning-number-1' untuk Prize 1
    try:
        element = driver.find_element(By.CLASS_NAME, "winning-number-1")
        hasil_4d = element.text.strip()
        
        if len(hasil_4d) == 4 and hasil_4d.isdigit():
            print(f"SGP Berhasil: {hasil_4d}")
            with open("data_keluaran_sgp.txt", "a") as f:
                f.write(f"\n{hasil_4d}")
        else:
            print(f"SGP: Data ditemukan tapi format salah: {hasil_4d}")
    except:
        # Cadangan: Cari angka 4 digit di tabel mana saja
        elements = driver.find_elements(By.TAG_NAME, "td")
        for el in elements:
            teks = el.text.strip()
            if len(teks) == 4 and teks.isdigit():
                print(f"SGP Berhasil (Cadangan): {teks}")
                with open("data_keluaran_sgp.txt", "a") as f:
                    f.write(f"\n{teks}")
                break

except Exception as e:
    print(f"SGP Error: {e}")
finally:
    driver.quit()
