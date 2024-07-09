import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent

conexao = sqlite3.connect(ROOT_PATH / 'meu_banco.db')
print(conexao)
cursor = conexao.cursor()

#cursor.execute('CREATE TABLE clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome VARCHAR(100), email VARCHAR(150))')

def criar_tabela(conexao, cursor):
    try:
        cursor.execute(
            "CREATE TABLE clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome VARCHAR(100),"
            "email VARCHAR(150))"
        )
        conexao.commit()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        conexao.rollback()

def inserir_registro(conexao, cursor, nome, email):
    try:
        data = (nome, email)
        cursor.execute("INSERT INTO clientes (nome, email) VALUES (?,?);", data)
        conexao.commit()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        conexao.rollback()

def atualizar_registro(conexao, cursor, nome, email, id):
    try:
        data = (nome, email, id)
        cursor.execute("UPDATE clientes SET nome=?, email=? WHERE id=?;", data)
        conexao.commit()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        conexao.rollback()

def excluir_registro(conexao, cursor, id):
    try:
        data = (id,)
        cursor.execute("DELETE FROM clientes WHERE id=?;", data)
        conexao.commit()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        conexao.rollback()

def inserir_muitos(conexao, cursor, dados):
    try:
        cursor.executemany('INSERT INTO clientes (nome, email) VALUES (?,?)', dados)
        conexao.commit()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        conexao.rollback()


def recuperar_cliente(cursor, id):
    cursor.row_factory = sqlite3.Row
    cursor.execute('SELECT * FROM clientes WHERE id=?', (id,))
    return cursor.fetchone()

def listar_clientes(cursor):
    return cursor.execute('SELECT * FROM clientes ORDER BY nome;')


# atualizar_registro(conexao, cursor, "Guilherme Carvalho", "gui@gmail.com", 1)
# atualizar_registro(conexao, cursor, "Lenor Carvalho", "lenor@gmail.com", 2)
# excluir_registro(conexao, cursor, 2)

dados = [
    ('Lenor', 'lenor@gmail.com'),
    ('Mary', 'mary@gmail.com')
]
# inserir_muitos(conexao, cursor, dados)

cliente = recuperar_cliente(cursor, 1)
print(dict(cliente))
print(cliente["nome"])

clientes = listar_clientes(cursor)
for cliente in clientes:
    print(dict(cliente))