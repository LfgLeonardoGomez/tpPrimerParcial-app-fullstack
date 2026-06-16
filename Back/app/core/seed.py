from app.core.security import hash_password
from app.core.uow import UnitOfWork
from app.rol.model import Rol
from app.modules.usuarios.model import Usuario
from app.formadepago.model import FormaDePago
from app.estadopedido.model import EstadoPedido


ROLES_BASE = [
    {
        "codigo": "ADMIN",
        "nombre": "Administrador",
        "descripcion": "Acceso completo al sistema",
    },
    {
        "codigo": "STOCK",
        "nombre": "Stock",
        "descripcion": "Gestión de productos, ingredientes y stock",
    },
    {
        "codigo": "PEDIDOS",
        "nombre": "Pedidos",
        "descripcion": "Gestión de pedidos del sistema",
    },
    {
        "codigo": "CLIENT",
        "nombre": "Cliente",
        "descripcion": "Usuario cliente del sistema",
    },
]


FORMAS_PAGO_BASE = [
    {
        "codigo": "EFECTIVO",
        "nombre": "Efectivo",
        "descripcion": "Pago en efectivo contra entrega",
    },
    {
        "codigo": "MERCADOPAGO",
        "nombre": "MercadoPago",
        "descripcion": "Pago a través de MercadoPago",
    },
    {
        "codigo": "TRANSFERENCIA",
        "nombre": "Transferencia bancaria",
        "descripcion": "Transferencia bancaria directa",
    },
]


ESTADOS_PEDIDO_BASE = [
    {
        "codigo": "PENDIENTE",
        "descripcion": "Pedido recibido, esperando confirmación",
        "orden": 1,
        "es_terminal": False,
    },
    {
        "codigo": "CONFIRMADO",
        "descripcion": "Pedido confirmado, en preparación",
        "orden": 2,
        "es_terminal": False,
    },
    {
        "codigo": "EN_PREP",
        "descripcion": "Pedido en preparación en cocina",
        "orden": 3,
        "es_terminal": False,
    },
    {
        "codigo": "LISTO",
        "descripcion": "Pedido listo para retirar o entregar",
        "orden": 4,
        "es_terminal": False,
    },
    {
        "codigo": "ENTREGADO",
        "descripcion": "Pedido entregado exitosamente",
        "orden": 5,
        "es_terminal": True,
    },
    {
        "codigo": "CANCELADO",
        "descripcion": "Pedido cancelado",
        "orden": 6,
        "es_terminal": True,
    },
]


def seed_roles() -> None:
    with UnitOfWork() as uow:
        for rol_data in ROLES_BASE:
            rol_existente = uow.roles.get_by_codigo(rol_data["codigo"])

            if rol_existente:
                continue

            rol = Rol(
                codigo=rol_data["codigo"],
                nombre=rol_data["nombre"],
                descripcion=rol_data["descripcion"],
            )

            uow.session.add(rol)


def seed_formas_pago() -> None:
    with UnitOfWork() as uow:
        for fp_data in FORMAS_PAGO_BASE:
            fp_existente = uow.formas_pago.get_forma_de_pago_by_codigo(fp_data["codigo"])

            if fp_existente:
                continue

            fp = FormaDePago(
                codigo=fp_data["codigo"],
                nombre=fp_data["nombre"],
                descripcion=fp_data["descripcion"],
            )

            uow.session.add(fp)


def seed_estados_pedido() -> None:
    with UnitOfWork() as uow:
        for estado_data in ESTADOS_PEDIDO_BASE:
            estado_existente = uow.estadopedido.get_by_codigo(estado_data["codigo"])

            if estado_existente:
                continue

            estado = EstadoPedido(
                codigo=estado_data["codigo"],
                descripcion=estado_data["descripcion"],
                orden=estado_data["orden"],
                es_terminal=estado_data["es_terminal"],
            )

            uow.session.add(estado)


def seed_admin() -> None:
    with UnitOfWork() as uow:
        admin_existente = uow.usuarios.get_by_email("admin@foodstore.com")

        if admin_existente:
            return

        rol_admin = uow.roles.get_by_codigo("ADMIN")

        if not rol_admin:
            raise RuntimeError("No existe el rol ADMIN. Ejecutá seed_roles primero.")

        admin = Usuario(
            nombre="Admin",
            apellido="Sistema",
            email="admin@foodstore.com",
            celular="0000000000",
            password_hashed=hash_password("admin1234"),
            disabled=False,
            roles=[rol_admin],
        )

        uow.session.add(admin)



        # Credenciales del admin:
        # email: admin@foodstore.com
        # password: admin1234

def seed_test_users() -> None:
    with UnitOfWork() as uow:
        usuarios_test = [
            {
                "email": "stock@foodstore.com",
                "password": "stock1234",
                "nombre": "Juan",
                "apellido": "Stock",
                "rol": "STOCK"
            },
            {
                "email": "pedidos@foodstore.com",
                "password": "pedidos1234",
                "nombre": "Maria",
                "apellido": "Pedidos",
                "rol": "PEDIDOS"
            },
        ]

        for u in usuarios_test:
            if uow.usuarios.get_by_email(u["email"]):
                continue

            rol = uow.roles.get_by_codigo(u["rol"])
            nuevo = Usuario(
                nombre=u["nombre"],
                apellido=u["apellido"],
                email=u["email"],
                celular="0000000000",
                password_hashed=hash_password(u["password"]),
                disabled=False,
                roles=[rol],
            )
            uow.session.add(nuevo)

def seed_data() -> None:
    seed_roles()
    seed_formas_pago()
    seed_estados_pedido()
    seed_admin()
    seed_test_users()