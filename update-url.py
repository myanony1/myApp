import requests

# M3U dosyasındaki URL'yi çek
m3u_url = 'https://raw.githubusercontent.com/keyiflerolsun/IPTV_YenirMi/main/Kanallar/KekikAkademi.m3u'
response = requests.get(m3u_url)

# URL'yi al
new_url = response.text.strip()  # Eğer m3u dosyasındaki URL metinse, bunu alıyoruz

# index.html dosyasını aç ve URL'yi değiştir
index_file_path = 'index.html'

with open(index_file_path, 'r') as file:
    html_content = file.read()

# trgoals içeren URL'yi değiştirme
updated_html = html_content.replace('trgoals', new_url)

# Değiştirilen içeriği tekrar index.html dosyasına yaz
with open(index_file_path, 'w') as file:
    file.write(updated_html)

print("URL güncellemesi başarıyla yapıldı.")
