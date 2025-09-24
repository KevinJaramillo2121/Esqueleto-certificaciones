#  - Aplicativo para la Gestión de Expedientes de Certificación

## 1. Descripción del Proyecto

 es una plataforma web diseñada para la administración integral del ciclo de vida de los procesos de certificación de productos, procesos y servicios. El sistema centraliza y gestiona la información desde la solicitud inicial de un cliente hasta la emisión del certificado y su seguimiento posterior, mejorando la trazabilidad, eficiencia y comunicación entre todas las partes involucradas [1].

El aplicativo está diseñado para cumplir con los estándares internacionales clave en la evaluación de la conformidad, como **ISO/IEC 17065:2012** e **ISO/IEC 17067:2013** [1].

## 2. Estado Actual del Desarrollo

### Fase 1: Módulo de Gestión de Cuentas (Completado)

Esta versión inicial del proyecto establece la base de la aplicación, con un enfoque en la seguridad, la autenticación y la gestión de usuarios.
*   **Modelo de Usuario Personalizado:** Se ha implementado un sistema de usuarios que utiliza el **correo electrónico** como identificador principal.
*   **Flujo de Autenticación Completo:** Incluye registro de nuevos usuarios, inicio/cierre de sesión y un mecanismo seguro para la recuperación de contraseña.
*   **Página de Inicio Dinámica:** Muestra contenido diferente para usuarios autenticados y para visitantes.

### Fase 2: Módulo de Expedientes (En Desarrollo)

Se ha implementado la funcionalidad inicial para que los clientes gestionen la información fundamental de su empresa.
*   **Panel de Control (Dashboard):** Tras iniciar sesión, los usuarios son redirigidos a un dashboard personal que actúa como centro de operaciones.
*   **Gestión de Empresa:** Los usuarios ahora pueden registrar la información de su empresa (NIT, razón social, etc.). El sistema asocia automáticamente la empresa creada con la cuenta del usuario.
*   **Modelos de Datos:** Se han definido los modelos `Empresa`, `Sede` y `RepresentanteLegal`, sentando las bases para la gestión completa de expedientes.

## 3. Stack Tecnológico

*   **Backend:** Python 3
*   **Framework:** Django
*   **Base de Datos:** PostgreSQL
*   **Adaptador de BD:** `psycopg2-binary`

## 4. Estructura del Proyecto

La arquitectura MVT (Modelo-Vista-Plantilla) del proyecto se ha expandido para incluir el nuevo módulo de `expedientes`.

proyecto_certificacion/
├── aoxlab_project/ # Directorio de configuración principal
├── users/ # App para la gestión de usuarios y autenticación
├── expedientes/ # App para la gestión de empresas, solicitudes, etc.
│ ├── models.py # Modelos Empresa, Sede, RepresentanteLegal
│ ├── views.py # Vistas para Dashboard y creación de Empresa
│ ├── forms.py # Formulario para el modelo Empresa
│ ├── urls.py # URLs específicas del módulo de expedientes
│ └── migrations/
├── templates/ # Plantillas HTML globales
│ ├── expedientes/ # Plantillas para dashboard y formulario de empresa
│ └── registration/
└── manage.py


## 5. Guía de Instalación y Puesta en Marcha

Sigue estos pasos para configurar el entorno de desarrollo y ejecutar el proyecto en tu máquina local.

*(...El resto de la guía de instalación permanece igual...)*

## 2. Estado Actual del Desarrollo

### Fase 1: Módulo de Gestión de Cuentas (Completado)

Esta versión inicial del proyecto establece la base de la aplicación, con un enfoque en la seguridad, la autenticación y la gestión de usuarios.
*   **Modelo de Usuario Personalizado:** Utiliza el correo electrónico como identificador principal.
*   **Flujo de Autenticación Completo:** Incluye registro, inicio/cierre de sesión y recuperación de contraseña.

### Fase 2: Módulo de Expedientes - Gestión de Datos del Cliente (Completado)

Se ha implementado la funcionalidad completa para que los clientes gestionen la información fundamental de su empresa, un requisito previo para crear solicitudes de certificación.

*   **Panel de Control (Dashboard) Dinámico:** El dashboard del usuario ahora centraliza toda la gestión de su información. Muestra el estado actual y proporciona acciones contextuales (crear o editar) para cada sección.
*   **Gestión Completa de Empresa (CRUD):** Los usuarios pueden crear y editar la información principal de su empresa.
*   **Gestión Completa de Sedes (CRUD):** Se ha implementado la funcionalidad para que los clientes puedan añadir, listar, editar y eliminar múltiples sedes asociadas a su empresa.
*   **Gestión Completa de Representante Legal (CRUD):** Se ha habilitado la creación y edición de los datos del representante legal, incluyendo la carga de documentos PDF.
*   **Seguridad y Pertenencia de Datos:** Todas las vistas aseguran que un usuario solo pueda ver y modificar la información asociada a su propia cuenta.


