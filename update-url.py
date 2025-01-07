import requests
import re

# M3U dosyasındaki URL'leri çek
m3u_url = 'https://raw.githubusercontent.com/keyiflerolsun/IPTV_YenirMi/main/Kanallar/KekikAkademi.m3u'
response = requests.get(m3u_url)

# M3U dosyasındaki URL'leri al
m3u_content = response.text

# M3U dosyasındaki trgoals içeren URL'leri bul
m3u_urls = re.findall(r'https?://[^\s]+trgoals[^\s]+', m3u_content)

# index.html dosyasını aç ve URL'leri değiştir
index_file_path = 'index.html'

with open(index_file_path, 'r') as file:
    html_content = file.read()

# .index.html dosyasındaki trgoals içeren URL'leri bul
html_urls = re.findall(r'https?://[^\s]+trgoals[^\s]+', html_content)

# Eğer trgoals içeren URL'ler varsa, bunları M3U dosyasındaki URL'lerle değiştir
if html_urls:
    for old_url, new_url in zip(html_urls, m3u_urls):
        html_content = html_content.replace(old_url, new_url)

    # Değiştirilen içeriği tekrar index.html dosyasına yaz
    with open(index_file_path, 'w') as file:
        file.write(html_content)

    print("URL güncellemesi başarıyla yapıldı.")
else:
    print("trgoals içeren URL'ler bulunamadı.")
