# coding: utf-8

import os
import sqlite3
import funcoes

''' Este arquivo descreve as funções relacionadas a manipulação do banco de dados '''

_ARQUIVO_BANCO_ = './banco.sqlite'

def cria_banco():
    ''' Verifica se o banco já existe, caso contrário cria um novo.'''

    # Checa se o banco de dados já foi criado
    if not os.path.isfile(_ARQUIVO_BANCO_):

        con = sqlite3.connect(_ARQUIVO_BANCO_)
        cursor = con.cursor()
        cursor.execute('''
            CREATE TABLE usuario (
                id_usuario INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                senha TEXT NOT NULL,
                chave TEXT NOT NULL,
                chave_secreta TEXT NOT NULL,
                token TEXT NOT NULL
            );
        ''')

        cursor.execute('''
            CREATE TABLE local (
                id_local INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                arquivo TEXT NOT NULL,
                lat TEXT NOT NULL,
                lon TEXT NOT NULL
            );
        ''')

        cursor.execute('''
            CREATE TABLE usuario_local (
                id_usuario INTEGER NOT NULL,
                id_local INTEGER NOT NULL,
                FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario),
                FOREIGN KEY (id_local) REFERENCES local (id_local)
            );
        ''')

        con.close()


# *************************************** Tabela usuario ***************************************
def sqlite_consulta_usuario(nome, senha):
    ''' Verifica se existe no banco um usuário com este nome e com esta senha. '''
    
    usuario = ''
    con = sqlite3.connect(_ARQUIVO_BANCO_)
    cursor = con.cursor()
    # cursor.prepare("SELECT * FROM users where id=?")
    # execute($data);
    cursor.execute('SELECT * from usuario WHERE nome=? AND senha=?', (nome, senha))
   
    for linha in cursor.fetchall():
        usuario = linha

    con.close()
    return usuario

def sqlite_consulta_usuario_nome(nome):
    ''' Retorna o id do usuário cujo nome foi passado como parâmetro. '''
    
    usuario = ''
    con = sqlite3.connect(_ARQUIVO_BANCO_)
    cursor = con.cursor()
    # cursor.prepare("SELECT * FROM users where id=?")
    # execute($data);
    cursor.execute('SELECT * from usuario WHERE nome=?', (nome,))
   
    usuario = cursor.fetchone()
    
    if usuario == None:
        con.close()
        return 0

    con.close()
    return usuario

# *************************************** Tabela local ***************************************
def sqlite_cadastra_arquivo(nome_arquivo, lat, lon):
    ''' Insere na tabela local, o nome do arquivo e sua coordenada. '''
    
    con = sqlite3.connect(_ARQUIVO_BANCO_)
    cursor = con.cursor()
    cursor.execute('INSERT INTO local (arquivo, lat, lon) VALUES ("%s", "%s", %s)' % (nome_arquivo, lat, lon))
    idd = cursor.lastrowid
    con.commit()
    con.close()
    return idd
    
def sqlite_consulta_local(nome_arquivo):
    ''' Verifica se existe no banco um arquivo com este nome. '''
    
    local = ''
    con = sqlite3.connect(_ARQUIVO_BANCO_)
    cursor = con.cursor()
    # cursor.prepare("SELECT * FROM users where id=?")
    # execute($data);
    cursor.execute('SELECT * from local WHERE arquivo=?', (nome_arquivo,))
   
    local = cursor.fetchone()
    
    if local != None:
        return local
    
    con.close()
    return local

def sqlite_consulta_arquivos(id_local):
    ''' Retorna uma lista com todos os arquivos de acordo com o id passado como parâmetro. '''
    
    con = sqlite3.connect(_ARQUIVO_BANCO_)
    cursor = con.cursor()
    # cursor.prepare("SELECT * FROM users where id=?")
    # execute($data);
    cursor.execute('SELECT * from local WHERE id_local=?', (id_local,))
   
    linha = cursor.fetchone()

    con.close()
    return linha

# *************************************** Tabela usuario_local ***************************************
def sqlite_cadastra_usuario_arquivo(id_usuario, id_local):
    ''' Cadastrar na tabela usuario_local o id do usuario e do local '''
    
    con = sqlite3.connect(_ARQUIVO_BANCO_)
    cursor = con.cursor()
    cursor.execute('INSERT INTO usuario_local (id_usuario, id_local) VALUES ("%s", "%s")' % (id_usuario, id_local))
    con.commit()
    con.close()

def sqlite_consulta_id_usuario_local(id_usuario):
    ''' Retorna uma lista com todos os id's de arquivos que pertence ao usuário com id passado como parâmetro. '''
    
    lista_arquivos = list()
    con = sqlite3.connect(_ARQUIVO_BANCO_)
    cursor = con.cursor()
    # cursor.prepare("SELECT * FROM users where id=?")
    # execute($data);
    cursor.execute('SELECT * from usuario_local WHERE id_usuario=?', (id_usuario,))
   
    for linha in cursor.fetchall():
        lista_arquivos.append(linha[1])

    con.close()
    return lista_arquivos

def sqlite_consulta_id_local_usuario(id_local):
    ''' Retorna uma lista com todos os id's de usuários que pertence ao arquivo com id passado como parâmetro. '''
    
    lista_usuarios = list()
    con = sqlite3.connect(_ARQUIVO_BANCO_)
    cursor = con.cursor()
    # cursor.prepare("SELECT * FROM users where id=?")
    # execute($data);
    cursor.execute('SELECT * from usuario_local WHERE id_local=?', (id_local,))
   
    for linha in cursor.fetchall():
        lista_usuarios.append(linha[0])

    con.close()
    return lista_usuarios
    

def lista_arquivos_perto(minha_posicao):
    ''' Retorna uma lista com todos os arquivos que estejam dentro do raio definidos pelos parâmetros.  '''

    lista_arquivos = list()
    con = sqlite3.connect(_ARQUIVO_BANCO_)
    cursor = con.cursor()
    # cursor.prepare("SELECT * FROM users where id=?")
    # execute($data);
    cursor.execute('SELECT * from local')
   
    # Filtrando. Apenas as coordenadas que estão dentro do raio serão adicionadas na lista.
    for linha in cursor.fetchall():
        arquivo_posicao = {'lat': float(linha[2]), 'lon': float(linha[3])}
        teste = funcoes.verifica_posicao(minha_posicao, arquivo_posicao)
        
        if teste == True:
            lista_arquivos.append(linha)
    
    
    con.close()
    return lista_arquivos