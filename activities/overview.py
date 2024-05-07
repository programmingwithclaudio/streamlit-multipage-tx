import streamlit as st
import pandas as pd
import plotly.express as px

st.header("Análisis de Temperaturas")

# Cargar los datos
data = pd.read_parquet("public/datasets/temperature.parquet")

# Convertir la columna 'Fecha' a formato de fecha
data['Fecha'] = pd.to_datetime(data['Fecha'], format='%Y-%m-%d')

# Extraer el año y el mes de la columna 'Fecha'
data['Anio'] = data['Fecha'].dt.year.astype(int)  # Convertir 'Anio' a tipo entero
data['Mes'] = data['Fecha'].dt.month  # Obtener el número del mes


# Agrupar por año y por mes y calcular la temperatura promedio para cada grupo
temperatura_promedio = data.groupby(['Anio', 'Mes'])['temperature_2m'].mean().reset_index()

# Ordenar los años y los meses de manera ascendente
temperatura_promedio = temperatura_promedio.sort_values(by=['Anio', 'Mes'])

# Eliminar el índice del DataFrame antes de mostrarlo
temperatura_promedio_reset = temperatura_promedio.reset_index(drop=True)
# Mostrar la tabla
st.subheader("Tabla de Temperaturas Promedio")
st.write(temperatura_promedio_reset)


# Widget para seleccionar los años a mostrar en el gráfico
anios_unicos = temperatura_promedio['Anio'].unique()
selected_anios = st.multiselect("Seleccionar años:", anios_unicos, default=anios_unicos)

# Filtrar los datos por los años seleccionados
filtered_data = temperatura_promedio[temperatura_promedio['Anio'].isin(selected_anios)]

# Convertir los datos a un formato adecuado para el gráfico temporal
data_plot = filtered_data.pivot(index='Mes', columns='Anio', values='temperature_2m')

# Mostrar el gráfico temporal
st.subheader("Gráfico Temporal de Temperaturas Promedio")
st.line_chart(data_plot)
