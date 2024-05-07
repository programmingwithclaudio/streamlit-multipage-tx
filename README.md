# Streamlit Multipage App

[![App Preview](https://i.postimg.cc/wvTKJmTs/Screenshot-from-2024-05-07-11-03-18.png)](https://app-multipage-tx-diip.streamlit.app/)

¡Dale like y suscríbete! [ProgrammingWithClaudio YouTube Channel](https://www.youtube.com/@programmingwithclaudio/videos) para más contenido relacionado.

## Overview

Este proyecto es una aplicación multipágina desarrollada con Streamlit, que proporciona una interfaz interactiva para visualizar datos.

## Características

- Interfaz intuitiva y fácil de usar.
- Múltiples páginas para organizar y presentar diferentes funcionalidades.
- Despliegue sencillo con Docker.

## Tecnologías Utilizadas

- Docker 26.1.1
- Streamlit >=1.22
- Python 3.9

## Uso

1. Clona el repositorio:

```bash
git clone git@github.com:programmingwithclaudio/streamlit-multipage-tx.git
```

2. Ejemplo de despliegue con Docker:

```bash
docker build -t test25-app .
docker run --rm -it -p 8051:8051 test25-app
```

¡Explora la aplicación en [https://app-multipage-tx-diip.streamlit.app/](https://app-multipage-tx-diip.streamlit.app/)!

## Contribución

Las contribuciones son bienvenidas. Si tienes ideas para nuevas características, por favor abre un issue para discutirlo o envía un pull request.

## Licencia

Distribuido bajo la licencia MIT. Ver `LICENSE` para más información.

