import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from git import Repo
import os

# 1. İstenen URL'ye git ve "orb-link" class'ındaki ilk bağlantıyı bul
def get_redirected_url(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    first_link = soup.find('a', class_='orb-link')['href']
    return first_link

# 2. Yönlendirmeli linki aç ve en son oluşan URL'yi bul
def get_final_url(initial_url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.get(initial_url)
    final_url = driver.current_url
    driver.quit()
    return final_url

# 3. Final URL'nin sonuna "/channel.html?id=yayin1" ekleyip m3u8 linkini al
def get_m3u8_link(base_url):
    channel_url = f"{base_url}/channel.html?id=yayin1"
    response = requests.get(channel_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    m3u8_link = soup.find('source')['src']
    return m3u8_link

# 4. GitHub'a push etmek için dosyayı güncelle
def update_github_repo(m3u8_link, repo_path, file_path, commit_message):
    repo = Repo(repo_path)
    file_full_path = os.path.join(repo_path, file_path)
    
    # Dosyayı güncelle
    with open(file_full_path, 'w') as file:
        file.write(m3u8_link)

    # Git işlemleri
    repo.index.add([file_path])
    repo.index.commit(commit_message)
    origin = repo.remote(name='origin')
    origin.push()

# Ana işlem
if __name__ == "__main__":
    base_url = "https://bit.ly/m/taraftarium24hdizle"
    repo_path = "."  # GitHub Actions için çalışma dizini
    file_path = "urls.html"  # GitHub'daki dosya yolu

    try:
        initial_url = get_redirected_url(base_url)
        final_url = get_final_url(initial_url)
        m3u8_link = get_m3u8_link(final_url)
        update_github_repo(m3u8_link, repo_path, file_path, "Update m3u8 link")
        print("m3u8 link başarıyla güncellendi ve GitHub'a push edildi.")
    except Exception as e:
        print(f"Hata: {e}")
