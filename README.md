
# Kasten K10 Scraper

Este es un script en Python para scrapear la documentación de [Kasten K10](https://docs.kasten.io/latest/) y almacenarla en archivos Markdown.

## 📌 Características
- Extrae enlaces principales e internos de la documentación oficial.
- Descarga y limpia el contenido en formato Markdown.
- Organiza los archivos por categorías.
- Ejecuta el scraping en paralelo utilizando `ThreadPoolExecutor` para mejorar la eficiencia.

## 🚀 Instalación y uso

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/tu-repo/kasten-k10-scraper.git
cd kasten-k10-scraper
```

### 2️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3️⃣ Ejecutar el scraper
```bash
python scraper.py
```

## 📂 Estructura del proyecto
```
kasten-k10-scraper/
│── docs/                # Archivos de documentación extraídos
│── scraper.py           # Script principal de scraping
│── requirements.txt     # Dependencias del proyecto
│── README.md            # Este archivo
```

## ⚙️ Configuración
- Puedes definir el número de hilos para el scraping con la variable de entorno `MAX_WORKERS`.
- El contenido se guarda en la carpeta `docs/`.

## 📜 Licencia
Este proyecto se distribuye bajo la licencia MIT.
