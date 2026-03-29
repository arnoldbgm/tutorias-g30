from flask import Flask
from db import db
from flask_migrate import Migrate
from flask_restful import Api

# Importar tus modelos (tablas)
from models import productos, ventas
from resources.productos_resource import ProductosResource

app = Flask(__name__) # Instancia de tu servidor

# Conexion con tu bd (mysql, mariadb, pg, oracle, sqlite, etc)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:root@localhost:5432/mini_pos"

db.init_app(app) # Configuracion de Sqlalchemy

migrate  = Migrate(app, db)

api = Api(app) # Configura tu servidor para ser una API

# Aqui vas a definir las rutas de tu API
api.add_resource(ProductosResource, "/productos")


if __name__ == '__main__':
   app.run(debug=True) # Ejecucion del servidor