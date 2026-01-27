from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import time
import os
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'mockup_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'),
        logging.StreamHandler()
    ]
)

# Función para tomar la captura de pantalla
def take_screenshot(url, viewport, file_name, timeout=30):
    driver = None
    try:
        # Configurar las opciones del navegador
        options = Options()
        options.headless = True

        # Suprimir errores y advertencias de Chrome
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-logging')
        options.add_argument('--log-level=3')
        options.add_argument('--silent')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # Iniciar el navegador
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.set_page_load_timeout(timeout)

        # Configurar las dimensiones para cada vista ANTES de cargar la página
        if viewport == 'desktop':
            driver.set_window_size(1920, 1080)
        elif viewport == 'tablet':
            driver.set_window_size(1024, 1366)
        elif viewport == 'mobile':
            driver.set_window_size(430, 932)

        # Cargar la URL
        logging.info(f"Accediendo a {url} [{viewport}]...")
        driver.get(url)

        # Esperar a que la página se cargue completamente
        time.sleep(5)

        # Tomar la captura de pantalla
        driver.save_screenshot(file_name)
        logging.info(f"✓ Captura guardada: {file_name}")

        return True

    except TimeoutException:
        logging.error(f"✗ Timeout al acceder a {url} [{viewport}] - La página tardó más de {timeout}s en cargar")
        return False

    except WebDriverException as e:
        error_msg = str(e)
        if "ERR_NAME_NOT_RESOLVED" in error_msg:
            logging.error(f"✗ DNS no resuelto para {url} [{viewport}] - Verifica que el dominio existe")
        elif "ERR_CONNECTION_REFUSED" in error_msg:
            logging.error(f"✗ Conexión rechazada para {url} [{viewport}] - El servidor no responde")
        elif "ERR_CONNECTION_TIMED_OUT" in error_msg:
            logging.error(f"✗ Timeout de conexión para {url} [{viewport}]")
        else:
            logging.error(f"✗ Error de WebDriver para {url} [{viewport}]: {error_msg[:200]}")
        return False

    except Exception as e:
        logging.error(f"✗ Error inesperado para {url} [{viewport}]: {str(e)[:200]}")
        return False

    finally:
        # Cerrar el navegador siempre
        if driver:
            try:
                driver.quit()
            except:
                pass

# Función para combinar las capturas en un mockup
def combine_screenshots(site_name, output_dir='mockups', temp_dir='screenshots'):
    """
    Combina las 3 capturas de pantalla de un sitio en una sola imagen mockup.
    Layout: Tablet (izquierda solapada) - Desktop (centro) - Mobile (derecha solapada)
    """

    # Rutas de las imágenes
    desktop_path = f'{temp_dir}/{site_name}_desktop.png'
    tablet_path = f'{temp_dir}/{site_name}_tablet.png'
    mobile_path = f'{temp_dir}/{site_name}_mobile.png'

    # Verificar que existan todas las imágenes
    if not all(os.path.exists(path) for path in [desktop_path, tablet_path, mobile_path]):
        logging.error(f"✗ Faltan imágenes para {site_name}, no se puede crear mockup")
        return False

    try:
        # Cargar las imágenes y convertir a RGBA
        desktop = Image.open(desktop_path).convert('RGBA')
        tablet = Image.open(tablet_path).convert('RGBA')
        mobile = Image.open(mobile_path).convert('RGBA')

        # Obtener dimensiones
        desktop_w, desktop_h = desktop.size
        tablet_w, tablet_h = tablet.size
        mobile_w, mobile_h = mobile.size

        # Posiciones iniciales (relativas, desktop como referencia en 0,0)
        desktop_x_rel = 0
        desktop_y_rel = 0

        # Mobile: 50% hacia la izquierda desde la derecha del desktop
        # y 50% hacia abajo
        mobile_x_rel = desktop_w - int(mobile_w * 0.5)
        mobile_y_rel = int(mobile_h * 0.5)

        # Tablet: 50% hacia la derecha (negativo porque va a la izquierda del desktop)
        # y ajustar para que la parte inferior coincida con mobile
        tablet_x_rel = -int(tablet_w * 0.5)
        # Para que la parte inferior de tablet esté a la misma altura que mobile:
        # tablet_y + tablet_h = mobile_y + mobile_h
        # tablet_y = mobile_y + mobile_h - tablet_h
        tablet_y_rel = mobile_y_rel + mobile_h - tablet_h

        # Calcular bounding box
        # Puntos extremos de cada imagen
        positions = [
            (tablet_x_rel, tablet_y_rel, tablet_x_rel + tablet_w, tablet_y_rel + tablet_h),
            (desktop_x_rel, desktop_y_rel, desktop_x_rel + desktop_w, desktop_y_rel + desktop_h),
            (mobile_x_rel, mobile_y_rel, mobile_x_rel + mobile_w, mobile_y_rel + mobile_h)
        ]

        # Encontrar los límites del canvas
        min_x = min(pos[0] for pos in positions)
        min_y = min(pos[1] for pos in positions)
        max_x = max(pos[2] for pos in positions)
        max_y = max(pos[3] for pos in positions)

        # Dimensiones del canvas con margen
        margin = 20
        canvas_width = max_x - min_x + (2 * margin)
        canvas_height = max_y - min_y + (2 * margin)

        # Crear canvas con fondo transparente
        canvas = Image.new('RGBA', (canvas_width, canvas_height), color=(0, 0, 0, 0))

        # Ajustar posiciones absolutas en el canvas (compensar el min y agregar margen)
        tablet_x = tablet_x_rel - min_x + margin
        tablet_y = tablet_y_rel - min_y + margin
        desktop_x = desktop_x_rel - min_x + margin
        desktop_y = desktop_y_rel - min_y + margin
        mobile_x = mobile_x_rel - min_x + margin
        mobile_y = mobile_y_rel - min_y + margin

        # Pegar las imágenes en el canvas (orden: desktop primero, luego tablet y mobile encima)
        canvas.paste(desktop, (desktop_x, desktop_y), desktop)
        canvas.paste(tablet, (tablet_x, tablet_y), tablet)
        canvas.paste(mobile, (mobile_x, mobile_y), mobile)

        # Guardar la imagen combinada
        output_path = f'{output_dir}/{site_name}_mockup.png'
        canvas.save(output_path, 'PNG')
        logging.info(f"✓ Mockup generado: {output_path}")

        return True

    except Exception as e:
        logging.error(f"✗ Error generando mockup para {site_name}: {str(e)}")
        return False

