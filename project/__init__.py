from flask import Flask, redirect, url_for, render_template, request, session
from flask_session import Session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import delete, insert, update
from flask_login import current_user, login_required, LoginManager, login_user
from flask_user import roles_required

# Configure app
app = Flask(__name__)

# Configure the database
app.config.from_pyfile('app.cfg')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

# configurate sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def index():
    return render_template('index.html')

from models import Bolsa, InscricaoBolsa, Usuario

@app.route('/bolsa/<int:bolsa_id>', methods=['GET','POST'])
def bolsa(bolsa_id):
    # Request dos dados da bolsa no banco
    bolsa = Bolsa.getBolsa(bolsa_id)

    if request.method == 'GET':
        return render_template('bolsa.html', bolsa=bolsa)
    
    else:
        # if current_user.is_authenticated:
        if True: # linha de teste
            # aluno_id = current_user.id  # id do aluno logado
            aluno_id = 1 # linha de teste
            data = datetime.now() # data de inscrição

            # anexo submetido
            path = app.config["SOURCE_PATH"]+"project/data/curriculos/cur_{}_{}.pdf".format(aluno_id, bolsa_id)

            request.files['anexo'].save(path)
            # anexo.save(path)

            # Adicionando inscrição a tabela
            inscricao = InscricaoBolsa(aluno_id, bolsa_id, data, path)
            db.session.add(inscricao)
            db.session.commit()

            return render_template('/inscricaoConcluida.html')

        else:
            return redirect(url_for('login'))

        # return redirect(url_for('inscricao', bolsa_id=bolsa_id))

@app.route('/formbolsa', methods=['GET','POST'])
# @roles_required(['Professor']) # Para abrir página o usuário deve estar logado como professor.
def formBolsa():

    if request.method == 'POST':
        # dados do formulário
        dados = request.form.copy()

        # Convertendo de string para datetime
        dados['dataInicio'] = datetime.strptime(dados['dataInicio'], '%d/%m/%Y')
        dados['dataFim'] = datetime.strptime(dados['dataFim'], '%d/%m/%Y')

        # Adicionando dados na tabela de bolsas
        bolsa = Bolsa.addBolsa(**dados)

        return redirect(url_for('bolsa', bolsa_id=bolsa.id))
    else:
        return render_template('formBolsa.html')

@app.route('/bolsas', methods=['GET','POST'])
def feed():
    if request.method == 'GET':

        # Todas as bolsas disponíveis são mostradas
        bolsas = Bolsa.buscarBolsas()

        apresentacao = 'Lista das Bolsas ofertadas:'

        return render_template('feed.html', bolsas=bolsas, apresentacao=apresentacao)
    
    else:

        try:
            busca = request.form['busca']
        except:
            busca = ''
        
        if busca == '':
            # Todas as bolsas disponíveis são mostradas
            bolsas = Bolsa.buscarBolsas()

            apresentacao = f'Lista das Bolsas ofertadas:'        

        else:
            # filtra bolsas com string parecida com a buscada
            bolsas = Bolsa.buscarBolsas(busca)

            apresentacao = f'Lista das Bolsas ofertadas relacionadas a {busca}:'        

        return render_template('feed.html', bolsas=bolsas, apresentacao=apresentacao)

@app.route('/Aluno',methods=['GET'])
def paginaAluno():
    return render_template('PaginaAluno.html')
    
@app.route('/Professor')
def paginaProfessor():
    return render_template('PaginaProfessor.html')

@login_manager.user_loader
def load_user(user_id):
    return Usuario.get(user_id)

@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():

    if request.method == 'POST':
        # dados do formulário
        dados = request.form.copy()

        # Convertendo de string para datetime
        dados['nascimento'] = datetime.strptime(dados['nascimento'], '%d/%m/%Y')

        # adicionando usuário a tabela de Usuários
        usuario = Usuario.addUsuario(**dados)

        return redirect(url_for("login"))

    return render_template('paginaCadastro.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    """For GET requests, display the login form. 
    For POSTS, login the current user by processing the form.
    """
    if request.method == 'POST':
        # dados do formulário
        dados = request.form.copy()
        user = Usuario.query.filter_by(email=dados['email']).first()
        app.logger.info(user)
        if user:
            if user.password == dados['password']:
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                current_user = user # ainda não consigo pegar dados do current user

                return redirect(url_for("/")) # to-do: nao esta redirecionando nao sei porque

    return render_template("login.html")

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for("/"))