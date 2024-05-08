import streamlit as st
import pandas as pd
from glob import glob
import pandas as pd
import re
import plotly.express as px
import matplotlib.pyplot as plt
from PIL import Image


st.header("Análisis de Emisiones de Carbono CO2 por Vehículo de combustible")

ruta_archivos = "public/datasets/fuel_consumption_*.parquet"
datos_cargados = funcs.cargar_datos(ruta_archivos)
datos_procesados = funcs.etl_transformacion(datos_cargados)

# Widget para seleccionar el tipo de gráfico para el gráfico principal
tipo_grafico_principal = st.selectbox("Seleccione el tipo de gráfico para el gráfico principal:",
                                      options=["Histograma", "Gráfico de Caja", "Gráfico de Violín", "Gráfico de Densidad"])

# Widget para seleccionar el tipo de gráfico para el gráfico adicional
tipo_grafico_adicional = st.selectbox("Seleccione el tipo de gráfico para el gráfico adicional:",
                                      options=["Histograma", "Gráfico de Caja", "Gráfico de Violín", "Gráfico de Densidad"])
# Organizar los gráficos uno al lado del otro
st.write("### Gráficos")

# Configurar el layout de las columnas
col1, col2 = st.columns(2)

# Mostrar el gráfico principal seleccionado
with col1:
    st.write("#### Distribución de CO2 Emissions")
    if tipo_grafico_principal == "Histograma":
        st.plotly_chart(px.histogram(datos_procesados, x="co2_emissions_g_km", title="Distribución de CO2 Emissions"), use_container_width=True)
    elif tipo_grafico_principal == "Gráfico de Caja":
        st.plotly_chart(px.box(datos_procesados, y="co2_emissions_g_km", title="Gráfico de Caja de CO2 Emissions"), use_container_width=True)
    elif tipo_grafico_principal == "Gráfico de Violín":
        st.plotly_chart(px.violin(datos_procesados, y="co2_emissions_g_km", title="Gráfico de Violín de CO2 Emissions"), use_container_width=True)
    elif tipo_grafico_principal == "Gráfico de Densidad":
        st.plotly_chart(px.density_heatmap(datos_procesados, x="co2_emissions_g_km", y="engine_size_l", 
                                           title="Gráfico de Densidad de CO2 Emissions vs Engine Size"), use_container_width=True)

# Mostrar el gráfico adicional seleccionado
with col2:
    st.write("#### Distribución de Combined Fuel Consumption")
    if tipo_grafico_adicional == "Histograma":
        st.plotly_chart(px.histogram(datos_procesados, x="combined_l_100_km", title="Distribución de Combined Fuel Consumption"), use_container_width=True)
    elif tipo_grafico_adicional == "Gráfico de Caja":
        st.plotly_chart(px.box(datos_procesados, y="combined_l_100_km", title="Gráfico de Caja de Combined Fuel Consumption"), use_container_width=True)
    elif tipo_grafico_adicional == "Gráfico de Violín":
        st.plotly_chart(px.violin(datos_procesados, y="combined_l_100_km", title="Gráfico de Violín de Combined Fuel Consumption"), use_container_width=True)
    elif tipo_grafico_adicional == "Gráfico de Densidad":
        st.plotly_chart(px.density_heatmap(datos_procesados, x="combined_l_100_km", y="engine_size_l", 
                                           title="Gráfico de Densidad de Combined Fuel Consumption vs Engine Size"), use_container_width=True)
        
# Calcular el número de vehículos por marca
#vehiculos_por_marca = datos_procesados["make"].value_counts()

# # Crear el gráfico de barras con Matplotlib
# fig, ax = plt.subplots(figsize=(10, 6))
# ax.bar(vehiculos_por_marca.index, vehiculos_por_marca.values)
# ax.set_title("Número de vehículos por marca")
# ax.set_xlabel("Marca")
# ax.set_ylabel("Número de vehículos")
# ax.set_xticklabels(vehiculos_por_marca.index, rotation=45, ha='right')
# plt.tight_layout()

# # Mostrar el gráfico en Streamlit
# st.pyplot(fig)

