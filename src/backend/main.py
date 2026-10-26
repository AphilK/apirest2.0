import os
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from schemas import Clients, ClientCreate, Base

USERNAME = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE = os.getenv("POSTGRES_DB")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/clients/")
async def create_clients(client_data: ClientCreate):
    db = SessionLocal()
    db_client = Clients(
        name = client_data.name,
        email = client_data.email,
        genero = client_data.genero.value,
        endereco = client_data.endereco,
        telefone = client_data.telefone
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@app.get("/clients/{client_id}")
async def get_clients(client_id: int):
    db = SessionLocal()
    client = db.query(Clients).filter(Clients.id == client_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    return client

@app.put("/clients/{client_id}")
async def update_clients(client_id: int, client_data: ClientCreate):
    db = SessionLocal()
    client = db.query(Clients).filter(Clients.id == client_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    client.name = client_data.name
    client.email = client_data.email
    client.genero = client_data.genero
    client.endereco = client_data.endereco
    client.telefone = client_data.telefone

    db.commit()
    return client

@app.delete("/clients/{client_id}")
async def delete_client(client_id: int):
    db = SessionLocal()
    client = db.query(Clients).filter(Clients.id == client_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    client_name = client.name
    db.delete(client)
    db.commit()
    return {"Message": "Client {client_name} deleted succesfully"}
