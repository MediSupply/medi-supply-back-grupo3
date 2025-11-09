from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db_clientes = SQLAlchemy()


def init_db_clientes(app: Flask):
    db_clientes.init_app(app)
