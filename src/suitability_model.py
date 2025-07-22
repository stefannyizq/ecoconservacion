import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point, MultiPolygon
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

### 1. Cargar Capas Preprocesadas ###
def cargar_capas(rutas):
    capas = {}
    for clave, ruta in rutas.items():
        capas[clave] = gpd.read_file(ruta)
    return capas

### 2. Generar Grilla de Puntos ###
def generar_grilla(limite_gdf, resolucion=5000):
    union = limite_gdf.geometry.unary_union
    xmin, ymin, xmax, ymax = union.bounds
    x_coords = np.arange(xmin, xmax, resolucion)
    y_coords = np.arange(ymin, ymax, resolucion)
    grid_points = [Point(x, y) for x in x_coords for y in y_coords]
    grid_gdf = gpd.GeoDataFrame(geometry=grid_points, crs=limite_gdf.crs)
    grid_gdf = grid_gdf[grid_gdf.geometry.within(union)]
    return grid_gdf

### 3. Calcular Pesos con AHP ###
def calcular_ahp(criterios, comparaciones):
    import numpy as np
    import pandas as pd
    n = len(criterios)
    # Si 'comparaciones' no es un numpy array, conviértelo
    matriz = np.array(comparaciones, dtype=float)

    # Llenar la triangular inferior
    for i in range(n):
        for j in range(i+1, n):
            matriz[j, i] = 1 / matriz[i, j]

    suma_col = matriz.sum(axis=0)
    matriz_norm = matriz / suma_col
    pesos = matriz_norm.mean(axis=1)

    # Consistencia
    AW = np.dot(matriz, pesos)
    lambda_max = (AW / pesos).mean()
    IC = (lambda_max - n) / (n - 1)
    RI_dict = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
    RI = RI_dict[n]
    CR = IC / RI if RI > 0 else 0

    df_matriz = pd.DataFrame(matriz, index=criterios, columns=criterios)
    df_pesos = pd.DataFrame({'Criterio': criterios, 'Peso AHP': pesos.round(4)})

    return pesos, CR, IC, lambda_max, df_matriz, df_pesos

### 4. Calcular variables espaciales (distancias, clasificaciones, etc.) ###
def calcular_variables(grid_gdf, capas, pendiente_valores, uso_suelo_valores):
    # Unión geométrica para distancias
    grid_gdf = grid_gdf.copy()
    grid_gdf["dist_vias"] = grid_gdf.geometry.apply(lambda p: p.distance(capas["vias"].geometry.unary_union))
    grid_gdf["dist_vias_norm"] = 1 - (grid_gdf["dist_vias"] / grid_gdf["dist_vias"].max())
    grid_gdf["dist_protegidas"] = grid_gdf.geometry.apply(lambda p: p.distance(capas["proteccion"].geometry.unary_union))
    grid_gdf["dist_protegidas_norm"] = 1 - (grid_gdf["dist_protegidas"] / grid_gdf["dist_protegidas"].max())
    grid_gdf["dist_hidro"] = grid_gdf.geometry.apply(lambda p: p.distance(capas["hidrografia"].geometry.unary_union))
    grid_gdf["dist_hidro_norm"] = 1 - (grid_gdf["dist_hidro"] / grid_gdf["dist_hidro"].max())

    # Pendiente
    capas["pendiente"]["pendiente_valor"] = capas["pendiente"]["RANGO_PEND"].map(pendiente_valores)
    grid_gdf = gpd.sjoin_nearest(
        grid_gdf,
        capas["pendiente"][["geometry", "pendiente_valor"]],
        how='left',
        max_distance=1000
    )
    grid_gdf["pendiente_norm"] = grid_gdf["pendiente_valor"]

    # Uso del suelo
    capas["suelo"]["uso_idoneidad"] = capas["suelo"]["ID_Uso_Sue"].astype(int).map(uso_suelo_valores).fillna(0)
    grid_gdf = gpd.sjoin_nearest(
        grid_gdf,
        capas["suelo"][["geometry", "uso_idoneidad"]],
        how='left',
        max_distance=1000
    )
    grid_gdf["uso_suelo_norm"] = grid_gdf["uso_idoneidad"]

    return grid_gdf

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def calcular_indice_idoneidad(grid_gdf, pesos):
    """Calcula el índice de idoneidad (II) usando los pesos dados."""
    grid_gdf = grid_gdf.copy()
    grid_gdf["II"] = (
        pesos[0] * grid_gdf["dist_vias_norm"] +
        pesos[1] * grid_gdf["dist_protegidas_norm"] +
        pesos[2] * grid_gdf["dist_hidro_norm"] +
        pesos[3] * grid_gdf["pendiente_norm"] +
        pesos[4] * grid_gdf["uso_idoneidad"]
    )
    return grid_gdf

