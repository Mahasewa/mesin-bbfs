import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

# Perbaikan: Menggunakan Service agar tidak bentrok versi Chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get("https://www.hongkongpools.com/live.html")
    time.sleep(20) 

    element = driver.find_element(By.CSS_SELECTOR, "td.result, .result-6d, #result-6d")
    hasil_6d = "".join(filter(str.isdigit, element.text))
    hasil_4d = hasil_6d[-4:]

    if len(hasil_4d) == 4:
        try:
            with open("data_keluaran_hk.txt", "r") as f:
                lines = f.readlines()
                last_line = lines[-1].strip() if lines else ""
        except FileNotFoundError:
            last_line = ""

        if hasil_4d != last_line:
            with open("data_keluaran_hk.txt", "a") as f:
                f.write(f"\n{hasil_4d}")
            print(f"HK Berhasil Simpan: {hasil_4d}")
        else:
            print(f"HK: Angka {hasil_4d} sudah ada, skip.")

except Exception as e:
    print(f"HK Error: {e}")
finally:
    driver.quit()
