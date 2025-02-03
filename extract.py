import time
import json
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
target_url = "https://trgoals1150.xyz/"
driver.get(target_url)

# "player-poster" div'ine tıklamayı dene
try:
    poster = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "play-wrapper"))
    )
    ActionChains(driver).move_to_element(poster).click().perform()
    print("Player poster'ına tıklandı.")
except Exception as e:
    print("Player poster butonu bulunamadı veya tıklanamadı:", e)

# 20 saniye bekle
print("Video yükleniyor, 20 saniye bekleniyor...")
time.sleep(20)

# Chrome performans loglarını çek
logs = driver.get_log("performance")

# ".m3u8" içeren URL'leri bul
m3u8_urls = set()

for entry in logs:
    try:
        log_json = json.loads(entry["message"])
        message = log_json.get("message", {})
        if message.get("method") == "Network.responseReceived":
            response_url = message.get("params", {}).get("response", {}).get("url", "")
            if ".m3u8" in response_url:
                m3u8_urls.add(response_url)
    except Exception:
        pass  # Hataları yoksay

driver.quit()

# Bulunan URL'leri urls.html dosyasına yaz
with open("urls.html", "w", encoding="utf-8") as f:
    f.write("<html><body>\n")
    for url in m3u8_urls:
        f.write(f"<p>{url}</p>\n")
    f.write("</body></html>\n")

print("Extraction complete. URLs written to urls.html")
