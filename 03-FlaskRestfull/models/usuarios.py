from db import db
from sqlalchemy import Column, Integer, String

class UsuariosTable(db.Model):
   __tablename__ = "usuarios"

   id = Column(Integer, primary_key=True)
   username = Column(String(50), unique=True, nullable=False)
   password = Column(String(255), nullable=False)
   role = Column(String(20), default="usuario")