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
# La creación de directorios se moverá a la función main después de reset_directory

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
        logger.info(f"Obteniendo enlaces principales de {BASE_URL}. Status: {response.status_code}")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        links = set()
        # Selector anterior: soup.select('.toctree-l1 > a.reference.internal')
        # NUEVO SELECTOR basado en el HTML proporcionado:
        main_nav_links = soup.select('li.theme-doc-sidebar-item-link-level-1 > a.menu__link, li.theme-doc-sidebar-item-category-level-1 > div.menu__list-item-collapsible > a.menu__link')
        
        logger.info(f"Número de elementos coincidentes con el nuevo selector: {len(main_nav_links)}")

        for a in main_nav_links:
            href = a.get('href') # Usar .get('href') es más seguro
            if href:
                # El filtro 'releasenotes' se mantiene.
                # El filtro para .html o / también se mantiene.
                # Se asume que los href son relativos a la raíz del dominio o a BASE_URL.
                if 'releasenotes' not in href: # Excluimos releasenotes directamente aquí
                    # Construcción de URL completa
                    # Si BASE_URL = 'https://docs.kasten.io/latest/' y href = '/latest/install'
                    # urljoin lo manejará correctamente produciendo 'https://docs.kasten.io/latest/install'
                    # Si href es algo como 'overview.html' (relativo a la página actual, aunque aquí es la base)
                    # urljoin(BASE_URL, 'overview.html') -> 'https://docs.kasten.io/latest/overview.html'
                    full_url = urljoin(BASE_URL, href)
                    
                    # Verificación adicional para asegurar que el enlace pertenece al dominio base deseado si es necesario
                    if full_url.startswith('https://docs.kasten.io/latest/'):
                        links.add(full_url)
                    else:
                        logger.warning(f"Enlace descartado (no coincide con el dominio base esperado): {full_url} (desde href: {href})")
            else:
                logger.warning(f"Elemento 'a' sin atributo href encontrado con el selector.")

        logger.info(f"Enlaces principales encontrados: {len(links)}")
        return list(links)

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error al obtener enlaces principales: {e}")
        return []

