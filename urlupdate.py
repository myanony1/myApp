import requests
from bs4 import BeautifulSoup

# Başlangıç URL'si (URL dinamik parametreler içeriyor)
start_url = "https://bit.ly/m/taraftarium24hdizle"

# İlk URL'yi al
response = requests.get(start_url)

# HTML içeriğini parse et
soup = BeautifulSoup(response.text, 'html.parser')

# URL'yi içeren <a> etiketini bul
link_tag = soup.find('a', href=True)

# Eğer link mevcutsa
if link_tag:
    final_url = link_tag['href']
    
    # Yönlendirilen URL'yi alın
    response_final = requests.get(final_url, allow_redirects=True)
    final_redirected_url = response_final.url  # En son yönlendirilmiş URL
    
    # URLs'i urls.html dosyasına yaz
    with open('urls.html', 'a') as file:
        file.write(f'<a href="{final_redirected_url}">{final_redirected_url}</a>\n')

    print(f"Yönlendirilen URL: {final_redirected_url}")
else:
    print("Yönlendirme linki bulunamadı.")
