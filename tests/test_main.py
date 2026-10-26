import sys
import os

path_backend = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "backend"))

sys.path.insert(0, path_backend)

from src.backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

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

    assert response_post.status_code == 200

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
