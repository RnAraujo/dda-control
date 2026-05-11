# Sistema de Registro de Derecho de Autor

Sistema integral para la gestión de registro de derechos de autor de productos de software, desarrollado con Django, PostgreSQL y TailwindCSS.

## 📋 Características

- ✅ Registro de participantes con datos personales y documento DNI
- ✅ Registro de productos de software con historial de cambios
- ✅ Gestión de registros de derechos de autor
- ✅ Sistema de pagos flexible (pago único o en cuotas)
- ✅ Exoneración de pagos para casos especiales
- ✅ Vistas públicas y privadas configurables
- ✅ Autenticación de usuarios
- ✅ Dashboard con estadísticas
- ✅ Interfaz moderna con TailwindCSS

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 4.2
- **Base de Datos**: PostgreSQL
- **Frontend**: TailwindCSS
- **Lenguaje**: Python 3.8+

## 📦 Requisitos Previos

- Python 3.8 o superior
- PostgreSQL 12 o superior
- pip (gestor de paquetes de Python)
- Git (opcional)

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/sistema-derecho-autor.git
cd sistema-derecho-autor
```

## Modelo de datos

### Participante

- Datos personales (nombres, apellidos, DNI)
- Información de contacto (email, teléfono)
- Ubicación (dirección, distrito, provincia, departamento, país)
- Documento DNI (PDF)
- Número ORCID (opcional)

### Producto

- Nombre, descripción y versión
- Categoría
- Estado (Borrador, Registrado, En Revisión, Observado, Aprobado, Rechazado)
- Historial de cambios con resoluciones

### Registro

- Relación producto-participante
- Estado del registro
- Exoneración de pagos

### Pagos

-  Planes de pago (cuotas)
-  Registro de pagos
-  Cuotas y comprobantes

## Funcionalidades por Rol

### Administrador

- CRUD completo de participantes
- CRUD completo de productos
- Gestión de registros
- Configuración de planes de pago
- Configuración de vistas públicas
- Visualización de estadísticas

### Participante (Vista Pública)

- Ver productos registrados
- Consultar su portal personal
- Ver estado de sus registros
- Consultar pagos realizados

### Usuario Invitado (Vista Pública)

- Ver productos públicos
- Buscar productos
- Acceso restringido según configuración

## Vistas Públicas

El sistema permite configurar tres modos de visibilidad:

- PÚBLICO: Cualquier persona puede ver los productos registrados
- PRIVADO: Solo participantes registrados pueden acceder
- PROTEGIDO: Requiere código de acceso para ver la información

## Sistema de Pagos

- Configuración de planes de pago (número de cuotas, intereses)
- Registro de pagos por cuota
- Subida de comprobantes de pago
- Seguimiento de saldos pendientes
- Opción de exoneración para casos especiales