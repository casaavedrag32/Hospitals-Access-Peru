# Hospitals-Access-Peru

## Filtrado de hospitales en funcionamiento

Para los análisis y mapas, se consideraron solo hospitales públicos en funcionamiento.  
Los criterios aplicados fueron:

1. **Estado**: `"ACTIVADO"`  
2. **Condición**: `"EN FUNCIONAMIENTO"`  
3. **Institución**: que pertenezca a `"MINSA"` o al `"GOBIERNO"` (buscando coincidencias en el nombre de la institución)

En código (Python/GeoPandas) se implementa así:

```python
hospitals_public = hospitals[
    (hospitals["Estado"].str.upper() == "ACTIVADO") &
    (hospitals["Condición"].str.upper() == "EN FUNCIONAMIENTO") &
    (hospitals["Institución"].str.contains("GOBIERNO|MINSA", case=False, na=False))
].copy()
