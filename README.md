# Priorización de zonas para conservación ecológica en paisajes agrícolas del sur occidente colombiano

Este proyecto tiene como objetivo desarrollar un análisis de aptitud ecológica en paisajes productivos del sur occidente colombiano, específicamente en los departamentos del Cauca y Valle del Cauca. La investigación se enfoca en identificar y priorizar zonas dentro de territorios agrícolas que presentan un alto potencial para la conservación de la biodiversidad y la conectividad ecológica.

A través de la integración de variables biofísicas, ambientales y de uso del suelo, el proyecto aplica herramientas de análisis espacial en entornos SIG (Sistemas de Información Geográfica) y programación en Python para construir un índice espacial que represente el valor relativo de conservación dentro del paisaje agrícola. Este índice se genera con base en criterios como la cercanía a áreas protegidas, la conectividad con fragmentos de cobertura vegetal natural, la pendiente del terreno, la cobertura boscosa existente, el uso actual del suelo, y la proximidad a fuentes hídricas.

El enfoque metodológico busca apoyar procesos de planificación territorial sostenible, conservación en matrices productivas, y restauración ecológica en zonas estratégicas. La aplicación del análisis se realiza por medio de scripts y notebooks en Python, lo que garantiza la trazabilidad, reproducibilidad y escalabilidad del proceso.

# Objetivos

- Analizar variables ecológicas y productivas del territorio.
- Generar un índice de prioridad para conservación.
- Visualizar zonas clave mediante mapas SIG.

# Estructura del repositorio

- `notebooks/`: notebooks para análisis y visualización.
- `src/`: scripts Python con funciones reutilizables.
- `results/`: mapas y gráficos generados.
- `docs/`: bibliografía y notas técnicas.
- `presentation/`: presentación final del proyecto.

# Requisitos

Este proyecto fue desarrollado en Python y requiere la instalación de varias librerías para el manejo
Para instalar todas las dependencias necesarias, se recomienda ejecutar el siguiente código desde la raíz del proyecto, donde se encuentra el archivo `requirements.txt`:

bash
pip install -r requirements.txt
geopandas
rasterio
shapely
matplotlib
pandas
numpy
folium
