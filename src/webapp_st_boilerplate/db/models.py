from cryptography.fernet import Fernet
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from webapp_st_boilerplate.config import settings
from webapp_st_boilerplate.db.database import Base


ENCRYPTION_KEY = settings.db_secrets.db_encryption_key
if not ENCRYPTION_KEY:
    raise OSError("La variabile d'ambiente db_encryption_key non è impostata.")

f = Fernet(ENCRYPTION_KEY.encode())


class Entity(Base):
    __tablename__ = "Entity"

    id = Column(Integer, primary_key=True)
    _entityName = Column("entityName", String(100))

    @hybrid_property
    def entityName(self):
        if self._entityName:
            try:
                return f.decrypt(self._entityName.encode()).decode()
            except Exception:
                return None
        return None

    @entityName.setter
    def entityName(self, value: str):
        if value is not None:
            self._entityName = f.encrypt(value.encode()).decode()
        else:
            self._entityName = None

    user_link = relationship("User", back_populates="entity_link")


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    entityId = Column(Integer, ForeignKey("Entity.id"))
    _name = Column("name", String(100))
    email = Column(String(100))
    password = Column(String(100))
    _role = Column("role", String(5))
    disabled = Column(Boolean)
    lastLogin = Column(DateTime)
    createdDate = Column(DateTime)
    updatedDate = Column(DateTime)

    @hybrid_property
    def name(self):
        if self._name:
            try:
                return f.decrypt(self._name.encode()).decode()
            except Exception:
                return None
        return None

    @name.setter
    def name(self, value: str):
        if value is not None:
            self._name = f.encrypt(value.encode()).decode()
        else:
            self._name = None

    @hybrid_property
    def role(self):
        if self._role:
            try:
                return f.decrypt(self._role.encode()).decode()
            except Exception:
                return None
        return None

    @role.setter
    def role(self, value: str):
        if value is not None:
            self._role = f.encrypt(value.encode()).decode()
        else:
            self._role = None

    entity_link = relationship("Entity", back_populates="user_link")
