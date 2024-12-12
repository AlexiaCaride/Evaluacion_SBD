# Usar una imagen base de Python
FROM python:3.8-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /scripts

# Copiar los scripts a la carpeta /scripts dentro del contenedor
COPY ./scripts /scripts

# Instalar las dependencias necesarias para conectar con MongoDB y pandas
RUN pip install pymongo pandas requests schedule

# Definir el comando por defecto para ejecutar los scripts
CMD ["python3", "conexionAPI.py"]
