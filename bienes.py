#en el siguiente codigo se genera un archivo CSV a partir de todos los datos obtenidos de todas las tablas de la pagina.
#librerias
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd

# opciones de navegacion
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-popup-blocking')

ser = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

driver = webdriver.Chrome(service=ser, options=options)

# inicio de navegador y busqueda
try:
    driver.get(
        'https://www.colombiacompra.gov.co/clasificador-de-bienes-y-servicios')
except:
    print('No se pudo ingresar a la URL solicitada')

def seleccionar_opcion(id_select, valor_opcion):
    select = Select(driver.find_element(By.ID, id_select))
    select.select_by_value(str(valor_opcion))
    time.sleep(1)

# obtener todas las opciones de los menús desplegables
grupos = Select(driver.find_element(By.ID, 'edit-grupos')).options

# lista para almacenar los datos
datos = []

# recorrer todas las opciones de los menús desplegables
for grupo in grupos:
    seleccionar_opcion('edit-grupos', grupo.get_attribute('value'))
    time.sleep(1)
    segmentos = Select(driver.find_element(By.ID, 'edit-segmento')).options
    for segmento in segmentos:
        seleccionar_opcion('edit-segmento', segmento.get_attribute('value'))
        time.sleep(1)
        familias = Select(driver.find_element(By.ID, 'edit-familia')).options
        for familia in familias:
            seleccionar_opcion('edit-familia', familia.get_attribute('value'))
            time.sleep(1)
            clases = Select(driver.find_element(By.ID, 'edit-clase')).options
            for clase in clases:
                seleccionar_opcion('edit-clase', clase.get_attribute('value'))
                time.sleep(1)
                productos = Select(driver.find_element(By.ID, 'edit-producto')).options
                for producto in productos:
                    seleccionar_opcion('edit-producto', producto.get_attribute('value'))
                    time.sleep(1)

                    # obtener los datos de la opción seleccionada
                    data = {'grupo': [grupo.text],
                            'segmento': [segmento.text],
                            'familia': [familia.text],
                            'clase': [clase.text],
                            'producto': [producto.text]}
                    datos.append(data)

# convertir los datos en un dataframe y guardarlos en un archivo csv
df = pd.DataFrame(datos)
clasificador_bienes = 'bienes_servicios.csv'
df.to_csv(clasificador_bienes)

driver.quit()