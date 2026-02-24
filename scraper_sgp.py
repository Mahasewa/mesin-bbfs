import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
    driver.get("https://www.singaporepools.com.sg/en/product/pages/4d_results.aspx")
    time.sleep(15)
    
    # Ambil Winning Number Pertama (Prize 1)
    element = driver.find_element(By.CLASS_NAME, "winning-number-1")
    hasil_4d = element.text.strip()

    if len(hasil_4d) == 4:
        with open("data_keluaran_sgp.txt", "a") as f:
            f.write(f"\n{hasil_4d}")
        print(f"SGP Berhasil: {hasil_4d}")
except Exception as e:
    print(f"SGP Error: {e}")
finally:
    driver.quit()
