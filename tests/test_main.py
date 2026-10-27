import os
import pytest
import redis.asyncio as aioredis
from fastapi.testclient import TestClient
from src.backend.main import app

client = TestClient(app)

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASS = os.getenv("REDIS_PASS")

if REDIS_PASS:
    REDIS_URL = f"redis://:{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}/0"
else:
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

def test_crud_client():
    response_post = client.post(
        url="/clients/", 
        json={"name":"test_name", 
              "email":"test_email", 
              "genero":"Homem Cisgênero", 
              "endereco":"test_endereco", 
              "telefone":"test_telefone"
            }
    )

    assert response_post.status_code == 201

    created_id = response_post.json()["id"]

    response_get = client.get(url=f"/clients/{created_id}")
    assert response_get.status_code == 200
    assert response_get.json() == response_post.json()

    response_put = client.put(url=f"/clients/{created_id}",
                                json={"name":"change_test", 
                                    "email":"change_test", 
                                    "genero":"Mulher Cisgênero", 
                                    "endereco":"change_test", 
                                    "telefone":"change_test"
                                }
                            )

    assert response_put.status_code == 200

    response_delete = client.delete(url=f"/clients/{created_id}")
    assert response_delete.status_code == 200
    assert "Message" in response_delete.json()

def test_create_bad_client():
    response = client.post(
            url="/clients/", 
            json={"name":1, 
                  "email":2, 
                  "genero":"genero", 
                  "endereco":True, 
                  "telefone":774586
                }
        )

    assert response.status_code == 422
    assert "detail" in response.json()

def test_get_nao_existe():
    response = client.get(
        url="/clients/999999999999"
    )

    assert response.status_code == 404
    assert "detail" in response.json()

def test_bad_delete_client():
    response = client.delete(
        url="/clients/999999999999"
    )

    assert response.status_code == 404
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_redis_cache():
    r = aioredis.from_url(REDIS_URL, decode_responses=True)

    try:
        payload = {
            "name": "Maria Silva",
            "email": "maria@example.com",
            "genero": "Mulher Cisgênero",
            "endereco": "Rua A, 123",
            "telefone": "75999999999"
        }

        response_post = client.post("/clients/", json=payload)  
        assert response_post.status_code == 201
        client_id = response_post.json()["id"]
        cache_key = f"client:{client_id}"

        assert await r.get(cache_key) is None

        response_get = client.get(f"/clients/{client_id}")
        assert response_get.status_code == 200

        cached_data = await r.get(cache_key)
        assert cached_data is not None
        assert isinstance(cached_data, str)
        assert "Maria Silva" in cached_data

        update_payload = {**payload, "name": "Maria Silva Alterada"}
        response_put = client.put(f"/clients/{client_id}", json=update_payload)
        assert response_put.status_code == 200

        assert await r.get(cache_key) is None

        client.get(f"/clients/{client_id}")
        assert await r.get(cache_key) is not None

        response_delete = client.delete(f"/clients/{client_id}")
        assert response_delete.status_code == 200

        assert await r.get(cache_key) is None
    finally:
        await r.aclose()