# Calcular el número de vehículos por marca
vehiculos_por_marca = datos_procesados["make"].value_counts().reset_index()
vehiculos_por_marca.columns = ["Marca", "Cantidad"]

# Calcular el número de vehículos por marca
vehiculos_por_marca = datos_procesados["make"].value_counts().reset_index()
vehiculos_por_marca.columns = ["Marca", "Cantidad"]

# Crear el gráfico de barras con Plotly Express y especificar el ancho
fig = px.bar(vehiculos_por_marca, x="Marca", y="Cantidad", title="Número de vehículos por marca", width=700,
             color="Cantidad", color_continuous_scale=px.colors.sequential.Viridis)

# Agregar el gráfico de barras dentro del mismo contenedor y centrarlo
with st.container():
    st.write("---")
    #st.header("Cantidad de vehículos por marca")
    st.write("##")
    # Agregar el gráfico y centrarlo
    st.plotly_chart(fig, use_container_width=True)
    # Aplicar estilos CSS para centrar el gráfico
    st.markdown("<style>div[data-testid='stPlotlyChart'] {margin: 0 auto;}</style>", unsafe_allow_html=True)




# Calcular el número de vehículos por marca
vehiculos_por_marca = datos_procesados["transmission"].value_counts().reset_index()
vehiculos_por_marca.columns = ["Marca", "Cantidad"]

# Calcular el número de vehículos por marca
vehiculos_por_marca = datos_procesados["transmission"].value_counts().reset_index()
vehiculos_por_marca.columns = ["Marca", "Cantidad"]

# Gráfico de caja para visualizar la distribución de co2_emissions_g_km por tipo de transmisión
fig3 = px.box(datos_procesados, x="transmission", y="co2_emissions_g_km", title="Distribución de CO2 Emissions por tipo de transmisión",
              color="transmission")

# Agregar el gráfico de caja dentro del mismo contenedor y centrarlo
with st.container():
    st.write("---")
    #st.header("Emisiones de CO2 por Tipo de Carfa")
    st.write("##")
    # Agregar el gráfico y centrarlo
    st.plotly_chart(fig3, use_container_width=True)
    # Aplicar estilos CSS para centrar el gráfico
    st.markdown("<style>div[data-testid='stPlotlyChart'] {margin: 0 auto;}</style>", unsafe_allow_html=True)


# Agrupar por marca y calcular el promedio del consumo combinado de combustible
consumo_promedio = datos_procesados.groupby('make')['combined_l_100_km'].mean().reset_index()

# Ordenar las marcas por consumo promedio de menor a mayor
consumo_promedio_sorted = consumo_promedio.sort_values(by='combined_l_100_km')

# Crear el gráfico de barras con Plotly Express y especificar la escala de colores
fig4 = px.bar(consumo_promedio_sorted, x='make', y='combined_l_100_km', 
             title='Consumo Promedio de Combustible por Marca', 
             labels={'make': 'Marca', 'combined_l_100_km': 'Consumo de Combustible (l/100km)'},
             color='combined_l_100_km', color_continuous_scale='Magma')  # Especificar la escala de colores


# Agregar el gráfico de caja dentro del mismo contenedor y centrarlo
with st.container():
    st.write("---")
    st.write("##")
    # Agregar el gráfico y centrarlo
    st.plotly_chart(fig4, use_container_width=True)
    # Aplicar estilos CSS para centrar el gráfico
    st.markdown("<style>div[data-testid='stPlotlyChart'] {margin: 0 auto;}</style>", unsafe_allow_html=True)



# # Definir las variables para el eje y
# variable_y = "co2_emissions_g_km"

# # Widget multiselect para seleccionar las variables para el eje x
# variables_x = st.multiselect("Selecciona las variables para el eje x:", options=datos_procesados.columns)

# # Crear un gráfico de dispersión para cada variable seleccionada
# for variable_x in variables_x:
#     # Crear el gráfico de dispersión con Plotly Express
#     fig_scatter = px.scatter(datos_procesados, x=variable_x, y=variable_y, title=f"Scatter Plot: {variable_x} vs {variable_y}")

