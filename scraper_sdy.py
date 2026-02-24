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
    print("Membuka Sydney Pools...")
    # Kita coba link alternatif yang lebih stabil untuk scraping
    driver.get("https://www.sydneypoolstoday.com/")
    time.sleep(20) # Tunggu lebih lama agar tabel angka termuat
    
    # Strategi: Cari semua baris tabel, lalu cari angka 6 digit di dalamnya
    found_data = None
    rows = driver.find_elements(By.TAG_NAME, "tr")
    
    for row in rows:
        text = row.text.replace(" ", "").strip()
        # Cari angka 6 digit yang mungkin nempel dengan teks lain
        import re
        match = re.search(r'\d{6}', text)
        if match:
            found_data = match.group()
            break

    if found_data:
        hasil_4d = found_data[-4:]
        print(f"SDY Berhasil Ditemukan: {found_data} -> 4D: {hasil_4d}")
        with open("data_keluaran_sdy.txt", "a") as f:
            f.write(f"\n{hasil_4d}")
    else:
        # Jika masih gagal, ambil teks dari elemen yang biasanya jadi tempat Prize 1
        print("Mencoba metode cadangan...")
        element = driver.find_element(By.XPATH, "//div[contains(@id, 'prize1')] | //td[contains(@class, 'result')]")
        data_raw = "".join(filter(str.isdigit, element.text))
        if len(data_raw) >= 4:
            hasil_4d = data_raw[-4:]
            with open("data_keluaran_sdy.txt", "a") as f:
                f.write(f"\n{hasil_4d}")
            print(f"SDY Berhasil (Metode Cadangan): {hasil_4d}")
        else:
            print("SDY: Benar-benar tidak menemukan angka di halaman ini.")

except Exception as e:
    print(f"SDY Error Sistem: {e}")
finally:
    driver.quit()
