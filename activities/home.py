import streamlit as st
from PIL import Image
from streamlit_lottie import st_lottie
import urllib.request
import json
import base64

def load_lottieurl(url):
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    return data

def local_css(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css('public/style/style.css')

# ---- LOAD ASSETS ----
#lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
# URL de la animación Lottie

# Ruta al archivo JSON que contiene la animación Lottie
json_path = "public/images/5jfUuoI3oW.json"

# Lee el contenido del archivo JSON
with open(json_path, "r") as f:
    lottie_coding = json.load(f)



# Directorio actual
current_directory = os.path.dirname(__file__)

# Construir la ruta completa al archivo de imagen
appweb_path = os.path.join(current_directory, 'public', 'images', 'appweb.PNG')
appbi_path = os.path.join(current_directory, 'public', 'images', 'appbi.png')

# Cargar las imágenes
appweb = Image.open(appweb_path)
appbi = Image.open(appbi_path)

st.title('Diip')

# ---- HEADER SECTION ----
with st.container():
    st.subheader("Hola, Somos el Equipo de Data Diip :wave:")
    st.title("!Transformando los datos a conocimiento!")
    st.write(
        "Nos apasiona encontrar formas de utilizar Python y los servicios en la Nube para ser más eficientes y efectivos en entornos empresariales."
    )
    st.write("[Learn More >](https://pythonandvba.com)")




# ---- WHAT I DO ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("¿Qué hacemos?")
        st.write("##")
        st.write(
            """
                Nuestro equipo ha llevado a cabo un proyecto integral que abarca desde el análisis de métricas de transporte 
                hasta el desarrollo de un modelo de machine learning (MLOPS), para mejorar la eficiencia y precisión en la toma de decisiones.
                
                **Análisis de Exploratorio EDA y Planificación de KPI's Claves:**
                Este proyecto utiliza una diferentes fuentes para obtener métricas de recorridos de transporte, como duración del viaje, 
                distancia recorrida, consumo de combustible, emisiones de CO2, velocidad promedio y la presencia de incidentes en la ruta.
                
                **Desarrollo de Modelo de Machine Learning:**
                Además, hemos desarrollado un modelo de machine learning que aborda desde el scraping de datos, exploratory data analysis (EDA), 
                extracción, transformación y carga (ETL) en Azure Data Lake, hasta el modelado de datos para predecir y optimizar diversos aspectos del transporte.
            """
        )
        st.write("[YouTube Channel >](https://www.youtube.com/@DataDiip)")
    with right_column:
        st_lottie(lottie_coding, height=400, key="coding")


# ---- PROJECTS ----
with st.container():
    st.write("---")
    st.header("Proyectos Desarrollados")
    st.write("##")
    image_column, text_column = st.columns((1, 2))
    with image_column:
        st.image(appbi)
    with text_column:
        st.subheader("Dashboard de Power BI para Control de Flotas de Taxis")
        st.write(
            """
            Este proyecto presenta un dashboard interactivo desarrollado en Power BI 
            para el control y gestión de flotas de taxis eléctricos y convencionales 
            en la región metropolitana de Nueva York.
            """
        )
        st.markdown("[Watch Video...](https://youtu.be/TXSOitGoINE)")
with st.container():
    image_column, text_column = st.columns((1, 2))
    with image_column:
        st.image(appweb)
    with text_column:
        st.subheader("Análisis de Métricas de Transporte con API")
        st.write(
            """
            Este proyecto utiliza una API para obtener métricas de recorridos de transporte, como duración del viaje, 
            distancia recorrida, consumo de combustible, emisiones de CO2, velocidad promedio y la presencia de incidentes en la ruta.
            Por ejemplo, al ingresar la información de un viaje desde el Aeropuerto de Newark hasta Jamaica Bay.
            """
        )
        st.markdown("[Watch Video...](https://youtu.be/FOULV9Xij_8)")


# ---- SECTION TO DISPLAY PROFILES ----

with st.container():
    st.markdown("<h1 style='text-align: center;'>Desarrollado por ⚙️ </h1>", unsafe_allow_html=True)
    st.markdown("<hr style='height:5px;border-width:0;color:gray;background-color:gray'>", unsafe_allow_html=True)

    personas = [
        {
            "nombre": "Claudio Quispe",
            "profesion": "Data Engineer",
            "github": "https://github.com/clblommberg",
            "linkedin": "https://www.linkedin.com/in/btorresdata/",
            "imagen_link": "public/images/claudio.jpg",
        },
        {
            "nombre": "Herlin Yauri",
            "profesion": "Data Analytics",
            "github": "https://github.com/HerlinData",
            "linkedin": "https://www.linkedin.com/in/herlin-yauri/",
            "imagen_link": "public/images/herlin.jpg",
        },
        {
            "nombre": "Duván Robayo",
            "profesion": "Data Architect",
            "github": "https://github.com/duvanroarq",
            "linkedin": "https://www.linkedin.com/in/duvanroarq/",
            "imagen_link": "public/images/duvan.jpg",
        },
        {
            "nombre": "Byron Torres",
            "profesion": "Machine Learning Engineer",
            "github": "https://github.com/byrontorres",
            "linkedin": "https://www.linkedin.com/in/btorresdata/",
            "imagen_link": "public/images/byron.jpg",
        },
        {
            "nombre": "Sevas Vasquez",
            "profesion": "Data Engineer",
            "github": "https://github.com/SebitaElGordito",
            "linkedin": "https://www.linkedin.com/in/ivan-parra-2501/",
            "imagen_link": "public/images/Sebas.jpg",
        },
        {
            "nombre": "Cristobal Quiroz",
            "profesion": "Data Engineer",
            "github": "https://github.com/cristobalqv",
            "linkedin": "https://www.linkedin.com/in/ivan-parra-2501/",
            "imagen_link": "public/images/cristobal.jpg",
    },
    ]

    def get_image_b64(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")

    # Mostrar los perfiles y las imágenes en bloques centrados
    column1, column2, column3 = st.columns(3)
    for idx, persona in enumerate(personas):
        with eval(f"column{idx % 3 + 1}"):
            st.markdown(
                f'<h2 style="text-align: center;">{persona["nombre"]}</h2>', unsafe_allow_html=True,
            )
            # Convertir la imagen a base64 y mostrarla
            persona_image = get_image_b64(persona["imagen_link"])
            st.markdown(
                f'<div style="display: flex; justify-content: center;"><img src="data:image/png;base64,{persona_image}" width="200"/></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<h3 style="text-align: center;">{persona["profesion"]}</h3>', unsafe_allow_html=True,
            )
            linkedin_logo = get_image_b64("public/images/LI-In-Bug.png")  # Convertir el logo de LinkedIn local a base64
            # Mostrar el logo de LinkedIn en un div
            st.markdown(
                f'<div style="display: flex; justify-content: center;"><a href="{persona["linkedin"]}"><img src="data:image/png;base64,{linkedin_logo}" alt="LinkedIn" width="45"/></a></div>',
                unsafe_allow_html=True,
            )
