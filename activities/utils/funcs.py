import re
import os
from glob import glob
import pandas as pd 
import pickle
import io
import pyarrow.parquet as pq
import streamlit as st
import toml

env_data = toml.load('env.toml')


def cargar_datos(ruta_archivos):
    """
    Carga los datos desde archivos .parquet en un DataFrame único.
    
    Args:
    - ruta_archivos (str): Ruta que sigue un patrón para encontrar archivos .parquet
    
    Returns:
    - pd.DataFrame: DataFrame que contiene los datos concatenados de todos los archivos.
    """
    # Obtener la lista de archivos .parquet que cumplen con el patrón
    files = glob(ruta_archivos)

    # Crear un diccionario para almacenar los DataFrames
    dfs = {}

    # Leer cada archivo y almacenar los DataFrames en el diccionario
    for file in files:
        # Obtener el nombre de la clave para el diccionario
        key = file.split('/')[-1].split('.')[0]  # Obtiene el nombre del archivo sin la extensión
        # Leer el archivo y almacenar el DataFrame en el diccionario
        dfs[key] = pd.read_parquet(file)

    # Concatenar los DataFrames en uno solo
    data_concatenated = pd.concat(dfs.values(), ignore_index=True)

    return data_concatenated

def limpiar_transmission(texto):
    """
    Limpia la columna 'transmission' eliminando los dígitos.
    
    Args:
    - texto (str): Texto a limpiar
    
    Returns:
    - str: Texto limpio
    """
    return re.sub(r'\d', '', texto)

def limpiar_datos(df):
    """
    Realiza la limpieza de datos en un DataFrame dado.
    
    Args:
    - df (pd.DataFrame): DataFrame a limpiar
    
    Returns:
    - pd.DataFrame: DataFrame limpio
    """
    # Limpiar caracteres y espacios en blanco de la columna 'vehicle_class'
    df['vehicle_class_c'] = df['vehicle_class'].str.replace(r'[^\w\s]', '').str.strip()
    df['vehicle_class_c'] = df['vehicle_class_c'].str.replace('-', '')
    df['vehicle_class_c'] = df['vehicle_class_c'].str.replace(':', '')
    df['vehicle_class_c'] = df['vehicle_class_c'].str.replace(' ', '_')
    df['vehicle_class_c'] = df['vehicle_class_c'].str.lower()    
    # Convertir la columna 'engine_size_l' a tipo float
    df['engine_size_l'] = df['engine_size_l'].astype(float)
    
    # Convertir las columnas de consumo de combustible a tipo float
    columnas_combustible = ['city_l_100_km', 'highway_l_100_km', 'combined_l_100_km']
    df[columnas_combustible] = df[columnas_combustible].astype(float)
    
    # Aplicar la función a cada elemento de la columna "transmission"
    df['transmission'] = df['transmission'].apply(limpiar_transmission)

    # Eliminar columnas 'model' y 'vehicle_class'
    columnas_drop = ['model','vehicle_class']
    df.drop(columns=columnas_drop, inplace=True)
    
    return df

def renombrar_transmision(df):
    """
    Renombra los valores de la columna 'transmission' en un DataFrame dado.
    
    Args:
    - df (pd.DataFrame): DataFrame a renombrar
    
    Returns:
    - pd.DataFrame: DataFrame con valores de 'transmission' renombrados
    """
    # Renombrar valores en la columna 'fuel_type'
    df['fuel_type'] = df['fuel_type'].replace({'X': 'Regular_gasoline', 'Z': 'Premium_gasoline'})
    df['fuel_type'] = df['fuel_type'].replace({'E': 'Other', 'D': 'Other', 'N': 'Other'})
    
    # Crear un diccionario de mapeo de etiquetas antiguas a nuevas
    mapeo_transmision = {
        'A': 'Automatico',
        'AM': 'Manual_automatizada',
        'AS': 'Automatico_cambioselectivo',
        'AV': 'Variable_continuamente',
        'M': 'Manual'
    }

    # Renombrar las etiquetas en la columna 'transmission'
    df['transmission'] = df['transmission'].map(mapeo_transmision)
    
    return df

def etl_transformacion(df):
    """
    Realiza el proceso de ETL (extracción, transformación y carga) en un DataFrame dado.
    
    Args:
    - df (pd.DataFrame): DataFrame a procesar
    
    Returns:
    - pd.DataFrame: DataFrame procesado
    """
    df_limpiados = limpiar_datos(df.copy())
    df_transformados = renombrar_transmision(df_limpiados.copy())
    return df_transformados

def procesar_dummies(registro):
    # Verificar si el input es un DataFrame o un diccionario (un solo registro)
    if isinstance(registro, pd.DataFrame):
        # DataFrame con un solo registro
        df_copy = registro.copy()
    elif isinstance(registro, dict):
        # Diccionario con un solo registro, lo convertimos a DataFrame
        df_copy = pd.DataFrame([registro])
    else:
        raise ValueError("El input debe ser un DataFrame o un diccionario")
    
    # Eliminar columnas no deseadas
    columnas_drop = ['make']  # Agrega aquí las columnas que deseas eliminar
    df_copy.drop(columns=columnas_drop, inplace=True)
    
    # Obtener dummies para las variables categóricas
    df_dummies = pd.get_dummies(df_copy, drop_first=False)
    
    # Reemplazar valores booleanos False por 0 y True por 1
    df_dummies = df_dummies * 1
    
    return df_dummies