# Función para limpiar capturas individuales
def cleanup_screenshots(site_name, temp_dir='screenshots'):
    """
    Elimina las capturas individuales después de generar el mockup.
    """
    try:
        for viewport in ['desktop', 'tablet', 'mobile']:
            file_path = f'{temp_dir}/{site_name}_{viewport}.png'
            if os.path.exists(file_path):
                os.remove(file_path)
        logging.info(f"✓ Capturas individuales eliminadas para {site_name}")
        return True
    except Exception as e:
        logging.warning(f"⚠ No se pudieron eliminar capturas para {site_name}: {str(e)}")
        return False

# Función principal para procesar múltiples sitios web
def process_websites(websites):
    # Crear carpetas si no existen
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')
    if not os.path.exists('mockups'):
        os.makedirs('mockups')

    # Estadísticas
    total_sites = len(websites)
    successful_mockups = []
    failed_sites = []
    partial_sites = []

    logging.info(f"Iniciando procesamiento de {total_sites} sitios web...")
    logging.info("=" * 70)

    for idx, url in enumerate(websites, 1):
        try:
            # Extraer el nombre del sitio web (dominio)
            site_name = url.split("//")[-1].split("/")[0]

            logging.info(f"\n[{idx}/{total_sites}] Procesando: {site_name}")
            logging.info("-" * 70)

            # Contadores para este sitio
            screenshots_success = 0
            viewports = ['desktop', 'tablet', 'mobile']

            # Tomar capturas en diferentes vistas
            for viewport in viewports:
                file_name = f'screenshots/{site_name}_{viewport}.png'
                success = take_screenshot(url, viewport, file_name)
                if success:
                    screenshots_success += 1

            # Si tenemos las 3 capturas, generar mockup
            if screenshots_success == 3:
                logging.info(f"✓ Capturas completas: {site_name} (3/3)")

                # Generar mockup
                if combine_screenshots(site_name):
                    successful_mockups.append(site_name)
                    # Limpiar capturas individuales
                    cleanup_screenshots(site_name)
                else:
                    partial_sites.append(f"{site_name} (capturas OK, mockup falló)")

            elif screenshots_success > 0:
                partial_sites.append(f"{site_name} (capturas parciales: {screenshots_success}/3)")
                logging.warning(f"⚠ Capturas incompletas: {site_name} ({screenshots_success}/3)")
                # Limpiar capturas parciales
                cleanup_screenshots(site_name)
            else:
                failed_sites.append(site_name)
                logging.error(f"✗ Sitio fallido: {site_name} (0/3 capturas)")

        except Exception as e:
            site_name = site_name if 'site_name' in locals() else url
            failed_sites.append(site_name)
            logging.error(f"✗ Error crítico procesando {url}: {str(e)[:200]}")

    # Reporte final
    logging.info("\n" + "=" * 70)
    logging.info("REPORTE FINAL")
    logging.info("=" * 70)
    logging.info(f"Total de sitios procesados: {total_sites}")
    logging.info(f"Mockups exitosos: {len(successful_mockups)}")
    logging.info(f"Sitios parciales: {len(partial_sites)}")
    logging.info(f"Sitios fallidos: {len(failed_sites)}")

    if successful_mockups:
        logging.info(f"\n✓ Mockups generados exitosamente: {len(successful_mockups)}")
        logging.info("Ubicación: ./mockups/")

    if partial_sites:
        logging.info("\n⚠ Sitios con problemas parciales:")
        for site in partial_sites:
            logging.info(f"  - {site}")

    if failed_sites:
        logging.info("\n✗ Sitios con errores:")
        for site in failed_sites:
            logging.info(f"  - {site}")

    logging.info("=" * 70)

