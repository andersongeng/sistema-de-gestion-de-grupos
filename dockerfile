# 1. Usamos una versión ligera de Python 3.11
FROM python:3.11-slim

# 2. Evitamos que Python genere archivos .pyc y que el output sea lento
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Creamos y nos situamos en la carpeta de la app dentro del contenedor
WORKDIR /app

# 4. Instalamos dependencias del sistema necesarias para psycopg2-binary y otras
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 5. Instalamos las librerías de Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Copiamos todo nuestro código a la carpeta /app
COPY . .

# 7. Exponemos el puerto que usará Flask
EXPOSE 8000

# 8. El comando para arrancar la app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "run:app"]