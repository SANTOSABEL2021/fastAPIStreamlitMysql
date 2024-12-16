from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração do banco de dados (SQLite para simplicidade)
DATABASE_URL = "sqlite:///bancoexemplo.db"
engine = create_engine(DATABASE_URL, echo=True)

# Base para as classes do SQLAlchemy
Base = declarative_base()


# Definição do modelo de Usuário
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String, unique=True, nullable=False)


# Criação das tabelas no banco de dados
Base.metadata.create_all(engine)

# Criação da sessão
Session = sessionmaker(bind=engine)
session = Session()


# Operações CRUD
def create_user(name, age, email):
    user = User(name=name, age=age, email=email)
    session.add(user)
    session.commit()
    print(f"Usuário {name} criado com sucesso!")


def get_users():
    users = session.query(User).all()
    for user in users:
        print(f"ID: {user.id}, Nome: {user.name}, Idade: {user.age}, Email: {user.email}")


def update_user(user_id, new_name=None, new_age=None, new_email=None):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        if new_name:
            user.name = new_name
        if new_age:
            user.age = new_age
        if new_email:
            user.email = new_email
        session.commit()
        print(f"Usuário {user_id} atualizado com sucesso!")
    else:
        print(f"Usuário {user_id} não encontrado.")


def delete_user(user_id):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        session.delete(user)
        session.commit()
        print(f"Usuário {user_id} excluído com sucesso!")
    else:
        print(f"Usuário {user_id} não encontrado.")


# Testando as operações
if __name__ == "__main__":
    # Criação de usuários
    create_user("Alice", 30, "alice@example.com")
    create_user("Bob", 25, "bob@example.com")

    # Consulta de usuários
    print("\nLista de usuários:")
    get_users()

    # Atualização de um usuário
    #print("\nAtualizando usuário:")
    #update_user(1, new_name="Alice Smith", new_age=31)

    # Consulta após atualização
    #print("\nLista de usuários após atualização:")
    #get_users()

    # Exclusão de um usuário
    #print("\nExcluindo usuário:")
    #delete_user(2)

    # Consulta após exclusão
    #print("\nLista de usuários após exclusão:")
    #get_users()
