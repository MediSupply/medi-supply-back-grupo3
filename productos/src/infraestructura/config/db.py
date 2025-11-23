from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db_productos = SQLAlchemy()


def init_db_productos(app: Flask):
    db_productos.init_app(app)
