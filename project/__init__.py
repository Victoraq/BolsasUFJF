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

    #Request todas as bolsas cadastradas
    bolsas = Bolsa.buscarBolsas()

    if len(bolsas) >= 4:
        bolsas = bolsas[:4]


    if 'aluno' in session and session['logged_in'] and session['aluno']:
        return render_template('index.html', session='aluno', user=session['user'], bolsas=bolsas)
    else:
        if 'professor' in session and session['professor']:
            return render_template('index.html', session='professor', user=session['user'], bolsas=bolsas)

    return render_template('index.html', session='naoLogado', user=None, bolsas=bolsas)
    


from models import Bolsa, InscricaoBolsa, Usuario

@app.route('/bolsa/<int:bolsa_id>', methods=['GET','POST'])
def bolsa(bolsa_id):
    # Request dos dados da bolsa no banco
    bolsa = Bolsa.getBolsa(bolsa_id)

    if request.method == 'GET':

        prof = Usuario.query.filter_by(id=bolsa.prof_id).first()
        if prof:
            nome = prof.nome + " " + prof.sobrenome 
        else: 
            nome = 'Não disponivel'

        return render_template('bolsa.html', bolsa=bolsa, nome=nome, professor=prof)
    
    else:
        if session['logged_in'] and session['aluno']:

            aluno_id = session['user'].id # linha de teste
            data = datetime.now() # data de inscrição

            # anexo submetido
            path = app.config["SOURCE_PATH"]+"project/data/curriculos/cur_{}_{}.pdf".format(aluno_id, bolsa_id)

            request.files['anexo'].save(path)

            # Adicionando inscrição a tabela
            inscricao = InscricaoBolsa(aluno_id, bolsa_id, data, path)
            db.session.add(inscricao)
            db.session.commit()

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
            
            #id do professor
            dados['professor'] = int(session['user'].id)

            # Adicionando dados na tabela de bolsas
            bolsa = Bolsa.addBolsa(**dados)

            return render_template("cadastradaSucesso.html")
        else:
            return render_template('formBolsa.html')

    else:
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



@app.route('/professor/<int:professor_id>', methods=['GET'])
def professor(professor_id):
    # Request dos dados do professor no banco
    professor = Usuario.buscarProfessorID(professor_id)
    bolsas = Bolsa.query.filter_by(prof_id=professor_id).all() 
    return render_template('paginaProfessor.html', professor=professor,bolsas=bolsas)


@app.route('/professores', methods=['GET', 'POST'])
def mostraProfessores():
    if request.method == 'GET':

        # Todos os professores são mostrados por nome
        professores = Usuario.buscarProfessores()

        apresentacao = 'Professores cadastrados:'

        return render_template('paginaProfessores.html', professores=professores, apresentacao=apresentacao)

    else:

        try:
            busca = request.form['busca']
        except:
            busca = ''

        if busca == '':
            # Todos os professores são mostrados por nome
            professores = Usuario.buscarProfessores()

            apresentacao = f'Professores cadastrados:'

        else:
            # filtra os professores de acordo com o nome passado por parametro
            nome = busca
            professores = Usuario.buscarProfessorNome(nome)

            if professores is None :
                apresentacao = f'Professor não encontrado :( '
            else:
                apresentacao = f'Resultado da busca:'

        return render_template('paginaProfessores.html', professores=professores, apresentacao=apresentacao)


@app.route('/Aluno/<int:user_id>',methods=['GET'])
def paginaAluno(user_id):
     

    if session['logged_in'] and session['aluno']:
        user = session['user']
        inscricoes = InscricaoBolsa.buscaInscricaoAluno(user.id)
        bolsas = InscricaoBolsa.buscaNome(inscricoes)

        return render_template('PaginaAluno.html',bolsas=bolsas, user=user)
    elif session['logged_in'] and session['professor']:
        user = session['user']
        return redirect(url_for('professor',professor_id = user.id))
    else:
        return render_template('/naoLogado.html')

    

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

                if user.aluno == True:
                    session['aluno'] = user.aluno
                else:
                    session['professor'] = user.professor

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