if __name__ == "__main__":
    # Lista de sitios web que deseas capturar
    websites = [
        "https://acuatika25.com.ar/",
        "https://decotay.com.ar/",
        "https://lanuscomputacion.com/",
        "https://aidbones.com/",
        "https://alquiriasolutions.com/",
        "https://alphatelservices.com/",
        "https://amarantus.esloogan.online/",
        "https://aptofisico.com/",
        "https://asistencia365.com.ar/",
        "https://abogario.com.ar/",
        "https://academiacopo.com/",
        "https://bennecke.com/",
        "https://genblocksa.com",
        "https://gretacloset.com/",
        "https://grupoalquilaga.com/",
        "https://ginailsenvalladolid.com/",
        "https://bercatti.com/",
        "https://banplast.com.ar/",
        "https://behshadarjomandi.com/",
        "https://consulting-21.com/",
        "https://centraldeturbos.com/",
        "https://citipix.eu/",
        "https://cvela2017.com/",
        "https://cosechanatural.com.ar/",
        "https://ciclorural.com/",
        "https://dermaklinic.cl/",
        "https://depaoli.com.ar/",
        "https://diaadianet.com.ar/",
        "https://draandreamamani.com/",
        "https://decotay.com.ar/",
        "https://ecoalimentaria.es",
        "https://entrenatvalladolid.com/",
        "https://ett.esloogan.online/",
        "https://ekilib.es/",
        "https://forttia.tech/",
        "https://geobauen.com/",
        "https://globaloltenia.es/",
        "https://tvmasmagazine.com/",
        "https://guiadepredadoresorellana.com/",
        "https://lacanchitalujan.com/",
        "https://lavozderozario.com",
        "https://matiasgarcetesuarez.com.ar/",
        "https://mako.com.ar/",
        "https://ntkic.com/",
        "https://negociosoptimizados.com/",
        "https://sosamirandaabogados.com.ar/",
        "https://talaiotaudio.com/",
        "https://todosalud.co/",
        "https://unipega.com/",
        "https://ingenieriaproyectos.com.ar",
        "https://inksomniumtattoo.com/",
        "https://pescaolidvalladolid.com/",
        "https://petruscigars.com/"
        "https://piscinasluciano.com.ar/",
        "https://pp.esloogan.online/",
        "https://playformacion.es/",
        "https://sofitex.com.ar/",
        "https://smartalk.cl/",
        "https://semikon.com.ar/",
        "https://semikongarden.com.ar/",
        "https://seararefrigeracion.com.ar/",
        "https://watervan.com.ar/",
        "https://muebles-cavah.com.ar/",
        "https://limpiezasmn.es/",
        "https://reformaplus.com/",
        "https://recomprando.com/",
        "https://rocadeguiapsicologia.es/",
        "https://ecoalimentaria.es/",
        "https://8mejor.top/",
        "https://healthybodychamp.com/",
        "https://saute.es/",
        "https://vestigiostudio.com/",
        "https://yourdream.ae",
    ]

    # Procesar todos los sitios web
    process_websites(websites)
