import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome seçeneklerini ayarlıyoruz
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

# ChromeDriver'ı başlatıyoruz
driver = webdriver.Chrome(options=chrome_options)

# Hedef URL'yi açıyoruz
target_url = "https://sonbahistv5.pages.dev/"
driver.get(target_url)

# "Play" butonuna tıklamak için bekliyoruz
try:
    play_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "player-poster"))  # Buraya gerçek player butonunun selector'ünü ekleyin
    )
    ActionChains(driver).move_to_element(play_button).click().perform()
    print("Play butonuna tıklandı.")
except Exception as e:
    print("Play butonu bulunamadı veya tıklanamadı:", e)

# Videonun yüklenmesini beklemek için 20 saniye bekleyelim
print("Video yükleniyor, 20 saniye bekleniyor...")
time.sleep(20)

# Chrome performance loglarını çekiyoruz
logs = driver.get_log("performance")

# ".m3u8" içeren URL'leri toplamak için bir set oluşturuyoruz
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
        pass  # Log işlenirken hata olursa yoksay

driver.quit()

# Bulunan URL'leri urls.html dosyasına yazıyoruz
with open("urls.html", "w", encoding="utf-8") as f:
    f.write("<html><body>\n")
    for url in m3u8_urls:
        f.write(f"<p>{url}</p>\n")
    f.write("</body></html>\n")

print("Extraction complete. URLs written to urls.html")
