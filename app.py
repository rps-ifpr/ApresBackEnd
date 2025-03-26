import streamlit as st        # Importa a biblioteca Streamlit para criação de apps web interativos
import json                   # Importa o módulo JSON para manipulação de dados no formato JSON
import os                     # Importa o módulo OS para interagir com o sistema operacional (verificar existência de arquivos, etc.)

# Título
st.title('Sistema Simples de Gestão de Usuários')  
# Define o título da aplicação na interface do Streamlit

st.write("Demonstra as operações CRUD")
# Exibe uma mensagem explicando que o app demonstra operações CRUD (Create, Read, Update, Delete)

# Caminho do arquivo
json_file_path = 'aulacrud.json'
# Define o caminho do arquivo JSON onde os dados dos usuários serão armazenados

# Função para ler os dados existentes (Operação "Read")
def load_user_data():
    if os.path.exists(json_file_path):          # Verifica se o arquivo JSON já existe no diretório
        with open(json_file_path, 'r') as file:   # Abre o arquivo em modo de leitura ('r')
            return json.load(file)                # Carrega os dados do arquivo JSON e retorna como um objeto Python (lista/dicionário)
    return []                                    # Se o arquivo não existir, retorna uma lista vazia

# Função para salvar os dados (Operações "Create" e "Update")
def save_user_data(data):
    with open(json_file_path, 'w') as file:       # Abre o arquivo JSON em modo de escrita ('w')
        json.dump(data, file, indent=4)           # Salva os dados fornecidos no arquivo, formatados com indentação de 4 espaços para melhor visualização

# Carrega os dados ao iniciar o app
if 'user_data' not in st.session_state:
    st.session_state.user_data = load_user_data()  
# Verifica se a chave 'user_data' já existe no estado da sessão. Se não existir, carrega os dados do arquivo JSON

# Função para adicionar um usuário (Operação "Create")
def add_user():
    user_info = {
        'name': st.session_state.name,         # Coleta o nome do usuário a partir do estado da sessão (valor digitado)
        'email': st.session_state.email          # Coleta o e-mail do usuário a partir do estado da sessão
    }
    st.session_state.user_data.append(user_info) # Adiciona o novo usuário à lista de usuários armazenada no estado da sessão
    save_user_data(st.session_state.user_data)     # Salva a lista atualizada no arquivo JSON
    st.session_state.name = ""                     # Limpa o campo 'name' no estado da sessão após a adição
    st.session_state.email = ""                    # Limpa o campo 'email' no estado da sessão após a adição
    st.success('Usuário adicionado com sucesso! (Operação Create)')
    # Exibe uma mensagem de sucesso para informar que o usuário foi adicionado

# Campos para entrada de dados
name = st.text_input('Nome:', key='name')
# Cria um campo de texto para o usuário inserir o nome; o valor é armazenado no st.session_state com a chave 'name'

email = st.text_input('E-mail:', key='email')
# Cria um campo de texto para o usuário inserir o e-mail; o valor é armazenado no st.session_state com a chave 'email'

# Botão para adicionar usuário
if st.button('Adicionar Usuário', on_click=add_user):
    pass
# Cria um botão que, ao ser clicado, chama a função add_user. A instrução 'pass' é usada pois a ação já é tratada pelo on_click

# Função para editar um usuário (Operação "Update")
def edit_user(index, new_name, new_email):
    st.session_state.user_data[index]['name'] = new_name  # Atualiza o nome do usuário na posição 'index'
    st.session_state.user_data[index]['email'] = new_email  # Atualiza o e-mail do usuário na posição 'index'
    save_user_data(st.session_state.user_data)            # Salva a lista atualizada no arquivo JSON
    st.success('Usuário atualizado com sucesso! (Operação Update)')
    # Exibe uma mensagem de sucesso informando que o usuário foi atualizado

# Função para excluir um usuário (Operação "Delete")
def delete_user(index):
    del st.session_state.user_data[index]   # Remove o usuário da lista com base no índice fornecido
    save_user_data(st.session_state.user_data)  # Salva a lista atualizada no arquivo JSON
    st.success('Usuário excluído com sucesso! (Operação Delete)')
    # Exibe uma mensagem de sucesso informando que o usuário foi excluído

# Seção para buscar e exibir dados (Operação "Read")
search_query = st.text_input('Buscar usuário por nome:')
# Cria um campo de texto para o usuário inserir uma consulta de busca (filtra por nome)

if search_query:
    # Se o usuário digitou algo no campo de busca, filtra os usuários que contenham o termo no nome (case-insensitive)
    found_users = [(index, user) for index, user in enumerate(st.session_state.user_data) if search_query.lower() in user['name'].lower()]
    if found_users:
        st.write('### Resultados da Busca')
        # Exibe um cabeçalho para os resultados da busca
        for index, user in found_users:
            st.json(user)
            # Exibe os dados do usuário no formato JSON para visualização
            edit_name = st.text_input(f'Editar nome para usuário {user["name"]}:', key=f'new_name{index}')
            # Campo de texto para inserir um novo nome para o usuário; cada campo possui uma chave única
            edit_email = st.text_input(f'Editar e-mail para usuário {user["name"]}:', key=f'new_email{index}')
            # Campo de texto para inserir um novo e-mail para o usuário; cada campo possui uma chave única
            if st.button(f'Atualizar {user["name"]}', key=f'update{index}'):
                edit_user(index, edit_name, edit_email)
                # Se o botão "Atualizar" for clicado, chama a função edit_user com o índice e os novos valores
            if st.button(f'Excluir {user["name"]}', key=f'delete{index}'):
                delete_user(index)
                # Se o botão "Excluir" for clicado, chama a função delete_user para remover o usuário
    else:
        st.error('Usuário não encontrado.')
        # Caso nenhum usuário seja encontrado com a busca, exibe uma mensagem de erro

# Mostrar todos os usuários (Operação "Read")
st.write('### Lista de Todos os Usuários')
# Exibe um cabeçalho para a lista completa de usuários

st.json(st.session_state.user_data)
# Exibe todos os usuários atualmente armazenados no estado da sessão no formato JSON
