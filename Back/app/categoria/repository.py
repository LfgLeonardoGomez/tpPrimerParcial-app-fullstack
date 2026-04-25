from sqlalchemy.orm import joinedload, selectinload
from sqlmodel import select, Session
from app import categoria
from app.categoria.model import Categoria
from app.categoria.schema import CategoriaCreate, CategoriaUpdate
from app.producto.model import Producto

class CategoriaRepository:
    def __init__(self, session: Session):
        self.session = session

    # def get_by_id(self, categoria_id: int) -> Categoria:
    #     statement = select(Categoria).where(Categoria.id == categoria_id, Categoria.disponible == True
    #                 ).options(selectinload(Categoria.productos).where(Producto.disponible == True))
    #     return self.session.exec(statement).first()
    
    # def get_all(self, offset:int=0, limit:int=100) -> list[Categoria]:
    #     statement = select(Categoria).offset(offset).limit(limit).where(
    #     Categoria.disponible == True
    #         ).order_by(Categoria.id).options(
    #     joinedload(Categoria.productos).where(Producto.disponible == True)
    #         )
    #     return self.session.exec(statement).all()
    
    def get_all(self, offset:int=0, limit:int=100) -> list[Categoria]:
        statement = select(Categoria).offset(offset).limit(limit).where(
        Categoria.disponible == True
        ).order_by(Categoria.id).options(
        selectinload(Categoria.productos)
        )
        categorias = self.session.exec(statement).all()
    
    # Filtrar productos eliminados en Python
        for categoria in categorias:
            categoria.productos = [p for p in categoria.productos if p.disponible]
    
        return categorias

    def get_by_id(self, categoria_id: int) -> Categoria:
        statement = select(Categoria).where(
            Categoria.id == categoria_id, 
            Categoria.disponible == True
            ).options(
            selectinload(Categoria.productos)
            )
        categoria = self.session.exec(statement).first()
    
    # Filtrar productos eliminados
        if categoria:
            categoria.productos = [p for p in categoria.productos if p.disponible]
    
        return categoria

    def get_by_nombre(self, nombre: str) -> Categoria:
        statement = select(Categoria).where(Categoria.nombre == nombre)
        return self.session.exec(statement).first()
    
    def create(self, categoria: Categoria) -> Categoria:
        self.session.add(categoria)
        self.session.flush()
        self.session.refresh(categoria)
        return categoria
    
    def update(self, categoria: CategoriaUpdate) -> Categoria:
        # categoria = self.get_by_id(categoria_id)
        # if not categoria:
        #     return None

        self.session.add(categoria)
        self.session.flush()
        self.session.refresh(categoria)
        return categoria
    
    def delete(self, categoria_id: int) -> None:
        categoria = self.get_by_id(categoria_id)
        if not categoria:
            raise ValueError("Categoria no encontrada")
        categoria.disponible = False
        self.session.add(categoria)
        self.session.flush()
        self.session.refresh(categoria)
        return categoria