# funcions script ml.py
# Función para cargar el modelo
def cargar_modelo(nombre_modelo):
    # Cargar la tabla Parquet
    table = pq.read_table(nombre_modelo)
    
    # Obtener los datos serializados del modelo de la tabla Parquet
    serialized_model = table.column('model_data')[0].as_py()
    
    # Deserializar el modelo
    modelo = pickle.loads(serialized_model)
    
    return modelo

# Definir la clase InputData para validar los datos de entrada
class InputData:
    def __init__(self, HoraRecogida, diaSemana, mes, Borough_id):
        self.HoraRecogida = HoraRecogida
        self.diaSemana = diaSemana
        self.mes = mes
        self.Borough_id = Borough_id

def predecir(modelo, data):
    # Extraer los valores de data
    hora_recogida = data.HoraRecogida
    diaSemana = data.diaSemana
    mes = data.mes
    borough_id = data.Borough_id

    # Crear un DataFrame con los valores extraídos
    input_data = pd.DataFrame({
        'HoraRecogida': [hora_recogida],
        'diaSemana': [diaSemana],
        'mes': [mes],
        'Borough_id': [borough_id]
    })

    # Convertir los datos de entrada a tipo float
    input_data = input_data.astype(float)

    # Realizar la predicción utilizando el modelo cargado desde el DataFrame
    prediction = modelo.predict(input_data)

    # Devolver la predicción como JSON
    return {"Probabilidad de conseguir pasajero": prediction.tolist()}

# page invertors.py

def calcular_rentabilidad_media(numero_vehiculos):

    # Cargar datos desde el archivo CSV
    file_path = 'public/datasets/electric_data.csv'
    electric_data = pd.read_csv(file_path)

    # Seleccionar los 10 autos eléctricos más rentables
    electric_data.sort_values(by=['Market Value ($)', 'Range (km)', 'City (kWh/100 km)'], ascending=[True, False, False], inplace=True)
    top_10_electricos = electric_data.head(10)

    # Mostrar la tabla con los datos de los 10 autos más rentables
    st.write("### Lista de los 10 autos más rentables:")
    st.write(top_10_electricos[['Make', 'Model', 'Market Value ($)', 'Range (km)', 'City (kWh/100 km)']])

    # Widget para ingresar el número de vehículos a comprar
    st.write("### Análisis para inversión en los 10 autos eléctricos más rentables:")
    numero_vehiculos_a_comprar = st.number_input("Ingrese el número de vehículos a comprar:", min_value=1, step=1, value=10)

    # Calcular la media de Market Value ($) de los 10 autos seleccionados
    media_market_value = top_10_electricos['Market Value ($)'].mean()

    # Calcular el monto total de la inversión
    inversion_total = media_market_value * numero_vehiculos_a_comprar

    # Calcular el costo medio por vehículo
    costo_medio_por_vehiculo = inversion_total / numero_vehiculos_a_comprar

    # Calcular el tiempo de retorno de la inversión en meses
    millas_dia_taxi = 80
    precio_milla_cobrada = 11
    costo_recarga_dia = 6
    tiempo_retorno_dias = inversion_total / ((precio_milla_cobrada - costo_recarga_dia) * millas_dia_taxi)
    tiempo_retorno_meses = tiempo_retorno_dias / 30

    # Redondear el tiempo de retorno de la inversión en meses
    tiempo_retorno_meses_redondeado = round(tiempo_retorno_meses, 2)

    # Mostrar resultados
    st.write("Número de vehículos a comprar (Lote):", numero_vehiculos_a_comprar)
    st.write("Monto total de la inversión:", inversion_total)
    st.write("Costo medio por vehículo:", costo_medio_por_vehiculo)
    st.write("Tiempo de retorno de la inversión en días:", tiempo_retorno_dias)
    st.write("Tiempo de retorno de la inversión en meses:", tiempo_retorno_meses_redondeado)


# scripts stations.py



api_url = 'https://www.mapquestapi.com/directions/v2/route?'
search_url = 'https://www.mapquestapi.com/search/v2/radius?'
traffic_url = 'https://www.mapquestapi.com/traffic/v2/incidents?'
key = env_data['MAPQUESTAPI']['key']

def find_charging_stations(origin, destination):
    route_url = api_url + urllib.parse.urlencode({"key": key, "from": origin, "to": destination})
    route_data = requests.get(route_url).json()
    locations = route_data['route']['locations']
    origin_latlng = locations[0]['latLng']
    destination_latlng = locations[-1]['latLng']
    
    result = []
    result.append("Are there charging stations near the route?")
    
    origin_stations = find_nearby_stations(origin_latlng)
    destination_stations = find_nearby_stations(destination_latlng)
    
    if origin_stations or destination_stations:
        result.append("Yes")
        if origin_stations:
            result.append(f"Charging stations near {origin}:")
            result.extend(print_stations(origin_stations))
        if destination_stations:
            result.append(f"Charging stations near {destination}:")
            result.extend(print_stations(destination_stations))
    else:
        result.append("No charging stations found near the route.")
    return result

def find_nearby_stations(latlng):
    radius_url = search_url + urllib.parse.urlencode({"key": key, "origin": f"{latlng['lat']},{latlng['lng']}", "radius": 10, "maxMatches": 3, "hostedData": "mqap.ntpois|group_sic_code=?|554101"})
    charging_stations_data = requests.get(radius_url).json()
    return charging_stations_data['searchResults'] if charging_stations_data['resultsCount'] > 0 else None

def print_stations(stations):
    result = []
    for station in stations:
        result.append(f"- {station['name']} at {station['fields']['address']}")
    return result
