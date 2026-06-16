from app.core.uow import UnitOfWork
from app.modules.producto.model import Producto



PRODUCTOS_SEED = [
    # PIZZAS
    {
        "nombre": "Pizza Muzzarella",
        "descripcion": "Pizza clásica de muzzarella con salsa de tomate y orégano",
        "precio_base": "12000",
        "stock_cantidad": 20,
        "imagen_url": "https://example.com/pizza-muzzarella.jpg",
        "disponible": True
    },
    {
        "nombre": "Pizza Napolitana",
        "descripcion": "Pizza con tomate fresco, ajo y muzzarella",
        "precio_base": "13500",
        "stock_cantidad": 15,
        "imagen_url": "https://example.com/pizza-napolitana.jpg",
        "disponible": True
    },
    {
        "nombre": "Pizza Fugazzeta",
        "descripcion": "Pizza rellena con cebolla y abundante queso",
        "precio_base": "15000",
        "stock_cantidad": 12,
        "imagen_url": "https://example.com/pizza-fugazzeta.jpg",
        "disponible": True
    },
    {
        "nombre": "Pizza Especial",
        "descripcion": "Pizza con jamón, morrón y aceitunas",
        "precio_base": "16000",
        "stock_cantidad": 10,
        "imagen_url": "https://example.com/pizza-especial.jpg",
        "disponible": True
    },
    {
        "nombre": "Pizza Calabresa",
        "descripcion": "Pizza con longaniza calabresa y muzzarella",
        "precio_base": "15500",
        "stock_cantidad": 8,
        "imagen_url": "https://example.com/pizza-calabresa.jpg",
        "disponible": True
    },

    # EMPANADAS
    {
        "nombre": "Empanada de Carne",
        "descripcion": "Empanada tradicional de carne cortada a cuchillo",
        "precio_base": "1800",
        "stock_cantidad": 50,
        "imagen_url": "https://example.com/empanada-carne.jpg",
        "disponible": True
    },
    {
        "nombre": "Empanada de Jamon y Queso",
        "descripcion": "Empanada rellena de jamón cocido y queso",
        "precio_base": "1700",
        "stock_cantidad": 45,
        "imagen_url": "https://example.com/empanada-jq.jpg",
        "disponible": True
    },
    {
        "nombre": "Empanada de Pollo",
        "descripcion": "Empanada con pollo desmenuzado y condimentos",
        "precio_base": "1750",
        "stock_cantidad": 40,
        "imagen_url": "https://example.com/empanada-pollo.jpg",
        "disponible": True
    },
    {
        "nombre": "Empanada Caprese",
        "descripcion": "Empanada de tomate, albahaca y muzzarella",
        "precio_base": "1700",
        "stock_cantidad": 35,
        "imagen_url": "https://example.com/empanada-caprese.jpg",
        "disponible": True
    },
    {
        "nombre": "Empanada Arabe",
        "descripcion": "Empanada abierta con carne especiada y limón",
        "precio_base": "1900",
        "stock_cantidad": 30,
        "imagen_url": "https://example.com/empanada-arabe.jpg",
        "disponible": True
    },

    # HAMBURGUESAS
    {
        "nombre": "Hamburguesa Clasica",
        "descripcion": "Hamburguesa con carne, lechuga, tomate y queso",
        "precio_base": "9500",
        "stock_cantidad": 20,
        "imagen_url": "https://example.com/burger-clasica.jpg",
        "disponible": True
    },
    {
        "nombre": "Hamburguesa Doble",
        "descripcion": "Doble medallón de carne con cheddar y panceta",
        "precio_base": "12500",
        "stock_cantidad": 15,
        "imagen_url": "https://example.com/burger-doble.jpg",
        "disponible": True
    },
    {
        "nombre": "Hamburguesa BBQ",
        "descripcion": "Hamburguesa con salsa barbacoa, cheddar y bacon",
        "precio_base": "11800",
        "stock_cantidad": 12,
        "imagen_url": "https://example.com/burger-bbq.jpg",
        "disponible": True
    },
    {
        "nombre": "Hamburguesa Criolla",
        "descripcion": "Hamburguesa con huevo, jamón y queso",
        "precio_base": "11000",
        "stock_cantidad": 10,
        "imagen_url": "https://example.com/burger-criolla.jpg",
        "disponible": True
    },
    {
        "nombre": "Hamburguesa Veggie",
        "descripcion": "Hamburguesa de lentejas con vegetales frescos",
        "precio_base": "9800",
        "stock_cantidad": 8,
        "imagen_url": "https://example.com/burger-veggie.jpg",
        "disponible": True
    },

    # BEBIDAS
    {
        "nombre": "Coca Cola 1.5L",
        "descripcion": "Gaseosa Coca Cola retornable de 1.5 litros",
        "precio_base": "3500",
        "stock_cantidad": 60,
        "imagen_url": "https://example.com/coca.jpg",
        "disponible": True
    },
    {
        "nombre": "Sprite 1.5L",
        "descripcion": "Gaseosa Sprite sabor lima limón",
        "precio_base": "3400",
        "stock_cantidad": 55,
        "imagen_url": "https://example.com/sprite.jpg",
        "disponible": True
    },
    {
        "nombre": "Agua Mineral",
        "descripcion": "Botella de agua mineral sin gas 1.5 litros",
        "precio_base": "2500",
        "stock_cantidad": 70,
        "imagen_url": "https://example.com/agua.jpg",
        "disponible": True
    },
    {
        "nombre": "Cerveza Lata",
        "descripcion": "Cerveza rubia en lata de 473ml",
        "precio_base": "3000",
        "stock_cantidad": 40,
        "imagen_url": "https://example.com/cerveza.jpg",
        "disponible": True
    },
    {
        "nombre": "Fernet con Coca",
        "descripcion": "Combo de Fernet y Coca Cola",
        "precio_base": "8500",
        "stock_cantidad": 25,
        "imagen_url": "https://example.com/fernet.jpg",
        "disponible": True
    }
]


def seed_productos():
    with UnitOfWork() as uow:
        productos_existentes = uow.productos.get_all(limit=1)

        if productos_existentes:
            print("Productos ya cargados.")
            return

        for data in PRODUCTOS_SEED:
            producto = Producto(**data)
            uow.productos.create(producto)

        print("Productos iniciales cargados correctamente.")