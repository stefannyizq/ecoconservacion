# src/visualization_tools.py

import matplotlib.pyplot as plt

def plot_layers(gdf_list, labels=None, colors=None, title="Capas superpuestas", ax=None):
    """
    Visualiza varias capas GeoDataFrame sobrepuestas.
    Args:
        gdf_list (list): Lista de GeoDataFrames a graficar.
        labels (list): Nombres de cada capa (opcional).
        colors (list): Colores para cada capa (opcional).
        title (str): Título del gráfico.
        ax: Eje de Matplotlib (opcional).
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 10))
    for i, gdf in enumerate(gdf_list):
        color = None if colors is None else colors[i]
        label = None if labels is None else labels[i]
        gdf.plot(ax=ax, color=color, edgecolor='black', label=label)
    ax.set_title(title)
    ax.legend()
    ax.set_xlabel("Coordenada X (Este)")
    ax.set_ylabel("Coordenada Y (Norte)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_grid(grid_gdf, base_gdf=None, ax=None, color='dodgerblue', markersize=3, alpha=0.7, title="Grilla regular de puntos"):
    """
    Visualiza una grilla de puntos sobre un GeoDataFrame base.
    Args:
        grid_gdf: GeoDataFrame con puntos de grilla.
        base_gdf: GeoDataFrame de fondo (ej: límite).
        ax: Eje de Matplotlib (opcional).
        color: Color de los puntos.
        markersize: Tamaño de los puntos.
        alpha: Transparencia.
        title: Título del gráfico.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 10))
    if base_gdf is not None:
        base_gdf.boundary.plot(ax=ax, edgecolor='black')
    grid_gdf.plot(ax=ax, color=color, markersize=markersize, alpha=alpha)
    ax.set_title(title)
    ax.set_xlabel("Coordenada X (Este)")
    ax.set_ylabel("Coordenada Y (Norte)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_suitability_map(gdf, column="idoneidad", cmap='YlGn', title="Mapa de idoneidad", ax=None):
    """
    Visualiza un mapa de idoneidad o similar.
    Args:
        gdf: GeoDataFrame con columna de idoneidad.
        column: Nombre de la columna a mapear.
        cmap: Colormap de Matplotlib.
        title: Título del gráfico.
        ax: Eje de Matplotlib (opcional).
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 10))
    gdf.plot(column=column, cmap=cmap, ax=ax, legend=True)
    ax.set_title(title)
    ax.set_xlabel("Coordenada X (Este)")
    ax.set_ylabel("Coordenada Y (Norte)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
