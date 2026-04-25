from sqlmodel import Session
from app.core.database import get_engine
from app.categoria.repository import CategoriaRepository
from app.ingrediente.repository import IngredienteRepository
from app.producto.repository import ProductoRepository

class UnitOfWork:
    def __init__(self):
        engine = get_engine()
        self.session: Session = Session(engine)

    def __enter__(self) -> "UnitOfWork":
        self.categorias = CategoriaRepository(self.session)
        self.productos = ProductoRepository(self.session)
        self.ingredientes = IngredienteRepository(self.session)
        # Aquí irían más repositorios: self.productos = ProductoRepository(...)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()