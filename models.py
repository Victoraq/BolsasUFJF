
import db

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

    def __init__(self, titulo, modalidade, carga_horaria, remuneracao,
                 departamento, dataInicio, dataFim, descricao, selecao):
        """Constructor."""
        self.titulo = titulo
        self.modalidade = modalidade
        self.carga_horaria = carga_horaria
        self.remuneracao = remuneracao
        self.departamento = departamento
        self.dataInicio = dataInicio
        self.dataFim = dataFim
        self.descricao = descricao
        self.selecao = selecao
