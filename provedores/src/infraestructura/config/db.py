from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db_provedores = SQLAlchemy()


def init_db_provedores(app: Flask):
    db_provedores.init_app(app)

