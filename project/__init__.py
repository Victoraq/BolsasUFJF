from flask import Flask, redirect, url_for, render_template, request, session
from flask_session import Session
import json
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import delete, insert, update

# Configure app
app = Flask(__name__)

# Configure the database
app.config.from_pyfile('/home/victor/Documentos/Modelagem_Sistemas/trab/project/app.cfg')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# @app.route('/')
# def index():
#     return render_template('formBolsa.html')