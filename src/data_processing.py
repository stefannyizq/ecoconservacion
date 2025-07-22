# src/data_preparation.py
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx
import os

def leer_limite_valle(ruta_municipios, cod_dpto='76'):
    gdf_mun = gpd.read_file(ruta_municipios)
    valle = gdf_mun[gdf_mun['DPTO_CCDGO'] == cod_dpto]
    valle_diss = valle.dissolve(by='DPTO_CCDGO')
    return valle_diss

def construir_rutas_capas():
    rutas = {
        # Límite departamental procesado y guardado en tu flujo
        "limite_valle": "../data/limites/limite_valle.shp",

        # Capas originales según tus carpetas reales (usa / siempre)
        "vias": "/home/p2/Programacion_sig2/ecoconservaion-suroccidente/Datos/catografiabasica_valle/CBTR_VIA.shp",
        "areas_protegidas": "/home/p2/Programacion_sig2/ecoconservaion-suroccidente/Datos/areas_protegidas/runap_-_Registro_Unico_Nacional_AP.shp",
        "curvas_nivel": "/home/p2/Programacion_sig2/ecoconservaion-suroccidente/Datos/catografiabasica_valle/CBRL_CURVAS.shp",
        "pendientes": "/home/p2/Programacion_sig2/ecoconservaion-suroccidente/Datos/suelo_valle/SUELO_SHP/CBRL_PENDIENTES_CN100.shp",
        "suelo": "/home/p2/Programacion_sig2/ecoconservaion-suroccidente/Datos/suelo_valle/SUELO_SHP/SLCS_COBERTURA_SUELO.shp",
        "hidrografia": "/home/p2/Programacion_sig2/ecoconservaion-suroccidente/Datos/hidrologia_valle/AGUA_SHP/SP_CUERPO_AGUA.shp",
    }
    return rutas



def leer_shapefile(ruta):
    return gpd.read_file(ruta)

def guardar_shapefile(gdf, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    gdf.to_file(output_path)

def recortar_y_reproyectar(capa, limite, epsg=3116):
    if capa.crs != limite.crs:
        capa = capa.to_crs(limite.crs)
    recorte = gpd.overlay(capa, limite, how='intersection')
    return recorte.to_crs(epsg)

def redondear_columnas_area(gdf, area_col='AREA', length_col='Shape_leng'):
    gdf[area_col] = (gdf[area_col]/1000).round(0)
    if length_col in gdf.columns:
        gdf[length_col] = gdf[length_col].round(0)
    return gdf

def validar_y_exportar(gdf, output_path):
    if not gdf.is_valid.all():
        gdf['geometry'] = gdf['geometry'].buffer(0)
    gdf.to_file(output_path)

