def weighted_linear_combination(gdf, weights, columns):
    """
    Calcula un índice de aptitud ecológica usando combinación lineal ponderada.
    
    Parámetros:
        gdf: GeoDataFrame con columnas normalizadas.
        weights: lista de pesos (suman 1).
        columns: columnas normalizadas a combinar.

    Retorna:
        GeoDataFrame con nueva columna 'suitability_index'.
    """
    if len(weights) != len(columns):
        raise ValueError("Número de pesos debe coincidir con el número de columnas")
    
    gdf['suitability_index'] = sum(w * gdf[col] for w, col in zip(weights, columns))
    return gdf