#     # Mostrar el gráfico en Streamlit
#     st.plotly_chart(fig_scatter)


# # Definir las variables para el eje y
# variable_y = "co2_emissions_g_km"

# # Widget multiselect para seleccionar las variables para el eje x
# variables_x = st.multiselect("Selecciona las variables para el eje x:", options=datos_procesados.columns)

# # Dividir el espacio en columnas según el número de variables seleccionadas
# num_cols = len(variables_x) if len(variables_x) <= 4 else 4
# cols = st.columns(num_cols)

# # Tamaño deseado para los gráficos
# fig_width = 600
# fig_height = 500

# # Crear un gráfico de dispersión para cada variable seleccionada
# for i, variable_x in enumerate(variables_x):
#     # Crear el gráfico de dispersión con Plotly Express
#     fig_scatter = px.scatter(datos_procesados, x=variable_x, y=variable_y, title=f"Scatter Plot {i+1}: {variable_x} vs {variable_y}", color=variable_x, color_continuous_scale='Viridis', width=fig_width, height=fig_height)

#     # Mostrar el gráfico en la columna correspondiente
#     with cols[i % num_cols]:
#         st.plotly_chart(fig_scatter, use_container_width=True)

# Definir las variables para el eje y
variable_y = "co2_emissions_g_km"

# Widget multiselect para seleccionar las variables para el eje x
variables_x = st.multiselect("Selecciona las variables para el eje x:", options=datos_procesados.columns)

# Dividir el espacio en columnas y filas según el número de variables seleccionadas
num_cols = 2  # Número de columnas (dos gráficos por columna)
num_filas = (len(variables_x) + 1) // 2  # Número de filas necesarias

# Crear una cuadrícula de columnas y filas
cols = st.columns(num_cols)
rows = [st.container() for _ in range(num_filas)]

# Tamaño deseado para los gráficos
fig_width = 600
fig_height = 500

# Crear un gráfico de dispersión para cada variable seleccionada
for i, variable_x in enumerate(variables_x):
    # Crear el gráfico de dispersión con Plotly Express
    fig_scatter = px.scatter(datos_procesados, x=variable_x, y=variable_y, title=f"Scatter Plot {i+1}: {variable_x} vs {variable_y}", color=variable_x, color_continuous_scale='Viridis', width=fig_width, height=fig_height)

    # Mostrar el gráfico en la fila y columna correspondiente
    with rows[i // 2]:
        with cols[i % num_cols]:
            st.plotly_chart(fig_scatter, use_container_width=True)


datos_dummies = funcs.procesar_dummies(datos_procesados)
datos_corr = datos_dummies[['fuel_type_Premium_gasoline', 'fuel_type_Regular_gasoline',
       'highway_l_100_km', 'city_l_100_km',
       'transmission_Variable_continuamente',
       'vehicle_class_c_pickup_truck_small', 'engine_size_l', 'cylinders',
       'vehicle_class_c_fullsize', 'vehicle_class_c_midsize',
       'vehicle_class_c_sport_utility_vehicle_standard']]
# Calcular la matriz de correlación
correlation_matrix = datos_corr.corr()
# Crear el gráfico de correlación con Plotly Express
fig_corr = px.imshow(correlation_matrix,
                     labels=dict(color="Correlación"),
                     x=datos_corr.columns,
                     y=datos_corr.columns,
                     title="Matriz de Correlación",
                     width=800,  # Ancho del gráfico
                     height=800)  # Alto del gráfico

# Agregar el gráfico de caja dentro del mismo contenedor y centrarlo
with st.container():
    st.write("---")
    st.write("##")
    # Agregar el gráfico y centrarlo
    st.plotly_chart(fig_corr, use_container_width=True)
    # Aplicar estilos CSS para centrar el gráfico y ajustar el tamaño de la fuente
    st.markdown("""
    <style>
    div[data-testid='stPlotlyChart'] {
        margin: 0 auto;
    }
    div[data-testid='stPlotlyChart'] .plot-container .svg-container .main-svg text {
        font-size: 10px;
    }
    </style>
    """, unsafe_allow_html=True)


