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

# 1️⃣ .player-poster.clickable öğesine tıklama
try:
    player_poster = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "player-poster.clickable"))
    )
    ActionChains(driver).move_to_element(player_poster).click().perform()
    print("✅ .player-poster.clickable tıklandı.")
except Exception as e:
    print("❌ .player-poster.clickable tıklanamadı:", e)

# 2️⃣ 7 saniye bekle
WebDriverWait(driver, 10).until(lambda driver: True)  # 7 saniye bekletme

# 3️⃣ "REKLAMI GEC" butonuna tıklama
try:
    skip_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'REKLAMI GEC')]"))
    )
    ActionChains(driver).move_to_element(skip_button).click().perform()
    print("✅ 'REKLAMI GEC' butonuna tıklandı.")
except Exception as e:
    print("❌ 'REKLAMI GEC' butonu bulunamadı veya tıklanamadı:", e)

# 4️⃣ .m3u8 linklerini çekme
logs = driver.get_log("performance")
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

# 5️⃣ URLs'yi urls.html dosyasına yaz
with open("urls.html", "w", encoding="utf-8") as f:
    f.write("<html><body>\n")
    for url in m3u8_urls:
        f.write(f"<p>{url}</p>\n")
    f.write("</body></html>\n")

print("✅ Extraction complete. URLs written to urls.html")
