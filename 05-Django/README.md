# Primeros pasos con Django 🦾🐍
[<img src="https://daiderd.com/nix-darwin/images/nix-darwin.png" width="200px" alt="logo" />](https://github.com/LnL7/nix-darwin)
### 1. Crear un entorno virtual 🐍

```bash
python -m venv venv

```

### 2. Activar el entorno virtual ⚡
- En Windows:
    ```bash
        venv\Scripts\activate
    ```
- En gitbash:
    ```
        source venv/Scripts/activate
    ```
- En macOS y Linux:
    ```bash
        source venv/bin/activate
    ```


### 3. Instalacion de Django
```bash
pip install django
```
### 4. Crear un proyecto en Django
Con este comando crearemos nuestro primer proyecto en Django
```bash
django-admin startproject core .
```
### 5. Como levantar mi proyecto de Django
```bash
python manage.py migrate
python manage.py runserver
```
### 6. Crear un superusuario en Django
```bash
python manage.py createsuperuser
```
### 7. Instalacion de JAZZMINE
```bash
pip install -U django-jazzmin
```
En tu ``core/settings.py``📂, coloca ``jazzim`` antes del ``django.contrib.admin``
```py
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
]
```
### 8. Creacion de una aplicacion
```
python manage.py startapp productos
```
Siempre que tu crees un aplicativo en Django, este debe de ser registrado en el ``core/settings.py``📂
```py
INSTALLED_APPS = [
    'nombre_aplicativo'
]
```
### 9. Modelado de la base de datos
![image](https://github.com/user-attachments/assets/f69a535b-f8f1-4c3b-a065-4b8f518a9f85)
Si modelas lo siguiente
```py
class CategoriasModel(models.Model):
   nombre = models.CharField(max_length=255)
```
Esto no se vera en tu base de datos hasta que tu ejecutes lo siguiente
```
python manage.py makemigrations
python manage.py migrate
```
### 10. Registrar un modelo en mi admin de Django

```py
from django.contrib import admin
from .models import CategoriasModel, ProductosModel

@admin.register(CategoriasModel)
class CategoriasAdmin(admin.ModelAdmin):
   list_display =  ["nombre"]

@admin.register(ProductosModel)
class ProductoAdmin(admin.ModelAdmin):
   list_display = ["titulo", "stock", "contenido"]
```

---
## Django REST Framework 🐍

### 1. Instalacion de Django REST Framework
```bash
pip install djangorestframework
```
### 2. Registrar Django REST Framework en el settings.py
```py
INSTALLED_APPS = [
    'rest_framework',
]
```
### 3. Creacion de los serializadores
El serializador que permite deserealizar la data, validar la data y especificar que se va enviar o mostrar al cliente

Nostros debemos de crear el archivo ``serializers.py``📂
```py
from rest_framework import serializers
from .models import CategoriaModel

# Este sera un serializador para Categorias
class CategoriasSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaModel
        fields = ['categoria']
```
### 4. Creacion de los views
Crearemos un view de tipo get para poder listar las categorias
```py
from rest_framework import generics
from .models import CategoriaModel
from .serializers import CategoriasSerializer

# Endpoint para mostrar todas las categorias
class ListCategorias(generics.ListAPIView):
   # SELECT * FROM categorias
   queryset = CategoriaModel.objects.all() #La consulta que se hara la bd y se mostrara
   serializer_class = CategoriasSerializer #Es la forma en como se mostrara la data
```
### 5. Creacion de las URLS
Crearemos las urls asociandolas a un view
```py
from django.urls import path
from .views import ListCategorias

urlpatterns = [
   path('categorias/', ListCategorias.as_view())
]
```

### 6. Registrar las urls de la aplicacion en el proyecto
```py
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('nombre_aplicativo.urls'))
]
```

