from pydantic import BaseModel, ConfigDict
from enum import Enum

class Genero(str, Enum):
    homem_cis = "Homem Cisgênero"
    mulher_cis = "Mulher Cisgênero"
    homem_trans = "Homem Transgênero"
    mulher_trans = "Mulher Transgênero"
    nao_binario = "Não-binário"
    agenero = "Agênero"
    genero_fluido = "Gênero-fluido"
    bigenero = "Bigênero"

class ClientBase(BaseModel):
    name: str
    email: str
    genero: Genero
    endereco: str
    telefone: str

class ClientCreate(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: int

    model_config = ConfigDict(from_attributes=True)