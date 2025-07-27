# Usa una imagen base de Python
FROM python:latest

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de la aplicación al contenedor
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir Flask==2.3.2 mysql-connector-python

# Exponer el puerto
EXPOSE 5000

# Comando para iniciar la aplicación
CMD ["python", "app.py"]