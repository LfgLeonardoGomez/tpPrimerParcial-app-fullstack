
from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from app.core.limiter import limiter
from app.modules.categoria.router import router as categoria_router
from app.modules.producto.router import router as producto_router
from app.modules.ingrediente.router import router as ingrediente_router
from app.modules.usuarios.router import router as usuario_router
from app.modules.direccioentrega.router import router as direccionentrega_router
from app.detallepedido.router import router as detalle_pedido_router
from app.modules.pedido.router import router as pedido_router
from app.modules.uploads.router import router as uploads_router
from app.modules.pago.router import router as pagos_router
from app.core.database import create_db_and_tables
from app.core.seed import seed_data
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware




@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    seed_data()

    yield

app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categoria_router)
app.include_router(producto_router)
app.include_router(ingrediente_router)
app.include_router(usuario_router)
app.include_router(direccionentrega_router)
app.include_router(detalle_pedido_router)
app.include_router(pedido_router)
app.include_router(uploads_router)
app.include_router(pagos_router)

# ─── Favicon ──────────────────────────────────────────────────────────────────
# Evita el error 404 en navegadores que piden /favicon.ico automáticamente.
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    # Responde con contenido vacío y content-type image/x-icon
    return Response(content=b"", media_type="image/x-icon")

# ─── Raíz → redirige al KDS ──────────────────────────────────────────────────
# Para que el usuario acceda directamente al Dashboard de Cocina
# abriendo http://localhost:8000 sin recordar la ruta exacta.
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


# ─── Health check ────────────────────────────────────────────────────────────
# Endpoint de verificación para monitoreo (load balancers, Docker healthcheck).
@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "version": "1.0.0"}

# ─── Debug: rooms activas del ConnectionManager ──────────────────────────────
# Muestra qué sockets están en cada room. Útil para verificar que el cajero
# esté en role:pedidos antes de hacer pruebas de WS.
@app.get("/debug/ws-rooms", tags=["debug"])
def ws_rooms():
    from app.core.websocket import manager
    return {
        "total_connections": manager.get_active_connections_count(),
        "rooms": manager.get_rooms_info(),
    }
