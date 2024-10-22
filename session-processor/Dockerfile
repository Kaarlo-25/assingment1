# Usa una imagen oficial de Python como imagen base
FROM python:3.9

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos actuales al contenedor
COPY . .

# Instala las dependencias necesarias
RUN pip install pika pymongo

# Ejecuta el script y asegúrate de que los logs se muestran en tiempo real (sin buffering)
CMD ["python", "-u", "session_processor.py"]