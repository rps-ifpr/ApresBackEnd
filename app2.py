import pyodbc

# Conexão com o banco de dados
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=SEU_SERVIDOR;DATABASE=SEU_BANCO;UID=usuario;PWD=senha')
cursor = conn.cursor()

# Consulta para pegar os registros mascarados
cursor.execute("SELECT CPF_CNPJ, NOME_DEVEDOR FROM DM_DIVIDA_ATIVA WHERE CPF_CNPJ LIKE 'XXX%'")

# Itera pelas linhas (cursor com for)
for row in cursor.fetchall():
    cpf_mascarado = row.CPF_CNPJ
    nome = row.NOME_DEVEDOR

    # Aqui você aplica uma lógica para descobrir o CPF correto, ex:
    # Consultar outra tabela com os dados completos
    cursor2 = conn.cursor()
    cursor2.execute("SELECT CPF_CNPJ FROM OUTRA_TABELA WHERE NOME_DEVEDOR = ?", nome)
    resultado = cursor2.fetchone()

    if resultado:
        cpf_real = resultado.CPF_CNPJ
        print(f"Atualizando {nome} - {cpf_mascarado} -> {cpf_real}")

        # Atualiza o valor no banco
        cursor3 = conn.cursor()
        cursor3.execute("UPDATE DM_DIVIDA_ATIVA SET CPF_CNPJ = ? WHERE CPF_CNPJ = ?", cpf_real, cpf_mascarado)
        conn.commit()
    else:
        print(f"CPF real não encontrado para {nome}")

cursor.close()
conn.close()
