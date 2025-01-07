import requests
import re

# M3U dosyasındaki URL'leri çek
m3u_url = 'https://raw.githubusercontent.com/keyiflerolsun/IPTV_YenirMi/main/Kanallar/KekikAkademi.m3u'
response = requests.get(m3u_url)

# M3U dosyasındaki içerik
m3u_content = response.text

# Dosyanın içeriğini yazdırarak kontrol edin
print("M3U Dosyasının İçeriği:")
print(m3u_content)

# trgoals içeren http-referrer URL'lerini bulmak için regex kullanıyoruz
m3u_referrer_urls = re.findall(r'#EXTVLCOPT:http-referrer=https?://[^\s]+trgoals[^\s]*', m3u_content)

# M3U dosyasındaki bulunan URL'leri yazdır
if m3u_referrer_urls:
    print("\ntrgoals içeren http-referrer URL'leri:")
    for url in m3u_referrer_urls:
        print(url)
else:
    print("trgoals içeren http-referrer URL bulunamadı.")

# index.html dosyasını aç ve URL'leri değiştir
index_file_path = '.index.html'

with open(index_file_path, 'r') as file:
    html_content = file.read()

# .index.html dosyasındaki trgoals içeren URL'leri bul
html_referrer_urls = re.findall(r'https?://[^\s]+trgoals[^\s]*', html_content)

# Eğer trgoals içeren URL'ler varsa, bunları M3U dosyasındaki URL'lerle değiştir
if html_referrer_urls:
    for old_url, new_url in zip(html_referrer_urls, m3u_referrer_urls):
        html_content = html_content.replace(old_url, new_url)

    # Değiştirilen içeriği tekrar index.html dosyasına yaz
    with open(index_file_path, 'w') as file:
        file.write(html_content)

    print("URL güncellemesi başarıyla yapıldı.")
else:
    print("trgoals içeren http-referrer URL'ler bulunamadı.")
