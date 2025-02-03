from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# WebDriver'ı başlat
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Tarayıcıyı görünmez yapmak
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# ChromeDriver kurulumunu yap
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Sayfayı aç
url = 'https://sonbahistv5.pages.dev/'
driver.get(url)

# Sayfanın yüklenmesini bekle
driver.implicitly_wait(10)

# Video etiketini bul
video_element = driver.find_element(By.TAG_NAME, 'video')

# Blob URL'sini al
blob_url = video_element.get_attribute('src')

# URL'yi yazdır
print(f'Blob URL: {blob_url}')

# URL'yi bir dosyaya kaydet
with open('blob_url.txt', 'w') as f:
    f.write(blob_url)

# Tarayıcıyı kapat
driver.quit()
