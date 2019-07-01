from project import db
from models import Bolsa, Usuario, InscricaoBolsa
from datetime import datetime

# create database
db.create_all()

# test
#db.session.add(Bolsa("titulo","Iniciação cientifica", "20h", "Voluntário","Reitoria",datetime.now(),datetime.now(),"Testando","Testando"))

db.session.commit()