import re
import os
from glob import glob
import pandas as pd 


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



