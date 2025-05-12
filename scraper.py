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
from urllib3.util.retry import Retry # Corregido import
from datetime import datetime

# 🔹 Asegurarse de que el archivo de log existe en el directorio raíz del proyecto
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scraper.log")
if not os.path.exists(log_file):
    with open(log_file, 'w', encoding='utf-8') as f: # Añadido encoding
        pass

# 🔹 Configuración del LOG
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='w', encoding='utf-8'), # Añadido encoding
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# 🔹 URL base del sitio a scrapear
BASE_URL = os.getenv('BASE_URL', 'https://docs.kasten.io/latest/')

# 🔹 Directorios de trabajo
DOCS_DIR = os.getenv('DOCS_DIR', 'docs/')
TMP_DIR = os.path.join(DOCS_DIR, 'tmp/')
# La creación de directorios se maneja en main()

# 🔹 Headers para evitar bloqueos
HEADERS = {
    'User-Agent': os.getenv('USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
}

# 🔹 Número de hilos para scraping en paralelo
MAX_WORKERS = int(os.getenv('MAX_WORKERS', multiprocessing.cpu_count() * 2))

# 🔹 Configuración de reintentos y pool de conexiones
session = requests.Session()
# El total de reintentos, factor de backoff y códigos de estado para reintentar
# pueden ajustarse según la fiabilidad del sitio web.
retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retries, pool_connections=MAX_WORKERS + 5, pool_maxsize=MAX_WORKERS + 5) # Ajustar pool size
session.mount('http://', adapter)
session.mount('https://', adapter)

### 🔹 Función para obtener los enlaces de la página principal
def get_main_links():
    """ Extrae los enlaces relevantes desde la página principal del sitio """
    try:
        response = session.get(BASE_URL, headers=HEADERS, timeout=30) # Añadido timeout
        logger.info(f"Obteniendo enlaces principales de {BASE_URL}. Status: {response.status_code}")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        links = set()
        # NUEVO SELECTOR basado en el HTML proporcionado:
        main_nav_links = soup.select('li.theme-doc-sidebar-item-link-level-1 > a.menu__link, li.theme-doc-sidebar-item-category-level-1 > div.menu__list-item-collapsible > a.menu__link')
        
        logger.info(f"Número de elementos coincidentes con el selector principal: {len(main_nav_links)}")

        for a_tag in main_nav_links:
            href = a_tag.get('href') 
            if href:
                if 'releasenotes' not in href.lower(): # Excluir 'releasenotes' (insensible a mayúsculas)
                    full_url = urljoin(BASE_URL, href) # urljoin maneja bien los / al inicio/final
                    
                    # Asegurar que solo procesamos URLs dentro del dominio y path esperado
                    if full_url.startswith(BASE_URL):
                        links.add(full_url)
                    else:
                        # Si el href es una URL absoluta a otro dominio, o no empieza con /latest/ después de unir
                        # esto podría ser un log útil
                        logger.debug(f"Enlace principal descartado (fuera de BASE_URL tras urljoin): {full_url} (href original: {href})")
            else:
                logger.warning("Elemento 'a' sin atributo href encontrado con el selector principal.")

        if not links:
            logger.warning(f"No se encontraron enlaces principales válidos en {BASE_URL} con el selector actual.")
            # Podrías intentar un selector de respaldo o simplemente retornar la lista vacía
            # Ejemplo de selector de respaldo más general si el anterior falla:
            # fallback_links = soup.select('nav[aria-label="Docs sidebar"] a.menu__link')
            # logger.info(f"Intentando con selector de respaldo, encontrados: {len(fallback_links)}")
            # for a_tag_fb in fallback_links: ... (lógica similar) ...

        logger.info(f"Enlaces principales encontrados y filtrados: {len(links)}")
        return list(links)

    except requests.exceptions.Timeout:
        logger.error(f"❌ Timeout al obtener enlaces principales de {BASE_URL}")
        return []
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error de Request al obtener enlaces principales: {e}")
        return []
    except Exception as e:
        logger.error(f"❌ Error inesperado en get_main_links: {e}", exc_info=True)
        return []

