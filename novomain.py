from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Dict

app = FastAPI()

# Modelo de dados para Cliente
class Cliente(BaseModel):
    nome: str
    telefone: str
    email: EmailStr

# Dicionário para armazenar os clientes
clientes: Dict[int, Cliente] = {}

# ID inicial para controle dos clientes
current_id = 1

# Criar um novo cliente (Create)
@app.post("/clientes/", status_code=201)
def create_cliente(cliente: Cliente):
    global current_id
    clientes[current_id] = cliente
    cliente_id = current_id
    current_id += 1
    return {"id": cliente_id, "cliente": cliente}

# Obter todos os clientes (Read)
@app.get("/clientes/")
def get_clientes():
    return {"clientes": clientes}

# Obter um cliente específico pelo ID (Read)
@app.get("/clientes/{cliente_id}")
def get_cliente(cliente_id: int):
    if cliente_id not in clientes:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"id": cliente_id, "cliente": clientes[cliente_id]}

# Atualizar um cliente existente (Update)
@app.put("/clientes/{cliente_id}")
def update_cliente(cliente_id: int, cliente: Cliente):
    if cliente_id not in clientes:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    clientes[cliente_id] = cliente
    return {"message": "Cliente atualizado com sucesso", "id": cliente_id, "cliente": cliente}

# Deletar um cliente (Delete)
@app.delete("/clientes/{cliente_id}")
def delete_cliente(cliente_id: int):
    if cliente_id not in clientes:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    del clientes[cliente_id]
    return {"message": f"Cliente com ID {cliente_id} foi deletado com sucesso"}

