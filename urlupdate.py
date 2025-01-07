import requests
from parsel import Selector

def trgoals_domaini_al():
    try:
        # İlk isteği gönder
        istek = requests.get("https://bit.ly/m/taraftarium24hdizle")
        
        # HTML analiz etmek için Selector kullan
        secici = Selector(istek.text)
        
        # İlk bağlantıyı almak için XPath ifadesini kullan
        first_link = secici.xpath("//section[@class='links']/a[1]/@href").get()

        # Bağlantıyı kontrol et
        if not first_link:
            raise ValueError("İlk bağlantı alınamadı.")
        
        print(f"İlk bağlantı URL'si: {first_link}")
        
        return first_link
    except Exception as e:
        raise ValueError(f"Yönlendirme URL'si alınırken hata oluştu: {e}")

if __name__ == "__main__":
    try:
        final_url = trgoals_domaini_al()
        print(f"Son yönlendirme URL'si: {final_url}")
    except Exception as e:
        print(f"Hata: {e}")
