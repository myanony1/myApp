import json
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome ayarları
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

driver = webdriver.Chrome(options=chrome_options)

# 1. ADIM: Bit.ly üzerinden ilk yönlendirme
def get_target_url():
    try:
        print("🌐 Bit.ly bağlantısına gidiliyor...")
        driver.get("https://bit.ly/m/taraftarium24w")
        
        # Linkler bölümünün yüklenmesini bekle
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//section[@class='links']"))
        )
        print("✅ Linkler bölümü yüklendi")
        
        # İlk linki bul ve JavaScript ile gerçek URL'yi al
        first_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//section[@class='links']/a)[1]"))
        )
        first_url = driver.execute_script("return arguments[0].href;", first_link)
        print(f"🔗 İlk link URL: {first_url}")
        
        # Doğrudan hedef URL'ye git (Bit.ly bypass)
        print("⏩ Bit.ly bypass ediliyor...")
        driver.get(first_url)
        
        # 10 saniye bekleyerek ek yönlendirmeler için
        print("⏳ Ek yönlendirmeler bekleniyor (10sn)...")
        time.sleep(10)
        
        # Son URL kontrolü
        WebDriverWait(driver, 30).until(
            lambda d: "taraftarium" in d.current_url.lower() or "trgoals" in d.current_url.lower()
        )
        target_url = driver.current_url
        print(f"🎯 Son hedef URL: {target_url}")
        
        return target_url
        
    except Exception as e:
        print(f"❌ Kritik hata: {str(e)}")
        return None

# Hedef URL'yi al
target_url = get_target_url()

if not target_url:
    driver.quit()
    exit()

# 2. ADIM: Son hedef sitede işlemler
try:
    print(f"🌍 Hedef siteye gidiliyor: {target_url}")
    driver.get(target_url)
    
    # Sayfanın tam yüklenmesini garanti altına al
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )
    
    # Logo tıklama
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.topLogo1"))
    ).click()
    print("✅ Logoya tıklandı")
    
    # Sayfa pozisyonu ayarla
    driver.execute_script("window.scrollTo(0, 700)")
    
    # Video player'ı aktifleştir
    player = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "player"))
    )
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", player)
    player.click()
    print("▶️ Video oynatıcı aktif")
    
    # Reklam geç butonu
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'REKLAMI GEC')]"))
    ).click()
    print("✅ Reklam geçildi")

except Exception as e:
    print(f"⚠️ İşlem hatası: {str(e)}")

# 3. ADIM: M3U8 linklerini topla
m3u8_links = set()
try:
    print("🔍 M3U8 linkleri aranıyor...")
    logs = driver.get_log('performance')
    
    for entry in logs:
        try:
            log = json.loads(entry['message'])['message']
            if log['method'] == 'Network.responseReceived':
                url = log['params']['response']['url']
                if '.m3u8' in url and 'video.twimg.com' not in url:
                    m3u8_links.add(url)
        except:
            continue
            
    print(f"📥 {len(m3u8_links)} adet M3U8 linki bulundu")
    
except Exception as e:
    print(f"❌ Log okuma hatası: {str(e)}")

# 4. ADIM: HTML güncelleme
if m3u8_links:
    try:
        with open('.index.html', 'r+', encoding='utf-8') as f:
            content = f.read()
            
            # exotrgoals1 güncelle
            exo1 = "\n".join([
                f"Lig Sports {idx} HD | 1 {url.rsplit('/', 1)[0]}/yayinzirve.m3u8 {target_url}"
                for idx, url in enumerate(m3u8_links, 1)
            ])
            content = re.sub(
                r'(<div class="exotrgoals1">).*?(</div>)',
                rf'\1\n{exo1}\n\2',
                content,
                flags=re.DOTALL
            )
            
            # exotrgoals2 güncelle
            exo2 = "\n".join([
                f"Lig Sports {idx} HD | 2 {url.rsplit('/', 1)[0]}/yayin1.m3u8 {target_url}"
                for idx, url in enumerate(m3u8_links, 1)
            ])
            content = re.sub(
                r'(<div class="exotrgoals2">).*?(</div>)',
                rf'\1\n{exo2}\n\2',
                content,
                flags=re.DOTALL
            )
            
            f.seek(0)
            f.write(content)
            f.truncate()
            print("🔄 HTML başarıyla güncellendi")
            
    except Exception as e:
        print(f"❌ Dosya işleme hatası: {str(e)}")
        
driver.quit()
