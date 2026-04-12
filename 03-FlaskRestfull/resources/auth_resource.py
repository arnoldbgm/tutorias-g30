from flask_restful import Resource
from flask import request
from models.usuarios import UsuariosTable
from db import db
from flask_jwt_extended import (create_access_token, 
                                create_refresh_token,
                                get_jwt_identity,
                                jwt_required)

import bcrypt

class RegisterUserResource(Resource):
   
   # Crear un endpoint para el registro de usuarios
   def post(self):
      # Siempre se captura la informacion que se envia
      data = request.get_json()
      # {
      #    "username": "andres",
      #    "password": "123456"
      # }

      # Siempre se valida que el usuario no exista
      if UsuariosTable.query.filter_by(username=data["username"]).first():
         return {
            "msg": "El usuario ya existe"
         }, 400
      
      # Encriptado la contraseña
      hashed = bcrypt.hashpw(
                  data["password"].encode("utf-8"), 
                  bcrypt.gensalt()
                  ).decode("utf-8")

      # Crear el nuevo usuario
      new_user = UsuariosTable(
         username = data["username"],
         password = hashed
      )

      # Insetaramos el usuarios
      db.session.add(new_user)
      db.session.commit()

      return {
         "msg": "Usuario creado exitsomante"
      }, 201
   
class LoginUserResource(Resource):
   # Un login siempre va a ser de tipo POST
   def post (self):
      data = request.get_json()
      # {
      #    "username" : "andres",
      #    "password" : "123456"
      # }

      # Vamos a buscar el usuario dentro de la bd
      # Lo vamos a buscar por el username

      user = UsuariosTable.query.filter_by(username=data["username"]).first()

      if not user:
         return {
            "msg": "Usuario incorrecto o contraseña incorrecta"
         }, 401
      
      # Vamos a comprar las contraseñas
      if not bcrypt.checkpw(data["password"].encode("utf-8"), 
                            user.password.encode("utf-8")):
         return {
            "msg": "Usuario incorrecto o contraseña incorrecta"
         }, 401

      # Si el usuario es el correcto
      # Debemos de crear el access token y el refresh token

      access_token = create_access_token(identity=user.username)
      refresh_token = create_refresh_token(identity=user.username)

      return {
         'access_token': access_token,
         'refresh_token': refresh_token   
      }, 200
   

class RefreshTokenResource(Resource):

   @jwt_required(refresh=True)
   def post(self):
      user_username = get_jwt_identity() # Obtener el usuario que esta haciendo la peticion
      new_access_token = create_access_token(identity=user_username)

      return {
         "access_token": new_access_token
      }, 201