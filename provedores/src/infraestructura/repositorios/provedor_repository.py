from typing import List, Optional

from src.dominio.entities.provedor import Pais, Provedor
from src.dominio.repositorios.provedor_repository import ProvedorRepository
from src.infraestructura.config.db import db_provedores
from src.infraestructura.dto.provedor import ProvedorModel


class ProvedorRepositoryImpl(ProvedorRepository):
    """Implementación del repositorio de proveedores con base de datos SQLAlchemy."""

    def _model_to_entity(self, model: ProvedorModel) -> Provedor:
        """Convierte un modelo de base de datos a una entidad del dominio."""
        return Provedor(
            id=model.id,
            nit=model.nit,
            nombre=model.nombre,
            pais=Pais(model.pais.lower()),
            direccion=model.direccion,
            telefono=model.telefono,
            email=model.email,
        )

    def _entity_to_model(self, entity: Provedor, include_id: bool = True) -> ProvedorModel:
        """Convierte una entidad del dominio a un modelo de base de datos."""
        model = ProvedorModel(
            nit=entity.nit,
            nombre=entity.nombre,
            pais=entity.pais.value,
            direccion=entity.direccion,
            telefono=entity.telefono,
            email=entity.email,
        )
        if include_id and entity.id:
            model.id = entity.id
        return model

    def obtener_todos(self) -> List[Provedor]:
        """Obtiene todos los proveedores."""
        try:
            models = db_provedores.session.query(ProvedorModel).all()
            return [self._model_to_entity(model) for model in models]
        except Exception:
            return []

    def obtener_por_id(self, provedor_id: int) -> Optional[Provedor]:
        """Obtiene un proveedor por su ID."""
        try:
            model = db_provedores.session.query(ProvedorModel).filter_by(id=provedor_id).first()
            if model:
                return self._model_to_entity(model)
            return None
        except Exception:
            return None

    def obtener_por_nit(self, nit: int) -> Optional[Provedor]:
        """Obtiene un proveedor por su NIT."""
        try:
            model = db_provedores.session.query(ProvedorModel).filter_by(nit=nit).first()
            if model:
                return self._model_to_entity(model)
            return None
        except Exception:
            return None

    def obtener_por_pais(self, pais: str) -> List[Provedor]:
        """Obtiene proveedores por país."""
        try:
            models = db_provedores.session.query(ProvedorModel).filter_by(pais=pais.lower()).all()
            return [self._model_to_entity(model) for model in models]
        except Exception:
            return []

    def buscar_por_nombre(self, nombre: str) -> List[Provedor]:
        """Busca proveedores por nombre."""
        try:
            models = db_provedores.session.query(ProvedorModel).filter(ProvedorModel.nombre.ilike(f"%{nombre}%")).all()
            return [self._model_to_entity(model) for model in models]
        except Exception:
            return []

    def crear(self, provedor: Provedor) -> Provedor:
        """Crea un nuevo proveedor."""
        try:
            model = self._entity_to_model(provedor, include_id=False)
            db_provedores.session.add(model)
            db_provedores.session.commit()
            db_provedores.session.refresh(model)
            return self._model_to_entity(model)
        except Exception as e:
            db_provedores.session.rollback()
            raise e

    def actualizar(self, provedor: Provedor) -> Provedor:
        """Actualiza un proveedor existente."""
        try:
            model = db_provedores.session.query(ProvedorModel).filter_by(id=provedor.id).first()
            if not model:
                raise ValueError(f"Proveedor con ID {provedor.id} no encontrado")

            model.nit = provedor.nit
            model.nombre = provedor.nombre
            model.pais = provedor.pais.value
            model.direccion = provedor.direccion
            model.telefono = provedor.telefono
            model.email = provedor.email

            db_provedores.session.commit()
            db_provedores.session.refresh(model)
            return self._model_to_entity(model)
        except ValueError:
            raise
        except Exception as e:
            db_provedores.session.rollback()
            raise e

    def eliminar(self, provedor_id: int) -> bool:
        """Elimina un proveedor por su ID."""
        try:
            model = db_provedores.session.query(ProvedorModel).filter_by(id=provedor_id).first()
            if not model:
                return False

            db_provedores.session.delete(model)
            db_provedores.session.commit()
            return True
        except Exception:
            db_provedores.session.rollback()
            return False
