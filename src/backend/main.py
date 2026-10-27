from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
import redis.asyncio as aioredis

from src.backend.database import engine, Base, get_db
from src.backend.models import ClientModel
from src.backend.schemas import ClientCreate, ClientResponse
from src.backend.redis_client import get_redis

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Rest 2.0")

CACHE_EXPIRE_SECONDS = 120

@app.post("/clients/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_clients(client_data: ClientCreate, db: Session = Depends(get_db)):
    db_client = ClientModel(
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

@app.get("/clients/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: int, 
    db: Session = Depends(get_db), 
    redis: aioredis.Redis = Depends(get_redis)
):
    cache_key = f"client:{client_id}"

    cached_client = await redis.get(cache_key)
    if cached_client:
        return ClientResponse.model_validate_json(cached_client)

    client = db.query(ClientModel).filter(ClientModel.id == client_id).first()

    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")

    client_response = ClientResponse.model_validate(client)

    await redis.set(cache_key, client_response.model_dump_json(), ex=CACHE_EXPIRE_SECONDS)

    return client_response

@app.put("/clients/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: int, 
    client_data: ClientCreate, 
    db: Session = Depends(get_db), 
    redis: aioredis.Redis = Depends(get_redis)
):
    client = db.query(ClientModel).filter(ClientModel.id == client_id).first()

    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")

    client.name = client_data.name
    client.email = client_data.email
    client.genero = client_data.genero
    client.endereco = client_data.endereco
    client.telefone = client_data.telefone

    db.commit()
    db.refresh(client)

    cache_key = f"client:{client_id}"
    await redis.delete(cache_key)

    return client

@app.delete("/clients/{client_id}")
async def delete_client(
    client_id: int, 
    db: Session = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis)
):
    client = db.query(ClientModel).filter(ClientModel.id == client_id).first()

    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")

    client_name = client.name
    message = f"Client {client_name} deletado com sucesso!"

    db.delete(client)
    db.commit()

    cache_key = f"client:{client_id}"
    await redis.delete(cache_key)

    return {"Message": message}