# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Activar entorno virtual (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear base de datos PostgreSQL
# Accede a PostgreSQL y crea la base de datos:
# CREATE DATABASE derecho_autor_db;

# Realizar migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver