import sqlite3

#CONECTAR AO BANCO DE DADO OU CRIAR UM NOVO BANCO DE DADOS

conn = sqlite3.connect('dados.db')

#CRIAR A TABELA DE LIVROS

conn.execute('CREATE TABLE IF NOT EXISTS livros(\
	id INTEGER PRIMARY KEY,\
	titulo TEXT,\
	autor TEXT,\
	editora TEXT,\
	ano_publicacao INTEGER,\
	isbn TEXT)')

#CRIAR A TABELA DE USUÁRIOS

conn.execute('CREATE TABLE IF NOT EXISTS usuarios(\
	id INTEGER PRIMARY KEY,\
	nome TEXT,\
	sobrenome TEXT,\
	endereco TEXT,\
	email TEXT,\
	telefone TEXT)')

#CRIAR A TABELA DE EMPRÉSTIMO

conn.execute('CREATE TABLE IF NOT EXISTS emprestimo(\
	id INTEGER PRIMARY KEY,\
	id_livro INTEGER,\
	id_usuario INTEGER,\
	data_emprestimo TEXT,\
	devolucao TEXT,\
	FOREIGN KEY(id_livro) REFERENCES livros(id),\
	FOREIGN KEY(id_usuario) REFERENCES usuarios(id))')

conn.commit()
conn.close()

