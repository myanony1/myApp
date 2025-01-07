import requests
from bs4 import BeautifulSoup
import re

# URL ve GitHub dosya bilgileri
target_url = "https://bit.ly/m/taraftarium24hdizle"
github_repo = "myanony1/myApp"  # Değiştir
file_path = ".index.html"
branch = "main"

# GitHub token (GitHub Action'da secrets olarak tanımlanacak)
github_token = "YOUR_GITHUB_TOKEN"

# 1. Hedef URL'den .links class'ındaki ilk bağlantıyı çek
def get_redirected_url(target_url):
    response = requests.get(target_url)
    soup = BeautifulSoup(response.text, "html.parser")
    link_element = soup.select_one(".links a")
    if link_element:
        link = link_element["href"]
        # Yönlendirme URL'sini çek
        redirected_response = requests.get(link, allow_redirects=True)
        return redirected_response.url
    return None

# 2. GitHub'dan dosyayı indir ve güncelle
def update_index_file(new_url):
    headers = {"Authorization": f"token {github_token}"}
    # Dosyayı çek
    file_url = f"https://api.github.com/repos/{github_repo}/contents/{file_path}"
    response = requests.get(file_url, headers=headers)
    file_data = response.json()
    content = requests.utils.unquote(file_data["content"])
    
    # exotrgoals1 içindeki trgoals URL'sini güncelle
    updated_content = re.sub(
        r'class="exotrgoals1">.*?trgoals.*?</div>',
        f'class="exotrgoals1">{new_url}</div>',
        content,
        flags=re.DOTALL
    )
    
    # Dosyayı güncelle
    if updated_content != content:
        update_data = {
            "message": "Update exotrgoals1 URL",
            "content": updated_content.encode("utf-8").decode("latin1"),
            "sha": file_data["sha"],
            "branch": branch
        }
        update_response = requests.put(file_url, headers=headers, json=update_data)
        return update_response.status_code == 200
    return False

# Çalıştır
if __name__ == "__main__":
    new_url = get_redirected_url(target_url)
    if new_url:
        success = update_index_file(new_url)
        if success:
            print("index.html başarıyla güncellendi.")
        else:
            print("Güncelleme başarısız.")
    else:
        print("URL çekilemedi.")
