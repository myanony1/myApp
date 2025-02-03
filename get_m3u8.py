import requests
from bs4 import BeautifulSoup

# Anasayfa URL'si
url = "https://sonbahistv5.pages.dev"

# Sayfayı çekme
response = requests.get(url)

# Sayfanın HTML içeriğini parse etme
soup = BeautifulSoup(response.text, "html.parser")

# m3u8 URL'sini bulma
# Örnek: <video src="https://example.com/stream.m3u8">
m3u8_url = None
for video in soup.find_all("video"):
    if video.get("src"):
        m3u8_url = video["src"]
        break

# Eğer m3u8 URL'si bulunduysa, HTML dosyasına yazma
if m3u8_url:
    with open("urls.html", "w") as file:
        file.write(f"<html><body><h1>Stream URL</h1><p>{m3u8_url}</p></body></html>")
else:
    print("m3u8 URL'si bulunamadı.")
