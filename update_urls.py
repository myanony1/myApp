import requests
from bs4 import BeautifulSoup

# URL'yi çekmek için bit.ly adresi
target_url = "https://bit.ly/m/taraftarium24hdizle"

# HTML'yi al
response = requests.get(target_url)
soup = BeautifulSoup(response.text, "html.parser")

# .links sınıfını bul
links = soup.find_all(class_='links')

if links:
    # İlk bağlantıyı al
    first_link = links[0].get('href')
    
    # Yönlendirme URL'sine git ve gerçek URL'yi al
    redirect_response = requests.get(first_link, allow_redirects=True)
    
    # Yönlendirilmiş URL'yi al
    final_url = redirect_response.url
    
    # .m3u8 URL'sini ve referer URL'sini çıkart
    m3u8_url = final_url.split(' ')[0]  # Eğer URL içerisinde farklı parametreler varsa bu kısmı tekrar kontrol edin
    referer_url = final_url.split(' ')[1]  # Eğer URL içerisinde farklı parametreler varsa bu kısmı tekrar kontrol edin

    # Şimdi, index.html dosyasındaki exotrgoals sınıfında bunları güncelle
    index_url = "https://raw.githubusercontent.com/myanony1/myApp/main/.index.html"
    index_response = requests.get(index_url)
    index_html = index_response.text

    # HTML içeriğini güncelle
    updated_html = index_html.replace("https://k0.b4c8d3e9f1a2b7c5d5.cfd/yayinzirve.m3u8", m3u8_url)
    updated_html = updated_html.replace("https://trgoals1097.xyz", referer_url)

    # Güncellenmiş HTML dosyasını geri göndermek için commit yap
    with open(".index.html", "w") as file:
        file.write(updated_html)

    # Git işlemleri
    import subprocess
    subprocess.run(["git", "config", "--global", "user.name", "ActionBot"])
    subprocess.run(["git", "config", "--global", "user.email", "actionbot@example.com"])
    subprocess.run(["git", "add", ".index.html"])
    subprocess.run(["git", "commit", "-m", "Updated m3u8 and referer URLs"])
    subprocess.run(["git", "push"])

else:
    print("No links found.")
