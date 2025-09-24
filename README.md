# - Aplicativo para la Gestión de Expedientes de Certificación

## 1. Descripción del Proyecto

 es una plataforma web diseñada para la administración integral del ciclo de vida de los procesos de certificación de productos, procesos y servicios. El sistema centraliza y gestiona la información desde la solicitud inicial de un cliente hasta la emisión del certificado y su seguimiento posterior, mejorando la trazabilidad, eficiencia y comunicación entre todas las partes involucradas [1].

El aplicativo está diseñado para cumplir con los estándares internacionales clave en la evaluación de la conformidad, como **ISO/IEC 17065:2012** e **ISO/IEC 17067:2013** [1].

### Roles de Usuario Principales

El sistema está diseñado para servir a diferentes perfiles de usuario, cada uno con un panel de control y permisos específicos [1]:
*   **Cliente Solicitante:** Gestiona la información de su empresa, crea solicitudes de certificación y consulta el estado de sus procesos.
*   **Personal Interno (Revisores, Director de Certificaciones):** Revisa solicitudes, planifica evaluaciones y toma decisiones sobre la certificación.
*   **Evaluadores y Expertos Técnicos:** Acceden a los expedientes asignados para ejecutar las evaluaciones y cargar las evidencias correspondientes.

## 2. Estado Actual del Desarrollo (Fase Inicial)

Esta versión inicial del proyecto establece la base de la aplicación, con un enfoque en la seguridad, la autenticación y la gestión de usuarios. La funcionalidad implementada hasta la fecha es:

### Módulo de Gestión de Cuentas y Acceso

*   **Modelo de Usuario Personalizado:** Se ha implementado un sistema de usuarios que utiliza el **correo electrónico** como identificador principal para el inicio de sesión, en lugar del nombre de usuario tradicional.
*   **Registro de Nuevos Usuarios (Signup):** Un formulario permite a los nuevos clientes (rol "Cliente Solicitante") crear una cuenta en el sistema, proporcionando su nombre, apellido y correo electrónico.
*   **Inicio y Cierre de Sesión (Login/Logout):** Funcionalidad completa para que los usuarios puedan autenticarse y cerrar su sesión de forma segura.
*   **Recuperación de Contraseña:** Se ha implementado un flujo seguro para el reseteo de contraseñas a través del correo electrónico, utilizando las robustas herramientas incorporadas en Django [1].
*   **Página de Inicio Dinámica:** La página principal de la aplicación muestra contenido diferente dependiendo de si el usuario ha iniciado sesión o es un visitante.

## 3. Stack Tecnológico

*   **Backend:** Python 3
*   **Framework:** Django
*   **Base de Datos:** PostgreSQL
*   **Adaptador de BD:** `psycopg2-binary`

## 4. Estructura del Proyecto

El proyecto sigue la arquitectura MVT (Modelo-Vista-Plantilla) de Django y está organizado de la siguiente manera:

proyecto_certificacion/
├── aoxlab_project/ # Directorio de configuración principal del proyecto
│ ├── settings.py # Configuración (BD, apps instaladas, etc.)
│ ├── urls.py # URLs principales del proyecto
│ └── ...
├── users/ # App de Django para la gestión de usuarios
│ ├── models.py # Modelos Rol y Usuario personalizado
│ ├── views.py # Vistas para registro (SignUpView)
│ ├── forms.py # Formulario de creación de usuario
│ ├── urls.py # URLs específicas de la app users
│ └── migrations/ # Migraciones de la base de datos
├── templates/ # Plantillas HTML globales
│ ├── registration/ # Plantillas de autenticación (login, signup, etc.)
│ └── home.html # Página de inicio
└── manage.py # Script de gestión de Django


## 5. Guía de Instalación y Puesta en Marcha

Sigue estos pasos para configurar el entorno de desarrollo y ejecutar el proyecto en tu máquina local.

### Prerrequisitos

*   Python 3.x
*   PostgreSQL instalado y un servidor en ejecución.
*   Git

### Pasos

1.  **Clonar el repositorio:**
    ```
    git clone <URL_de_tu_repositorio_github>
    cd proyecto_certificacion
    ```

2.  **Crear y activar un entorno virtual:**
    ```
    # En macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # En Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instalar las dependencias:**
    ```
    pip install -r requirements.txt
    ```
    *(Nota: Asegúrate de crear un archivo `requirements.txt` ejecutando `pip freeze > requirements.txt`)*

4.  **Configurar la base de datos:**
    *   Crea una base de datos vacía en PostgreSQL para el proyecto (ej. `aoxlab_db`).
    *   Renombra el archivo `.env.example` a `.env` (o crea uno) y añade las credenciales de tu base de datos. Se recomienda usar una librería como `python-decouple` para gestionar variables de entorno.
    *   Ajusta la configuración en `aoxlab_project/settings.py` para que apunte a tu base de datos:
    ```
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'nombre_de_tu_db',
            'USER': 'tu_usuario_postgres',
            'PASSWORD': 'tu_contrasena',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```

5.  **Ejecutar las migraciones:**
    ```
    python manage.py migrate
    ```

6.  **Crear un superusuario (opcional):**
    ```
    python manage.py createsuperuser
    ```

7.  **Iniciar el servidor de desarrollo:**
    ```
    python manage.py runserver
    ```

La aplicación estará disponible en `http://127.0.0.1:8000/`.

## 6. Próximos Pasos

La siguiente fase del desarrollo se centrará en la construcción del **Módulo de Solicitud de Certificación**, que permitirá a los usuarios autenticados:
*   Ser redirigidos a un panel de control (Dashboard).
*   Registrar y gestionar la información de su `Empresa`, `Sedes` y `Representante Legal`.
