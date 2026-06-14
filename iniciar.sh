#!/bin/bash

echo "Iniciando configuración de UNPi Study Manager..."

# 1. Comprobar si existe la carpeta del entorno virtual
if [ ! -d "venv" ]; then
    echo "🌱 Creando entorno virtual híbrido (vinculado al sistema)..."
    # La bandera --system-site-packages permite usar el wxPython nativo de Linux
    python3 -m venv --system-site-packages venv
fi

# 2. Activar el entorno virtual
echo "🔌 Activando entorno..."
source venv/bin/activate

# 3. Instalar SOLO las dependencias extra (como reportlab)
if [ -f "requirements.txt" ]; then
    echo "📦 Instalando dependencias extra..."
    pip install -r requirements.txt
else
    echo "⚠️ Advertencia: No se encontró requirements.txt."
fi

# 4. Iniciar la aplicación
echo "🚀 Abriendo el entorno de estudio..."
python3 main.py