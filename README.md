## Estado Actual del Proyecto (Fin de Fase 4)

La aplicación ahora soporta los flujos de trabajo completos tanto para el **Cliente** como para la **Revisión Inicial del Personal Interno**.

### Funcionalidades Implementadas:

*   **Flujo del Cliente (Completado):**
    *   Autenticación y gestión de perfil (Empresa, Sedes, Representante Legal).
    *   Creación, diligenciamiento detallado (Alcances, Recursos) y envío de Solicitudes de Certificación.

*   **Flujo del Personal Interno (Fase Inicial):**
    *   **Panel de Control para Staff:** Un dashboard que lista las solicitudes pendientes por revisar.
    *   **Redirección por Rol:** El sistema dirige a clientes y personal a sus respectivos paneles al iniciar sesión.
    *   **Interfaz de Revisión:** Una vista detallada permite al personal revisar cada ítem del alcance de una solicitud, marcarlo como "Conforme" / "No Conforme" y añadir observaciones.
    *   **Automatización de Estado:** El sistema actualiza automáticamente el estado de la solicitud a "En Subsanación" o "En Planificación" basándose en el resultado de la revisión.

## Cómo Ejecutar el Proyecto
*(Esta sección permanece igual)*

## Siguientes Pasos (Fase 4 y 5)
La próxima fase de desarrollo se centrará en completar el ciclo de revisión y comenzar la planificación de las evaluaciones:
1.  **Cerrar el Ciclo de Subsanación:** Permitir al cliente ver las observaciones del revisor y reenviar la solicitud corregida.
2.  **Módulo de Planificación:**
    *   Crear una interfaz para que un Director pueda gestionar la base de datos de Evaluadores.
    *   Desarrollar la vista de planificación para asignar actividades y evaluadores a las solicitudes aprobadas.
