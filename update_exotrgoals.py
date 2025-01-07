import requests
from bs4 import BeautifulSoup
import base64
import subprocess
import os

# URL'den bağlantıyı al ve yönlendir
def fetch_new_url():
    try:
        response = requests.get("https://bit.ly/m/taraftarium24hdizle", allow_redirects=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        link_element = soup.select_one(".links a")
        if link_element and link_element['href']:
            return link_element['href']
        else:
            print("No valid link found in .links class.")
            return None
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return None

# Dosyayı güncelle
def update_html_file(new_url):
    file_path = ".index.html"
    try:
        with open(file_path, "r") as file:
            content = file.read()

        updated_content = content.replace(
            next((line for line in content.splitlines() if "exotrgoals1" in line and "trgoals" in line), ""),
            f'<div class="exotrgoals1">{new_url}</div>'
        )

        with open(file_path, "w") as file:
            file.write(updated_content)

        print("File updated successfully.")
    except Exception as e:
        print(f"Error updating file: {e}")

# Git işlemleri
def commit_and_push_changes():
    try:
        subprocess.run(["git", "config", "--global", "user.name", "github-actions[bot]"])
        subprocess.run(["git", "config", "--global", "user.email", "github-actions[bot]@users.noreply.github.com"])
        subprocess.run(["git", "add", ".index.html"])
        subprocess.run(["git", "commit", "-m", "Update .index.html via workflow"])
        subprocess.run(["git", "push", "origin", "main"])
        print("Changes pushed to repository.")
    except Exception as e:
        print(f"Error committing and pushing changes: {e}")

# Main
if __name__ == "__main__":
    new_url = fetch_new_url()
    if new_url:
        update_html_file(new_url)
        commit_and_push_changes()
