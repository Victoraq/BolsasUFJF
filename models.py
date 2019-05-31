
from project import db
from bleach import clean

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

class InscricaoBolsa(db.Model):
    """ Classe modelo para construção da tabela de inscrições de bolsa """

    id = db.Column(db.Integer, primary_key = True)
    id_aluno = db.Column(db.Integer)
    id_bolsa = db.Column(db.Integer)
    data = db.Column(db.DateTime)
    anexo = db.Column(db.Text)

    def __init__(self, id_aluno, id_bolsa, data, anexo):
        """Constructor."""
        self.id_aluno = id_aluno
        self.id_bolsa = id_bolsa
        self.data = data
        self.anexo = anexo