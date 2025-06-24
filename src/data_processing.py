import geopandas as gpd
import pandas as pd
import os

def load_vector_data(filepath):
    """
    Carga un archivo vectorial (como .shp o .geojson) y lo devuelve como un GeoDataFrame.
    """
    return gpd.read_file(filepath)

def clip_layer(layer, boundary):
    """
    Recorta una capa geoespacial según una capa límite (boundary).
    """
    return gpd.overlay(layer, boundary, how='intersection')

def merge_layers(layers):
    """
    Une múltiples GeoDataFrames en una sola capa.
    """
    return gpd.GeoDataFrame(pd.concat(layers, ignore_index=True))

def normalize_column(gdf, column):
    """
    Normaliza los valores de una columna en un GeoDataFrame entre 0 y 1.
    """
    min_val = gdf[column].min()
    max_val = gdf[column].max()
    gdf[column + '_norm'] = (gdf[column] - min_val) / (max_val - min_val)
    return gdf
