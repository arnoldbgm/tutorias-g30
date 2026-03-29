# Dentro de los resource
# Vamos a definir la logica del negocio
# Aqui vamos a definiir el comportamiento de cada endpoint

from flask_restful import Resource # Clase que me ayuda a definir el comportamiento
from flask import request
from models.productos import ProductosTable
from db import db

class ProductosResource(Resource):
   # HTTP metodos GET, POST, PUT, DELETE

   def get(self):
      return {
         "msg": "GET EXITOSO"
      }

   def post(self):
      # Aqui ira toda la logica para crear
      # un producto
      # Lo primero que se envia es un JSON

      # {
      #    "nombre": "Coca Cola",
      #    "precio": 10.5,
      #    "stock": 100
      # }

      data = request.get_json() # Capturar lo que envian
      
      # Para insetnar en la base de datos, primero
      # hay que formatear la data
      nuevo_producto = ProductosTable(
         nombre = data["nombre"],
         precio = data["precio"],
         stock = data["stock"]
      )

      # Luego de tener todo preparado, pasas a insertar
      db.session.add(nuevo_producto)
      db.session.commit()

      return {
         "msg": "Producto creado exitosamente",
         "nombre": nuevo_producto.nombre,
         "precio": nuevo_producto.precio
      }
