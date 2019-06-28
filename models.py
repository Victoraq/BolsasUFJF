
from project import db
from bleach import clean
from sqlalchemy import UniqueConstraint

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



class Usuario(db.Usuario):
  
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
    senha = db.Column(db.String(20))
    status = db.Column(db.Integer) #Se refere ao status de Professor ou Aluno, um boolean?#
    
    def _init_(self, id, nome,sobrenome,telefone,email,nascimento,periodo,
               matricula,chave,username,senha,status):
        """Constructor"""
        
        self.id = clean(id)
        self.nome = clean(nome)
        self.sobrenome = clean(sobrenome)
        self.telefone = clean(telefone)
        self.email = clean(email)
        self.nascimento = clean(nascimento)
        self.periodo = clean(periodo)
        self.matricula= clean(matricula)
        self.curso = clean(curso)
        self.username = clean(username)
        self.senha = clean(senha)
    
    
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