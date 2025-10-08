# ==============================================
#  DOCKERFILE PARA PROYECTO DJANGO (PRODUCCIÓN)
#  Autor: Camilo Mercado
#  Proyecto: CONTROL_DE_ASISTENCIA
#  Base: Python 3.12-slim
# ==============================================

# --------------------------
# Etapa 1: Builder
# --------------------------
FROM python:3.12-slim AS builder

# Evitar prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar paquetes Python
# (libpq-dev y build-essential son necesarios para psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copiar el archivo de dependencias
COPY requirements.txt .

# Actualizar pip e instalar dependencias en una capa temporal (/install)
RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt


# --------------------------
# Etapa 2: Runtime (producción)
# --------------------------
FROM python:3.12-slim AS runtime

# Variables de entorno globales
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Instalar solo lo necesario para ejecutar psycopg2 (sin compilar nada)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Crear usuario seguro (no root)
RUN addgroup --system django && adduser --system --ingroup django django

# Establecer directorio de trabajo
WORKDIR /app

# Copiar dependencias instaladas desde la etapa builder
COPY --from=builder /install /usr/local

# Copiar el código fuente (sin .env gracias al .dockerignore)
COPY . .

# Crear directorios necesarios y ajustar permisos
RUN mkdir -p /app/staticfiles /app/logs && chown -R django:django /app

# Copiar y preparar el script de entrada (entrypoint)
COPY --chown=django:django entrypoint.sh /entrypoint.sh

# Cambiar a root temporalmente para ajustar permisos
USER root
RUN sed -i 's/\r$//' /entrypoint.sh && chmod 755 /entrypoint.sh

# Instalar gunicorn y psycopg2-binary por seguridad (por si no están en requirements.txt)
RUN pip install --no-cache-dir gunicorn psycopg2-binary

# Volver al usuario seguro
USER django

# Exponer el puerto 80
EXPOSE 80

# Comando de inicio
ENTRYPOINT ["/entrypoint.sh"]
