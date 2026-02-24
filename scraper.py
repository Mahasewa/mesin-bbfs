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

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    print("Membuka hongkongpools.com...")
    driver.get("https://www.hongkongpools.com/")
    time.sleep(25) # Menunggu tabel benar-benar muncul

    # Strategi: Cari baris pertama (tr) di dalam tabel (tbody)
    # Biasanya kolom 'Result' ada di kolom ke-4 (td[4])
    try:
        # Kita ambil baris pertama dari data tabel
        baris_pertama = driver.find_element(By.XPATH, "//table//tbody/tr[1]")
        kolom_result = baris_pertama.find_element(By.XPATH, "./td[4]").text
        
        # Bersihkan data (ambil angka saja)
        hasil_6d = "".join(filter(str.isdigit, kolom_result))
        
        if len(hasil_6d) >= 4:
            hasil_4d = hasil_6d[-4:]
            print(f"Data tabel ditemukan: {hasil_6d} -> 4D: {hasil_4d}")
            
            # LOGIKA ANTI-DUPLIKAT
            try:
                with open("data_keluaran_hk.txt", "r") as f:
                    lines = f.readlines()
                    last_line = lines[-1].strip() if lines else ""
            except FileNotFoundError:
                last_line = ""

            if hasil_4d != last_line:
                with open("data_keluaran_hk.txt", "a") as f:
                    f.write(f"\n{hasil_4d}")
                print(f"HK Berhasil Simpan ke File: {hasil_4d}")
            else:
                print(f"HK: Angka {hasil_4d} sudah ada di baris terakhir, skip.")
        else:
            print(f"Format angka tidak sesuai: {kolom_result}")

    except Exception as e_inner:
        print(f"Gagal membaca baris tabel: {e_inner}")
        # Cadangan: Jika XPath gagal, pakai cara ambil semua teks seperti tadi
        print("Menjalankan metode cadangan (Scan Teks)...")
        import re
        page_text = driver.find_element(By.TAG_NAME, "body").text
        all_6d = re.findall(r'\d{6}', page_text)
        if all_6d:
            # Ambil yang paling atas (terbaru)
            hasil_4d = all_6d[0][-4:]
            # Jalankan logika simpan yang sama...
            with open("data_keluaran_hk.txt", "a") as f: f.write(f"\n{hasil_4d}")

except Exception as e:
    print(f"HK Error Sistem: {e}")
finally:
    driver.quit()
