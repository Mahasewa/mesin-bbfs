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
    driver.get("https://www.sydneypoolstoday.com/")
    time.sleep(15)
    
    # Mencari angka result di tabel utama SDY
    element = driver.find_element(By.ID, "prizetitle") # Contoh ID umum di web SDY
    hasil_6d = "".join(filter(str.isdigit, element.text))
    hasil_4d = hasil_6d[-4:]

    if len(hasil_4d) == 4:
        with open("data_keluaran_sdy.txt", "a") as f:
            f.write(f"\n{hasil_4d}")
        print(f"SDY Berhasil: {hasil_4d}")
except Exception as e:
    print(f"SDY Error: {e}")
finally:
    driver.quit()
