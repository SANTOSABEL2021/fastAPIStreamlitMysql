from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Enum, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.hash import bcrypt
import enum

# Configuração do banco de dados
DATABASE_URL = "mysql+pymysql://root:root@localhost/usuarios_bd"
engine = create_engine(DATABASE_URL, echo=True)  # Adicionado echo para depuração
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Enum para o perfil do usuário
class PerfilEnum(enum.Enum):
    usuario = "usuario"
    administrador = "administrador"
    externo = "externo"

# Modelo da tabela
class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    login = Column(String(50), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    perfil = Column(Enum(PerfilEnum), nullable=False)

# Modelos Pydantic
class UsuarioBase(BaseModel):
    nome: str = Field(..., example="João da Silva", description="Nome completo do usuário")
    login: str = Field(..., example="joao.silva", description="Login único do usuário")
    senha: str = Field(..., example="senha_segura123", description="Senha do usuário")
    perfil: PerfilEnum = Field(..., example=PerfilEnum.usuario, description="Perfil do usuário")

class LoginModel(BaseModel):
    login: str = Field(..., example="joao.silva", description="Login único do usuário")
    senha: str = Field(..., example="senha_segura123", description="Senha do usuário")

# Função para testar conexão com o banco de dados
def testar_conexao():
    try:
        with engine.connect() as conn:
            # Usando `text` para executar consulta direta
            conn.execute(text("SELECT 1"))
        return "Conexão com o banco de dados bem-sucedida!"
    except Exception as e:
        return f"Erro ao conectar ao banco de dados: {e}"

# Criação do banco de dados
Base.metadata.create_all(bind=engine)

# Inicialização do app
app = FastAPI(title="API de Usuários", description="API para gerenciamento de usuários", version="1.0.0")

# Testar conexão na inicialização do FastAPI
mensagem_conexao = testar_conexao()
print(mensagem_conexao)

@app.on_event("startup")
async def verificar_conexao():
    print("Verificando conexão com o banco de dados...")
    print(mensagem_conexao)

# Dependência do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota de cadastro
@app.post("/cadastro/", status_code=status.HTTP_201_CREATED, tags=["Usuários"], summary="Cadastrar novo usuário")
def cadastrar_usuario(usuario: UsuarioBase, db: Session = Depends(get_db)):
    """
    Cadastra um novo usuário no sistema.
    """
    # Verifica se o login já existe
    usuario_existente = db.query(Usuario).filter(Usuario.login == usuario.login).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Login já cadastrado.")

    # Criação do novo usuário
    hashed_senha = bcrypt.hash(usuario.senha)
    novo_usuario = Usuario(
        nome=usuario.nome, login=usuario.login, senha=hashed_senha, perfil=usuario.perfil
    )
    db.add(novo_usuario)
    try:
        db.commit()
        db.refresh(novo_usuario)
        return {"message": "Usuário cadastrado com sucesso!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao cadastrar usuário: {str(e)}")

# Rota de login
@app.post("/login/", tags=["Autenticação"], summary="Realizar login")
def login(dados: LoginModel, db: Session = Depends(get_db)):
    """
    Autentica um usuário no sistema.
    """
    usuario = db.query(Usuario).filter(Usuario.login == dados.login).first()
    if not usuario or not bcrypt.verify(dados.senha, usuario.senha):
        raise HTTPException(status_code=401, detail="Login ou senha inválidos.")
    return {
        "message": "Login realizado com sucesso!",
        "perfil": usuario.perfil.value,
        "nome": usuario.nome,
    }
