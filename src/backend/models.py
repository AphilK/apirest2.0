from sqlalchemy.orm import Mapped, mapped_column   
from src.backend.database import Base

class ClientModel(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True, nullable=False)
    email: Mapped[str] = mapped_column(index=True, nullable=False)
    genero: Mapped[str] = mapped_column(index=True, nullable=False)
    endereco: Mapped[str] = mapped_column(index=True, nullable=False)
    telefone: Mapped[str] = mapped_column(index=True, nullable=False)
