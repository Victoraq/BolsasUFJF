
from models import Bolsa
from project import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bolsa')
def bolsa(dados=None):
    # Fazer request dos dados pro banco
    # if not dados:
    #     dados = 
    return render_template('bolsa.html', **dados)

@app.route('/formbolsa', methods=['POST'])
def formBolsa():
    dados = db.session.query(Bolsa).all()

    return redirect(url_for('bolsa',dados=dados))
