import streamlit as st
from streamlit_folium import st_folium

import geopandas as gpd
from geopandas import GeoSeries
from shapely.geometry import Point, LineString

import folium
from folium import Marker, GeoJson
from folium.plugins import MarkerCluster

import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import matplotlib.pyplot as plt 
import chardet

# ---------------------------
# Configuración
# ---------------------------
st.set_page_config(page_title="Hospital Access Peru", layout="wide")

# ---------------------------
# Carga de datos (ajusta paths)
# ---------------------------
districts = gpd.read_file(r'data/shape_file/DISTRITOS.shp').to_crs("EPSG:4326")
districts["UBIGEO"] = districts["IDDIST"].astype(str)

hospitals = pd.read_csv("data/hospitals.csv", encoding = "latin1")
hospitals["UBIGEO"] = hospitals["UBIGEO"].astype(str)
hospitals = hospitals.dropna(subset=["NORTE", "ESTE"])
hospitals_gdf = gpd.GeoDataFrame(
    hospitals,
    geometry=gpd.points_from_xy(hospitals["NORTE"], hospitals["ESTE"]),
    crs="EPSG:4326"
)
hospitals_gdf["UBIGEO"] = hospitals_gdf["UBIGEO"].astype(str)

popcenters = gpd.read_file(r'data/shape_file/CCPP_IGN100K.shp').to_crs("EPSG:4326")
popcenters = popcenters.dropna(subset=["X", "Y"])
pop_centers_gdf = gpd.GeoDataFrame(
    popcenters,
    geometry=gpd.points_from_xy(popcenters["X"], popcenters["Y"]),
    crs="EPSG:4326"
)

# ---------------------------
# Tabs principales
# ---------------------------
tab1, tab2, tab3 = st.tabs(["🗂️ Descripción de Datos", "🗺️ Mapas Estáticos", "🌍 Mapas dinámicos"])

# ---------------------------
# Tab 1
# ---------------------------
with tab1:
    st.markdown(
        """
        # 🗂️ Data Description

        **Unidad de análisis:** hospitales públicos operativos en Perú.  
        **Fuentes de datos:**  
        - MINSA – IPRESS (subset de establecimientos operativos).  
        - Centros Poblados – IGN/INEI.  

        **Reglas de filtrado:**  
        - Solo hospitales operativos (`Estado = ACTIVADO`, `Condición = EN FUNCIONAMIENTO`).  
        - Coordenadas válidas (`ESTE`, `NORTE` no nulos).
        """
    )

    # Filtrar hospitales operativos con coordenadas
    hospitals_filtered = hospitals.dropna(subset=["NORTE", "ESTE"])
    hospitals_operativos = hospitals_filtered[
        (hospitals_filtered["Estado"] == "ACTIVADO") & 
        (hospitals_filtered["Condición"] == "EN FUNCIONAMIENTO")
    ]

    # Totales
    total_hospitals = hospitals_filtered.shape[0]
    total_public_hospitals = hospitals_operativos.shape[0]

    # Columnas para mostrar los números
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Total de hospitales")
        st.markdown(f"<h1 style='text-align:center;color:blue;'>{total_hospitals}</h1>", unsafe_allow_html=True)

    with col2:
        st.markdown("### Total de hospitales públicos operativos")
        st.markdown(f"<h1 style='text-align:center;color:green;'>{total_public_hospitals}</h1>", unsafe_allow_html=True)

# ---------------------------
# Tab 2
# ---------------------------
with tab2:
    
    # Resumen por departamento
    dept_summary = hospitals.groupby("Departamento").size().reset_index(name="Total_Hospitals")
    dept_summary = dept_summary.sort_values(by="Total_Hospitals", ascending=False)

    st.write("### Tabla resumen (Departamentos con más hospitales)")
    st.dataframe(dept_summary)

    # Bar chart
    fig, ax = plt.subplots(figsize=(8, 5))
    dept_summary.plot(kind="bar", x="Departamento", y="Total_Hospitals", ax=ax, legend=False)
    plt.title("Total de hospitales por departamento")
    plt.ylabel("Número de hospitales")
    plt.xticks(rotation=90)
    st.pyplot(fig)

    # Map
    st.image("output/mapa5.png", caption="Mapa de hospitales en el Perú", use_column_width=True)



# ---------------------------
# Tab 3
# ---------------------------
with tab3:
   
    st.write("### Proximity Map")

    with open("output/proximity_combinado.html", "r", encoding="utf-8") as f:
        html_lima_max = f.read()
    st.components.v1.html(html_lima_max, height=500, scrolling=True)