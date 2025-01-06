import requests
from lxml import html
import subprocess

# URL'yi çekmek için bit.ly adresi
target_url = "https://bit.ly/m/taraftarium24hdizle"

# HTML'yi al
response = requests.get(target_url)

# Lxml ile parsing yap
tree = html.fromstring(response.content)

# .links sınıfını bul
links = tree.xpath('//a[@class="links"]/@href')

if links:
    first_link = links[0]
    
    # Yönlendirme URL'sine git ve gerçek URL'yi al
    redirect_response = requests.get(first_link, allow_redirects=True)
    referer_url = redirect_response.url  # Yönlendirilmiş URL'yi al

    # Şimdi, index.html dosyasındaki exotrgoals1 sınıfında referer URL'yi güncelle
    index_url = "https://raw.githubusercontent.com/myanony1/myApp/main/.index.html"
    index_response = requests.get(index_url)
    index_html = index_response.text

    # Lxml ile index.html'i de işle
    tree = html.fromstring(index_html)
    
    # .m3u8 dosyasını ve referer URL'sini bulmak için XPath kullan
    m3u8_tags = tree.xpath('//div[@class="exotrgoals1"]//text()[contains(., ".m3u8")]')
    referer_tags = tree.xpath('//div[@class="exotrgoals1"]//text()[contains(., "https://")]')

    # Eğer m3u8 ve referer URL'leri bulunduysa, değiştir
    if m3u8_tags and referer_tags:
        # İlk .m3u8 ve referer URL'sini değiştir
        updated_html = html.tostring(tree, pretty_print=True).decode('utf-8')
        
        # .m3u8 URL'sini değiştir
        updated_html = updated_html.replace(m3u8_tags[0], referer_url.split(' ')[0])  # .m3u8 URL'yi değiştir
        updated_html = updated_html.replace(referer_tags[0], referer_url.split(' ')[1])  # Referer URL'yi değiştir

        # Güncellenmiş HTML dosyasını kaydet
        with open(".index.html", "w") as file:
            file.write(updated_html)

        # Git işlemleri
        subprocess.run(["git", "config", "--global", "user.name", "ActionBot"])
        subprocess.run(["git", "config", "--global", "user.email", "actionbot@example.com"])
        subprocess.run(["git", "add", ".index.html"])

        # Git status kontrolü
        status_result = subprocess.run(["git", "status", "-s"], capture_output=True, text=True)
        print("Git Status:", status_result.stdout)  # Değişikliklerin olup olmadığını kontrol et

        subprocess.run(["git", "commit", "-m", "Updated referer URL via GitHub Actions"])
        subprocess.run(["git", "push"])
    else:
        print("exotrgoals1 sınıfında .m3u8 veya referer URL'si bulunamadı.")
else:
    print("No links found.")

with open(".index.html", "r") as file:
    print(file.read())  # Dosyanın içeriğini kontrol et
