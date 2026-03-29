# Todo lo que va estar dentro de la carpeta de models
# Van a ser solamente TABLAS

from db import db
from sqlalchemy import Column, Integer, Float, ForeignKey


class VentasTable(db.Model):

   __tablename__ = "ventas"

   id = Column(Integer, primary_key=True)
   cantidad = Column(Integer, nullable=False)
   total = Column(Float, nullable=False)

   # La relacion con la tabla productos
   producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)