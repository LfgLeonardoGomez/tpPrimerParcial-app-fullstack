
from fastapi import FastAPI
from app.categoria.router import router as categoria_router
from app.producto.router import router as producto_router
from app.ingrediente.router import router as ingrediente_router
from app.core.database import create_db_and_tables
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from seed import seed_productos


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    #seed_productos()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categoria_router)
app.include_router(producto_router)
app.include_router(ingrediente_router)