from selenium import webdriver

# Tentukan path ke ChromeDriver yang sesuai
chrome_driver_path = "path_ke_chromedriver"

# Buat objek Service dengan path ChromeDriver
chrome_driver_service = webdriver.chrome.service.Service(chrome_driver_path)

# Inisialisasi WebDriver dengan Service object
driver = webdriver.Chrome(service=chrome_driver_service)

# Buka halaman web
driver.get("https://www.google.com")

# Tunggu beberapa detik (opsional)
import time
time.sleep(5)

# Tutup browser
driver.quit()
