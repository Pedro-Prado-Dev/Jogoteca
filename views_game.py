from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app
from jogoteca import db
from model import Jogos
from helpers import recupera_imagem
from helpers import deleta_arquivo
from helpers import FormularioJogo

import time


@app.route('/')
def index():
    games_list = Jogos.query.order_by(Jogos.id)
    return render_template('list.html', titulo='Games', games=games_list )

@app.route('/new')
def new():
    if 'user_loguin' not in session or session['user_loguin'] == None:
        return redirect(url_for('login', next_page=url_for('new')))
    
    form = FormularioJogo()
    return render_template('new.html', titulo='Novo Jogo', form=form)

@app.route('/editar/<int:id>')
def editar(id):
    if 'user_loguin' not in session or session['user_loguin'] == None:
        return redirect(url_for('login', next_page=url_for('editar')))
    
    jogo = Jogos.query.filter_by(id=id).first()
    form = FormularioJogo(request.form)
    
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console
    
    capa_jogo = recupera_imagem(id=id)
    return render_template('editar.html', titulo='Editando Jogo', id=id, capa_jogo=capa_jogo, form=form)

@app.route('/create',methods=['POST'])
def create():
    form = FormularioJogo(request.form)
    
    if not form.validate_on_submit():
        return redirect(url_for('new'))
    
    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data
    
    jogo = Jogos.query.filter_by(nome=nome).first()
    if jogo:
        flash('jogo já existente!')
        return redirect(url_for('index'))
    
    novo_jogo = Jogos(nome = nome, categoria= categoria, console = console)
    db.session.add(novo_jogo)
    db.session.commit()
    
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{novo_jogo.id}-{timestamp}.jpg')
    
    return redirect(url_for('index'))

@app.route('/atualizar',methods=['POST'])
def atualizar():
    jogo = Jogos.query.filter_by(id=request.form['id']).first()
    form = FormularioJogo(request.form)
    
    if form.validate_on_submit():
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data
        
        db.session.add(jogo)
        db.session.commit()
        
        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(jogo.id)
        arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')
    
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    print(id)
    if 'user_loguin' not in session or session['user_loguin'] == None:
        return redirect(url_for('login'))
    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo deletado com sucesso')
    
    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)
