from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os
import time
import random

#Ruta de descarga personalizada
download_path = r"D:\Z.MIO\X\ALGORITMOS\PROYECTO FINAL\archivosDescargados"

#Crear la carpeta si no existe
os.makedirs(download_path, exist_ok=True)

#Configuración de Chrome para descargas automáticas
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_path,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

#Opciones adicionales para evitar detección
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

#  Iniciar WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

#Función para simular tipeo humano
def escribir_como_humano(elemento, texto):
    for caracter in texto:
        elemento.send_keys(caracter)
        time.sleep(random.uniform(0.1, 0.3))

try:
    # Acceder a Sciencie Direct
    driver.get("https://research-ebsco-com.crai.referencistas.com/c/rfbjy2/search?defaultdb=aps")

    # Esperar a que el botón esté presente y hacer clic en "Iniciar sesión con Google"
    google_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btn-google"))
    )
    google_button.click()
    print("Se hizo clic en el botón de Google correctamente.")

    #Ingresar correo
    username = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "identifierId"))
    )
    escribir_como_humano(username, "cristianc.cortesb@uqvirtual.edu.co")
    username.send_keys(Keys.RETURN)
    time.sleep(3)

    #Ingresar contraseña
    password = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "Passwd"))
    )
    escribir_como_humano(password, "1094944141")
    password.send_keys(Keys.RETURN)
    time.sleep(10)


    # Realizar la búsqueda
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search-input"))  # Nuevo ID del campo de búsqueda
    )

    escribir_como_humano(search_box, "computational thinking")
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)

    # Esperar y hacer clic en el botón desplegable de "Mostrar resultados"
    dropdown_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "results-per-page-dropdown-toggle-button"))  # Nuevo ID del botón
    )
    dropdown_button.click()
    time.sleep(2)

    # Seleccionar la opción de "50 resultados por página"
    option_50 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '50')]"))
    )
    option_50.click()
    time.sleep(2)

    #----------------------------------------modificar aca abajo-----------------------------





    # Iterar sobre las primeras 5 páginas
    for pagina in range(1, 6):
        try:
            
            # Seleccionar todos los resultados
            select_all_checkbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//label[@for='select-all-results']"))
            )
            select_all_checkbox.click()
            time.sleep(2)
            
            #Clic en Exportar
            export_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'export-all-link-button')]"))
                        )
            export_button.click()
            time.sleep(2)
            
            
            # Clic en "Export citation to BibTeX"
            export_bibtex_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Export citation to BibTeX')]]"))
            )
            export_bibtex_button.click()
            time.sleep(2)
            
            #deseleccionar los resultados
            select_all_checkbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//label[@for='select-all-results']"))
            )
            select_all_checkbox.click()
            time.sleep(2)

            # Ir a la siguiente página
            if pagina < 5:
                next_page_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@data-aa-name='srp-next-page']"))
            )

            # Desplazar hasta el botón
            driver.execute_script("arguments[0].scrollIntoView();", next_page_button)
            time.sleep(1)

            # Clic con JavaScript para evitar bloqueos
            driver.execute_script("arguments[0].click();", next_page_button)

            print(f"➡ Avanzando a la página {pagina + 1}...")
            time.sleep(5)

        except Exception as e:
            print(f"⚠ Error en la página {pagina}: {e}")

    print("Descarga completada hasta la página 5.")

except Exception as e:
    print(f"Error general: {e}")
