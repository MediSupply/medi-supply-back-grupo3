from typing import List, Optional

from src.dominio.entities.cliente import Cliente
from src.dominio.repositorios.cliente_repository import ClienteRepository
from src.infraestructura.config.db import db_clientes
from src.infraestructura.dto.cliente import ClienteModel


class ClienteRepositoryImpl(ClienteRepository):
    """Implementación del repositorio de clientes con base de datos SQLAlchemy."""

    def _model_to_entity(self, model: ClienteModel) -> Cliente:
        """Convierte un modelo de base de datos a una entidad del dominio."""
        return Cliente(
            id=model.id,
            nombre=model.nombre,
            email=model.email,
            telefono=model.telefono,
            direccion=model.direccion,
            razon_social=model.razon_social,
            nit=model.nit,
        )

    def _entity_to_model(self, entity: Cliente) -> ClienteModel:
        """Convierte una entidad del dominio a un modelo de base de datos."""
        return ClienteModel(
            id=entity.id,
            nombre=entity.nombre,
            email=entity.email,
            telefono=entity.telefono,
            direccion=entity.direccion,
            razon_social=entity.razon_social,
            nit=entity.nit,
        )

    def obtener_todos(self) -> List[Cliente]:
        """Obtiene todos los clientes."""
        try:
            models = db_clientes.session.query(ClienteModel).all()
            return [self._model_to_entity(model) for model in models]
        except Exception as e:
            print(f"Error obteniendo todos los clientes: {e}")
            return []

    def obtener_por_id(self, cliente_id: str) -> Optional[Cliente]:
        """Obtiene un cliente por su ID."""
        try:
            model = db_clientes.session.query(ClienteModel).filter_by(id=cliente_id).first()
            if model:
                return self._model_to_entity(model)
            return None
        except Exception as e:
            print(f"Error obteniendo cliente por ID: {e}")
            return None

    def obtener_por_categoria(self, categoria: str) -> List[Cliente]:
        """Obtiene clientes por categoría."""
        # Cliente no tiene categoría, por ahora retornamos lista vacía
        # Si se necesita esta funcionalidad, se debe agregar categoría a la entidad
        return []

    def buscar_por_nombre(self, nombre: str) -> List[Cliente]:
        """Busca clientes por nombre."""
        try:
            nombre_lower = f"%{nombre.lower()}%"
            models = db_clientes.session.query(ClienteModel).filter(ClienteModel.nombre.ilike(nombre_lower)).all()
            return [self._model_to_entity(model) for model in models]
        except Exception as e:
            print(f"Error buscando clientes por nombre: {e}")
            return []

    def crear(self, cliente: Cliente) -> Cliente:
        """Crea un nuevo cliente."""
        try:
            # Verificar si ya existe un cliente con el mismo NIT
            existing = db_clientes.session.query(ClienteModel).filter_by(nit=cliente.nit).first()
            if existing:
                raise ValueError(f"Ya existe un cliente con el NIT {cliente.nit}")

            model = self._entity_to_model(cliente)
            db_clientes.session.add(model)
            db_clientes.session.commit()
            return self._model_to_entity(model)
        except Exception as e:
            db_clientes.session.rollback()
            print(f"Error creando cliente: {e}")
            raise
