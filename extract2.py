import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
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
target_url = "https://taraffco6.baby/"
driver.get(target_url)

# Sayfanın tamamen yüklenmesini bekle
try:
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    print("✅ Sayfa tamamen yüklendi.")
except Exception as e:
    print("❌ Sayfa yüklenemedi:", e)

# Sayfayı kaydır
try:
    driver.execute_script("window.scrollTo(0, 500);")
    print("✅ Sayfa kaydırıldı.")
except Exception as e:
    print("❌ Sayfa kaydırılamadı:", e)

# <div id="dqqqqq"> öğesine tıkla
try:
    dqqqqq_div = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "dqqqqq"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", dqqqqq_div)
    driver.execute_script("arguments[0].click();", dqqqqq_div)
    print("✅ <div id='dqqqqq'> öğesine tıklandı.")
except Exception as e:
    print("❌ <div id='dqqqqq'> öğesi tıklanamadı:", e)

# <div id="player"> öğesine tıkla
try:
    player_div = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "player"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", player_div)
    driver.execute_script("arguments[0].click();", player_div)
    print("✅ <div id='player'> öğesine tıklandı.")
except Exception as e:
    print("❌ <div id='player'> öğesi tıklanamadı:", e)

# "REKLAMI GEC" butonuna tıkla
try:
    skip_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'REKLAMI GEC')]")
    ))
    ActionChains(driver).move_to_element(skip_button).click().perform()
    print("✅ 'REKLAMI GEC' butonuna tıklandı.")
except Exception as e:
    print("❌ 'REKLAMI GEC' butonu bulunamadı veya tıklanamadı:", e)

# .m3u8 linklerini çekme
logs = driver.get_log("performance")
m3u8_urls = set()

for entry in logs:
    try:
        log_json = json.loads(entry["message"])
        message = log_json.get("message", {})
        if message.get("method") == "Network.responseReceived":
            response_url = message.get("params", {}).get("response", {}).get("url", "")
            if ".m3u8" in response_url and not response_url.startswith("https://video.twimg.com"):
                m3u8_urls.add(response_url)
    except Exception:
        pass

driver.quit()

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

    for class_name, url_suffix in exolig_classes.items():
        new_content = "\n".join(
            [f"<div class='{class_name}' style='display:none'>\n  Lig Sports {index} HD | 3 {url.replace(url.split('/')[-1], url_suffix)} {target_url}\n</div>" 
             for index, url in enumerate(m3u8_urls, start=1)]
        )
        
        # Sınıfa göre içeriği değiştir
        content = re.sub(
            rf'(<div class=[\'\"]{class_name}[\'\"][^>]*>)(.*?)(</div>)',
            rf'\1\n{new_content}\n\3',
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
