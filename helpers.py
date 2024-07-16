import os
from flask_wtf.form import _Auto
from jogoteca import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField

class FormularioJogo(FlaskForm):
    nome = StringField('Nome do Jogo', [validators.DataRequired(), validators.Length(min=1,max=50)])
    categoria = StringField('Categoria', [validators.DataRequired(), validators.Length(min=1,max=40)])
    console = StringField('Console', [validators.DataRequired(), validators.Length(min=1,max=20)])
    salvar = SubmitField('Salvar')
        

class FormularioLogin(FlaskForm):
    nickname = StringField('Nickname', [validators.DataRequired(), validators.Length(min=1,max=8)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1,max=100)])
    login = SubmitField('Login')

class FormularioUser(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=1,max=50)])
    nickname = StringField('Nickname', [validators.DataRequired(), validators.Length(min=1,max=8)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1,max=100)])
    senha_confirmada = PasswordField('Confirme a Senha', [validators.DataRequired(), validators.Length(min=1,max=100)])
    cadastrar = SubmitField('Cadastrar')

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo
        
    return 'capa_padrao.jpg'

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))
            