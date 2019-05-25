# from flask import Flask, redirect, url_for, render_template, request, session
# from flask_session import Session
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from sqlalchemy import delete, insert, update
from models import Bolsa
from project import app

@app.route('/')
def index():
    return render_template('formBolsa.html')

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
        
# if __name__ == '__main__':
#     app.run(debug=True)