from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def trgoals_domaini_al():
    try:
        # Chrome options ayarları
        options = Options()
        options.add_argument('--headless')  # Tarayıcıyı başlatmadan çalıştır
        driver = webdriver.Chrome(options=options)

        # Web sayfasına git
        driver.get("https://bit.ly/m/taraftarium24hdizle")
        
        # Sayfanın yüklenmesi için birkaç saniye bekle
        time.sleep(3)

        # İlk butona tıklamak için butonun XPath'ini kullan
        first_button = driver.find_element(By.XPATH, "//section[@class='links']/a[1]")
        first_button.click()

        # Yönlendirme sonrası sayfanın tamamen yüklenmesi için bekle
        time.sleep(3)

        # Şu anki URL'yi al
        final_url = driver.current_url

        print(f"Yönlendirme URL'si: {final_url}")
        
        # Tarayıcıyı kapat
        driver.quit()

        return final_url
    except Exception as e:
        print(f"Hata: {e}")
        driver.quit()  # Tarayıcıyı kapatmayı unutma
        return None

if __name__ == "__main__":
    final_url = trgoals_domaini_al()
    if final_url:
        print(f"Son yönlendirme URL'si: {final_url}")
    else:
        print("Bir hata oluştu.")
