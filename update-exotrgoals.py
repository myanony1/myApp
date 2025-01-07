from Kekik.cli import konsol
from httpx import Client
from parsel import Selector
import re

class TRGoals:
    def __init__(self, index_html_dosyasi):
        self.index_html_dosyasi = index_html_dosyasi
        self.httpx = Client(timeout=10)

    def referer_domainini_al(self):
        referer_deseni = r'(https?://[^/]*trgoals[^/]*\.[^\s/]+)'
        with open(self.index_html_dosyasi, "r") as dosya:
            icerik = dosya.read()

        if eslesme := re.search(referer_deseni, icerik):
            return eslesme[1]
        else:
            raise ValueError("Index.html dosyasında 'trgoals' içeren referer domain bulunamadı!")

    def trgoals_domaini_al(self):
        istek = self.httpx.post("http://10.0.2.0:1221/api/v1/cf", json={"url": "https://bit.ly/m/taraftarium24hdizle"})
        secici = Selector(istek.text)
        redirect_url = secici.xpath("(//section[@class='links']/a)[1]/@href").get()

        while "bit.ly" in redirect_url:
            redirect_url = self.redirect_gec(redirect_url)

        return redirect_url

    def redirect_gec(self, redirect_url: str):
        istek = self.httpx.post("http://10.0.2.0:1221/api/v1/url", json={"url": redirect_url})
        redirect_url = istek.json().get("url")

        domain = redirect_url[:-1] if redirect_url.endswith("/") else redirect_url

        if "error" in domain:
            raise ValueError("Redirect domain hatalı..")

        return domain

    def yeni_domaini_al(self, eldeki_domain: str) -> str:
        def check_domain(domain: str) -> str:
            if domain == "https://trgoalsgiris.xyz":
                raise ValueError("Yeni domain alınamadı")
            return domain

        try:
            yeni_domain = check_domain(self.redirect_gec(eldeki_domain))
        except Exception:
            konsol.log("[red][!] `redirect_gec(eldeki_domain)` fonksiyonunda hata oluştu.")
            try:
                yeni_domain = check_domain(self.trgoals_domaini_al())
            except Exception:
                konsol.log("[red][!] `trgoals_domaini_al` fonksiyonunda hata oluştu.")
                try:
                    yeni_domain = check_domain(self.redirect_gec("https://t.co/JbIFBZKZpO"))
                except Exception:
                    konsol.log("[red][!] `redirect_gec('https://t.co/JbIFBZKZpO')` fonksiyonunda hata oluştu.")
                    rakam = int(eldeki_domain.split("trgoals")[1].split(".")[0]) + 1
                    yeni_domain = f"https://trgoals{rakam}.xyz"

        return yeni_domain

    def index_html_guncelle(self):
        eldeki_domain = self.referer_domainini_al()
        konsol.log(f"[yellow][~] Bilinen Domain : {eldeki_domain}")

        yeni_domain = self.yeni_domaini_al(eldeki_domain)
        konsol.log(f"[green][+] Yeni Domain    : {yeni_domain}")

        kontrol_url = f"{yeni_domain}/channel.html?id=yayin1"

        with open(self.index_html_dosyasi, "r") as dosya:
            index_html_icerik = dosya.read()

        if not (eski_yayin_url := re.search(r'https?:\/\/[^\/]+\.(workers\.dev|shop|cfd)\/?', index_html_icerik)):
            raise ValueError("Index.html dosyasında eski yayın URL'si bulunamadı!")

        eski_yayin_url = eski_yayin_url[0]
        konsol.log(f"[yellow][~] Eski Yayın URL : {eski_yayin_url}")

        response = self.httpx.get(kontrol_url)

        if not (yayin_ara := re.search(r'var baseurl = "(https?:\/\/[^"]+)"', response.text)):
            secici = Selector(response.text)
            baslik = secici.xpath("//title/text()").get()
            if baslik == "404 Not Found":
                yeni_domain = eldeki_domain
                yayin_ara = [None, eski_yayin_url]
            else:
                konsol.print(response.text)
                raise ValueError("Base URL bulunamadı!")

        yayin_url = yayin_ara[1]
        konsol.log(f"[green][+] Yeni Yayın URL : {yayin_url}")

        yeni_index_html_icerik = index_html_icerik.replace(eski_yayin_url, yayin_url)
        yeni_index_html_icerik = yeni_index_html_icerik.replace(eldeki_domain, yeni_domain)

        with open(self.index_html_dosyasi, "w") as dosya:
            dosya.write(yeni_index_html_icerik)

if __name__ == "__main__":
    guncelleyici = TRGoals(".index.html")
    guncelleyici.index_html_guncelle()
