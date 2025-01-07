import httpx
from parsel import Selector

def trgoals_domaini_al(self):
    # URL'yi istek ile alıyoruz
    istek = httpx.get("https://bit.ly/m/taraftarium24hdizle")  # bit.ly üzerinden yönlendirme yapılacak
    secici = Selector(istek.text)
    
    # İlk bağlantıyı alıyoruz
    redirect_url = secici.xpath("(//section[@class='links']/a)[1]/@href").get()

    # Eğer bit.ly içeren bir URL varsa, yönlendirmeyi takip ediyoruz
    while "bit.ly" in redirect_url:
        redirect_url = self.redirect_gec(redirect_url)

    return redirect_url

try:
    with open('urls.html', 'a') as file:
        file.write(f'<a href="{final_redirected_url}">{final_redirected_url}</a>\n')
        print(f'URL added: {final_redirected_url}')
except Exception as e:
    print(f"Error writing to file: {e}")

