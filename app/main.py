from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

BASE_URL = "https://jsonplaceholder.typicode.com/posts"


@app.get("/data")
def listar_dados():
    """Lista todos os dados da API externa"""
    response = requests.get(BASE_URL)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Erro ao buscar dados externos")
    return response.json()


@app.get("/data/{item_id}")
def buscar_dado(item_id: int):
    """Busca um dado pelo ID"""
    response = requests.get(f"{BASE_URL}/{item_id}")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    elif response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Erro ao buscar dado externo")
    return response.json()


@app.post("/data")
def criar_dado(item: dict):
    """Cria um novo dado via API externa"""
    if not item.get("title") or not item.get("body") or not item.get("userId"):
        raise HTTPException(status_code=400, detail="Dados inválidos")
    response = requests.post(BASE_URL, json=item)
    if response.status_code != 201:
        raise HTTPException(status_code=response.status_code, detail="Erro ao criar dado externo")
    return response.json()
