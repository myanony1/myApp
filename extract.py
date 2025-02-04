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
target_url = "https://trgoals1152.xyz/"
driver.get(target_url)

# 1️⃣ Sayfanın tamamen yüklenmesini bekle
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

# 3️⃣ Sayfayı kaydır
try:
    driver.execute_script("window.scrollTo(0, 500);")
    print("✅ Sayfa kaydırıldı.")
except Exception as e:
    print("❌ Sayfa kaydırılamadı:", e)

# 4️⃣ <div id="player"> öğesine tıkla
try:
    player_div = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "player"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", player_div)
    driver.execute_script("arguments[0].click();", player_div)
    print("✅ <div id='player'> öğesine tıklandı.")
except Exception as e:
    print("❌ <div id='player'> öğesi tıklanamadı:", e)

# 5️⃣ 10 saniye bekle
WebDriverWait(driver, 10).until(lambda driver: True)

# 6️⃣ "REKLAMI GEC" butonuna tıkla
try:
    skip_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'REKLAMI GEC')]"))
    )
    ActionChains(driver).move_to_element(skip_button).click().perform()
    print("✅ 'REKLAMI GEC' butonuna tıklandı.")
except Exception as e:
    print("❌ 'REKLAMI GEC' butonu bulunamadı veya tıklanamadı:", e)

# 7️⃣ .m3u8 linklerini çekme (video.twimg.com dışındakiler)
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
        pass  # Hataları yoksay

driver.quit()

# 8️⃣ URLs'yi urls.html dosyasına yazma (SADECE exotrgoals2 içeriğini değiştir)
import re

# Yeni HTML bloklarını oluştur
new_entries = []
for index, url in enumerate(m3u8_urls, start=1):
    entry = f"""<div class='exotrgoals2' style='display:none'>
      Lig Sports {index} HD | 5 {url} {target_url}
</div>"""
    new_entries.append(entry)
new_content = "\n".join(new_entries)

try:
    # Mevcut dosyayı oku
    with open(".index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Eski exotrgoals2 içeriğini regex ile bul ve yeniyle değiştir
    updated_content = re.sub(
        r'<div class=[\'"]exotrgoals2[\'"].*?</div>\s*',
        new_content,
        content,
        flags=re.DOTALL
    )
    
    # Eğer hiç exotrgoals2 yoksa yeni içeriği ekle
    if updated_content == content:
        if "</body>" in content:
            updated_content = content.replace("</body>", new_content + "\n</body>")
        else:
            updated_content = content + "\n" + new_content

except FileNotFoundError:
    # Dosya yoksa tamamen yeni oluştur
    updated_content = f"""<html><body>
{new_content}
</body></html>"""

# Dosyayı güncelle
with open(".index.html", "w", encoding="utf-8") as f:
    f.write(updated_content)

print("✅ Extraction complete. exotrgoals2 divs updated, other content preserved")
