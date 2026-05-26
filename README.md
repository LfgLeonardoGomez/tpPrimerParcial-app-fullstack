# FoodStore — Backend API

*Trabajo Práctico — Programación 4*  
*UTN — Facultad Regional Mendoza*

---

## Integrantes

| Nombre | Apellido |
|--------|----------|
| Leonardo | Gómez |
| Nicolás | Castro |

---

## Descripción del Proyecto

Este repositorio contiene el *backend* de *FoodStore*, una aplicación fullstack de pedidos de comida. La API expone endpoints RESTful para gestionar el catálogo de productos (pizzas, empanadas, hamburguesas, bebidas), usuarios, pedidos, direcciones de entrega, estados de pedido, historial de cambios, formas de pago y más.

El servidor se encarga de:

- Exponer una API REST segura con autenticación JWT.
- Gestionar la persistencia de datos con PostgreSQL a través de SQLModel.
- Precargar automáticamente el catálogo de productos al iniciar (seed integrado).
- Habilitar CORS para comunicación con el frontend en desarrollo.

---

## Tecnologías

| Tecnología | Uso |
|------------|-----|
| *Python 3* | Lenguaje principal |
| *FastAPI* | Framework web para APIs de alto rendimiento |
| *SQLModel* | ORM/Modelado de datos sobre SQLAlchemy |
| *PostgreSQL* | Base de datos relacional |
| *Uvicorn* | Servidor ASGI para ejecutar la aplicación |
| *Pydantic* | Validación y serialización de datos |
| *python-jose* | Manejo de tokens JWT |
| *passlib + bcrypt* | Hashing seguro de contraseñas |
| *python-dotenv* | Carga de variables de entorno desde .env |
| *python-multipart* | Soporte para formularios multipart |

---

## Requisitos Previos

- Python 3.10+ instalado
- PostgreSQL corriendo localmente (o accesible remotamente)
- Variables de entorno configuradas en un archivo .env en la raíz del proyecto

---

## Instalación

1. *Crear y activar el entorno virtual:*

   bash
   python -m venv .venv
   .venv\Scripts\activate
   

2. *Instalar dependencias:*

   bash
   pip install -r requirements.txt
   

3. *Configurar variables de entorno:*

   Crear un archivo .env en la raíz con los datos de conexión a la base de datos y demás configuraciones necesarias.

---

## Levantar el Servidor

Desde la raíz del proyecto, ejecutar:

bash
uvicorn app.main:app --reload


Por defecto, el servidor estará disponible en:

- *URL base:* http://127.0.0.1:8000
- *Documentación interactiva (Swagger UI):* http://127.0.0.1:8000/docs
- *Documentación alternativa (ReDoc):* http://127.0.0.1:8000/redoc

---

## Seed de Datos

El proyecto incluye un *seed automático* que se ejecuta al levantar el servidor. Esto significa que:

- Las tablas se crean automáticamente si no existen.
- El catálogo inicial de productos (pizzas, empanadas, hamburguesas y bebidas) se precarga solo al iniciar la aplicación.

No es necesario correr ningún script extra.

---

## Estructura de Módulos


app/
├── categoria/           # Gestión de categorías de productos
├── core/                # Configuración central, base de datos, seed, UoW
├── db/                  # Scripts y utilidades de base de datos
├── detallepedido/       # Líneas de detalle de cada pedido
├── direccioentrega/     # Direcciones de entrega de los usuarios
├── estadopedido/        # Estados posibles de un pedido
├── formadepago/         # Medios de pago disponibles
├── historialestadopedido/  # Historial de cambios de estado
├── ingrediente/         # Ingredientes y su stock
├── main.py              # Punto de entrada de la aplicación
├── pedido/              # Gestión de pedidos
├── producto/            # Catálogo de productos
├── rol/                 # Roles de usuario
└── usuarios/            # Gestión de usuarios y autenticación


---

## Licencia

Proyecto académico — UTN FRM, Programación 4.

## Video de presentación

Link al video explicativo del proyecto:

https://youtu.be/4odNGl1uBh0
