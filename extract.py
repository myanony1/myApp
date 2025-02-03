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

# 1️⃣ Sayfanın tamamen yüklenmesini beklemek (sayfa yükleme durumu)
try:
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    print("✅ Sayfa tamamen yüklendi.")
except Exception as e:
    print("❌ Sayfa yüklenemedi:", e)

# 2️⃣ <a> öğesini tıklamak (logo)
try:
    logo_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.topLogo1"))
    )
    logo_link.click()
    print("✅ Logo tıklanarak ana sayfaya yönlendirildi.")
except Exception as e:
    print("❌ Logo öğesi tıklanamadı:", e)

# 3️⃣ <div id="player"> öğesinin tıklanabilir olmasını bekle
try:
    player_div = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "player"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", player_div)
    driver.execute_script("arguments[0].click();", player_div)  # JavaScript ile tıklama
    print("✅ <div id='player'> öğesine tıklandı.")
except Exception as e:
    print("❌ <div id='player'> öğesi tıklanamadı:", e)

# 4️⃣ 10 saniye bekle
WebDriverWait(driver, 10).until(lambda driver: True)  # 10 saniye bekletme

# 5️⃣ "REKLAMI GEC" butonuna tıklama
try:
    skip_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'REKLAMI GEC')]"))
    )
    ActionChains(driver).move_to_element(skip_button).click().perform()
    print("✅ 'REKLAMI GEC' butonuna tıklandı.")
except Exception as e:
    print("❌ 'REKLAMI GEC' butonu bulunamadı veya tıklanamadı:", e)

# 6️⃣ .m3u8 linklerini çekme
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

# 7️⃣ URLs'yi urls.html dosyasına yaz
with open("urls.html", "w", encoding="utf-8") as f:
    f.write("<html><body>\n")
    for url in m3u8_urls:
        f.write(f"<p>{url}</p>\n")
    f.write("</body></html>\n")

print("✅ Extraction complete. URLs written to urls.html")
