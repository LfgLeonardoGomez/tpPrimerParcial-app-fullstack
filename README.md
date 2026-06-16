# FoodStore — Backend API

**Trabajo Práctico — Programación 4**  
**UTN — Facultad Regional Mendoza**

> Parte del proyecto Food Store TPI Programación 4.  
> Repos relacionados: [Panel Admin](https://github.com/LfgLeonardoGomez/admin-app-food-store-final-) · [Tienda Cliente](https://github.com/LfgLeonardoGomez/store-app-food-store-final)

---

## Integrantes

| Nombre | Apellido |
|--------|----------|
| Leonardo | Gómez |
| Nicolás | Castro |

---

## Descripción del Proyecto

Este repositorio contiene el **backend** de **FoodStore**, una aplicación fullstack de pedidos de comida. La API expone endpoints RESTful para gestionar el catálogo de productos, usuarios, pedidos, direcciones de entrega, pagos y más.

El servidor se encarga de:

- Exponer una API REST segura con autenticación JWT y RBAC (4 roles)
- Gestionar la persistencia de datos con PostgreSQL a través de SQLModel
- Notificar cambios de estado de pedidos en tiempo real vía WebSocket
- Procesar pagos con MercadoPago Checkout PRO
- Gestionar imágenes de productos y categorías en Cloudinary
- Precargar datos iniciales automáticamente al iniciar (seed integrado)
- Aplicar rate limiting en endpoints de autenticación

---

## Tecnologías

| Tecnología | Uso |
|------------|-----|
| **Python 3** | Lenguaje principal |
| **FastAPI** | Framework web para APIs de alto rendimiento |
| **SQLModel** | ORM/Modelado de datos sobre SQLAlchemy |
| **PostgreSQL** | Base de datos relacional |
| **Uvicorn** | Servidor ASGI para ejecutar la aplicación |
| **Pydantic** | Validación y serialización de datos |
| **python-jose** | Manejo de tokens JWT |
| **passlib + bcrypt** | Hashing seguro de contraseñas |
| **WebSocket** | Notificaciones en tiempo real de estados de pedido |
| **Cloudinary** | Almacenamiento y gestión de imágenes |
| **MercadoPago** | Pasarela de pagos (Checkout PRO) |
| **slowapi** | Rate limiting en endpoints de autenticación |
| **python-dotenv** | Carga de variables de entorno desde `.env` |
| **python-multipart** | Soporte para formularios multipart |

---

## Requisitos Previos

- Python 3.10+
- PostgreSQL 15+ corriendo localmente

---

## Instalación

1. **Crear y activar el entorno virtual:**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. **Instalar dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno:**

   ```bash
   cp .env.example .env
   ```

   Completar `.env` con las credenciales de base de datos, Cloudinary y MercadoPago.

---

## Levantar el Servidor

```bash
uvicorn app.main:app --reload
```

- **URL base:** `http://localhost:8000`
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

Las tablas y el seed se ejecutan automáticamente al iniciar.

---

## Credenciales seed

| Rol | Email | Contraseña |
|-----|-------|------------|
| Admin | admin@foodstore.com | admin1234 |
| Stock | stock@foodstore.com | stock1234 |
| Pedidos | pedidos@foodstore.com | pedidos1234 |

---

## Estructura de Módulos

```
app/
├── core/                # Configuración, BD, seed, UoW, WebSocket
├── modules/
│   ├── auth/            # Login, registro, refresh, logout
│   ├── usuarios/        # CRUD usuarios y roles
│   ├── categoria/       # Categorías de productos
│   ├── producto/        # Catálogo de productos
│   ├── ingrediente/     # Ingredientes
│   ├── pedido/          # Gestión de pedidos + WebSocket
│   ├── pago/            # Integración MercadoPago
│   ├── uploads/         # Upload/delete imágenes Cloudinary
│   └── direccioentrega/ # Direcciones de entrega
└── main.py              # Punto de entrada
```

---

## Video de presentación

[Pendiente — se actualizará antes de la entrega]
