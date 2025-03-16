
# Kasten K10 Scraper

Este es un script en Python para scrapear la documentación de [Kasten K10](https://docs.kasten.io/latest/) y almacenarla en archivos Markdown.

## 📌 Características

- Extrae enlaces principales e internos de la documentación oficial.
- Descarga y limpia el contenido en formato Markdown.
- Organiza los archivos por categorías.
- Ejecuta el scraping en paralelo utilizando `ThreadPoolExecutor` para mejorar la eficiencia.

## 🚀 Instalación y uso

### 1️⃣ Clonar el repositorio

git clone https://github.com/tu-repo/kasten-k10-scraper.git
cd kasten-k10-scraper

### 2️⃣ Instalar dependencias

pip install -r requirements.txt

### 3️⃣ Configurar variables de entorno (opcional)

export BASE_URL="https://docs.kasten.io/latest/"
export DOCS_DIR="docs/"
export USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
export MAX_WORKERS=8

### 4️⃣ Ejecutar el scraper

python scraper.py

## 📂 Estructura del proyecto

kasten-k10-scraper/
│── docs/                # Archivos de documentación extraídos
│── scraper.py           # Script principal de scraping
│── requirements.txt     # Dependencias del proyecto
│── README.md            # Este archivo

## ⚙️ Configuración

- Puedes definir el número de hilos para el scraping con la variable de entorno `MAX_WORKERS`.
- El contenido se guarda en la carpeta `docs/`.

## 📜 Licencia

Este proyecto se distribuye bajo la licencia GNU General Public License v3.0.
