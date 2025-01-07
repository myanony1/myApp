import requests
from bs4 import BeautifulSoup

# M3U dosyasındaki referer URL'sini çek
m3u_url = "https://raw.githubusercontent.com/keyiflerolsun/IPTV_YenirMi/main/Kanallar/KekikAkademi.m3u"
response = requests.get(m3u_url)

# M3U dosyasının içeriğini al
m3u_content = response.text

# "http-referrer=" içeren satırı bul
referer_url = None
for line in m3u_content.splitlines():
    if line.startswith("#EXTVLCOPT:http-referrer="):
        referer_url = line.split("=")[1]
        break

if not referer_url:
    raise ValueError("Referer URL bulunamadı!")

# .index.html dosyasını aç ve içeriğini yükle
html_file = "./.index2.html"  # .index.html dosyasının doğru yolu

with open(html_file, 'r') as file:
    soup = BeautifulSoup(file, 'html.parser')

# .index.html dosyasındaki 'exotrgoals1' sınıfı içindeki div'i bul
div = soup.find('div', class_='exotrgoals1')

if div:
    # Div'in içindeki metni al ve URL'yi güncelle
    text = div.get_text()
    parts = text.split(" ")
    
    # .m3u8 URL'sinin sonrasındaki referer URL'yi değiştir
    for i, part in enumerate(parts):
        if part.endswith(".m3u8"):
            parts[i + 1] = referer_url  # Sonraki öğe referer URL'si olacak
            break

    # Yeniden güncellenmiş metni div içinde düzenle
    div.string = " ".join(parts)

    # Güncellenmiş HTML'yi kaydet
    with open(html_file, 'w') as file:
        file.write(str(soup))
else:
    raise ValueError("exotrgoals1 sınıfına sahip div bulunamadı!")
