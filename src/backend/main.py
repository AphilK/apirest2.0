import os
from enum import Enum
from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

USERNAME = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE = os.getenv("POSTGRES_DB")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
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

class Clients(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    genero = Column(String, index=True)
    endereco = Column(String, index=True)
    telefone = Column(String, index=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/clients/")
async def create_clients(name: str, email: str, genero: Genero, endereco: str, telefone: str):
    db = SessionLocal()
    db_client = Clients(name=name, email=email, genero=genero, endereco=endereco, telefone=telefone)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@app.get("/clients/{client_id}")
async def get_clients(client_id: int):
    db = SessionLocal()
    client = db.query(Clients).filter(Clients.id == client_id).first()
    return client

@app.put("/clients/{client_id}")
async def update_clients(client_id: int, name: str, email: str, genero: Genero, endereco: str, telefone: str):
    db = SessionLocal()
    client = db.query(Clients).filter(Clients.id == client_id).first()
    client.name = name
    client.email = email
    client.genero = genero
    client.endereco = endereco
    client.telefone = telefone
    db.commit()
    return client

@app.delete("/clients/{client_id}")
async def delete_client(client_id: int):
    db = SessionLocal()
    client = db.query(Clients).filter(Clients.id == client_id).first()
    client_name = client.name
    db.delete(client)
    db.commit()
    return {"Message": "Client {client_name} deleted succesfully"}
