from fastapi import FastAPI

app = FastAPI()
#uvicorn main:app --reload
# Rota inicial (endpoint raiz)
@app.get("/")
def bem_vindo():
    return {"message": "Bem-vindo à API FastAPI!"}

# Rota para obter informações por meio de parâmetros na URL
@app.get("/items/{item_id}")
def ler_item(item_id: int, query_param: str = None):
    return {"item_id": item_id, "query_param": query_param}


# Rota para criar um novo item (POST)
@app.post("/items/")
def create_item(item: dict):
    return {"message": "Item criado com sucesso!", "item": item}

# Rota para atualizar um item (PUT)
@app.put("/items/{item_id}")
def update_item(item_id: int, item: dict):
    return {"message": "Item atualizado com sucesso!", "item_id": item_id, "item": item}

# Rota para deletar um item (DELETE)
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": f"Item {item_id} deletado com sucesso!"}

