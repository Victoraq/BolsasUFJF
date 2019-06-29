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
        if session['logged_in'] and session['aluno']:

            aluno_id = session['user'].id # linha de teste
            data = datetime.now() # data de inscrição

            # anexo submetido
            path = app.config["SOURCE_PATH"]+"project/data/curriculos/cur_{}_{}.pdf".format(aluno_id, bolsa_id)

            request.files['anexo'].save(path)
            # anexo.save(path)

            # Adicionando inscrição a tabela
            # To-do: consertar inscrição
            inscricao = InscricaoBolsa(aluno_id, bolsa_id, data, path)
            app.logger.info('aqui foi')
            db.session.add(inscricao)
            db.session.commit()
            app.logger.info('aqui tambem foi')

            return render_template('/inscricaoConcluida.html')
    
    return render_template('/naoLogado.html')

        # return redirect(url_for('inscricao', bolsa_id=bolsa_id))

@app.route('/formbolsa', methods=['GET','POST'])
def formBolsa():

    # só é possivel acessa a página se estiver logado e for professor
    if session['logged_in'] and not session['aluno']:

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

    else:
        app.logger.info('acesso negado')
        return index()

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
        
        #Procurando usuario no banco de dados
        user = Usuario.query.filter_by(email=dados['email']).first()
        
        if user:
            if user.password == dados['password']:
                user.authenticated = True
                session['logged_in'] = True
                session['aluno'] = user.aluno
                session['user'] = user

                return index()

    return render_template("login.html")

@app.route("/logout", methods=["GET"])
def logout():
    """Logout the current user."""
    user = session['user']
    user.authenticated = False

    # Limpando sessao
    session['logged_in'] = False
    session['aluno'] = None
    session['user'] = None

    return index()