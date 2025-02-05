import json
import re
import time
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

# İlk URL'yi aç
initial_url = "https://bit.ly/m/taraftarium24w"
driver.get(initial_url)

# Sayfanın tamamen yüklenmesini bekle
try:
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    print("✅ İlk sayfa tamamen yüklendi.")
except Exception as e:
    print("❌ İlk sayfa yüklenemedi:", e)

# İlk bağlantıyı tıkla ve yönlendirmeleri takip et
try:
    first_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "(//section[@class='links']/a)[1]"))
    )
    first_target_url = first_link.get_attribute("href")
    driver.get(first_target_url)
    print(f"✅ İlk bağlantıya tıklandı, yeni URL: {first_target_url}")

    # İlk yönlendirmeyi bekle
    WebDriverWait(driver, 10).until(lambda d: d.current_url != first_target_url)
    second_target_url = driver.current_url
    driver.get(second_target_url)
    print(f"✅ İkinci yönlendirme tamamlandı, yeni URL: {second_target_url}")

    # 30 saniye bekle (Sonraki yönlendirmeleri takip etmek için)
    time.sleep(30)

    # En son yönlendirilmiş URL'yi al
    WebDriverWait(driver, 10).until(lambda d: d.current_url != second_target_url)
    final_target_url = driver.current_url
    print(f"✅ En son yönlendirilmiş URL: {final_target_url}")

except Exception as e:
    print("❌ Bağlantıya tıklanamadı veya yönlendirme başarısız:", e)
    driver.quit()
    exit()

# Yeni hedef URL'ye git
driver.get(final_target_url)

# Sayfanın tamamen yüklenmesini bekle
try:
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    print("✅ Yeni sayfa tamamen yüklendi.")
except Exception as e:
    print("❌ Yeni sayfa yüklenemedi:", e)

# <a> öğesini tıklamak (logo)
try:
    logo_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.topLogo1"))
    )
    logo_link.click()
    print("✅ Logo tıklanarak ana sayfaya yönlendirildi.")
except Exception as e:
    print("❌ Logo öğesi tıklanamadı:", e)

# Sayfayı kaydır
try:
    driver.execute_script("window.scrollTo(0, 500);")
    print("✅ Sayfa kaydırıldı.")
except Exception as e:
    print("❌ Sayfa kaydırılamadı:", e)

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

# 10 saniye bekle
WebDriverWait(driver, 10).until(lambda driver: True)

# "REKLAMI GEC" butonuna tıkla
try:
    skip_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'REKLAMI GEC')]"))
    )
    ActionChains(driver).move_to_element(skip_button).click().perform()
    print("✅ 'REKLAMI GEC' butonuna tıklandı.")
except Exception as e:
    print("❌ 'REKLAMI GEC' butonu bulunamadı veya tıklanamadı:", e)

# .m3u8 linklerini çekme (video.twimg.com dışındakiler)
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

# URLs'yi alıp exotrgoals1 ve exotrgoals2 içeriğini oluştur
new_content_exotrgoals1 = "\n".join(
    [f"Lig Sports {index} HD | 1 {url.replace(url.split('/')[-1], 'yayinzirve.m3u8')} {final_target_url}" for index, url in enumerate(m3u8_urls, start=1)]
)
new_content_exotrgoals2 = "\n".join(
    [f"Lig Sports {index} HD | 2 {url.replace(url.split('/')[-1], 'yayin1.m3u8')} {final_target_url}" for index, url in enumerate(m3u8_urls, start=1)]
)

# HTML dosyasını aç ve sadece mevcut div içeriğini değiştir
try:
    with open(".index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Sadece içeriği değiştirmek için regex ile güncelleme yapıyoruz
    updated_content = re.sub(
        r'(<div class=[\'"]exotrgoals1[\'"][^>]*>)(.*?)(</div>)',
        rf'\1\n{new_content_exotrgoals1}\n\3',
        content,
        flags=re.DOTALL
    )
    
    updated_content = re.sub(
        r'(<div class=[\'"]exotrgoals2[\'"][^>]*>)(.*?)(</div>)',
        rf'\1\n{new_content_exotrgoals2}\n\3',
        updated_content,
        flags=re.DOTALL
    )

    # Eğer içerik değiştiyse dosyayı güncelle
    if updated_content != content:
        with open(".index.html", "w", encoding="utf-8") as f:
            f.write(updated_content)
        print("✅ exotrgoals1 ve exotrgoals2 div içerikleri güncellendi.")
    else:
        print("ℹ️ exotrgoals1 ve exotrgoals2 içerikleri zaten güncel.")
    
except FileNotFoundError:
    print("❌ Hata: .index.html dosyası bulunamadı.")
except Exception as e:
    print(f"❌ Dosya güncellenirken hata oluştu: {e}")
