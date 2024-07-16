from flask import render_template, request, redirect, session, flash, url_for
from helpers import FormularioLogin, FormularioUser
from model import Usuarios
from jogoteca import app,db
from flask_bcrypt import check_password_hash, generate_password_hash

@app.route('/login')
def login():
    next_page = request.args.get('next_page')
    form = FormularioLogin()
    return render_template('login.html', next_page= next_page, form=form)

@app.route('/authenticate',methods=['POST'])
def authenticate():
    form = FormularioLogin(request.form)
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    try :
        senha = check_password_hash(usuario.senha, form.senha.data)
    except:
        senha = False
    
    if usuario and senha:
        
        session['user_loguin'] = usuario.nickname
        flash(usuario.nickname + ' Usuario logado com sucesso')
        next_page = request.form['next_page'] if request.form['next_page'] != 'None' else '/'
        return redirect(next_page)

    else:
        flash('Usuario não existente')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['user_loguin'] = None
    flash('Logout efetuado com sucesso')
    return redirect(url_for('index'))


@app.route('/novo_usuario')
def novo_usuario():
    form = FormularioUser()
    return render_template('new_user.html', form=form)

@app.route('/cria_usuario', methods=['POST'])
def cria_usuario():
    form = FormularioUser(request.form)
    
    if not form.validate_on_submit():
        flash('Preencha todos os campos!')
        return redirect(url_for('novo_usuario'))
    
    nome = form.nome.data
    nickname = form.nickname.data
    senha = form.senha.data
    senha_confirmada = form.senha_confirmada.data
    
    user = Usuarios.query.filter_by(nickname=nickname).first()
    if user:
        flash('Nickname já existente')
        return redirect(url_for('novo_usuario'))
    
    if senha != senha_confirmada:
        flash('Prencha os campos Senha e Senha Confirmada com a mesma senha')
        return redirect(url_for('novo_usuario'))
    
    novo_usuario = Usuarios(nome=nome, nickname=nickname, senha=generate_password_hash(senha).decode('utf-8'))
    db.session.add(novo_usuario)
    db.session.commit()
    
    session['user_loguin'] = nickname
    flash(nickname + ' Usuario logado com sucesso')
    return redirect(url_for('index'))