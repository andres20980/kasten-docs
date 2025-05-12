import os
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import shutil
import re
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from datetime import datetime

# 🔹 Asegurarse de que el archivo de log existe en el directorio raíz del proyecto
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scraper.log")
if not os.path.exists(log_file):
    with open(log_file, 'w') as f:
        pass

# 🔹 Configuración del LOG
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='w'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# 🔹 URL base del sitio a scrapear
BASE_URL = os.getenv('BASE_URL', 'https://docs.kasten.io/latest/')

# 🔹 Directorios de trabajo
DOCS_DIR = os.getenv('DOCS_DIR', 'docs/')
TMP_DIR = os.path.join(DOCS_DIR, 'tmp/')
os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)

# 🔹 Headers para evitar bloqueos
HEADERS = {
    'User-Agent': os.getenv('USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
}

# 🔹 Número de hilos para scraping en paralelo
MAX_WORKERS = int(os.getenv('MAX_WORKERS', multiprocessing.cpu_count() * 2))

# 🔹 Configuración de reintentos y pool de conexiones
session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
adapter = HTTPAdapter(max_retries=retries, pool_connections=20, pool_maxsize=100)
session.mount('http://', adapter)
session.mount('https://', adapter)

### 🔹 Función para obtener los enlaces de la página principal
def get_main_links():
    """ Extrae los enlaces relevantes desde la página principal del sitio """
    try:
        response = session.get(BASE_URL, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        links = set()
        for a in soup.select('.toctree-l1 > a.reference.internal'):
            href = a['href']
            if href.endswith(('.html', '/')) and 'releasenotes' not in href:
                full_url = urljoin(BASE_URL, href)
                links.add(full_url)

        return list(links)

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error al obtener enlaces principales: {e}")
        return []

### 🔹 Función para extraer enlaces internos dentro de una página
def get_internal_links(soup, base_url):
    """ Extrae los enlaces internos de una página específica """
    internal_links = set()
    for a in soup.select('a[href]'):
        href = a['href']
        if href.startswith('#') or 'mailto:' in href:
            continue

        full_url = urljoin(base_url, href)
        if BASE_URL in full_url and full_url != base_url and full_url.endswith(('.html', '/')) and 'releasenotes' not in full_url:
            internal_links.add(full_url)

    return list(internal_links)

### 🔹 Función para extraer contenido de una página
def scrape_page(url):
    """ Extrae y limpia el contenido de una página específica, incluyendo enlaces internos """
    try:
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remover elementos irrelevantes
        for tag in soup(["script", "style", "link", "meta"]):
            tag.decompose()

        title = soup.find('h1')
        page_content = f"# {title.text.strip()}\n\n" if title else ""

        sections = set()
        for tag in soup.find_all(['h2', 'h3', 'h4', 'p', 'ul', 'ol']):
            text = tag.text.strip()
            if "Release Notes" in text:
                continue

            if tag.name in ['h2', 'h3', 'h4']:
                page_content += f"\n## {text}\n"
            elif tag.name == 'p':
                if text not in sections:
                    page_content += f"{text}\n"
                    sections.add(text)
            elif tag.name == 'ul':
                for li in tag.find_all('li'):
                    li_text = li.text.strip()
                    if li_text not in sections:
                        page_content += f"- {li_text}\n"
                        sections.add(li_text)
            elif tag.name == 'ol':
                for i, li in enumerate(tag.find_all('li'), 1):
                    li_text = li.text.strip()
                    if li_text not in sections:
                        page_content += f"{i}. {li_text}\n"
                        sections.add(li_text)

        if not page_content.strip():
            return None, None, []

        file_name = urlparse(url).path.strip('/').replace('/', '_').replace('.html', '') + ".md"
        file_name = re.sub(r'\.md\.md$', '.md', file_name)  # Corrige archivos con doble `.md.md`
        category = file_name.split('_')[1] if '_' in file_name else "otros"
        file_path = os.path.join(TMP_DIR, file_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(page_content)

        return file_path, category, get_internal_links(soup, url)

    except Exception as e:
        logger.error(f"❌ Error al procesar {url}: {e}")
        return None, None, []

### 🔹 Función para scrapear todas las páginas en paralelo con UNA barra de progreso
def scrape_all():
    main_links = get_main_links()
    if not main_links:
        return {}, 0

    logger.info(f"\n🔗 Se detectaron {len(main_links)} enlaces principales para procesar.")

    scraped_files = {}
    visited_urls = set(main_links)
    urls_to_scrape = list(main_links)  # Lista de URLs iniciales a scrapear

    # Preparar una sola barra de progreso para todos los enlaces a scrapear
    pbar = tqdm(total=len(urls_to_scrape), desc="Scraping pages", unit="page")
    total_pages = 0
    all_urls = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        while urls_to_scrape:
            futures = {executor.submit(scrape_page, url): url for url in urls_to_scrape}
            urls_to_scrape = []  # Limpiar la lista para la siguiente ronda de scraping

            # Procesar resultados de futures
            for future in as_completed(futures):
                file, category, internal_links = future.result()
                pbar.update(1)  # Actualizar la barra de progreso por cada página procesada
                if file:
                    scraped_files.setdefault(category, []).append(file)
                    total_pages += 1
                for link in internal_links:
                    if link not in visited_urls:
                        visited_urls.add(link)
                        urls_to_scrape.append(link)
                        pbar.total += 1  # Aumentar el total de la barra de progreso con nuevos enlaces

    pbar.close()  # Cerrar la barra de progreso al final del proceso
    logger.info(f"\n🔗 Se detectaron {len(all_urls)} enlaces internos adicionales.\n")

    return scraped_files, total_pages

### 🔹 Función para unificar archivos por categoría
def unify_files(scraped_files):
    """ Unifica archivos en un solo Markdown por cada categoría """
    for category, files in scraped_files.items():
        output_file = os.path.join(DOCS_DIR, f"{category}.md")

        with open(output_file, 'w', encoding='utf-8') as f_out:
            f_out.write(f"# {category.capitalize()} Documentation\n\n")
            for file in files:
                with open(file, 'r', encoding='utf-8') as f_in:
                    f_out.write(f"\n\n## {os.path.basename(file)}\n")
                    f_out.write(f_in.read())

    shutil.rmtree(TMP_DIR, ignore_errors=True)

### 🔹 Función para limpiar la documentación
def clean_documentation(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    cleaned_lines = []
    for line in lines:
        # Eliminar espacios extra al final de cada línea
        clean_line = line.rstrip() + '\n'
        
        # Corregir encabezados para asegurar consistencia, por ejemplo:
        clean_line = re.sub(r'#+', lambda match: '#' * (len(match.group(0)) + 1), clean_line)

        # Eliminar caracteres no deseados
        clean_line = clean_line.replace('ï', '')

        # Agregar más reglas de limpieza según sea necesario
        # Ejemplo: eliminar líneas completamente vacías
        if clean_line.strip():
            cleaned_lines.append(clean_line)

    # Escribir de nuevo al archivo con las líneas limpias
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(cleaned_lines)

    print(f"Archivo limpiado: {file_path}")

### 🔹 Función para limpiar todos los documentos en un directorio
def clean_all_documents(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.md'):  # Asegurarse de que sólo se procesan archivos Markdown
            file_path = os.path.join(directory, filename)
            clean_documentation(file_path)

### 🔹 Función para reiniciar un directorio
def reset_directory(directory):
    """Elimina el directorio especificado y lo recrea para asegurar que esté vacío."""
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)
    print(f"Directorio '{directory}' reiniciado.")

### 🔹 Función principal
def main():
    print("\n🚀 Iniciando scraping del Manual de Kasten K10\n")
    
    # Reinicia el directorio docs/ y asegura la creación de subdirectorios necesarios antes de comenzar el scraping
    reset_directory(DOCS_DIR)
    os.makedirs(TMP_DIR, exist_ok=True)  # Asegúrate de que el directorio temporal existe

    scraped_files, total_pages = scrape_all()

    if scraped_files:
        unify_files(scraped_files)
        print("\n📜 Resumen:")
        print(f"✅ Total de archivos procesados: {total_pages}")
        print(f"📂 Archivos unificados en la carpeta: {DOCS_DIR}")
        # Llamar a la función de limpieza después de unificar los archivos
        clean_all_documents(DOCS_DIR)
        print("🟢 Proceso finalizado con éxito.\n")
        
        # Registrar la fecha y hora de actualización en el archivo de log
        with open(log_file, 'a') as f:
            f.write(f"Documentos actualizados el día {datetime.now().strftime('%d/%m/%Y')} a las {datetime.now().strftime('%H:%M:%S')}h\n")
    else:
        print("⚠️ No se encontraron archivos para procesar.")

if __name__ == "__main__":
    main()
