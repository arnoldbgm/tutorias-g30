from flask import Flask
from db import db
from flask_migrate import Migrate
from sqlalchemy import Column, Integer, String, Double

# Crear una instancia de Flask
# 💾 CONFIGURACIONES 
app = Flask(__name__)
# Aqui va tu conexion a tu Bd
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mydatabase.db" # Ejemplo con SQLite

db.init_app(app)
migrate = Migrate(app,db)

# 🧱 MODELOS (Tablas)
# Siempre debes de heredar db.Model
class Product(db.Model):
   __tablename__ = "productos" #Nombrar a la tabla

   # Las columnas de tu tabla
   id = Column(Integer, primary_key=True)
   nombre = Column(String(100))
   precio = Column(Double)
   stock = Column(Integer)
   categoria = Column(String(50))

class Movies(db.Model):
   __tablename__ = "peliculas"

   id = Column(Integer, primary_key=True)
   titulo = Column(String(100))
   director = Column(String(100))
   anio = Column(Integer)

# ↗️ Endpoints (rutas)
# localhost:5000/usuarios => Listar usuarios
# localhost:5000/crear-user => Crear un nuevo usuario
@app.route("/")
def home():
   return "Hola, bienvenido a mi API!"

@app.route("/usuarios")
def listar_usuarios():
   return "Aqui estan todos mis usuarios"

if __name__ == '__main__':
   app.run(debug=True)