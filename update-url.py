import requests
import re

# URL'yi al
url = "https://raw.githubusercontent.com/keyiflerolsun/IPTV_YenirMi/main/Kanallar/KekikAkademi.m3u"
response = requests.get(url)

# Eğer başarılı bir yanıt aldıysak
if response.status_code == 200:
    content = response.text

    # "http-referrer" satırındaki ve "trgoals" içeren URL'yi bul
    match = re.search(r"#EXTVLCOPT:http-referrer=(https://[^\s]+trgoals[^\s]+)", content)
    if match:
        referer_url = match.group(1)

        # .index.html dosyasını oku
        with open('.index.html', 'r', encoding='utf-8') as file:
            html_content = file.read()

        # .index.html içeriğindeki referer URL'yi güncelle
        updated_html = re.sub(r"(https://[^\s]+)", referer_url, html_content)

        # Güncellenmiş içeriği dosyaya yaz
        with open('.index.html', 'w', encoding='utf-8') as file:
            file.write(updated_html)

        print("Referer URL başarıyla güncellendi.")
    else:
        print("trgoals içeren bir http-referrer URL bulunamadı.")
else:
    print(f"URL'yi alırken hata oluştu: {response.status_code}")
