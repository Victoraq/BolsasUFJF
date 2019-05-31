from flask import Flask, redirect, url_for, render_template, request, session
from flask_session import Session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import delete, insert, update

# Configure app
app = Flask(__name__)

# Configure the database
app.config.from_pyfile('/home/victor/Documentos/Modelagem_Sistemas/BolsasUFJF/project/app.cfg')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# configurate sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def index():
    return render_template('index.html')

from models import Bolsa

@app.route('/bolsa/<int:bolsa_id>')
def bolsa(bolsa_id):
    # Request dos dados pro banco
    bolsa = Bolsa.query.filter_by(id=bolsa_id).first()

    return render_template('bolsa.html', bolsa=bolsa)

@app.route('/formbolsa', methods=['GET','POST'])
def formBolsa():

    if request.method == 'POST':
        # dados do formulário
        dados = request.form.copy()

        # Convertendo de string para datetime
        dados['dataInicio'] = datetime.strptime(dados['dataInicio'], '%d/%m/%Y')
        dados['dataFim'] = datetime.strptime(dados['dataFim'], '%d/%m/%Y')

        # Adicionando dados na tabela de bolsas
        bolsa = Bolsa(**dados)
        db.session.add(bolsa)
        db.session.commit()

        return redirect(url_for('bolsa', bolsa_id=bolsa.id))
    else:
        return render_template('formBolsa.html')

@app.route('/formGen',method =['GET','POST'])
def formGen():
    
    if request.method == 'POST':
        #dados do cadastro
        dados = resquest.form.copy()
        
        #convertendo de String para datatime
        dados['nascimento'] = datetime.strptime(dados['nascimento'], '%d%m%Y')
        
        # Adicionando dados na tabela de cadastro
        bolsa = Bolsa(**dados)
        db.session.add()
        db.session.commit()
        
        return redirect(url_for('',))
    else:
        return render_template('Index')