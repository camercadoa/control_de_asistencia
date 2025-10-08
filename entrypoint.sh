#!/bin/sh
# ==============================================
# Script de inicio del contenedor Django
# ==============================================

echo "🚀 Iniciando contenedor Django..."

# Esperar a que la base de datos esté lista (si es externa, breve pausa)
echo "⏳ Esperando a la base de datos..."
sleep 3

# Aplicar migraciones
echo "📦 Ejecutando migraciones..."
python manage.py migrate --noinput

# Recolectar archivos estáticos
echo "🎨 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Iniciar el servidor Gunicorn en el puerto 80
echo "🌐 Iniciando Gunicorn en el puerto 80..."
exec gunicorn core_asistencia.wsgi:application \
    --bind 0.0.0.0:80 \
    --workers 3 \
    --timeout 120
