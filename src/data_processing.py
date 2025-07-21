# src/data_processing.py

import geopandas as gpd
from pathlib import Path

def load_shapefile(filepath):
    """
    Carga un shapefile como GeoDataFrame.
    Parámetros:
        filepath (str): Ruta al archivo .shp
    Retorna:
        gpd.GeoDataFrame
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {filepath}")
    return gpd.read_file(path)

def reproject_layer(gdf, epsg_code=3116):
    """
    Reproyecta un GeoDataFrame al sistema CRS especificado.
    Parámetros:
        gdf (GeoDataFrame): Capa de entrada
        epsg_code (int): Código EPSG de destino
    Retorna:
        GeoDataFrame reproyectado
    """
    return gdf.to_crs(epsg=epsg_code)

def clip_layer(layer, mask):
    """
    Recorta una capa geográfica usando otra capa como máscara.
    Parámetros:
        layer (GeoDataFrame): Capa a recortar
        mask (GeoDataFrame): Máscara (polígono)
    Retorna:
        GeoDataFrame recortado
    """
    return gpd.clip(layer, mask)
