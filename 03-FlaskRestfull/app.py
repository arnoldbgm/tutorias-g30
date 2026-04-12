from flask import Flask
from db import db
from flask_migrate import Migrate
from flask_restful import Api

# Importar tus modelos (tablas)
from models import productos, ventas, usuarios
from resources.productos_resource import ProductosResource
from resources.auth_resource import (RegisterUserResource, 
                                    LoginUserResource, 
                                    RefreshTokenResource)

# Importaciones de JWT
from flask_jwt_extended import JWTManager

app = Flask(__name__)  # Instancia de tu servidor

# Conexion con tu bd (mysql, mariadb, pg, oracle, sqlite, etc)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:root@localhost:5432/mini_pos"
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 60 # 1 minuto
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 60 * 5 # 5 minutos

jwt = JWTManager(app)

db.init_app(app)  # Configuracion de Sqlalchemy

migrate = Migrate(app, db)

api = Api(app)  # Configura tu servidor para ser una API

# Aqui vas a definir las rutas de tu API
api.add_resource(ProductosResource, "/productos")
api.add_resource(RegisterUserResource, "/registro")
api.add_resource(LoginUserResource, "/login")
api.add_resource(RefreshTokenResource, "/refresh")

if __name__ == '__main__':
    app.run(debug=True)  # Ejecucion del servidor
