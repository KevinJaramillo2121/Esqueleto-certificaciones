# AOXLAB - Aplicativo para la Gestión de Expedientes de Certificación

## 1. Descripción del Proyecto

**AOXLAB** es una plataforma web diseñada para la administración integral del ciclo de vida de los procesos de certificación de productos, procesos y servicios. El sistema centraliza y gestiona la información desde la solicitud inicial de un cliente hasta la emisión del certificado y su seguimiento posterior, mejorando la trazabilidad, eficiencia y comunicación entre todas las partes involucradas [1].

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

