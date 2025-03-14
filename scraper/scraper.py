import os
import requests
from bs4 import BeautifulSoup
import markdownify
import time

# Configuración
BASE_URL = "https://docs.kasten.io/latest/install/index.html"
BASE_DIR = "docs"
MAX_FILES = 20
MAX_SIZE_MB = 10
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Función para obtener todos los enlaces internos
def get_links(base_url):
    response = requests.get(base_url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Error al acceder a {base_url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/") or href.startswith("https://docs.kasten.io"):
            full_url = href if href.startswith("http") else f"https://docs.kasten.io{href}"
            if full_url not in links and "kasten.io" in full_url:
                links.append(full_url)

    return links

# Función para limpiar y convertir HTML a Markdown
def clean_content(html):
    soup = BeautifulSoup(html, "html.parser")

    # Eliminar elementos innecesarios
    for tag in soup(["script", "style", "nav", "footer", "header", "meta"]):
        tag.extract()

    return markdownify.markdownify(str(soup), heading_style="ATX")

# Función para guardar contenido en archivos
def save_content(filename, content):
    filepath = os.path.join(BASE_DIR, filename)

    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Guardado: {filename}")

# Scraping principal
def scrape_docs():
    links = get_links(BASE_URL)
    total_links = len(links)
    print(f"Encontrados {total_links} enlaces.")

    chunk_size = max(1, total_links // MAX_FILES)
    file_count = 1
    collected_texts = []

    for i, link in enumerate(links):
        print(f"Procesando {link}...")
        response = requests.get(link, headers=HEADERS)

        if response.status_code == 200:
            content_md = clean_content(response.text)
            collected_texts.append(content_md)

        # Cada "chunk_size" páginas, guardamos un archivo
        if (i + 1) % chunk_size == 0 or i == total_links - 1:
            combined_text = "\n\n".join(collected_texts)
            filename = f"{str(file_count).zfill(2)}_documento.md"

            # Verificar tamaño antes de guardar
            if len(combined_text.encode("utf-8")) / (1024 * 1024) < MAX_SIZE_MB:
                save_content(filename, combined_text)
                file_count += 1
                collected_texts = []

        if file_count > MAX_FILES:
            break

        time.sleep(1)  # Para evitar bloqueo por demasiadas peticiones

if __name__ == "__main__":
    scrape_docs()