## 6. Próximos Pasos
# 🛠️ Roadmap de Desarrollo - Módulo de Certificación AOXLAB

Este documento describe los próximos pasos para la implementación del sistema de gestión de certificaciones. Cada fase representa un hito funcional clave en el flujo de trabajo, desde la creación de solicitudes hasta la emisión de certificados.

---

## 📍 FASE 3: El Corazón de la Aplicación - Creación y Gestión de Solicitudes

**🎯 Objetivo:** Construir el núcleo funcional que permite a un cliente crear, detallar y enviar una solicitud de certificación.

### 🔧 Tareas:
- **Modelos `Solicitud` y `Alcance`:**
  - Definir en `expedientes/models.py`.
  - Migrar a la base de datos.
  - `Solicitud`: vinculada a `Empresa`, incluye `estado`, `fecha_creacion`.
  - `Alcance`: vinculado a `Solicitud`.

- **Creación de Solicitud:**
  - Desde el dashboard del cliente.
  - Estado inicial: `"Borrador"`.

- **Vista de Detalle de la Solicitud:**
  - Página dedicada por solicitud.
  - Permite añadir alcances y recursos.

- **Gestión del Alcance (CRUD):**
  - Añadir, editar y eliminar ítems del alcance (productos, procesos, servicios).

- **Gestión de Recursos por Alcance:**
  - Asociar `PersonaClave`, `EquipoClave`, `DocumentoProceso`.
  - Soporte para carga de archivos.

- **Envío de la Solicitud:**
  - Botón `"Enviar a Revisión"`.
  - Cambia estado y bloquea edición por el cliente.
  - Visible para personal interno.

---

## 🧩 FASE 4: Flujo de Trabajo Interno - Revisión y Planificación

**🎯 Objetivo:** Crear interfaces y lógica para revisión y planificación por parte del personal de AOXLAB.

### 🔧 Tareas:
- **Roles y Permisos:**
  - Crear roles: `"Revisor"`, `"Director de Certificaciones"`.
  - Usar mixins/decoradores para control de acceso.

- **Dashboard del Personal Interno:**
  - Listado de solicitudes en estado `"En Revisión"`.

- **Interfaz de Revisión de Solicitud:**
  - Visualización completa de datos enviados.
  - Marcar ítems como `"Conforme"` / `"No Conforme"`.
  - Añadir observaciones.

- **Lógica de Aprobación/Devolución:**
  - Cambiar estado a `"En Planificación"` o devolver al cliente con observaciones.

---

## 📅 FASE 5: Planificación y Ejecución de la Evaluación

**🎯 Objetivo:** Permitir al Director planificar evaluaciones y a los evaluadores ejecutar tareas asignadas.

### 🔧 Tareas:
- **Módulo de Evaluadores (CRUD):**
  - Gestión de base de datos de evaluadores.

- **Interfaz de Planificación:**
  - Crear actividades como `"Visita en sitio"` o `"Revisión documental"`.
  - Asignar evaluadores y fechas.

- **Dashboard del Evaluador:**
  - Visualización de actividades asignadas.

- **Carga de Evidencias:**
  - Subida de archivos por parte del evaluador.

---

## ✅ FASE 6: Control de Calidad y Decisión Final

**🎯 Objetivo:** Revisar evidencias y tomar decisión final sobre la solicitud.

### 🔧 Tareas:
- **Interfaz de Revisión de Evidencias:**
  - Verificación por parte del Revisor o Director.

- **Flujo de Devolución de Evidencias:**
  - Devolver tareas al evaluador si hay inconsistencias.

- **Decisión Final y Bloqueo:**
  - Acción `"Aprobar Expediente"`.
  - Bloqueo total de la solicitud.

---

## 🏁 FASE 7: Emisión de Certificados y Módulos Finales

**🎯 Objetivo:** Finalizar el ciclo con la emisión de certificados y gestión post-certificación.

### 🔧 Tareas:
- **Generación de Certificado en PDF:**
  - Función que genera PDF con plantilla y datos del alcance aprobado.

- **Módulo de Seguimiento:**
  - Registro y gestión de quejas, amonestaciones y apelaciones.

- **Log de Auditoría:**
  - Verificar que el modelo `Auditoria` registre todas las acciones críticas.

---

> ✍️ Este roadmap está sujeto a ajustes según los avances técnicos y las necesidades del equipo. Cada fase debe ser validada funcionalmente antes de pasar a la siguiente.



