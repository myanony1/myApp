import requests
from bs4 import BeautifulSoup
import subprocess

# Verilen URL'den yeni bağlantıyı al
def fetch_redirected_url():
    try:
        # URL'yi al
        url = "https://bit.ly/m/taraftarium24hdizle"
        response = requests.get(url)
        response.raise_for_status()  # Hata kontrolü

        # Sayfayı parse et
        soup = BeautifulSoup(response.text, 'html.parser')

        # .links class'ı altındaki ilk bağlantıyı bul
        first_link = soup.select_one('.links a')['href']
        print(f"First link: {first_link}")

        return first_link
    except Exception as e:
        print(f"URL alımı sırasında hata oluştu: {e}")
        return None

# .index.html dosyasını güncelle
def update_html_file(new_url):
    file_path = ".index.html"
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # trgoals ile başlayan URL'yi bul ve yeni URL ile değiştir
        updated_content = content.replace(
            'trgoals', new_url
        )

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(updated_content)

        print(".index.html güncellendi.")
    except Exception as e:
        print(f".index.html güncellenirken hata oluştu: {e}")

# Git ile değişiklikleri gönder
def commit_and_push_changes():
    try:
        subprocess.run(["git", "config", "--global", "user.name", "github-actions[bot]"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "github-actions[bot]@users.noreply.github.com"], check=True)
        subprocess.run(["git", "add", ".index.html"], check=True)
        subprocess.run(["git", "commit", "-m", "Update .index.html with new URL"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Değişiklikler başarıyla gönderildi.")
    except subprocess.CalledProcessError as e:
        print(f"Git işlemleri sırasında hata oluştu: {e}")

# Ana iş akışı
if __name__ == "__main__":
    new_url = fetch_redirected_url()
    if new_url:
        update_html_file(new_url)
        commit_and_push_changes()
