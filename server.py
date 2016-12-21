# coding: utf-8

import sqlite3
from flask import Flask, render_template
from flask import redirect
from flask import request
from flask import send_from_directory
from flask import session
from jinja2 import Environment
from jinja2 import PackageLoader
import hashlib
import random
import funcoes
import banco
from werkzeug import secure_filename
from drop import ClienteDropbox
import os
import json

app = Flask(__name__, static_url_path='/static')
env = Environment(loader=PackageLoader(__name__, 'templates'))


@app.route('/', methods=['GET'])
def home():
    return env.get_template('login.html').render()

# Arquivos estáticos (CSS, JS, etc.)
@app.route('/static/<path:path>', methods=['GET'])
def static_file(path):
    return app.send_static_file(path)

# **************************************** Cadastra usuario ****************************************
@app.route('/cadastro', methods=['GET'])
def cadastro():
    return env.get_template('cadastrar.html').render()


@app.route('/cadastrar', methods=['POST'])
def cadastrar():

    nome = request.form['nome']
    senha = request.form['senha']
    senha_confirmar = request.form['senha2']

    # Verifica se a senha e senha2 são as mesmas.
    if senha == senha_confirmar:
        verifyIsWrite = banco.sqlite_cadastra_cliente(nome , senha)

        if verifyIsWrite != 0:
            return redirect('/')

    return env.get_template('cadastrar.html').render()

# **************************************** autenticar e login ****************************************
@app.route('/logout', methods=['GET'])
def logout():
    del session['nome']
    del session['coo']
    return redirect('/')

# Lembrar de mudar para post, se não, pode haver ataque xss
@app.route('/autenticar', methods=['POST'])
def autenticar():

    nome = request.form['nome']
    senha = request.form['senha']

    if nome and senha:
        usuario = banco.sqlite_consulta_usuario(nome, senha)

        if usuario:
            session['nome'] = nome
            session['senha'] = senha

        else:
            return redirect('/')

    return redirect('/lista_arquivos_upload')

# **************************************** Upa arquivos ****************************************
@app.route('/coordenadas/<string:coordenadas>', methods=['GET'])
def pega_coordenada(coordenadas):
    ''' Recebe a coordenadas vindo do cliente. '''

    print '\n\n ' + str(coordenadas) + '\n\n\n'
    session['coo'] = coordenadas

    return session['coo']

@app.route('/deletar/<string:nome>', methods=['GET'])
def deleta_arquivo(nome):
    print nome

    # Verifica se o usuário logado existe no banco.
    usuario = banco.sqlite_consulta_usuario(session['nome'], session['senha'])

    drop = ClienteDropbox(usuario[3], usuario[4], usuario[5])
    drop.deletar_arquivo(nome)

    arquivo = banco.sqlite_consulta_local(nome)

    #os.remove(nome)
    banco.sqlite_deleta_usuario_local(usuario[0], arquivo[0])
    banco.sqlite_deleta_arquivo(nome)

    return redirect('/lista_arquivos_upload')

@app.route('/download/<string:nome>', methods=['GET'])
def download_arquivo(nome):
    print nome

    # Verifica se o usuário logado existe no banco.
    usuario = banco.sqlite_consulta_usuario(session['nome'], session['senha'])

    drop = ClienteDropbox(usuario[3], usuario[4], usuario[5])
    drop.baixar_arquivo(nome)
    return env.get_template('usuario.html').render()

@app.route('/upar', methods=['GET', 'POST'])
def upa_arquivos():
    ''' upa arquivos do diretório do usuário. '''

    coordenadas = ''
    nome_arquivo = ''

    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        nome_arquivo = f.filename
        geo = request.form

        ''' Pegando a localizacao.
        for key, value in geo.iteritems():
            coordenadas = key

        print '\n\n ' + str(coordenadas) + '\n\n'''
        p = session['coo'].split(',')

        lat = p[0]
        lon = p[1]

        posicao_arquivo = {'lat':float(lat), 'lon':float(lon)}

        # Salvando minha posição na sessão.
        session['minha_posicao'] = posicao_arquivo

        # Verifica se o usuário logado existe no banco.
        usuario = banco.sqlite_consulta_usuario(session['nome'], session['senha'])

        if usuario:
            # Verifica se o mesmo arquivo está sendo upado, novamente.
            local = banco.sqlite_consulta_local(nome_arquivo)

            # Verifica se o arquivo escolhido pelo usuário já foi upado, caso sim, não deixa cadastrar.
            if local == None:
                # upando o arquivo para o dropbox
                drop = ClienteDropbox(usuario[3], usuario[4], usuario[5])
                foi = drop.upar_arquivo(nome_arquivo)

                if foi == False:
                    print '\n\n ***** Is not possible up in files *****\n\n'
                    return env.get_template('usuario.html').render(name=session['nome'])

                # Cadastra na tabela local.
                id_local = banco.sqlite_cadastra_arquivo(nome_arquivo, posicao_arquivo['lat'], posicao_arquivo['lon'])

                # Pega o id do usuario.
                id_usuario = banco.sqlite_consulta_usuario_nome(session['nome'])[0]

                # Cadastra na tabela usuario_local
                banco.sqlite_cadastra_usuario_arquivo(id_usuario, id_local)

        # Apaga o arquivo do servidor Flask.
        os.remove(nome_arquivo)

    return redirect('/lista_arquivos_upload')


# **************************************** Listar arquivos na aba upload ****************************************
@app.route('/lista_arquivos_upload', methods=['GET'])
def lista_arquivos():
    ''' Lista todos os arquivos do usuário em uma tabela na aba de upload.'''

    id_usuario = banco.sqlite_consulta_usuario_nome(session['nome'])[0]
    lista = banco.sqlite_consulta_id_usuario_local(id_usuario)
    lista_arquivos = list()

    # Com a lista de id's dos arquivos do usuario(id_usuario), agora é hora de pegar todos os arquivos com id presente na lista.
    for linha in lista:
        x = banco.sqlite_consulta_arquivos(linha)
        lista_arquivos.append(x)

    # Pega todos os arquivos que estão pertos e printa.
    listar_perto = []
    try:
        listar_perto = listar_arquivos_perto()
    except:
        pass

    return env.get_template('usuario.html').render(name=session['nome'], lista=lista_arquivos, listar_download=listar_perto)


# **************************************** Listar arquivos perto ****************************************
def listar_arquivos_perto():
    ''' Retorna uma lista de arquivos que estejam perto do usuário. '''

    p = session['coo'].split(',')

    lat = p[0]
    lon = p[1]

    minha_posicao = {'lat':float(lat), 'lon':float(lon)}

    # Gerando uma lista com todos os arquivos que estão perto.
    lista_de_arquivos_perto = banco.lista_arquivos_perto(minha_posicao)

    lista_id_usuarios = list()
    print str(lista_de_arquivos_perto)

    return lista_de_arquivos_perto


@app.route('/lista_pin', methods=['GET'])
def lista_pin():

    lista = banco.sqlite_consulta_todos_arquivos()
    lis = json.dumps(lista)

    print str(lis)

    return lis

# **************************************** Init ****************************************
if __name__ == "__main__":
    banco.cria_banco()
    app.secret_key = 'm;4slF=Y6]Afb/.p9Xd7iO8(V0yU~R"'
    app.run(host='0.0.0.0', port=8989, threaded=True, debug=True)
