# En este codigo se utiliza la forma de busqueda manual de cada uno de los grupos, es decir
# nosotros mismos debemos entregarle la ruta para que busque y almacene los datos.
#librerias
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd

#opciones de navegacion
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-popup-blocking')

ser = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

driver = webdriver.Chrome(service = ser, options = options)

#inicio de navegador y busqueda
try:
    driver.get('https://www.colombiacompra.gov.co/clasificador-de-bienes-y-servicios')
except:
        print('No se pudo ingresar a la URL solicitada')

grupo = Select(driver.find_element(By.ID, 'edit-grupos'))
grupo.select_by_value('A')
time.sleep(1)
segmento = Select(driver.find_element(By.ID, 'edit-segmento'))
segmento.select_by_value(str('10'))
time.sleep(1)
familia = Select(driver.find_element(By.ID, 'edit-familia'))
familia.select_by_value(str('1010'))
time.sleep(1)
clases = Select(driver.find_element(By.ID, 'edit-clase'))
clases.select_by_value(str('101015'))
time.sleep(1)
productos = Select(driver.find_element(By.ID, 'edit-producto'))
productos.select_by_value(str('10101501'))
time.sleep(1)


#se crea el documento csv
try:
    data = {'segmento':[segmento.first_selected_option.text],
            'familia': [familia.first_selected_option.text],
            'clase': [clases.first_selected_option.text],
            'producto': [productos.first_selected_option.text]}

    df = pd.DataFrame(data)

    clasificador_bienes = 'bienes_servicios_1.csv'
    df.to_csv(clasificador_bienes)

    del df
except:
    print("error en la creacion del csv")
driver.quit()