# Entorno de Estudio UNPi
Aplicación de escritorio diseñada para organizar materias (datos, materiales, apuntes), tomar apuntes y planificar la semana de estudio. También el usuario podrá estduair con 4 métodos de estudio (Apunte libre, Sprint Memoria, Matriz de Analisis y Flashcards).

#Requisitos:
* Python 3.x
* wxPython
* ReportLab

#Instalación y Ejecución en Linux:
1. Clona este repositorio o descarga el código.
2. Abre una terminal en la carpeta del proyecto.
3. Crea un entorno virtual: `python3 -m venv .venv --system-site-packages`
4. Actívalo: `source .venv/bin/activate`
5. Instala las dependencias: `pip install -r requirements.txt`
6. Ejecuta el programa con el script incluido: `./iniciar.sh` (o `python3 main.py`).

*Nota: La base de datos SQLite se generará automáticamente de forma limpia al iniciar por primera vez.*
