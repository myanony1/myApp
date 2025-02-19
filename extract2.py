import json
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome seçeneklerini ayarla
chrome_options = Options()
chrome_options.add_argument('--headless')  # Arka planda çalıştır
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

# ChromeDriver'ı başlat
driver = webdriver.Chrome(options=chrome_options)

# Hedef URL'yi aç
target_url = "https://popk24.cfd/channel.html?id=yayinstar"
driver.get(target_url)

# Sayfanın tamamen yüklenmesini bekle
try:
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    print("✅ Sayfa tamamen yüklendi.")
except Exception as e:
    print("❌ Sayfa yüklenemedi:", e)

# Sayfa içindeki baseurl değerini almak için JavaScript çalıştır
try:
    base_url = driver.execute_script("return window.config.match.source.split('/list/')[0];")
    print(f"✅ Base URL alındı: {base_url}")
except Exception as e:
    print("❌ Base URL alınamadı:", e)
    base_url = ""  # Hata olursa boş bırak

# Güncellenmiş class isimleri ve URL değişiklikleri
exolig_classes = {
    "exoligbir3": ("Lig Sports 1 HD | 3", "yayinstar.m3u8"),
    "exolig2": ("Lig Sports 2 HD", "yayinb2.m3u8"),
    "exolig3": ("Lig Sports 3 HD", "yayinb3.m3u8"),
    "exolig4": ("Lig Sports 4 HD", "yayinb4.m3u8"),
    "exolig5": ("Lig Sports 5 HD", "yayinb5.m3u8"),
    "exoss1": ("S Sport 1 HD", "yayinss.m3u8"),  # Yeni eklendi
    "exoss2": ("S Sport 2 HD", "yayinss2.m3u8"),  # Yeni eklendi
    "exot1": ("Tivibu Spor 1 HD", "yayint1.m3u8"),  # Yeni eklendi
    "exot2": ("Tivibu Spor 2 HD", "yayint2.m3u8"),  # Yeni eklendi
    "exot3": ("Tivibu Spor 3 HD", "yayint3.m3u8"),  # Yeni eklendi
    "exot4": ("Tivibu Spor 4 HD", "yayint4.m3u8"),  # Yeni eklendi
}

# HTML dosyasını aç ve içeriği güncelle
try:
    with open(".index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Sadece var olan div'lerin içeriğini güncelle
    for class_name, (lig_sports_name, url_suffix) in exolig_classes.items():
        # Tam URL'yi oluştur
        full_url = f"{base_url}/list/{url_suffix}" if base_url else "#"

        # Güncellenmiş içerik
        updated_content = f"  {lig_sports_name} {full_url} {target_url}\n"

        # HTML'deki ilgili div içeriğini değiştir
        content = re.sub(
            rf'(<div class=[\'\"]{class_name}[\'\"][^>]*>)(.*?)(</div>)',
            rf'\1\n{updated_content}\n\3',
            content,
            flags=re.DOTALL
        )

    # Eğer içerik değiştiyse dosyayı güncelle
    with open(".index.html", "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ {', '.join(exolig_classes.keys())} div içerikleri güncellendi.")

except FileNotFoundError:
    print("❌ Hata: .index.html dosyası bulunamadı.")
except Exception as e:
    print(f"❌ Dosya güncellenirken hata oluştu: {e}")

# Tarayıcıyı kapat
driver.quit()