def clasificar_idoneidad(valor):
    """Clasifica un valor de II en una categoría."""
    if valor < 0.2:
        return "Muy baja"
    elif valor < 0.4:
        return "Baja"
    elif valor < 0.6:
        return "Media"
    elif valor < 0.8:
        return "Alta"
    else:
        return "Muy alta"

def graficar_idoneidad(grid_gdf, columna="II"):
    """Genera un mapa del índice de idoneidad clasificado por colores."""
    grid_gdf = grid_gdf.copy()
    grid_gdf["label"] = grid_gdf[columna].apply(clasificar_idoneidad)
    color_map = {
        "Muy baja": "#d73027",
        "Baja": "#fc8d59",
        "Media": "#fee08b",
        "Alta": "#d9ef8b",
        "Muy alta": "#1a9850"
    }
    grid_gdf["color"] = grid_gdf["label"].map(color_map)
    legend_patches = [
        mpatches.Patch(color=color_map[cat], label=cat) 
        for cat in ["Muy baja", "Baja", "Media", "Alta", "Muy alta"]
    ]
    fig, ax = plt.subplots(figsize=(10, 8))
    grid_gdf.plot(ax=ax, color=grid_gdf['color'], edgecolor='gray', linewidth=0.1, markersize=18)
    plt.legend(
        handles=legend_patches,
        title="Índice de Idoneidad",
        loc='center left',
        bbox_to_anchor=(1.05, 0.5), 
        frameon=True
    )
    ax.set_title("Mapa del Índice de Idoneidad (II)", fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def zonas_prioritarias_por_percentil(grid_gdf, columna="II", percentil=0.75, buffer_m=None, export_path=None):
    """
    Identifica, grafica y exporta zonas prioritarias (puntos o buffers) según percentil.
    Args:
        grid_gdf: GeoDataFrame de puntos.
        columna: Campo índice.
        percentil: Valor percentil.
        buffer_m: Radio de buffer (en unidades CRS, por ejemplo 500 si es metros). Si None, exporta puntos.
        export_path: Ruta para exportar el shapefile/geojson. Si None, no exporta.
    Returns:
        zonas_gdf: GeoDataFrame de zonas prioritarias.
        umbral: valor umbral usado.
    """
    umbral = grid_gdf[columna].quantile(percentil)
    zonas_gdf = grid_gdf[grid_gdf[columna] >= umbral].copy()
    
    # Si quieres buffers para visualización/área:
    if buffer_m is not None:
        zonas_gdf["geometry"] = zonas_gdf.geometry.buffer(buffer_m)

    fig, ax = plt.subplots(figsize=(10, 8))
    grid_gdf.plot(ax=ax, color="lightgrey", edgecolor='white', linewidth=0.1, markersize=12)
    if not zonas_gdf.empty:
        zonas_gdf.plot(ax=ax, color="green", edgecolor='black', linewidth=0.6, alpha=0.8, markersize=18)
    ax.set_title(f"Zonas Prioritarias según {columna} (≥ {umbral:.2f})", fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    # Exportar si se desea
    if export_path:
        zonas_gdf.to_file(export_path)
        print(f"Zonas prioritarias exportadas a: {export_path}")

    return zonas_gdf, umbral

def resumen_percentiles(grid_gdf, columna="II", percentiles=[0.25, 0.5, 0.75, 0.9, 0.95]):
    """Imprime un resumen estadístico con percentiles clave del índice de idoneidad."""
    print(grid_gdf[columna].describe(percentiles=percentiles))

