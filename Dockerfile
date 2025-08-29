# Imagen base con Python
FROM python:3.11-slim

# Definir directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar paquetes
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivo de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto donde corre Dash (por defecto 8050)
EXPOSE 8050

# Comando para iniciar la aplicación
CMD ["python", "main_2.py"]
