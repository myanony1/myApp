import requests
from bs4 import BeautifulSoup

# GitHub'daki index.html dosyasının URL'si
index_url = 'https://raw.githubusercontent.com/myanony1/myApp/main/index.html'

# HTML'yi al
response = requests.get(index_url)
soup = BeautifulSoup(response.text, 'html.parser')

# exotrgoals sınıflarındaki verileri çek
divs = soup.find_all('div', class_='exotrgoals1')  # İlk sınıf exotrgoals1, diğerleri exotrgoals2, exotrgoals3 vb.

for div in divs:
    # Yayın ismini al
    kanal_adi = div.contents[0].strip().split(' | ')[0]
    
    # Yayın URL'si ve referer URL'sini al
    parts = div.contents[1].split(' ')
    yayin_url = parts[0]  # Örneğin: https://k0.b4c8d3e9f1a2b7c5d5.cfd/yayinzirve.m3u8
    referer_url = parts[1]  # Örneğin: https://trgoals1097.xyz
    
    # m3u8 URL'sini çek
    m3u8_url = yayin_url.split(' ')[0]  # m3u8 linki
    print(f"Yayın Adı: {kanal_adi}, Yayın URL: {yayin_url}, Referer URL: {referer_url}, M3U8 URL: {m3u8_url}")
    
    # Burada API veya başka bir şekilde URL'leri kontrol etmeniz gerekebilir
    # Eğer URL'ler değişmişse, HTML'yi güncelleyin
    # Örnek: URL'leri değiştirme ve güncelleme işlemi

# index.html dosyasını güncelleyin (örneğin yazı biçiminde)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))

print("index.html dosyası güncellendi.")
