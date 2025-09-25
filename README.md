# Proyecto de Gestión de Expedientes de Certificación - AOXLAB

## Descripción General

Este proyecto es una aplicación web desarrollada con Django, diseñada para digitalizar y gestionar el ciclo de vida completo de los procesos de certificación de productos, procesos y servicios de AOXLAB S.A.S. El sistema cumple con los requisitos funcionales y normativos descritos, asegurando la trazabilidad, eficiencia y seguridad de la información.

## Estado del Proyecto (Funcionalmente Completo)

El desarrollo de todas las funcionalidades principales ha concluido. El sistema ahora soporta todos los flujos de trabajo requeridos, desde la solicitud inicial del cliente hasta la gestión post-certificación.

### Funcionalidades Implementadas:

-   **Portal del Cliente:** Registro, gestión de perfil, creación de solicitudes de certificación, carga de documentación y seguimiento del estado del proceso.
-   **Portal del Personal (Roles):**
    -   **Revisor:** Revisión de solicitudes iniciales y devolución con observaciones.
    -   **Director de Certificaciones:** Planificación de evaluaciones (asignación de evaluadores, fechas), revisión final y toma de decisión de aprobación.
    -   **Evaluador:** Acceso a tareas asignadas, carga de evidencias y corrección de no conformidades.
-   **Generación de Certificados:** Emisión automática de certificados en formato PDF tras la aprobación de un expediente.
-   **Módulo de Auditoría:** Registro detallado de todas las acciones críticas realizadas en el sistema para una trazabilidad completa.
-   **Módulo de Seguimiento:** Gestión de quejas, apelaciones, amonestaciones y sanciones asociadas a los clientes certificados.

## Cómo Ejecutar el Proyecto

1.  Clona el repositorio.
2.  Crea y activa un entorno virtual:
    ```
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
    .\venv\Scripts\activate    # En Windows
    ```
3.  Instala las dependencias:
    ```
    pip install -r requirements.txt
    ```
4.  Aplica las migraciones:
    ```
    python manage.py migrate
    ```
5.  Crea un superusuario para acceder al admin:
    ```
    python manage.py createsuperuser
    ```
6.  Ejecuta el servidor de desarrollo:
    ```
    python manage.py runserver
    ```

## Siguientes Pasos (Post-Desarrollo)

Con el desarrollo funcional completado, las próximas etapas se centrarán en:
-   **Despliegue (Staging/Producción):** Configurar el entorno de producción (servidor, base de datos, Gunicorn, Nginx).
-   **Pruebas de Aceptación de Usuario (UAT):** Realizar pruebas con usuarios finales para validar el flujo y recibir feedback.
-   **Refinamiento de UI/UX:** Mejorar la interfaz de usuario basándose en el feedback.
-   **Documentación Final:** Generar manuales de usuario y documentación técnica detallada.
