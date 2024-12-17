import streamlit as st
import json
import os

# Título da aplicação
st.title('Sistema Simples de Gestão de Usuários')
st.write("Interface de gerenciamento de usuários que demonstra as operações CRUD")

# Caminho do arquivo JSON
json_file_path = 'user_data.json'

# Ler dados existentes no arquivo JSON (Operação "Read")
def load_user_data():
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            return json.load(file)
    return []

# Salvar dados no arquivo JSON (Operações "Create" e "Update")
def save_user_data(data):
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Carrega os dados ao iniciar o aplicativo
if 'user_data' not in st.session_state:
    st.session_state.user_data = load_user_data()

# Função para adicionar usuário (Operação "Create")
def add_user():
    user_info = {
        'name': st.session_state.name,
        'email': st.session_state.email
    }
    st.session_state.user_data.append(user_info)
    save_user_data(st.session_state.user_data)
    st.session_state.name = ""
    st.session_state.email = ""
    st.success('Usuário adicionado com sucesso! (Operação Create)')

# Campos para entrada de dados
name = st.text_input('Nome:', key='name')
email = st.text_input('E-mail:', key='email')

# Botão para adicionar usuário
if st.button('Adicionar Usuário', on_click=add_user):
    pass

# Função para editar usuário (Operação "Update")
def edit_user(index, new_name, new_email):
    st.session_state.user_data[index]['name'] = new_name
    st.session_state.user_data[index]['email'] = new_email
    save_user_data(st.session_state.user_data)
    st.success('Usuário atualizado com sucesso! (Operação Update)')

# Função para excluir usuário (Operação "Delete")
def delete_user(index):
    del st.session_state.user_data[index]
    save_user_data(st.session_state.user_data)
    st.success('Usuário excluído com sucesso! (Operação Delete)')

# Seção para buscar e exibir dados de um usuário (Operação "Read")
search_query = st.text_input('Buscar usuário por nome:')
if search_query:
    found_users = [(index, user) for index, user in enumerate(st.session_state.user_data) if search_query.lower() in user['name'].lower()]
    if found_users:
        st.write('### Resultados da Busca')
        for index, user in found_users:
            st.json(user)
            edit_name = st.text_input(f'Editar nome para usuário {user["name"]}:', key=f'new_name{index}')
            edit_email = st.text_input(f'Editar e-mail para usuário {user["name"]}:', key=f'new_email{index}')
            if st.button(f'Atualizar {user["name"]}', key=f'update{index}'):
                edit_user(index, edit_name, edit_email)
            if st.button(f'Excluir {user["name"]}', key=f'delete{index}'):
                delete_user(index)
    else:
        st.error('Usuário não encontrado.')

# Mostrar todos os usuários (Operação "Read")
st.write('### Lista de Todos os Usuários')
st.json(st.session_state.user_data)