### 🔹 Función para extraer enlaces internos dentro de una página
def get_internal_links(soup, base_url_of_current_page):
    """ Extrae los enlaces internos de una página específica """
    internal_links = set()
    for a in soup.select('a[href]'):
        href = a.get('href')
        if not href or href.startswith('#') or 'mailto:' in href:
            continue

        # Usar la URL de la página actual como base para resolver enlaces relativos
        full_url = urljoin(base_url_of_current_page, href)
        
        # Filtrar para incluir solo URLs bajo 'https://docs.kasten.io/latest/'
        # y excluir 'releasenotes' y la propia URL base de la página actual
        if full_url.startswith('https://docs.kasten.io/latest/') and \
           full_url != base_url_of_current_page and \
           'releasenotes' not in full_url:
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
        for tag_name in ["script", "style", "link", "meta", "header", "footer", "nav", "aside"]: # Añadidos más tags comunes
            for tag_content in soup.find_all(tag_name):
                tag_content.decompose()
        
        # Intentar encontrar el contenido principal de forma más específica
        # Muchos sistemas de documentación usan <article> o <main> o divs con id="main-content", "content", etc.
        content_area = soup.find('article') or soup.find('main') or soup.find(id='main-content') or soup.find(class_='theme-doc-markdown markdown')
        if not content_area:
            content_area = soup # Si no se encuentra un área específica, usar todo el body procesado

        title_tag = content_area.find('h1')
        page_content = f"# {title_tag.text.strip()}\n\n" if title_tag else ""

        # Mejorar la extracción de contenido para evitar duplicados y mantener estructura
        processed_texts = set() # Para evitar duplicados exactos de texto
        
        for tag in content_area.find_all(['h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'pre', 'table']):
            # Omitir si el tag está dentro de un elemento ya descompuesto o irrelevante (ej. botones de copia en <pre>)
            if any(parent.name in ["button", "figure"] for parent in tag.parents): # Ejemplo de exclusión
                continue

            text_content = ""
            if tag.name.startswith('h'):
                text_content = f"\n{'#' * int(tag.name[1:])} {tag.get_text(separator=' ', strip=True)}\n"
            elif tag.name == 'p':
                text_content = f"{tag.get_text(separator=' ', strip=True)}\n"
            elif tag.name == 'ul':
                list_items = ""
                for li in tag.find_all('li', recursive=False): # Solo li directos para evitar anidamiento incorrecto
                    li_text = li.get_text(separator=' ', strip=True)
                    if li_text: list_items += f"- {li_text}\n"
                if list_items: text_content = list_items
            elif tag.name == 'ol':
                list_items = ""
                for i, li in enumerate(tag.find_all('li', recursive=False), 1):
                    li_text = li.get_text(separator=' ', strip=True)
                    if li_text: list_items += f"{i}. {li_text}\n"
                if list_items: text_content = list_items
            elif tag.name == 'pre': # Para bloques de código
                code_block = tag.get_text() # .get_text() simple para pre puede ser suficiente
                text_content = f"\n```\n{code_block.strip()}\n```\n"
            elif tag.name == 'table': # Extracción básica de tablas a formato Markdown
                table_md = "\n"
                headers = [th.get_text(strip=True) for th in tag.select('thead th, tr:first-child th, tr:first-child td')]
                if headers:
                    table_md += f"| {' | '.join(headers)} |\n"
                    table_md += f"|{' --- |' * len(headers)}\n"
                
                for row in tag.select('tbody tr'):
                    cells = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
                    if cells: table_md += f"| {' | '.join(cells)} |\n"
                text_content = table_md + "\n"

            if text_content.strip() and text_content not in processed_texts:
                page_content += text_content
                processed_texts.add(text_content)
        
        # Eliminar líneas vacías múltiples, dejando solo una
        page_content = re.sub(r'\n\s*\n', '\n\n', page_content).strip()

        if not page_content:
            logger.info(f"Contenido vacío para {url}, descartando.")
            return None, None, []

        # Nombre de archivo y categoría
        parsed_url_path = urlparse(url).path
        # Remover '/latest/' del inicio si está presente para nombres de archivo más cortos
        if parsed_url_path.startswith('/latest/'):
            cleaned_path = parsed_url_path[len('/latest/'):]
        else:
            cleaned_path = parsed_url_path.strip('/')
            
        file_name_base = cleaned_path.replace('/', '_').replace('.html', '')
        if not file_name_base: # En caso de que la URL sea solo /latest/
            file_name_base = "index"
            
        file_name = file_name_base + ".md"
        file_name = re.sub(r'_index\.md$', '.md', file_name) # si termina en _index.md, solo .md
        file_name = re.sub(r'\.md\.md$', '.md', file_name)  # Corrige archivos con doble `.md.md`
        
        path_parts = cleaned_path.split('/')
        category = path_parts[0] if path_parts and path_parts[0] else "general"
        if not category or category == "index.html": # Si la URL es /latest/ o /latest/index.html
             category = "overview"


        file_path = os.path.join(TMP_DIR, file_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(page_content)
        
        # Extraer enlaces internos de la página actual
        internal_links = get_internal_links(soup, url)

        return file_path, category, internal_links

    except Exception as e:
        logger.error(f"❌ Error al procesar {url}: {e}")
        return None, None, []

### 🔹 Función para scrapear todas las páginas en paralelo con UNA barra de progreso
def scrape_all():
    main_links = get_main_links()
    if not main_links:
        logger.warning("No se encontraron enlaces principales para procesar en scrape_all.")
        return {}, 0 # MODIFICADO: Devolver dos valores

    logger.info(f"\n🔗 Se detectaron {len(main_links)} enlaces principales para procesar.")

    scraped_files = {}
    visited_urls = set(main_links) # Añadir enlaces principales a visitados desde el inicio
    urls_to_scrape_queue = list(main_links) 
    
    total_pages_processed = 0
    
    # Usar tqdm para la barra de progreso
    # Inicializar con el número actual de URLs, se actualizará dinámicamente
    with tqdm(total=len(urls_to_scrape_queue), desc="Scraping pages", unit="page") as pbar:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(scrape_page, url): url for url in urls_to_scrape_queue}
            
            while futures:
                new_futures = {}
                for future in as_completed(futures):
                    url_processed = futures[future] # Obtener la URL original de este future
                    pbar.update(1) # Actualizar por cada future completado

                    try:
                        file_path, category, internal_links = future.result()
                        if file_path and category:
                            scraped_files.setdefault(category, []).append(file_path)
                            total_pages_processed += 1
                        
                        # Añadir nuevos enlaces internos a la cola y actualizar total de pbar
                        for link in internal_links:
                            if link not in visited_urls:
                                visited_urls.add(link)
                                # No añadir directamente a urls_to_scrape_queue para evitar modificarla mientras se itera
                                # En su lugar, los añadimos a new_futures para la próxima ronda de submissions
                                if link not in futures and link not in new_futures : # Evitar re-procesar si ya está encolado
                                    new_futures[executor.submit(scrape_page, link)] = link
                                    pbar.total +=1 # Aumentar el total de la barra de progreso
                                    pbar.refresh() # Refrescar para mostrar el nuevo total
                    except Exception as exc:
                        logger.error(f"Error procesando future para URL {url_processed}: {exc}")
                
                futures = new_futures # Preparar el siguiente lote de futures

    return scraped_files, total_pages_processed


### 🔹 Función para unificar archivos por categoría
def unify_files(scraped_files):
    """ Unifica archivos en un solo Markdown por cada categoría """
    logger.info("Unificando archivos por categoría...")
    for category, files in scraped_files.items():
        # Sanitizar nombre de categoría para nombres de archivo
        safe_category_name = re.sub(r'[^\w\-_\.]', '_', category)
        if not safe_category_name: # Si la categoría queda vacía después de sanitizar
            safe_category_name = "unknow_category"
            
        output_file = os.path.join(DOCS_DIR, f"{safe_category_name}.md")

        # Ordenar archivos alfabéticamente por nombre base para consistencia
        # Esto ayuda si el orden de scraping no es determinístico debido al multithreading
        files.sort(key=lambda f: os.path.basename(f))

        with open(output_file, 'w', encoding='utf-8') as f_out:
            f_out.write(f"## {category.replace('_', ' ').capitalize()} Documentation\n") # Título principal del archivo de categoría
            for file_path in files:
                # Usar el nombre del archivo original (sin .md y reemplazando '_') como sub-cabecera
                base_name = os.path.basename(file_path)
                sub_header_name = base_name[:-3].replace('_', ' ').replace('-', ' ') # Quitar .md
                # Capitalizar cada palabra del sub_header_name
                sub_header_name = ' '.join(word.capitalize() for word in sub_header_name.split())


                f_out.write(f"### {sub_header_name}\n") # Usar H3 para subsecciones dentro de la categoría
                try:
                    with open(file_path, 'r', encoding='utf-8') as f_in:
                        f_out.write(f_in.read())
                    f_out.write("\n\n") # Espacio entre contenidos de archivos
                except Exception as e:
                    logger.error(f"Error leyendo el archivo temporal {file_path}: {e}")
        logger.info(f"Categoría '{category}' unificada en {output_file}")

    # Limpiar directorio temporal después de unificar todos los archivos
    if os.path.exists(TMP_DIR):
        try:
            shutil.rmtree(TMP_DIR)
            logger.info(f"Directorio temporal {TMP_DIR} eliminado.")
        except Exception as e:
            logger.error(f"No se pudo eliminar el directorio temporal {TMP_DIR}: {e}")
    else:
        logger.info(f"Directorio temporal {TMP_DIR} no encontrado, no necesita limpieza.")


### 🔹 Función para limpiar la documentación (ejemplo, se puede expandir)
def clean_documentation(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        cleaned_lines = []
        for line in lines:
            clean_line = line.rstrip() # Eliminar espacios extra al final
            
            # Eliminar múltiples líneas en blanco consecutivas (más de 2)
            if cleaned_lines and not clean_line.strip() and not cleaned_lines[-1].strip():
                continue # Evitar añadir más líneas en blanco si la anterior ya lo era

            # Ejemplo: normalizar encabezados (opcional, ya se intenta en scrape_page)
            # clean_line = re.sub(r'^#(\s)', r'##\1', clean_line) # asegurar min H2 si solo es H1
            
            # Eliminar caracteres no deseados específicos (ejemplo)
            clean_line = clean_line.replace('ïƒ ', '') # Carácter problemático específico

            cleaned_lines.append(clean_line + '\n') # Añadir newline de nuevo

        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(cleaned_lines)
        # logger.info(f"Archivo limpiado: {file_path}") # Puede ser muy verboso
    except Exception as e:
        logger.error(f"Error limpiando el archivo {file_path}: {e}")


### 🔹 Función para limpiar todos los documentos en un directorio
def clean_all_documents(directory):
    logger.info(f"Iniciando limpieza de documentos en: {directory}")
    cleaned_count = 0
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            file_path = os.path.join(directory, filename)
            clean_documentation(file_path)
            cleaned_count +=1
    logger.info(f"Limpieza finalizada. Archivos Markdown procesados: {cleaned_count}")


### 🔹 Función para reiniciar un directorio
def reset_directory(directory):
    """Elimina el directorio especificado y lo recrea para asegurar que esté vacío."""
    if os.path.exists(directory):
        shutil.rmtree(directory)
        logger.info(f"Directorio '{directory}' eliminado.")
    os.makedirs(directory)
    logger.info(f"Directorio '{directory}' recreado.")

### 🔹 Función principal
def main():
    print("\n🚀 Iniciando scraping del Manual de Kasten K10\n")
    
    reset_directory(DOCS_DIR)
    # TMP_DIR se crea dentro de DOCS_DIR, así que se recreará también.
    # Aseguramos que TMP_DIR exista explícitamente por si DOCS_DIR ya existía y no fue reseteado (aunque reset_directory lo hace)
    os.makedirs(TMP_DIR, exist_ok=True) 
    logger.info(f"Directorio de trabajo temporal: {TMP_DIR}")
    logger.info(f"Directorio de salida final: {DOCS_DIR}")

    scraped_files, total_pages = scrape_all()

    if scraped_files and total_pages > 0:
        unify_files(scraped_files)
        print("\n📜 Resumen:")
        print(f"✅ Total de páginas procesadas y guardadas: {total_pages}")
        print(f"📂 Archivos unificados en la carpeta: {DOCS_DIR}")
        
        clean_all_documents(DOCS_DIR) # Limpiar los archivos finales unificados
        
        print("🟢 Proceso finalizado con éxito.\n")
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"Documentos actualizados el día {datetime.now().strftime('%d/%m/%Y')} a las {datetime.now().strftime('%H:%M:%S')}h. Total páginas: {total_pages}\n")
    else:
        print("⚠️ No se encontraron archivos para procesar o ningún enlace principal fue válido.")
        logger.warning("No se procesaron archivos o no se encontraron enlaces principales válidos.")
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"Intento de actualización el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}: No se procesaron archivos.\n")


if __name__ == "__main__":
    main()
