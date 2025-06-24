import folium

def plot_folium_map(gdf, column, map_center, zoom_start=10):
    """
    Crea un mapa interactivo con folium mostrando el índice de aptitud.
        Parámetros:
        gdf: GeoDataFrame con geometría.
        column: nombre de la columna a visualizar.
        map_center: coordenadas [lat, lon] del centro del mapa.
    """
    fmap = folium.Map(location=map_center, zoom_start=zoom_start)
    folium.GeoJson(
        gdf,
        name='Aptitud',
        style_function=lambda x: {
            'fillColor': '#blue',
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.6
        },
        tooltip=folium.GeoJsonTooltip(fields=[column])
    ).add_to(fmap)
    return fmap