### 🔹 Función para extraer enlaces internos dentro de una página
def get_internal_links(soup, base_url_of_current_page):
    """ Extrae los enlaces internos de una página específica """
    internal_links = set()
    # Buscar dentro de un área de contenido más específica si es posible
    content_area_for_links = soup.find('article') or soup.find('main') or soup
    
    for a_tag in content_area_for_links.select('a[href]'):
        href = a_tag.get('href')
        if not href or href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:'):
            continue

        full_url = urljoin(base_url_of_current_page, href)
        
        # Limpiar fragmentos de la URL y parámetros de query
        parsed_full_url = urlparse(full_url)
        cleaned_url = parsed_full_url._replace(fragment="", query="").geturl()

        if cleaned_url.startswith(BASE_URL) and \
           cleaned_url != base_url_of_current_page and \
           'releasenotes' not in cleaned_url.lower(): # insensible a mayúsculas
            internal_links.add(cleaned_url)
            
    return list(internal_links)

### 🔹 Función para extraer contenido de una página
def scrape_page(url):
    """ Extrae y limpia el contenido de una página específica, aplicando formato Markdown. """
    try:
        response = session.get(url, headers=HEADERS, timeout=30)
        logger.info(f"Scraping {url} - Status: {response.status_code}")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remover elementos irrelevantes
        elements_to_remove = ["script", "style", "link", "meta", "header", "footer", "nav", "aside", 
                              ".breadcrumb", ".theme-edit-this-page", ".table-of-contents", 
                              "figure", "button.clean-btn.menu__caret"] # Clases específicas del sitio
        for selector in elements_to_remove:
            for tag_content in soup.select(selector):
                tag_content.decompose()
        
        content_area = soup.find('article') or soup.find('main') or soup.find(class_='theme-doc-markdown markdown')
        if not content_area:
            content_area = soup.find('body') or soup # Fallback
            if content_area is soup:
                 logger.warning(f"No se encontró área de contenido específica para {url}, usando body completo.")


        page_title_text = "Sin Título"
        title_tag_html = content_area.find('h1') 
        if title_tag_html:
            page_title_text = title_tag_html.get_text(separator=' ', strip=True)
            title_tag_html.decompose() # Evitar duplicar el H1
        elif soup.title and soup.title.string:
            page_title_text = soup.title.string.strip()
            # Heurística para limpiar títulos comunes de Sphinx/Docusaurus
            page_title_text = re.sub(r'\s*\|\s*.*?$', '', page_title_text) # Eliminar " | Sitio"
            page_title_text = re.sub(r'\s*·\s*.*?$', '', page_title_text) # Eliminar " · Sitio"


        page_content_parts = [f"# {page_title_text}\n\n"]
        processed_content_hashes = set() 

        for tag in content_area.find_all(['h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'pre', 'table', 'blockquote', 'hr']):
            if any(parent.name in ["figcaption"] for parent in tag.parents):
                continue

            text_content = ""
            tag_text_stripped = tag.get_text(" ", strip=True) # Para la clave del hash
            
            # Si el texto es muy corto o ya procesado, saltar
            if len(tag_text_stripped) < 5 and not tag.name in ['hr']: # Permitir <hr>
                continue
            
            content_hash = hash(tag.name + ":" + tag_text_stripped)
            if content_hash in processed_content_hashes:
                continue
            processed_content_hashes.add(content_hash)

            if tag.name.startswith('h'):
                level = int(tag.name[1:])
                header_text = tag.get_text(separator=' ', strip=True)
                if header_text:
                    text_content = f"\n{'#' * level} {header_text}\n\n"
            elif tag.name == 'p':
                paragraph_text = tag.get_text(separator=' ', strip=True)
                if paragraph_text:
                    text_content = f"{paragraph_text}\n\n"
            elif tag.name == 'ul':
                list_items = ""
                for li in tag.find_all('li', recursive=False): 
                    li_text = " ".join(li.get_text(separator=' ', strip=True).split()) # Normalizar espacios
                    if li_text: list_items += f"- {li_text}\n"
                if list_items: text_content = list_items + "\n"
            elif tag.name == 'ol':
                list_items = ""
                for i, li in enumerate(tag.find_all('li', recursive=False), 1):
                    li_text = " ".join(li.get_text(separator=' ', strip=True).split()) # Normalizar espacios
                    if li_text: list_items += f"{i}. {li_text}\n"
                if list_items: text_content = list_items + "\n"
            elif tag.name == 'pre':
                code_tag = tag.find('code')
                lang = ''
                if code_tag and code_tag.get('class'):
                    lang_class = [cls for cls in code_tag.get('class') if cls.startswith('language-')]
                    if lang_class:
                        lang = lang_class[0].replace('language-', '')
                
                code_block = tag.get_text().strip() # get_text() simple es mejor para <pre>
                text_content = f"\n```{lang}\n{code_block}\n```\n\n"
            elif tag.name == 'table':
                table_md = "\n"
                try:
                    headers = [th.get_text(strip=True).replace('|', '\\|') for th in tag.select('thead th, tr:first-child th, tr:first-child td')]
                    if headers:
                        table_md += f"| {' | '.join(headers)} |\n"
                        table_md += f"|{' :---: |' * len(headers)}\n"
                    
                    for row_idx, row in enumerate(tag.select('tbody tr, tr:not(:first-child)')): # Intentar capturar más filas
                        if not headers and row_idx == 0: # Si no hay thead, usar la primera fila como cabecera (riesgoso)
                            headers = [td.get_text(strip=True).replace('|', '\\|') for td in row.find_all(['td', 'th'])]
                            if headers:
                                table_md += f"| {' | '.join(headers)} |\n"
                                table_md += f"|{' :---: |' * len(headers)}\n"
                                continue # Saltar esta fila ya que se usó como cabecera
                        cells = [td.get_text(strip=True).replace('\n', ' ').replace('|', '\\|') for td in row.find_all(['td', 'th'])]
                        if cells: table_md += f"| {' | '.join(cells)} |\n"
                    if table_md.strip() == "" or table_md.count("|") < 2 : # Si la tabla es trivial o vacía
                        text_content = ""
                    else:
                        text_content = table_md + "\n"
                except Exception as table_e:
                    logger.warning(f"No se pudo convertir tabla compleja en {url} a Markdown: {table_e}. Contenido: {str(tag)[:200]}")
                    text_content = f"\n[Contenido de tabla omitido debido a complejidad]\n\n"

            elif tag.name == 'blockquote':
                quote_text = ""
                for p_tag in tag.find_all('p'): # A menudo blockquotes contienen párrafos
                    quote_text += "> " + p_tag.get_text(separator='\n> ', strip=True) + "\n"
                if not quote_text: # Fallback si no hay <p> dentro
                    quote_text = "> " + tag.get_text(separator='\n> ', strip=True)
                if quote_text.strip() != ">":
                    text_content = f"\n{quote_text.strip()}\n\n"
            elif tag.name == 'hr':
                text_content = "\n---\n\n"

            if text_content.strip():
                page_content_parts.append(text_content)
        
        final_page_content = "".join(page_content_parts)
        final_page_content = re.sub(r'\n\s*\n{2,}', '\n\n', final_page_content).strip()

        if not final_page_content or final_page_content == f"# {page_title_text}":
            logger.info(f"Contenido útil vacío para {url} después del procesamiento, descartando.")
            return None, None, []

        parsed_url_path = urlparse(url).path
        if parsed_url_path.startswith('/latest/'):
            cleaned_path = parsed_url_path[len('/latest/'):]
        else:
            cleaned_path = parsed_url_path.strip('/')
            
        file_name_base = cleaned_path.replace('/', '_').replace('.html', '')
        if not file_name_base or file_name_base == "_": # Para URL base como /latest/
            file_name_base = "overview_index" 
            
        file_name = file_name_base + ".md"
        # Si el nombre de archivo termina en _index.md (común en algunos generadores), simplificar a .md
        file_name = re.sub(r'_index\.md$', '.md', file_name, flags=re.IGNORECASE)
        # Corregir doble extensión .md.md
        file_name = re.sub(r'\.md\.md$', '.md', file_name, flags=re.IGNORECASE)
        
        path_parts = [part for part in cleaned_path.split('/') if part] # Filtrar partes vacías
        category = path_parts[0] if path_parts and path_parts[0] not in ["index.html", ""] else "overview"

        file_path = os.path.join(TMP_DIR, file_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(final_page_content)
        
        internal_links = get_internal_links(soup, url)

        return file_path, category, internal_links

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"❌ Error HTTP al procesar {url}: {http_err.response.status_code} - {http_err}")
        return None, None, []
    except requests.exceptions.RequestException as req_err: # Captura más genérica de requests
        logger.error(f"❌ Error de Red al procesar {url}: {req_err}")
        return None, None, []
    except Exception as e:
        logger.error(f"❌ Error general al procesar {url}: {e}", exc_info=True)
        return None, None, []

### 🔹 Función para scrapear todas las páginas en paralelo
def scrape_all():
    main_links = get_main_links()
    if not main_links:
        logger.warning("No se encontraron enlaces principales. Terminando scrape_all.")
        return {}, 0 

    logger.info(f"\n🔗 Se detectaron {len(main_links)} enlaces principales para procesar.")

    scraped_files = {}
    # Usar un conjunto para URLs visitadas para evitar reprocesar y bucles
    # Usar una lista para la cola de URLs a procesar para mantener el orden de descubrimiento (BFS-like)
    urls_to_scrape_queue = list(main_links)
    visited_urls = set(main_links) # Marcar los iniciales como visitados
    
    total_pages_processed = 0
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Enviar la primera tanda de URLs principales
        active_futures = {executor.submit(scrape_page, url): url for url in urls_to_scrape_queue}
        # Inicializar pbar con el número actual de tareas
        pbar = tqdm(total=len(active_futures), desc="Scraping pages", unit="page")

        while active_futures:
            next_round_futures = {} # Para los nuevos enlaces descubiertos
            for future in as_completed(active_futures):
                url_that_was_processed = active_futures[future]
                pbar.update(1) # Actualizar por cada tarea completada

                try:
                    file_path, category, internal_links_found = future.result()
                    if file_path and category:
                        scraped_files.setdefault(category, []).append(file_path)
                        total_pages_processed += 1
                    
                    if internal_links_found:
                        for link in internal_links_found:
                            if link not in visited_urls:
                                visited_urls.add(link)
                                # Añadir al pool de ejecución para la siguiente "iteración"
                                if link not in active_futures and link not in next_round_futures:
                                     #logger.debug(f"Encolando nuevo enlace: {link}")
                                     next_round_futures[executor.submit(scrape_page, link)] = link
                                     pbar.total += 1 # Incrementar el total de la barra de progreso
                                     # pbar.refresh() # Opcional, refrescar si el total cambia mucho
                except Exception as exc:
                    logger.error(f"Excepción al procesar el future para la URL {url_that_was_processed}: {exc}", exc_info=True)
            
            active_futures = next_round_futures # Mover a la siguiente ronda de tareas
            pbar.refresh() # Refrescar la barra de progreso al final de cada "nivel" de scraping

        pbar.close() # Cerrar la barra de progreso al finalizar

    if total_pages_processed > 0:
        logger.info(f"\n🔗 Scraping completado. Total de URLs visitadas: {len(visited_urls)}. Páginas guardadas: {total_pages_processed}.")
    else:
        logger.warning("\n🔗 Scraping completado, pero no se guardaron páginas. Revisa los logs para errores o falta de contenido.")
        
    return scraped_files, total_pages_processed

### 🔹 Función para unificar archivos por categoría
def unify_files(scraped_files):
    logger.info("Unificando archivos por categoría...")
    for category, files in scraped_files.items():
        safe_category_name = re.sub(r'[^\w\-_.]', '_', category.lower())
        if not safe_category_name: 
            safe_category_name = "unknown_category"
            
        output_file = os.path.join(DOCS_DIR, f"{safe_category_name}.md")
        files.sort(key=lambda f: os.path.basename(f))

        with open(output_file, 'w', encoding='utf-8') as f_out:
            category_title = category.replace('_', ' ').replace('-', ' ').title()
            f_out.write(f"# {category_title} Documentation\n\n") 
            
            for file_path in files:
                base_name = os.path.basename(file_path)
                sub_header_name = os.path.splitext(base_name)[0].replace('_', ' ').replace('-', ' ').title()
                if not sub_header_name: 
                    sub_header_name = "Contenido Adicional"

                f_out.write(f"## {sub_header_name}\n\n")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f_in:
                        content = f_in.read().strip()
                        # Eliminar el H1 si el contenido del archivo lo tiene, ya que tenemos H1 y H2
                        content = re.sub(r"^\s*#\s+[^\n]+\n*", "", content, count=1, flags=re.IGNORECASE)
                        f_out.write(content)
                    f_out.write("\n\n---\n\n") 
                except Exception as e:
                    logger.error(f"Error leyendo el archivo temporal {file_path} para unificar: {e}")
        logger.info(f"Categoría '{category}' unificada en {output_file}")

    if os.path.exists(TMP_DIR):
        try:
            shutil.rmtree(TMP_DIR)
            logger.info(f"Directorio temporal {TMP_DIR} eliminado.")
        except Exception as e:
            logger.error(f"No se pudo eliminar el directorio temporal {TMP_DIR}: {e}")

### 🔹 Función para limpiar la documentación (ejemplo básico)
def clean_documentation(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Eliminar múltiples líneas en blanco consecutivas a solo dos
        content = re.sub(r'\n\s*\n{2,}', '\n\n', content)
        # Eliminar espacios al final de las líneas
        content = re.sub(r' +\n', '\n', content)
        # Eliminar caracteres problemáticos específicos si los hubiera
        content = content.replace('ïƒ ', '') 

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content.strip() + '\n') # Asegurar un solo newline al final
    except Exception as e:
        logger.error(f"Error limpiando el archivo {file_path}: {e}")

### 🔹 Función para limpiar todos los documentos en un directorio
def clean_all_documents(directory):
    logger.info(f"Iniciando limpieza final de documentos en: {directory}")
    cleaned_count = 0
    if not os.path.isdir(directory):
        logger.warning(f"Directorio para limpieza no encontrado: {directory}")
        return
        
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            file_path = os.path.join(directory, filename)
            clean_documentation(file_path)
            cleaned_count +=1
    logger.info(f"Limpieza finalizada. Archivos Markdown procesados: {cleaned_count}")

### 🔹 Función para reiniciar un directorio
def reset_directory(directory):
    if os.path.exists(directory):
        try:
            shutil.rmtree(directory)
            logger.info(f"Directorio '{directory}' eliminado.")
        except Exception as e:
            logger.error(f"Error al eliminar el directorio '{directory}': {e}. Saliendo.")
            exit(1) # Salir si no se puede limpiar el directorio
    try:
        os.makedirs(directory)
        logger.info(f"Directorio '{directory}' (re)creado.")
    except Exception as e:
        logger.error(f"Error al crear el directorio '{directory}': {e}. Saliendo.")
        exit(1)


### 🔹 Función principal
def main():
    print("\n🚀 Iniciando scraping del Manual de Kasten K10\n")
    
    reset_directory(DOCS_DIR)
    os.makedirs(TMP_DIR, exist_ok=True) 
    logger.info(f"Directorio de trabajo temporal: {TMP_DIR}")
    logger.info(f"Directorio de salida final: {DOCS_DIR}")

    scraped_files, total_pages = scrape_all()

    if scraped_files and total_pages > 0:
        unify_files(scraped_files) # Esto ya elimina TMP_DIR al final
        print("\n📜 Resumen:")
        print(f"✅ Total de páginas procesadas y guardadas: {total_pages}")
        print(f"📂 Archivos unificados en la carpeta: {DOCS_DIR}")
        
        # clean_all_documents(DOCS_DIR) # La limpieza ahora es más integrada
        
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
