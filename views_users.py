from flask import render_template, request, redirect, session, flash, url_for
from helpers import FormularioUsuario
from model import Usuarios
from jogoteca import app

@app.route('/login')
def login():
    next_page = request.args.get('next_page')
    form = FormularioUsuario()
    return render_template('login.html', next_page= next_page, form=form)

@app.route('/authenticate',methods=['POST'])
def authenticate():
    form = FormularioUsuario(request.form)
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    
    if usuario:
        if form.senha.data == usuario.senha :
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