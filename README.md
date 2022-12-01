# Resultados de aprendizaje

Es un servicio automatizado en línea que permite gestionar para las instituciones educativas las evaluaciones de cursos basados en indicadores de logro

## Comenzando 🚀

_Estas instrucciones le permitirán obtener una copia del proyecto en funcionamiento en su máquina local._

### Requerimientos 📋

_Antes de empezar, necesitará:_

* python >= 3.7
* postgresql >= 10.15


# Requerimientos
---
_Instale los requerimientos con utilizando el gestor de paquete **pip**:_
```
pip install -r requirements/base.pip
```
En caso de fallar la instalacion de los requerimientos en Linux. realizar los siguientes pasos:
   - sudo apt-get install libpq-dev
   - pip install wheel
   - pip install -r requirements/base.pip

### Secrets.json 🔧

Antes de comenzar, utilice esta estructura pra crear el _secrets.json_
```
{
    "FILENAME": "secrets.json",
    "SECRET_KEY": "w19n&$g)3y#)%p5yqj#nvogzvupgo4ioxjv3^_)v$#zsourw38",
    "DEBUG": true,
    "DOMINIOS_PROPIOS": [
        "*"
    ],
    "DATABASE_DEFAULT": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "5433",
        "ATOMIC_REQUESTS": true
    },
    "USE_S3":false
}
```

y ubíquelo en la raíz del proyecto (al nivel de _manage.py_)

### Instalación 🔧
_Ejecute las migraciones:_

```
python manage.py makemigrations
python manage.py migrate

Cargue los datos iniciales a la base de datos utilizando el siguiente comando:
    - python manage.py cargar_informacion_inicial

_En este punto, ejecute el programa:_
```
python manage.py runserver
```

_Abra el navegador y acceda al sistema:_
```
http://localhost:8000
```