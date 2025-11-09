from src.infraestructura.config.db import db_clientes


class ClienteModel(db_clientes.Model):
    """Modelo de base de datos para Cliente."""

    __tablename__ = "clientes"

    id = db_clientes.Column(db_clientes.String, nullable=False, primary_key=True)
    nombre = db_clientes.Column(db_clientes.String, nullable=False)
    email = db_clientes.Column(db_clientes.String, nullable=False)
    telefono = db_clientes.Column(db_clientes.String, nullable=False)
    direccion = db_clientes.Column(db_clientes.String, nullable=False)
    razon_social = db_clientes.Column(db_clientes.String, nullable=False)
    nit = db_clientes.Column(db_clientes.String, nullable=False, unique=True)

    def __repr__(self):
        return f"<ClienteModel {self.id}: {self.nombre}>"

