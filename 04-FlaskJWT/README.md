# 📌 **Guía: JWT con Flask + bcrypt 

---

# 📂 **1. Estructura del proyecto**

```bash
/project_root
├── app.py
├── db.py
├── models/
│   └── user.py
├── resources/
│   └── auth_resource.py
├── utils/
│   └── auth.py
├── create_admin.py
```

---

# 🧩 **2. Archivo: `db.py`**

👉 Aquí solo inicializas la BD

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

---

# 🧩 **3. Archivo: `models/user.py`**

👉 Aquí defines el modelo de usuario

```python
from db import db
from sqlalchemy import Column, Integer, String

class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), default="usuario")
```

---

# 🧩 **4. Archivo: `app.py` (IMPORTANTE)**

👉 Este es el **archivo más importante**

```python
from flask import Flask
from flask_restful import Api
from db import db
from flask_migrate import Migrate

# JWT
from flask_jwt_extended import JWTManager

# MODELO (para claims)
from models.user import User

# RESOURCES
from resources.auth_resource import (
    RegisterResource,
    LoginResource,
    RefreshResource
)

app = Flask(__name__)

# 🔹 Configuración BD
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/db_blogs_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 🔹 Configuración JWT
app.config["JWT_SECRET_KEY"] = "super-secret-key"

# 🔹 Inicializar
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# 🔹 JWT
jwt = JWTManager(app)

# 🔥 AQUÍ VA EL PAYLOAD (CLAIMS)
@jwt.additional_claims_loader
def add_claims(identity):
    user = User.query.get(identity)
    return {
        "role": user.role
    }

# 🔹 Rutas
api.add_resource(RegisterResource, '/register')
api.add_resource(LoginResource, '/login')
api.add_resource(RefreshResource, '/refresh')

if __name__ == '__main__':
    app.run(debug=True)
```

---

# 🧩 **5. Archivo: `resources/auth_resource.py`**

👉 Aquí va TODO lo de autenticación

```python
from flask_restful import Resource
from flask import request
from db import db
from models.user import User

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)

import bcrypt
```

---

## 🔐 Registro

```python
class RegisterResource(Resource):

    def post(self):
        data = request.get_json()

        if User.query.filter_by(username=data['username']).first():
            return {'message': 'Usuario ya existe'}, 400

        hashed = bcrypt.hashpw(
            data['password'].encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        user = User(
            username=data['username'],
            password=hashed,
            role="usuario"
        )

        db.session.add(user)
        db.session.commit()

        return {'message': 'Usuario creado'}, 201
```

---

## 🔐 Login

```python
class LoginResource(Resource):

    def post(self):
        data = request.get_json()

        user = User.query.filter_by(username=data['username']).first()

        if not user:
            return {'message': 'Credenciales incorrectas'}, 401

        if not bcrypt.checkpw(
            data['password'].encode('utf-8'),
            user.password.encode('utf-8')
        ):
            return {'message': 'Credenciales incorrectas'}, 401

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
```

---

## 🔁 Refresh

```python
class RefreshResource(Resource):

    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()

        new_access_token = create_access_token(identity=user_id)

        return {'access_token': new_access_token}
```

---

# 🧩 **6. Archivo: `utils/auth.py` (Middleware)**

👉 Aquí proteges rutas

```python
from flask_jwt_extended import jwt_required, get_jwt

def admin_required(fn):

    @jwt_required()
    def wrapper(*args, **kwargs):

        claims = get_jwt()

        if claims.get("role") != "admin":
            return {'message': 'Solo admin'}, 403

        return fn(*args, **kwargs)

    return wrapper
```

---

# 🧩 **7. Archivo: `create_admin.py`**

👉 Para crear admin SIN endpoint

```python
from app import app
from db import db
from models.user import User
import bcrypt

with app.app_context():

    if not User.query.filter_by(username="admin").first():

        hashed = bcrypt.hashpw(
            "admin123".encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        admin = User(
            username="admin",
            password=hashed,
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("✅ Admin creado")
```

---

# 🧪 **8. Flujo de prueba**

## 1. Registro

```json
POST /register
{
  "username": "juan",
  "password": "123456"
}
```

---

## 2. Login

```json
POST /login
```

👉 devuelve tokens

---

## 3. Usar token

```
Authorization: Bearer TOKEN
```

---

## 4. Refresh

```json
POST /refresh
```

---

# 🧠 **RESUMEN CLAVE PARA TU CLASE**

👉 ¿Dónde va cada cosa?

| Archivo            | Qué hace                       |
| ------------------ | ------------------------------ |
| `app.py`           | Configura JWT + rutas + claims |
| `models/user.py`   | Modelo                         |
| `auth_resource.py` | Login / Register               |
| `auth.py`          | Middleware                     |
| `create_admin.py`  | Crear admin                    |
