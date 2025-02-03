import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Chrome seçeneklerini ayarlıyoruz
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

# ChromeDriver'ı başlatıyoruz
driver = webdriver.Chrome(options=chrome_options)

# Hedef URL'yi açıyoruz
target_url = "https://trgoals1150.xyz/"
driver.get(target_url)

# Reklamın tamamlanmasını ve asıl video linkinin yüklenmesini beklemek için 30 saniye bekle
print("Reklamın geçmesini bekliyoruz...")
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
