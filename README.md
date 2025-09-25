# APLICATIVO PARA LA GESTIÓN DE EXPEDIENTES DE CERTIFICACIÓN 

Este proyecto es una aplicación web desarrollada con Django para gestionar de manera integral el ciclo de vida de los procesos de certificación de productos, procesos y servicios, siguiendo las normativas ISO/IEC 17065:2012.

## Estado Actual del Proyecto (Fin de Fase 6)

El sistema ahora soporta un flujo de trabajo casi completo, desde la creación de la solicitud por parte del cliente hasta la ejecución y revisión de las tareas de evaluación. Los diferentes roles (Cliente, Director, Evaluador, Revisor) tienen paneles y funcionalidades específicas.

### Funcionalidades Implementadas:

*   **Flujo del Cliente (Completado):**
    *   Registro y gestión de perfil de empresa.
    *   Creación y envío de solicitudes de certificación detalladas.

*   **Flujo de Revisión de Solicitud (Completado):**
    *   El personal interno puede revisar las solicitudes, marcar ítems como "No Conforme" y enviar observaciones al cliente para su corrección.

*   **Flujo de Planificación de la Evaluación (Completado):**
    *   El Director de Certificaciones puede gestionar una base de datos de Evaluadores.
    *   Puede crear un plan de evaluación detallado para cada solicitud aprobada, asignando actividades, evaluadores y fechas.
    *   Puede iniciar formalmente la fase de ejecución, cambiando el estado de la solicitud.

*   **Flujo de Ejecución y Revisión de Evidencias (Completado):**
    *   **Dashboard del Evaluador:** Los evaluadores tienen un panel personalizado que muestra únicamente sus tareas asignadas.
    *   **Carga de Evidencias:** Los evaluadores pueden subir archivos de evidencia para cada una de sus actividades.
    *   **Panel del Revisor:** Los revisores (o el Director) pueden ver las evidencias cargadas y marcarlas como "Conforme" o "No Conforme", añadiendo observaciones.
    *   **Ciclo de Corrección:** Si una evidencia es rechazada, la tarea se marca como "Con Inconsistencias" y se notifica visualmente al evaluador, quien puede ver las observaciones y subir una nueva versión para reiniciar el ciclo de revisión.
    *   **Finalización de la Fase:** Cuando todas las actividades de una solicitud son aprobadas por el revisor, la solicitud avanza al siguiente estado.

## Cómo Ejecutar el Proyecto
*(Esta sección permanece igual)*

## Siguientes Pasos (Fase 7)

La próxima fase de desarrollo se centrará en el **Módulo de Decisión y Emisión**, que es la etapa final del proceso principal:
-   Crear un dashboard para el **Director de Certificaciones** donde vea las solicitudes con evidencias ya revisadas.
-   Implementar la funcionalidad para que el Director pueda hacer una revisión final del expediente completo.
-   Desarrollar la acción de "Aprobar Expediente", que bloqueará toda la información para evitar modificaciones.
-   Crear un sistema para generar y emitir el certificado final en formato PDF, basado en plantillas.
