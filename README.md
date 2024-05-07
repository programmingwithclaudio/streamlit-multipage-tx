

## Docker 578mb super
```bash
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
```

## Docker 1.13gb
```bash
# app/Dockerfile

FROM python:3.9-slim

# Añadir etiqueta de versión para la imagen base
LABEL version="1.0"

# Instalar dependencias del sistema operativo
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos de la aplicación
COPY . .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto utilizado por Streamlit
EXPOSE 8501

# Establecer el comando de salud
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Establecer el punto de entrada para ejecutar la aplicación Streamlit
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]




```
