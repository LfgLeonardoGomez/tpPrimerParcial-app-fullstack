from sqlalchemy.orm import selectinload
from sqlmodel import select, Session
from app.ingrediente.model import Ingrediente
from app.ingrediente.schema import IngredienteCreate, IngredienteUpdate

class IngredienteRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, ingrediente_id: int):
        statement = select(Ingrediente).where(Ingrediente.id == ingrediente_id
                    ).options(selectinload(Ingrediente.productos))
        return self.session.exec(statement).first()
    
    def get_all(self, offset:int=0, limit:int=100) -> list[Ingrediente]:
        statement = select(Ingrediente).offset(offset).limit(limit).where(Ingrediente.disponible == True).order_by(Ingrediente.id)
        return self.session.exec(statement).all()
    
    def get_by_nombre(self, nombre: str) -> Ingrediente:
        statement = select(Ingrediente).where(Ingrediente.nombre == nombre)
        return self.session.exec(statement).first()
    
    def create(self, ingrediente: Ingrediente) -> Ingrediente:
        self.session.add(ingrediente)
        self.session.flush()
        self.session.refresh(ingrediente)
        return ingrediente
    
    def update(self,ingrediente: IngredienteUpdate) -> Ingrediente:
        self.session.add(ingrediente)
        self.session.flush()
        self.session.refresh(ingrediente)
        return ingrediente
    
    def delete(self, ingrediente_id: int) -> None:
        ingrediente = self.get_by_id(ingrediente_id)
        if not ingrediente:
            raise ValueError("Ingrediente no encontrado")
        ingrediente.disponible = False
        self.session.add(ingrediente)
        self.session.flush()
        self.session.refresh(ingrediente)
        return ingrediente
    
    