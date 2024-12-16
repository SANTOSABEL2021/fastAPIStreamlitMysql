from fastapi import FastAPI
import httpx

app = FastAPI()

# URL da API pública
API_BASE_URL = "https://jsonplaceholder.typicode.com"

@app.get("/posts/")
async def get_posts():
    """
    Retorna uma lista de posts obtidos da API pública.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/posts")
        # Checa se a requisição foi bem-sucedida
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Não foi possível obter os posts da API."}

@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    """
    Retorna um post específico baseado no ID, obtido da API pública.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/posts/{post_id}")
        # Checa se a requisição foi bem-sucedida
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Post com ID {post_id} não encontrado."}

@app.get("/cep/{nr_cep}")
async def pegar_cep(nr_cep: int):
    """
    Retorna um post específico baseado no ID, obtido da API pública.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://viacep.com.br/ws/{nr_cep}/json/")
        # Checa se a requisição foi bem-sucedida
        if response.status_code == 200:
            return response.json()
        else:
            return response
