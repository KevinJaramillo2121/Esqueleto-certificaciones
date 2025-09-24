# Sistema de Gestión de Expedientes

Este proyecto es una aplicación web desarrollada con Django para gestionar el ciclo de vida completo de los procesos de certificación, desde la solicitud del cliente hasta la emisión del certificado, cumpliendo con las normativas ISO/IEC 17065:2012 e ISO/IEC 17067:2013.

## Estado Actual del Proyecto (Fin de Fase 3)

La aplicación ha completado el desarrollo de toda la interfaz y lógica del lado del **Cliente (Solicitante)**.

### Funcionalidades Implementadas:
*   **Autenticación de Usuarios:** Registro, inicio y cierre de sesión.
*   **Gestión de Perfil de Cliente:**
    *   Creación y edición de la información de la **Empresa**.
    *   Gestión de múltiples **Sedes** por empresa.
    *   Creación y edición de los datos del **Representante Legal**.
*   **Flujo de Solicitud de Certificación:**
    *   Creación de una nueva solicitud, con validación de que el perfil de la empresa esté completo.
    *   Dashboard que lista todas las solicitudes del cliente y su estado.
    *   **Gestión del Alcance:** CRUD completo (Crear, Editar, Eliminar) para añadir los productos, procesos o servicios a certificar en una solicitud.
    *   **Gestión de Recursos por Alcance:** Para cada ítem del alcance, el cliente puede añadir:
        *   Personas Clave
        *   Equipos Clave (con subida de archivos para hojas de vida)
        *   Documentación del Proceso (con subida de archivos)
    *   **Envío a Revisión:** El cliente puede enviar la solicitud finalizada, cambiando su estado a "En Revisión" y bloqueando futuras ediciones.

## Cómo Ejecutar el Proyecto

### Prerrequisitos
- Python 3.8+
- PostgreSQL
- `pip` y `virtualenv`

### Pasos para la Instalación

1.  **Clonar el repositorio:**
    ```
    git clone <URL-del-repositorio>
    cd <nombre-del-repositorio>
    ```

2.  **Crear y activar un entorno virtual:**
    ```
    python -m venv env
    source env/bin/activate  # En Windows: env\Scripts\activate
    ```

3.  **Instalar dependencias:**
    ```
    pip install -r requirements.txt
    ```

4.  **Configurar la base de datos:**
    - Asegúrate de que PostgreSQL esté en ejecución.
    - Crea una base de datos (ej. `PerroViejo_db`).
    - Renombra el archivo `.env.example` a `.env` y edita las variables de entorno con tus credenciales de base de datos:
    ```
    SECRET_KEY=tu-secret-key-aqui
    DEBUG=True
    DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME
    ```

5.  **Aplicar migraciones:**
    ```
    python manage.py migrate
    ```

6.  **Crear un superusuario (opcional, para admin):**
    ```
    python manage.py createsuperuser
    ```

7.  **Ejecutar el servidor de desarrollo:**
    ```
    python manage.py runserver
    ```
    La aplicación estará disponible en `http://127.0.0.1:8000/`.

## Siguientes Pasos (Fase 4)
La próxima fase de desarrollo se centrará en construir las interfaces y la lógica para el **personal interno de la app**, incluyendo:
-   Dashboard para revisores y directores.
-   Revisión de solicitudes.
-   Planificación de evaluaciones.



Funcionalidades y Cambios Implementados:

Gestión de Detalle de Solicitud y Alcance:

Se ha creado la SolicitudDetailView como el centro de operaciones para una solicitud individual, accesible solo por el propietario.

Se ha implementado el CRUD completo (Create, Update, Delete) para el modelo Alcance, permitiendo al cliente definir los ítems a certificar.

Gestión de Recursos por Alcance:

Se han añadido los modelos PersonaClave, EquipoClave y DocumentoProceso, vinculados a cada Alcance.

Se ha implementado la AlcanceDetailView, una nueva página para gestionar los recursos específicos de cada ítem del alcance (personal, equipos y documentos).

Se han implementado las vistas y formularios CRUD para PersonaClave, EquipoClave y DocumentoProceso, permitiendo una gestión detallada.

Finalización del Flujo del Cliente:

Se ha implementado la vista EnviarSolicitudView, que permite al cliente cambiar el estado de la solicitud de 'Borrador' a 'En Revisión'.

Se han añadido validaciones para asegurar que una solicitud solo se pueda enviar si tiene al menos un alcance definido y si se encuentra en estado 'Borrador'.

Una vez enviada, la solicitud y sus componentes quedan bloqueados para edición, cumpliendo con los requisitos del flujo de trabajo.

Mejoras de UI/UX:

Se ha añadido una plantilla genérica (generic_form.html) para reutilizar en múltiples vistas de creación/edición.

Se han activado todos los enlaces y botones, creando un flujo de usuario coherente desde el dashboard hasta la gestión de recursos y el envío final."