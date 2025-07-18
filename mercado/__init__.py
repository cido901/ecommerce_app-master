from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# mercado/__init__.py
# Inicializa o app Flask, SQLAlchemy e Bcrypt
# Este arquivo configura o contexto da aplicação e importa as rotas
# para garantir que estejam registradas no app Flask.
# Também configura a URI do banco de dados e a chave secreta do app.    
db = SQLAlchemy()
login_manager = LoginManager()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mercado.db"
app.config["SECRET_KEY"] = '25212afdc696c15e058d8d4b'
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager.init_app(app)

from mercado import routes