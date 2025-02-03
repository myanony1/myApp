import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome seçeneklerini ayarlıyoruz
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

driver = webdriver.Chrome(options=chrome_options)

target_url = "https://trgoals1150.xyz/"  # Gerçek URL'nizi buraya koyun
driver.get(target_url)

# Reklamı atlamak için eğer buton varsa tıklama (buton seçicisini siteye göre ayarlayın)
try:
    skip_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.skip-ad"))
    )
    skip_button.click()
    print("Reklam atlandı.")
except Exception as e:
    print("Reklam atlama butonu bulunamadı veya tıklanamadı:", e)

# Asıl video akışı başlaması için yeterli süre bekleyin (örneğin 20 saniye)
time.sleep(20)

# Network loglarını çekiyoruz
logs = driver.get_log("performance")
m3u8_urls = set()

for entry in logs:
    try:
        log_json = json.loads(entry["message"])
        message = log_json.get("message", {})
        if message.get("method") == "Network.responseReceived":
            response_url = message.get("params", {}).get("response", {}).get("url", "")
            # Örneğin: URL'de 'ad' kelimesi varsa reklam akışı olarak kabul edebiliriz
            if ".m3u8" in response_url and "ad" not in response_url.lower():
                m3u8_urls.add(response_url)
    except Exception:
        pass

driver.quit()

# Sonuçları yazdırma
with open("urls.html", "w", encoding="utf-8") as f:
    f.write("<html><body>\n")
    for url in m3u8_urls:
        f.write(f"<p>{url}</p>\n")
    f.write("</body></html>\n")

print("Extraction complete. URLs written to urls.html")
