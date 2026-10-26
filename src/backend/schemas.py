from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from enum import Enum

Base = declarative_base()

class Genero(str, Enum):
    homem_cis = "Homem Cisgênero"
    mulher_cis = "Mulher Cisgênero"
    homem_trans = "Homem Transgênero"
    mulher_trans = "Mulher Transgênero"
    nao_binario = "Não-binário"
    agenero = "Agênero"
    genero_fluido = "Gênero-fluido"
    bigenero = "Bigênero"

class ClientResponse(BaseModel):
    id: int
    name: str
    email: str
    genero: Genero
    endereco: str
    telefone: str

    class Config:
        from_attributes = True

class Clients(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    genero = Column(String, index=True)
    endereco = Column(String, index=True)
    telefone = Column(String, index=True)

class ClientCreate(BaseModel):
    name: str
    email: str
    genero: Genero
    endereco: str
    telefone: str