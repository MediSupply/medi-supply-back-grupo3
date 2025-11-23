from src.dominio.entities.provedor import Pais
from src.infraestructura.config.db import db_provedores


class ProvedorModel(db_provedores.Model):
    """Modelo de base de datos para Provedor."""

    __tablename__ = "provedores"

    id = db_provedores.Column(db_provedores.Integer, nullable=False, primary_key=True, autoincrement=True)
    nit = db_provedores.Column(db_provedores.Integer, nullable=False, unique=True)
    nombre = db_provedores.Column(db_provedores.String, nullable=False)
    pais = db_provedores.Column(db_provedores.String, nullable=False)
    direccion = db_provedores.Column(db_provedores.String, nullable=False)
    telefono = db_provedores.Column(db_provedores.Integer, nullable=False)
    email = db_provedores.Column(db_provedores.String, nullable=False)

    def __repr__(self):
        return f"<ProvedorModel {self.id}: {self.nombre}>"
