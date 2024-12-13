import streamlit as st
import requests

# Configuração inicial
BASE_URL = "http://127.0.0.1:8000"
#teste

st.set_page_config(page_title="Sistema de Login", layout="centered")

# Função para validar campos
def validar_campos(*campos):
    return all(campo.strip() for campo in campos)

# Página de Login
def login_page():
    st.title("Login")

    login = st.text_input("Login")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if not validar_campos(login, senha):
            st.error("Todos os campos são obrigatórios.")
            return

        try:
            response = requests.post(f"{BASE_URL}/login/", json={"login": login, "senha": senha})
            if response.status_code == 200:
                dados = response.json()
                # Salva os dados de login na sessão
                st.session_state["logged_in"] = True
                st.session_state["perfil"] = dados["perfil"]
                st.session_state["nome"] = dados["nome"]
                st.experimental_rerun()
            else:
                st.error(response.json().get("detail", "Erro ao realizar login."))
        except requests.ConnectionError:
            st.error("Erro de conexão com a API. Certifique-se de que a API está rodando.")
        except Exception as e:
            st.error(f"Erro inesperado: {e}")

# Página de Cadastro
def cadastro_page():
    st.title("Cadastro de Usuário")

    nome = st.text_input("Nome")
    login = st.text_input("Login")
    senha = st.text_input("Senha", type="password")
    perfil = st.selectbox("Perfil", ["usuario", "administrador", "externo"])

    if st.button("Cadastrar"):
        if not validar_campos(nome, login, senha):
            st.error("Todos os campos são obrigatórios.")
            return

        try:
            response = requests.post(
                f"{BASE_URL}/cadastro/",
                json={"nome": nome, "login": login, "senha": senha, "perfil": perfil},
            )
            if response.status_code == 201:
                st.success("Usuário cadastrado com sucesso!")
            else:
                st.error(response.json().get("detail", "Erro ao cadastrar usuário."))
        except requests.ConnectionError:
            st.error("Erro de conexão com a API. Certifique-se de que a API está rodando.")
        except Exception as e:
            st.error(f"Erro inesperado: {e}")

# Página Principal
def principal_page():
    st.title("Página Principal")
    st.write(f"Bem-vindo(a), {st.session_state['nome']}!")
    st.write(f"Seu perfil: {st.session_state['perfil'].capitalize()}")

    if st.button("Sair"):
        # Limpa a sessão
        st.session_state["logged_in"] = False
        st.session_state.pop("perfil", None)
        st.session_state.pop("nome", None)
        st.experimental_rerun()

# Controle de navegação
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    principal_page()
else:
    st.sidebar.title("Navegação")
    opcao = st.sidebar.radio("Selecione uma opção", ["Login", "Cadastro"])

    if opcao == "Login":
        login_page()
    else:
        cadastro_page()
