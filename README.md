# MelquiMarket

## Descripción del Proyecto

MelquiMarket es un sistema de ecommerce diseñado para la gestión de productos y usuarios, orientado a negocios minoristas. Utiliza una arquitectura MVC (Modelo-Vista-Controlador) y está construido con **FastAPI** como backend y **Argon Dashboard** para el frontend. 

Este sistema permite:

- **Gestión de Usuarios**: Creación, actualización y visualización de usuarios. Los roles disponibles son "Administrador" y "Vendedor", con permisos diferenciados para cada uno.
- **Gestión de Productos**: Registro, visualización, edición, eliminación lógica, ventas, devoluciones y reabastecimientos.
- **Autenticación y Autorización**: Utiliza autenticación basada en tokens JWT.
- **Interfaz de Usuario**: Plantillas HTML personalizadas con **Argon Dashboard** que ofrecen un panel administrativo limpio y moderno.

## Estructura del Proyecto

El proyecto sigue la arquitectura MVC, organizada de la siguiente forma:

MelquiMarket/ │ ├── app/ │ ├── config.py │ ├── controllers/ │ │ ├── usuario_controller.py │ │ └── producto_controller.py │ ├── models/ │ │ ├── usuario.py │ │ └── producto.py │ ├── routes/ │ │ ├── auth_routes.py │ │ ├── usuario_routes.py │ │ ├── producto_routes.py │ │ ├── views_routes.py │ │ └── categoria_routes.py │ ├── schemas/ │ │ ├── usuario.py │ │ └── producto.py │ ├── utils/ │ │ └── auth.py │ └── views/ │ ├── dashboard.html │ ├── tablesProducts.html │ ├── tablesUsers.html │ └── SignIn.html │ ├── static/ │ └── argon/ │ ├── assets/ │ │ ├── css/ │ │ ├── js/ │ │ └── img/ │ ├── main.py └── README.md

## Requisitos Previos

Antes de iniciar, asegúrate de tener instalados los siguientes componentes:

- **Python 3.10 o superior**: Necesario para correr el backend.
- **Virtualenv**: Para crear un entorno virtual.
- **Node.js y npm** (opcional): Para manejar dependencias de frontend, si deseas personalizar los scripts.

## Instalación y Configuración del Proyecto

Sigue estos pasos para configurar y ejecutar el proyecto:

1. **Clonar el Repositorio**:

   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd MelquiMarket


Crear un Entorno Virtual:

python -m venv venv

Activar el Entorno Virtual:

    En Windows:

venv\Scripts\activate

En Linux/Mac:

    source venv/bin/activate

Instalar las Dependencias:

pip install -r requirements.txt

Si requirements.txt no existe, instala las dependencias principales:

pip install fastapi uvicorn sqlalchemy pydantic passlib bcrypt jinja2

Configurar la Base de Datos:

El sistema está configurado para usar SQLite por defecto. Puedes cambiar la configuración en app/config.py para usar otra base de datos si es necesario.

Para crear las tablas en la base de datos, ejecuta:

python main.py

Esto creará automáticamente las tablas especificadas en los modelos.

Levantar el Servidor:

Usa Uvicorn para iniciar el servidor FastAPI:

    uvicorn main:app --reload

    Acceder al Proyecto:
        Interfaz Web: Ve a http://127.0.0.1:8000/ para ver la página de inicio de sesión.
        Swagger UI (Documentación de la API): Puedes acceder a la documentación en http://127.0.0.1:8000/docs.

Uso del Sistema

    Inicio de Sesión: La página principal es el formulario de inicio de sesión (SignIn.html). Los usuarios registrados pueden iniciar sesión con su correo electrónico y contraseña.
    Dashboard: Una vez autenticado, el usuario es redirigido al dashboard.html, donde puede ver información resumida del sistema.
    Productos y Usuarios: En el dashboard hay opciones para gestionar productos y usuarios, accesibles según los permisos del rol del usuario.

Notas Adicionales

    Autenticación: La autenticación se maneja con JWT (JSON Web Tokens). El token de acceso se almacena en el localStorage del navegador y se utiliza para autorizar las peticiones a las rutas protegidas.
    Eliminación Lógica de Productos: Los productos no se eliminan físicamente de la base de datos, sino que se marca su atributo estado como False.
    Roles de Usuario: Existen dos tipos de roles - administrador y vendedor. Los administradores tienen permisos completos para todas las operaciones, mientras que los vendedores tienen acceso limitado (solo pueden gestionar inventario y ventas).

Contacto

Si tienes alguna pregunta o encuentras algún problema, puedes contactarnos a través del correo proporcionado en la sección de ayuda del dashboard.
