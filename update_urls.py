import requests
from bs4 import BeautifulSoup

# GitHub index.html dosyasının URL'si
GITHUB_URL = 'https://raw.githubusercontent.com/myanony1/myApp/main/index.html'

# index.html dosyasını al
response = requests.get(GITHUB_URL)

# HTML içeriğini BeautifulSoup ile analiz et
soup = BeautifulSoup(response.text, 'html.parser')

# class='exotrgoals' ile başlayan div'leri bul
exotrgoals_divs = soup.find_all('div', class_=lambda x: x and x.startswith('exotrgoals'))

# URL'leri kontrol et ve güncelle
for div in exotrgoals_divs:
    # Yayın ve referer URL'lerini al
    parts = div.text.split(' ')
    if len(parts) > 2:
        yayin_url = parts[2]  # 3. parça yayın URL'si
        referer_url = parts[3]  # 4. parça referer URL'si
        
        # URL'leri kontrol et
        try:
            # Yayın URL'sini kontrol et
            yayin_response = requests.get(yayin_url, timeout=10)
            
            # Referer URL'sini kontrol et
            referer_response = requests.get(referer_url, timeout=10)
            
            # Eğer her iki URL de geçerliyse, URL'yi güncelle
            if yayin_response.status_code in [200, 301, 302, 307] and referer_response.status_code in [200, 301, 302, 307]:
                print(f"[+] URL'ler geçerli: {yayin_url}, {referer_url}")
            else:
                print(f"[!] Hatalı URL'ler: {yayin_url}, {referer_url}")
                
                # URL'yi güncelle (gerekirse burada yeni URL'yi alabilirsiniz)
                yeni_yayin_url = "https://yeni.yayin.url"  # Yeni URL'yi buradan alırsınız
                yeni_referer_url = "https://yeni.referer.url"  # Yeni URL'yi buradan alırsınız
                div.string = div.text.replace(yayin_url, yeni_yayin_url).replace(referer_url, yeni_referer_url)
                
        except requests.RequestException as e:
            print(f"[!] Hata oluştu: {e}")
            continue

# Güncellenmiş HTML içeriğini kaydet
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))

print("[+] index.html güncellendi.")
