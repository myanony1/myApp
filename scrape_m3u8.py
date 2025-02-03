import requests
from bs4 import BeautifulSoup

# URL'yi al
url = 'https://sonbahistv5.pages.dev/'

# Sayfa içeriğini al
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# M3U8 URL'sini çek
m3u8_url = soup.find('source', {'type': 'application/x-mpegURL'})['src']

# URL'yi yazdır
print(f'M3U8 URL: {m3u8_url}')

# URL'yi dosyaya kaydet
with open('m3u8_url.txt', 'w') as f:
    f.write(m3u8_url)
