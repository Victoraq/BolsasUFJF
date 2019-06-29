
from project import db
from bleach import clean
from sqlalchemy import UniqueConstraint
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Bolsa(db.Model):
    """Classe modelo para construção da tabela de Bolsas"""

    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.Text, unique = True)
    modalidade = db.Column(db.Text)
    carga_horaria = db.Column(db.String(20))
    remuneracao = db.Column(db.String(60))
    departamento = db.Column(db.Text)
    dataInicio = db.Column(db.DateTime)
    dataFim = db.Column(db.DateTime)
    descricao = db.Column(db.Text)
    selecao = db.Column(db.Text)
    ativa = db.Column(db.Boolean)

    def __init__(self, titulo, modalidade, carga_horaria, remuneracao,
                 departamento, dataInicio, dataFim, descricao, selecao, ativa=True):
        """Constructor."""
        self.titulo = clean(titulo)
        self.modalidade = clean(modalidade)
        self.carga_horaria = clean(carga_horaria)
        self.remuneracao = clean(remuneracao)
        self.departamento = clean(departamento)
        self.dataInicio = dataInicio
        self.dataFim = dataFim
        self.descricao = clean(descricao)
        self.selecao = clean(selecao)
        self.ativa = ativa

    def addBolsa(titulo, modalidade, carga_horaria, remuneracao, departamento, dataInicio, dataFim, descricao, selecao):
        """ Armazena uma nova bolsa no banco de dados """

        bolsa = Bolsa(titulo, modalidade, carga_horaria, remuneracao,
                 departamento, dataInicio, dataFim, descricao, selecao)
        
        db.session.add(bolsa)
        db.session.commit()

        return bolsa

    def getBolsa(bolsa_id):
        """ Retorna bolsa com id passado como parâmetro """
        bolsa = Bolsa.query.filter_by(id=bolsa_id).first()

        return bolsa

    def buscarBolsas(busca=''): 
        """ Retorna todas as bolsas relacionadas a busca """
        
        if busca == '':
            bolsas = Bolsa.query.order_by(Bolsa.id).all()
            
            return bolsas

        else: 
            bolsas = Bolsa.query.filter(Bolsa.titulo.like(f'%{busca}%')).all()

            return bolsas
    

class Usuario(db.Model):
  
    "Classe de Controle de Usuários registrado na aplicação"
    
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.Text)
    sobrenome = db.Column (db.Text)
    telefone = db.Column(db.Text, unique = True)
    email = db.Column(db.Text, unique = True)
    nascimento = db.Column(db.DateTime)
    periodo = db.Column (db.Integer)
    matricula = db.Column (db.String(8))
    curso = db.Column(db.Integer)
    username = db.Column(db.String, unique = True)
    password = db.Column(db.String(20))
    aluno = db.Column(db.Boolean)
    professor = db.Column(db.Boolean)
    authenticated = db.Column(db.Boolean, default=False)
    
    def __init__(self,nome,sobrenome,telefone,email,nascimento,periodo,
               matricula,curso,username,password,role):
        """Constructor"""

        self.nome = clean(nome)
        self.sobrenome = clean(sobrenome)
        self.telefone = clean(telefone)
        self.email = clean(email)
        self.nascimento = nascimento
        self.periodo = clean(periodo)
        self.matricula= clean(matricula)
        self.curso = clean(curso)
        self.username = clean(username)
        self.password = clean(password)
        self.aluno = role == 'Aluno'
        self.professor = role == 'Professor'

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def addUsuario(nome,sobrenome,tel,email,nascimento,periodo,matricula,curso,username,password,role):
        
        user = Usuario(nome,sobrenome,tel,email,nascimento,periodo,matricula,curso,username,password,role)
        
        db.session.add(user)
        db.session.commit()

        return user
        
    
class InscricaoBolsa(db.Model):
    """ Classe modelo para construção da tabela de inscrições de bolsa """

    id = db.Column(db.Integer, primary_key = True)
    id_aluno = db.Column(db.Integer)
    id_bolsa = db.Column(db.Integer)
    data = db.Column(db.DateTime)
    anexo = db.Column(db.Text)

    __table_args__ = (UniqueConstraint('id_aluno', 'id_bolsa', name='inscricao_unica'),)

    def __init__(self, id_aluno, id_bolsa, data, anexo):
        """Constructor."""
        self.id_aluno = id_aluno
        self.id_bolsa = id_bolsa
        self.data = data
        self.anexo = anexo

        # Enviando email para professor com dados da inscrição
        self.emailDadosInscricao()

    def emailDadosInscricao(self):
        """Envia email com dados de inscrição para professor"""
        port = 465  # For SSL
        password = 'bolsas@123'
        password = ''

        sender_email = "bolsasufjf@gmail.com"
        receiver_email = "bolsasufjf@gmail.com"
        subject = f"Candidatura da bolsa mamofaf"
        # body = f"""\
        # Aluno: {aluno.nome} {aluno.sobrenome}
        
        # Matricula: {aluno.matricula}

        # Curso: {aluno.curso}

        # E-mail: {aluno.email}
        # """
        body = """\
        Aluno: aluno.nome} aluno.sobrenome
        
        Matricula: aluno.matricula

        Curso: aluno.curso

        E-mail: aluno.email
        """

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        filename = self.anexo

        # Open PDF file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        
        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename=curriculo.pdf",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)