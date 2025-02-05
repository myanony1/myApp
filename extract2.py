# Chrome ve Selenium kodu
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
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    print("✅ Sayfa tamamen yüklendi.")
    time.sleep(3)  # 3 saniye bekleme süresi eklendi
except Exception as e:
    print("❌ Sayfa yüklenemedi:", e)

# <div id="dqqqqq"> öğesini sayfadan sil
try:
    driver.execute_script("var element = document.getElementById('dqqqqq'); if(element) { element.remove(); }")
    print("✅ <div id='dqqqqq'> öğesi sayfadan silindi.")
    time.sleep(3)  # 3 saniye bekleme süresi eklendi
except Exception as e:
    print("❌ <div id='dqqqqq'> öğesi sayfadan silinemedi:", e)


# <div id="player"> öğesine tıkla
try:
    player_div = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "player"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", player_div)
    driver.execute_script("arguments[0].click();", player_div)
    print("✅ <div id='player'> öğesine tıklandı.")
time.sleep(10)
except Exception as e:
    print("❌ <div id='player'> öğesi tıklanamadı:", e)


# .m3u8 linklerini çekme
logs = driver.get_log("performance")
m3u8_urls = set()

for entry in logs:
    try:
        log_json = json.loads(entry["message"])
        message = log_json.get("message", {})
        if message.get("method") == "Network.responseReceived":
            response_url = message.get("params", {}).get("response", {}).get("url", "")
            print("Log Girdisi:", response_url)  # Tüm URL'leri yazdırarak incele
            # Filtreleme işlemi burada
            if ".m3u8" in response_url and not response_url.startswith("https://video.twimg.com"):
                m3u8_urls.add(response_url)
                print("✅ .m3u8 URL bulundu:", response_url)
    except Exception as e:
        print("Hata:", e)


driver.quit()

# Dinamik olarak ana domaini belirle
domain = ""
if m3u8_urls:
    sample_url = next(iter(m3u8_urls))  # Set'ten bir URL seç
    domain = "/".join(sample_url.split("/")[:3])  # URL'yi parçalayarak domaini al
    print(f"✅ Domain alındı: {domain}")  # Domaini yazdır

# Güncellenmiş class isimleri ve URL değişiklikleri
exolig_classes = {
    "exoligbir3": "yayinstar.m3u8",
    "exolig2": "yayinb2.m3u8",
    "exolig3": "yayinb3.m3u8",
    "exolig4": "yayinb4.m3u8",
    "exolig5": "yayinb5.m3u8",
}

# HTML dosyasını aç ve içeriği güncelle
try:
    with open(".index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Sadece var olan div'lerin içeriğini güncelle
    for class_name, url_suffix in exolig_classes.items():
        # Tam URL'yi oluştur
        full_url = f"{domain}/list/{url_suffix}"  # Dinamik olarak domain ve URL'yi birleştir
        
        # Div içeriğini güncelle
        updated_content = f"  Lig Sports HD | 3 {full_url} {target_url}\n"
        
        # Div içeriğini değiştir
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

