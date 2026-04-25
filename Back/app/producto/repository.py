from sqlalchemy.orm import selectinload
from sqlmodel import select, Session
from app import producto
from app.categoria.model import Categoria
from app.ingrediente.model import Ingrediente
from app.producto.model import Producto
from app.producto.schema import ProductoCreate, ProductoUpdate

class ProductoRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, producto_id: int)-> Producto: 
        statement = select(Producto).where(
            Producto.id == producto_id, 
            Producto.disponible == True
        ).options(
            selectinload(Producto.categorias),
            selectinload(Producto.ingredientes)
    )
        producto = self.session.exec(statement).first()
    
    # Filtrar categorías e ingredientes eliminados
        if producto:
            producto.categorias = [c for c in producto.categorias if c.disponible]
            producto.ingredientes = [i for i in producto.ingredientes if i.disponible]
    
        return producto

    def get_all(self, offset:int=0, limit:int=100) -> list[Producto]:
        statement = select(Producto).offset(offset).limit(limit).where(
            Producto.disponible == True
        ).order_by(Producto.id).options(
            selectinload(Producto.categorias),
            selectinload(Producto.ingredientes)
    )
        productos = self.session.exec(statement).all()
    
    # Filtrar categorías e ingredientes eliminados para cada producto
        for producto in productos:
            producto.categorias = [c for c in producto.categorias if c.disponible]
            producto.ingredientes = [i for i in producto.ingredientes if i.disponible]
    
        return productos
    
    def get_by_nombre(self, nombre: str) -> Producto:
        statement = select(Producto).where(Producto.nombre == nombre)
        return self.session.exec(statement).first()
    
    def create(self, producto: Producto) -> Producto:
        self.session.add(producto)
        self.session.flush()
        self.session.refresh(producto)
        return producto
    
    def update(self, producto: ProductoUpdate) -> Producto:
        
        self.session.add(producto)
        self.session.flush()
        self.session.refresh(producto)
        return producto
    
    def delete(self, producto_id: int) -> None:
        producto = self.get_by_id(producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")
        producto.disponible = False
        self.session.add(producto)
        self.session.flush()
        self.session.refresh(producto)
        return producto
    
    def update_categorias(self, producto : Producto, categorias: list[Categoria]) -> Producto:
        producto.categorias = categorias
        self.session.add(producto)
        self.session.flush()
        self.session.refresh(producto)
        return producto
    
    def update_ingredientes(self, producto: Producto, ingredientes: list[Ingrediente]) -> Producto:
        producto.ingredientes = ingredientes
        self.session.add(producto)
        self.session.flush()
        self.session.refresh(producto)
        return producto
        