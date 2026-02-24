import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Konfigurasi Browser
options = Options()
options.add_argument("--headless") # Berjalan di background
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
    driver.get("https://www.hongkongpools.com/live.html")
    time.sleep(10) # Menunggu web loading sempurna

    # Mencari elemen hasil 6D (biasanya di baris pertama tabel)
    # Kita ambil angka dari kolom result
    element = driver.find_element(By.XPATH, "//td[contains(@class, 'result')]")
    hasil_6d = element.text.replace(" ", "").strip()
    
    # Ambil 4 angka terakhir
    hasil_4d = hasil_6d[-4:]

    if len(hasil_4d) == 4:
        with open("data_keluaran_hk.txt", "a") as f:
            f.write(f"\n{hasil_4d}")
        print(f"Berhasil simpan 4D: {hasil_4d}")
    else:
        print("Data tidak valid atau belum update.")

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
