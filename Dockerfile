# Etapa de construcción
FROM python:3.9-slim-buster AS builder

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el contenido del directorio actual al contenedor
COPY . .

# Instalar las dependencias y Streamlit
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir streamlit

# Etapa final
FROM python:3.9-slim-buster AS app

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el contenido de la etapa de construcción al contenedor final
COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Exponer el puerto utilizado por Streamlit
EXPOSE 8501

# Comando para ejecutar la aplicación Streamlit
CMD ["streamlit", "run", "streamlit_app.py"]

