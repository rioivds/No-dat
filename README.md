# SIGSE

SIGSE (acrónimo de Sistema Integral de Gestión y Seguridad Escolar) es una aplicación web desarrollada por alumnos de la Escuela Proa con énfasis en TICs, especialidad en Desarrollo de Software, de Río Cuarto, Córdoba, Argentina. La aplicación está diseñada para gestionar los datos internos de una institución educativa, incluyendo bases de datos de alumnos, docentes, materias y calificaciones. Además, integra un sistema de detección de caras usando ESP32 para validar accesos y registrar asistencias, proporcionando un control integral de seguridad y datos para análisis.

La aplicación SIGSE permite el manejo eficiente de todos los datos internos de una institución educativa. A través de una base de datos MySQL, se gestionan los registros de alumnos, docentes, materias y calificaciones, las cuales se pueden importar mediante planillas. La aplicación también incluye un proyecto de redes que configura toda la infraestructura para permitir la operación del servidor y un dispositivo de detección de caras que se conecta a la aplicación para validar el acceso al edificio y registrar la asistencia, ofreciendo un control integral de seguridad y datos para su análisis. Además, se presentan gráficos que muestran el desempeño académico de los alumnos según cursos y otros criterios.

Tecnologías utilizadas
Backend: Python, Django
Frontend: HTML, CSS, JavaScript, SASS
Base de datos: MySQL
Hardware: ESP32 para detección de caras, FortiGate 100E, Switch x460-24t
Servidor: Aplicación desplegada en http://proadsrioiv.rf.gd/

Requisitos previos
Para utilizar la aplicación como usuario, no se requiere la instalación de ningún software adicional, ya que es una aplicación web accesible desde cualquier navegador.

Para instalar y configurar la aplicación como servidor, es necesario tener instalado:
Python
MySQL (Servidor de base de datos)
Librerías de Python: Django, mysqlclient, openpyxl, pandas, django-bootstrap4, pypdf2

## Instrucciones de instalación

Para instalar y ejecutar la aplicación, se pueden seguir las instrucciones de la [wiki](https://github.com/rioivds/No-dat/wiki/C%C3%B3mo-ejecutar-la-aplicaci%C3%B3n-%E2%80%90-Gu%C3%ADa-de-instalaci%C3%B3n)

## Configuración del entorno

Después de instalar las dependencias y realizar las migraciones de la base de datos, es necesario crear usuarios de acceso. Para ello, sigue estos pasos:
Abre la shell de Django:
python manage.py shell

Crea un usuario:
from django.contrib.auth.models import User
User.objects.create_user(username="nombre_usuario", password="contraseña")

Uso de la aplicación
Una vez instalada y configurada, puedes acceder a la aplicación en tu navegador. URL=http://IPSERVER:8000/
Asegúrate de crear usuarios de acceso como se indicó en la sección anterior. Utiliza las credenciales creadas para iniciar sesión y comenzar a gestionar los datos de la institución.

Contribución
Si deseas contribuir a este proyecto, por favor, ponte en contacto con la escuela Proa o a través de la cuenta de GitHub. Estamos abiertos a recibir contribuciones y mejorar esta aplicación.

### Licencia
Este proyecto pertenece a la institución educativa Proa©.
