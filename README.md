# Kasten K10 Scraper

Este es un script en Python para scrapear la documentación de Kasten K10 y almacenarla en archivos Markdown.

## Características

- Extrae enlaces principales e internos de la documentación oficial.
- Descarga y limpia el contenido en formato Markdown.
- Organiza los archivos por categorías.
- Ejecuta el scraping en paralelo utilizando `ThreadPoolExecutor` para mejorar la eficiencia.

## Requisitos previos

- Python 3.7 o superior
- `pip` (gestor de paquetes de Python)

## Instalación y uso

1. **Clonar el repositorio**

    ```sh
    git clone https://github.com/tu-repo/kasten-k10-scraper.git
    cd kasten-k10-scraper
    ```

2. **Instalar dependencias**

    ```sh
    pip install -r requirements.txt
    ```

3. **Configurar variables de entorno (opcional)**

    Exporta las siguientes variables de entorno según sea necesario para personalizar la configuración del scraper:

    - `BASE_URL`: URL base de la documentación que deseas scrapear (por defecto: `https://docs.kasten.io/latest/`).
    - `DOCS_DIR`: Directorio donde se guardarán los documentos descargados (por defecto: `docs/`).
    - `USER_AGENT`: Cadena de agente de usuario para las solicitudes HTTP (por defecto: `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36`).
    - `MAX_WORKERS`: Número de hilos para el scraping en paralelo. El valor predeterminado es el doble del número de núcleos de CPU de tu máquina. Ajusta este valor según la capacidad de tu sistema y las necesidades de rendimiento.

    Ejemplo para establecer las variables en sistemas basados en Unix/Linux:

    ```sh
    export BASE_URL="https://docs.kasten.io/latest/"
    export DOCS_DIR="docs/"
    export USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    export MAX_WORKERS=8  # Ajusta este número según sea necesario
    ```

4. **Ejecutar el scraper**

    ```sh
    python scraper.py
    ```

## Estructura del proyecto

```
kasten-k10-scraper/
├── docs/                # Archivos de documentación extraídos
├── scraper.py           # Script principal de scraping
├── requirements.txt     # Dependencias del proyecto
└── README.md            # Este archivo
```

## Configuración

- Puedes definir el número de hilos para el scraping con la variable de entorno `MAX_WORKERS`.
- El contenido se guarda en la carpeta `docs/`.

## Ejemplo de salida

Puedes ver un ejemplo de los archivos generados [aquí](enlace-a-ejemplo).

## Licencia

Este proyecto se distribuye bajo la licencia GNU General Public License v3.0.

## Contribuir

Este proyecto es de código abierto y las contribuciones son bienvenidas. Si deseas contribuir, por favor:

1. Forkea el repositorio.
2. Crea tu rama de características (`git checkout -b feature/AmazingFeature`).
3. Realiza tus cambios y confirma tus cambios (`git commit -m 'Add some AmazingFeature'`).
4. Sube tus cambios a la rama (`git push origin feature/AmazingFeature`).
5. Abre una Pull Request.

## Soporte

Si tienes algún problema o pregunta, por favor abre un issue en el repositorio o contacta al mantenedor del proyecto.