# Todo lo que va estar dentro de la carpeta de models
# Van a ser solamente TABLAS

from db import db
from sqlalchemy import Column, Integer, String, Float, DateTime

class ProductosTable(db.Model):

   # Definimos el nombre de la tabla
   __tablename__ = "productos"

   # Definimos las columnas
   id = Column(Integer, primary_key=True)
   nombre = Column(String(100), nullable=False)
   precio = Column(Float, nullable=False)
   stock = Column(Integer, nullable=False)
   created_at = Column(DateTime, server_default=db.func.now())