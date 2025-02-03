import time
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# ChromeDriver'ı repoda veya PATH'te hazır olduğunu varsayıyoruz.
# Eğer repoda bulunuyorsa "./chromedriver" yolunu kullanabilirsiniz.

# Chrome ayarları
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')

# Network loglarını aktif etmek için "performance" log seviyesini açıyoruz.
caps = DesiredCapabilities.CHROME.copy()
caps["goog:loggingPrefs"] = {"performance": "ALL"}

# ChromeDriver'ı başlat
driver = webdriver.Chrome(options=chrome_options, desired_capabilities=caps)

# Hedef URL
target_url = "https://sonbahistv5.pages.dev/"
driver.get(target_url)

# Sayfanın yüklenmesi ve network isteklerinin gerçekleşmesi için bekleyin
time.sleep(5)

# Performance loglarını çekelim
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
    except Exception as e:
        # Log işleme sırasında hata alırsa pas geçiyoruz.
        pass

driver.quit()

# Bulunan URL'leri urls.html dosyasına yazıyoruz.
with open("urls.html", "w", encoding="utf-8") as f:
    f.write("<html><body>\n")
    for url in m3u8_urls:
        f.write(f"<p>{url}</p>\n")
    f.write("</body></html>\n")

print("Extraction complete. URLs written to urls.html")
