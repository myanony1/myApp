from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ChromeOptions ayarları
options = Options()
options.headless = True  # Tarayıcıyı başsız çalıştırır

# WebDriver'ı başlat
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Sayfayı aç
driver.get('https://sonbahistv5.pages.dev/')

# Video elementinin yüklenmesini bekleyin
try:
    # 30 saniye boyunca video elementinin görünmesini bekler
    video_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, 'video'))
    )

    # Video URL'sini al
    video_url = video_element.get_attribute('src')

    print(f"Video URL: {video_url}")

finally:
    driver.quit()
