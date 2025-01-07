import requests
from parsel import Selector

def redirect_gec(url):
    """
    Yönlendirmeyi çözmek için kullanılır.
    """
    try:
        response = requests.get(url, allow_redirects=True)
        return response.url
    except Exception as e:
        raise ValueError(f"Yönlendirme sırasında hata oluştu: {e}")

def trgoals_domaini_al():
    """
    Verilen ana URL'den yönlendirme linklerini çıkarır.
    """
    try:
        # İlk isteği gönder
        istek = requests.get("https://bit.ly/m/taraftarium24hdizle")
        
        # HTML analiz etmek için Selector kullan
        secici = Selector(istek.text)
        
        # İlk yönlendirme linkini al
        redirect_url = secici.xpath("(//section[@class='links']/a)[1]/@href").get()
        
        # Yönlendirme çözülene kadar devam et
        while "bit.ly" in redirect_url:
            redirect_url = redirect_gec(redirect_url)
        
        return redirect_url
    except Exception as e:
        raise ValueError(f"Yönlendirme URL'si alınırken hata oluştu: {e}")

if __name__ == "__main__":
    try:
        final_url = trgoals_domaini_al()
        print(f"Son yönlendirme URL'si: {final_url}")
    except Exception as e:
        print(f"Hata: {e}")
