from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app
from jogoteca import db
from model import Jogos
from model import Usuarios
from helpers import recupera_imagem
from helpers import deleta_arquivo
import time


@app.route('/')
def index():
    games_list = Jogos.query.order_by(Jogos.id)
    return render_template('list.html', titulo='Games', games=games_list )

@app.route('/new')
def new():
    if 'user_loguin' not in session or session['user_loguin'] == None:
        return redirect(url_for('login', next_page=url_for('new')))
    return render_template('new.html', titulo='Novo Jogo')

@app.route('/editar/<int:id>')
def editar(id):
    if 'user_loguin' not in session or session['user_loguin'] == None:
        return redirect(url_for('login', next_page=url_for('editar')))
    
    jogo = Jogos.query.filter_by(id=id).first()
    capa_jogo = recupera_imagem(id=id)
    return render_template('editar.html', titulo='Editando Jogo', jogo=jogo, capa_jogo=capa_jogo)

@app.route('/create',methods=['POST'])
def create():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    
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
    
    jogo.nome = request.form['nome']
    jogo.categoria = request.form['categoria']
    jogo.console = request.form['console']
    
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

@app.route('/login')
def login():
    next_page = request.args.get('next_page')
    return render_template('login.html', next_page= next_page)

@app.route('/authenticate',methods=['POST'])
def authenticate():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha :
            session['user_loguin'] = usuario.nickname
            flash(usuario.nickname + ' Usuario logado com sucesso')
            next_page = request.form['next_page']
            return redirect(next_page)

    else:
        flash('Usuario não existente')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['user_loguin'] = None
    flash('Logout efetuado com sucesso')
    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)
