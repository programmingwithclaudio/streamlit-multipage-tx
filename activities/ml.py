import streamlit as st
import streamlit as st
import io
import pandas as pd
import warnings
from activities.utils import funcs

# Suprimir advertencias de deprecación
warnings.filterwarnings("ignore")

st.header("Análisis de Modelos Machine Learning")


def main():
    st.title("MoviPlus Estimator")


    # Cargar modelos
    MODELOS = {
        "XGBoost": "public/datasets/models/modelo_xgb.parquet",
        "Gradient Boosting": "public/datasets/models/modelo_gb.parquet"
    }

    # Selección del modelo
    modelo_seleccionado = st.selectbox("Seleccionar modelo:", list(MODELOS.keys()))


    # Entrada de datos
    st.subheader("Ingrese los datos para la predicción:")
    hora_recogida = st.number_input("Hora de recogida:", min_value=0, max_value=23, step=1)
    diaSemana = st.number_input("Dia de la semana:", min_value=1, max_value=7, step=1)
    mes = st.number_input("Mes:", min_value=1, max_value=12, step=1)
    borough_id = st.number_input("Borough ID:", min_value=0.0, step=1.0)

    # Realizar la predicción cuando se haga clic en el botón
    if st.button("Predecir"):
        # Crear objeto de datos de entrada
        input_data = funcs.InputData(HoraRecogida=hora_recogida, diaSemana=diaSemana, mes=mes, Borough_id=borough_id)

        # Realizar la predicción utilizando el modelo
        resultado = funcs.predecir(modelo, input_data)

        # Obtener la probabilidad de conseguir pasajero
        probabilidad = resultado["Probabilidad de conseguir pasajero"][0]

        # Formatear la probabilidad a dos decimales
        probabilidad_formateada = "{:.2f}".format(probabilidad)

        # Mostrar el resultado dentro de una caja de información con la carita correspondiente
        st.subheader("Resultado de la predicción:")
        if probabilidad < 1.0:
            st.error("La probabilidad de conseguir pasajero es muy baja: " + probabilidad_formateada + " :(")
        elif probabilidad < 30.00:
            st.warning("La probabilidad de conseguir pasajero es regular: " + probabilidad_formateada + " :|")
        elif probabilidad < 50.0:
            st.success("La probabilidad de conseguir pasajero es alta: " + probabilidad_formateada + " :)")
        else:
            st.balloons()
            st.success("¡La probabilidad de conseguir pasajero es muy alta! :D")

            # Mostrar el resultado dentro de una caja de información
            st.subheader("Resultado de la predicción:")
            with st.info("La probabilidad de conseguir pasajero es: " + probabilidad_formateada):
                pass


if __name__ == '__main__':
    main()
