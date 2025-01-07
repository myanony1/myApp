import httpx
import re
from parsel import Selector

def fetch_redirected_url():
    # URL'yi ziyaret et
    url = "https://bit.ly/m/taraftarium24hdizle"
    response = httpx.get(url)

    if response.status_code != 200:
        print(f"Error: Unable to fetch the URL. Status code: {response.status_code}")
        return None

    # Sayfa içeriğini parse et
    selector = Selector(response.text)
    redirect_url = selector.xpath("(//section[@class='links']/a)[1]/@href").get()

    if not redirect_url:
        print("Error: No redirect URL found.")
        return None

    # Eğer URL hala bit.ly linki içeriyorsa, yönlendirme işlemi yap
    while "bit.ly" in redirect_url:
        redirect_url = get_final_redirected_url(redirect_url)

    return redirect_url

def get_final_redirected_url(url):
    # URL'yi takip et ve son yönlendirilmiş URL'yi al
    try:
        with httpx.Client() as client:
            response = client.get(url, follow_redirects=True)
            return response.url
    except Exception as e:
        print(f"Error during redirection: {e}")
        return None

def save_to_file(url):
    # Dosyaya yazma işlemi
    try:
        with open('urls.html', 'a') as file:
            file.write(f'<a href="{url}">{url}</a>\n')
            print(f"URL added: {url}")
    except Exception as e:
        print(f"Error writing to file: {e}")

def main():
    # Yönlendirilmiş URL'yi al
    final_redirected_url = fetch_redirected_url()

    if final_redirected_url:
        # URL'yi dosyaya kaydet
        save_to_file(final_redirected_url)
    else:
        print("No valid redirected URL found.")

if __name__ == "__main__":
    main()
