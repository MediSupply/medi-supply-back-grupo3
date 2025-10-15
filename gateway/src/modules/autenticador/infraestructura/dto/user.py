from enum import Enum

from config.db import db
from sqlalchemy import Column
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, Nullable, Table
from sqlalchemy.orm import declarative_base

Base = db.declarative_base()


class Role(Enum):
    """Database role enum for infrastructure layer"""

    ADMIN = "ADMIN"
    USER = "USER"


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String, nullable=False, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    role = db.Column(SQLEnum(Role), nullable=False, default=Role.USER)
