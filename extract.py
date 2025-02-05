import json
import re
import time  # Yeni eklenen modül
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome seçeneklerini ayarla
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')  # Yeni eklenen optimizasyon
chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

# ChromeDriver'ı başlat
driver = webdriver.Chrome(options=chrome_options)

# Bit.ly URL'sine git
initial_url = "https://bit.ly/m/taraftarium24w"
driver.get(initial_url)

try:
    # Bit.ly yönlendirmelerini bekle
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//section[@class='links']"))
    )
    print("✅ Bit.ly yönlendirmeleri tamamlandı.")

    # İlk bağlantıyı bul ve tıkla
    first_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "(//section[@class='links']/a)[1]"))
    )
    first_link_url = first_link.get_attribute('href')
    print(f"🔗 İlk bağlantı: {first_link_url}")
    first_link.click()
    
    # 9 saniyelik otomatik yönlendirmeyi bekle
    print("⏳ 9 saniyelik yönlendirme bekleniyor...")
    time.sleep(10)  # 9s + 1s güvenlik payı
    
    # Son hedef URL'yi al
    target_url = driver.current_url
    print(f"🎯 Hedef URL: {target_url}")

except Exception as e:
    print(f"❌ Hata: {str(e)}")
    driver.quit()
    exit()

# Hedef sitede işlemler
try:
    driver.get(target_url)  # Sayfayı yeniden yükle
    
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    
    # Logo tıkla
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.topLogo1"))
    ).click()
    
    # Sayfayı kaydır
    driver.execute_script("window.scrollTo(0, 600);")
    
    # Video oynatıcıyı etkinleştir
    player = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "player"))
    )
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", player)
    player.click()
    
    # Reklamı geç
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'REKLAMI GEC')]"))
    ).click()

except Exception as e:
    print(f"❌ Site işlem hatası: {str(e)}")

# M3U8 linklerini topla
m3u8_urls = set()
try:
    logs = driver.get_log("performance")
    
    for entry in logs:
        try:
            log = json.loads(entry['message'])['message']
            if log['method'] == 'Network.responseReceived':
                url = log['params']['response']['url']
                if '.m3u8' in url and 'video.twimg.com' not in url:
                    m3u8_urls.add(url)
        except:
            continue

except Exception as e:
    print(f"❌ Log toplama hatası: {str(e)}")

# HTML güncelleme
if m3u8_urls:
    try:
        with open('.index.html', 'r+', encoding='utf-8') as f:
            content = f.read()
            
            # exotrgoals1 güncelle
            exo1 = "\n".join(
                f"Lig Sports {i} HD | 1 {url.rsplit('/', 1)[0]}/yayinzirve.m3u8 {target_url}" 
                for i, url in enumerate(m3u8_urls, 1)
            )
            content = re.sub(
                r'(<div class="exotrgoals1">).*?(</div>)',
                rf'\1\n{exo1}\n\2',
                content,
                flags=re.DOTALL
            )
            
            # exotrgoals2 güncelle
            exo2 = "\n".join(
                f"Lig Sports {i} HD | 2 {url.rsplit('/', 1)[0]}/yayin1.m3u8 {target_url}"
                for i, url in enumerate(m3u8_urls, 1)
            )
            content = re.sub(
                r'(<div class="exotrgoals2">).*?(</div>)',
                rf'\1\n{exo2}\n\2',
                content,
                flags=re.DOTALL
            )
            
            f.seek(0)
            f.write(content)
            print("✅ HTML başarıyla güncellendi!")
            
    except Exception as e:
        print(f"❌ Dosya hatası: {str(e)}")
else:
    print("⚠️ M3U8 linki bulunamadı!")

driver.quit()
