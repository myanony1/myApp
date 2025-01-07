import requests
from bs4 import BeautifulSoup

# URL'yi al
url = "https://bit.ly/m/taraftarium24hdizle"
response = requests.get(url)

# Sayfayı parse et
soup = BeautifulSoup(response.text, 'html.parser')

# .links class'ı altındaki ilk bağlantıyı bul
link_element = soup.select_one('.links a')

# Bağlantı bulunup bulunmadığını kontrol et
if link_element and link_element.get('href'):
    first_link = link_element['href']
    print(f"First link: {first_link}")

    # .index.html dosyasını aç ve içeriğini oku
    with open('.index.html', 'r', encoding='utf-8') as file:
        html = file.read()

    # .index.html dosyasındaki 'trgoals' içeren URL'yi ilk bağlantıyla değiştir
    new_html = html.replace('trgoals', first_link)

    # Eğer değişiklik yapıldıysa, dosyayı güncelle
    if new_html != html:
        with open('.index.html', 'w', encoding='utf-8') as file:
            file.write(new_html)
        print("HTML file updated successfully.")
    else:
        print("No changes to .index.html.")
else:
    print("No link found in the .links class.")


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
