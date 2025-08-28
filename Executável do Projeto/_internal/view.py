import sqlite3
import os
import sys


# FUNÇÃO PARA O CAMINHO DO BANCO DE DADOS (MESMA DO ARQUIVO PRINCIPAL)
def get_db_path():
    """Retorna o caminho correto do banco de dados para .exe ou IDE"""
    if getattr(sys, 'frozen', False):
        # Modo executável (.exe) - banco na mesma pasta do executável
        return os.path.join(os.path.dirname(sys.executable), 'dados.db')
    else:
        # Modo desenvolvimento (IDE) - banco na pasta do projeto
        return 'dados.db'


# CONECTAR AO BANCO DE DADOS
def connect():
    return sqlite3.connect(get_db_path())  # ← ALTERADO!


# FUNÇÃO PARA INSERIR UM NOVO LIVRO
def insert_book(titulo, autor, editora, ano_publicacao, isbn):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO livros(titulo, autor, editora, ano_publicacao, isbn)\
                    VALUES (?, ?, ?, ?, ?)', (titulo, autor, editora, ano_publicacao, isbn))
    conn.commit()
    conn.close()


# FUNÇÃO PARA INSERIR UM NOVO USUÁRIO
def insert_user(nome, sobrenome, endereco, email, telefone):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios(nome, sobrenome, endereco, email, telefone)\
                    VALUES (?, ?, ?, ?, ?)', (nome, sobrenome, endereco, email, telefone))
    conn.commit()
    conn.close()


# FUNÇÃO PARA EXIBIR USUÁRIOS
def get_users():
    conn = connect()
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios')
    users = c.fetchall()
    conn.close()
    return users


# FUNÇÃO PARA REGISTRAR UM NOVO EMPRÉSTIMO
def insert_loan(id_usuario, id_livro, data_emprestimo, devolucao):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO emprestimo(id_usuario, id_livro, data_emprestimo, devolucao)\
                    VALUES (?, ?, ?, ?)', (id_usuario, id_livro, data_emprestimo, devolucao))
    conn.commit()
    conn.close()


# FUNÇÃO PARA EXIBIR LIVROS
def exibir_livros():
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM livros")
        livros = cursor.fetchall()
        conn.close()
        return livros
    except Exception as e:
        print(f"Erro ao buscar livros: {e}")
        return []


def update_loan_return_date(id_emprestimo, data_devolucao):
    try:
        conn = connect()
        cursor = conn.cursor()
        # CORRECTED SQL SYNTAX
        cursor.execute('UPDATE emprestimo SET devolucao = ? WHERE id = ?',
                      (data_devolucao, id_emprestimo))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Erro ao atualizar devolução: {e}")
        return False

# CORRECT THE get_all_loans FUNCTION TO MATCH YOUR DATABASE STRUCTURE
def get_all_loans():
    try:
        conn = connect()
        cursor = conn.cursor()
        # CORRECTED TO MATCH YOUR TABLE NAME AND COLUMN NAMES
        cursor.execute('''
            SELECT e.id, l.titulo, u.nome, u.sobrenome, 
                   e.data_emprestimo, e.devolucao
            FROM emprestimo e
            JOIN livros l ON e.id_livro = l.id
            JOIN usuarios u ON e.id_usuario = u.id
            ORDER BY e.data_emprestimo DESC
        ''')
        result = cursor.fetchall()
        conn.close()
        return result
    except Exception as e:
        print(f"Erro ao buscar empréstimos: {e}")
        return []

# VERIFICAR SE UM LIVRO JÁ ESTÁ EMPRESTADO - FUNÇÃO NOVA!
def is_book_loaned(id_livro):
    """Verifica se um livro já está emprestado"""
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM emprestimo WHERE id_livro = ? AND devolucao IS NULL', (id_livro,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except Exception as e:
        print(f"Erro ao verificar empréstimo: {e}")
        return False

# VERIFICAR SE USUÁRIO EXISTE - FUNÇÃO NOVA!
def user_exists(id_usuario):
    """Verifica se um usuário existe"""
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM usuarios WHERE id = ?', (id_usuario,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except Exception as e:
        print(f"Erro ao verificar usuário: {e}")
        return False

# VERIFICAR SE LIVRO EXISTE - FUNÇÃO NOVA!
def book_exists(id_livro):
    """Verifica se um livro existe"""
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM livros WHERE id = ?', (id_livro,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except Exception as e:
        print(f"Erro ao verificar livro: {e}")
        return False


# EXEMPLO DE USO (para teste)
if __name__ == "__main__":
    livros_emprestados = get_all_loans()
    print("Livros emprestados:", livros_emprestados)

    livros = exibir_livros()
    print("Todos os livros:", livros)


    # Adicione esta função ao view.py
    def check_database_structure():
        conn = connect()
        cursor = conn.cursor()

        # Verificar tabelas existentes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("Tabelas no banco:", tables)

        # Verificar estrutura da tabela de empréstimos
        try:
            cursor.execute("PRAGMA table_info(emprestimos)")
            print("Estrutura de 'emprestimos':", cursor.fetchall())
        except:
            print("Tabela 'emprestimos' não existe")

        try:
            cursor.execute("PRAGMA table_info(emprestimo)")
            print("Estrutura de 'emprestimo':", cursor.fetchall())
        except:
            print("Tabela 'emprestimo' não existe")

        conn.close()


    # Execute uma vez para verificar
    check_database_structure()

def delete_table(emprestimos):
    try:
        conn = sqlite3.connect('seu_banco.db')
        cursor = conn.cursor()

        # DELETAR TABELA
        cursor.execute(f"DROP TABLE IF EXISTS {emprestimos}")

        conn.commit()
        conn.close()
        print(f"Tabela {emprestimos} deletada com sucesso!")

    except sqlite3.Error as e:
        print(f"Erro ao deletar tabela: {e}")
