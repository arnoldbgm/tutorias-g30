# 📧 Envío de Correos con Django + DRF (SIN Serializers) 🦾🐍

---

# 🎯 Objetivo de la clase

Al finalizar, el estudiante podrá:

* Configurar Django para enviar correos
* Crear un endpoint con DRF
* Enviar correos simples
* Enviar correos con plantilla HTML
* Probar todo con Postman

---

# 🔧 1. Configuración en Django

Ir a:

```bash
core/settings.py
```

Agregar:

```py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'TU_CORREO@gmail.com'
EMAIL_HOST_PASSWORD = 'TU_PASSWORD_DE_APLICACION'
```

---

# ⚠️ IMPORTANTE

* ❌ No usar contraseña real
* ✅ Usar contraseña de aplicación (Gmail)

---

# 🧠 Concepto clave (explicación simple)

> “Django no envía el correo directamente,
> se conecta a Gmail y le dice que lo envíe.”

---

# 🚀 2. Crear endpoint con DRF (correo simple)

## 📂 views.py

```py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail

class EnviarCorreoView(APIView):

    def post(self, request):
        destinatario = request.data.get('email')
        asunto = request.data.get('asunto')
        mensaje = request.data.get('mensaje')

        # Validación básica
        if not destinatario or not asunto or not mensaje:
            return Response({
                "error": "Todos los campos son obligatorios"
            }, status=400)

        if "@" not in destinatario:
            return Response({
                "error": "Email inválido"
            }, status=400)

        # Envío del correo
        send_mail(
            subject=asunto,
            message=mensaje,
            from_email='TU_CORREO@gmail.com',
            recipient_list=[destinatario],
            fail_silently=False,
        )

        return Response({
            "mensaje": "Correo enviado correctamente"
        })
```

---

# 🌐 3. Configurar URLs

## 📂 urls.py (app)

```py
from django.urls import path
from .views import EnviarCorreoView

urlpatterns = [
    path('enviar-correo/', EnviarCorreoView.as_view())
]
```

---

## 📂 urls.py (proyecto)

```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('nombre_app.urls'))
]
```

---

# 🧪 4. Probar con Postman

### Endpoint:

```
POST http://127.0.0.1:8000/api/enviar-correo/
```

---

### Body:

```json
{
    "email": "correo_destino@gmail.com",
    "asunto": "Prueba DRF",
    "mensaje": "Hola desde mi API 🚀"
}
```

---

### ✅ Respuesta esperada

```json
{
    "mensaje": "Correo enviado correctamente"
}
```

---

# 💥 5. Enviar correo con plantilla HTML

---

# 📂 5.1 Crear estructura

```bash
nombre_app/
│── templates/
│    └── correo/
│         └── bienvenida.html
```

---

# 🧾 5.2 Crear plantilla HTML

## 📂 bienvenida.html

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Bienvenido</title>
</head>
<body>
    <h1>Hola {{ nombre }} 👋</h1>
    <p>Gracias por registrarte en nuestra plataforma 🚀</p>
    <p>Estamos felices de tenerte.</p>
</body>
</html>
```

---

# ⚙️ 5.3 Configurar templates (si no está)

```py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    },
]
```

---

# 🚀 5.4 Modificar el APIView (HTML)

```py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

class EnviarCorreoView(APIView):

    def post(self, request):
        destinatario = request.data.get('email')
        nombre = request.data.get('nombre')

        if not destinatario or not nombre:
            return Response({
                "error": "Faltan datos"
            }, status=400)

        # Renderizar HTML
        html_content = render_to_string(
            'correo/bienvenida.html',
            {
                'nombre': nombre
            }
        )

        # Crear correo
        email = EmailMessage(
            subject='Bienvenido 🚀',
            body=html_content,
            from_email='TU_CORREO@gmail.com',
            to=[destinatario]
        )

        email.content_subtype = "html"
        email.send()

        return Response({
            "mensaje": "Correo con plantilla enviado"
        })
```

---

# 🧪 5.5 Probar con Postman

```json
{
    "email": "correo_destino@gmail.com",
    "nombre": "Demo"
}
```

Perfecto, aquí tienes la **guía corregida y adaptada**, ya con enfoque de API profesional (URL completa incluida) 👇

---

# 🖼️ Subida de Imágenes en Django (Local) 🦾🐍

---

# 🎯 Objetivo de la clase

Al finalizar, el estudiante podrá:

* Subir imágenes desde un endpoint
* Guardarlas en el servidor (local)
* Obtener la **URL completa** de la imagen
* Acceder a la imagen desde el navegador

---

# 🧠 Concepto clave

> “Django no guarda imágenes en la base de datos…
> guarda la ruta y el archivo se almacena en el servidor.”

---

# 🔧 1. Configuración en settings.py

```py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

# 📌 Explicación

* `MEDIA_URL` 👉 ruta pública
* `MEDIA_ROOT` 👉 carpeta física

---

# 🌐 2. Configurar urls.py (IMPORTANTE)

En el archivo principal:

```py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

# 🧠 Explicación simple

> “Esto permite que el navegador pueda acceder a los archivos.”

---

# 🧱 3. Crear modelo

## 📂 models.py

```py
from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to='productos/')
```

---

# ⚙️ 4. Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# 📦 5. Instalar dependencia

```bash
pip install pillow
```

---

# 🚀 6. Endpoint para subir imagen (SIN serializer)

## 📂 views.py

```py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Producto

class SubirImagenView(APIView):

    def post(self, request):
        nombre = request.data.get('nombre')
        imagen = request.FILES.get('imagen')

        if not nombre or not imagen:
            return Response({
                "error": "Nombre e imagen son obligatorios"
            }, status=400)

        producto = Producto.objects.create(
            nombre=nombre,
            imagen=imagen
        )

        # 🔥 URL COMPLETA (enfoque correcto de API)
        url_completa = request.build_absolute_uri(producto.imagen.url)

        return Response({
            "mensaje": "Imagen subida correctamente",
            "imagen_url": url_completa
        })
```

---

# 🌐 7. Configurar URL del endpoint

```py
from django.urls import path
from .views import SubirImagenView

urlpatterns = [
    path('subir-imagen/', SubirImagenView.as_view())
]
```

---

# 🧪 8. Probar con Postman

### Endpoint:

```
POST http://127.0.0.1:8000/api/subir-imagen/
```

---

### Tipo de Body:

👉 `form-data`

| KEY    | VALUE        | TYPE |
| ------ | ------------ | ---- |
| nombre | Producto 1   | Text |
| imagen | archivo .jpg | File |

---

# ✅ Resultado esperado (CORRECTO)

```json
{
    "mensaje": "Imagen subida correctamente",
    "imagen_url": "http://127.0.0.1:8000/media/productos/imagen.jpg"
}
```

---

# 🔍 9. Ver la imagen

Abrir en navegador:

```
http://127.0.0.1:8000/media/productos/imagen.jpg
```

---

# 📁 10. ¿Dónde se guarda?

```bash
/media/
   └── productos/
         └── imagen.jpg
```

---

# ⚠️ Errores comunes

* ❌ No instalar pillow
* ❌ Usar JSON en vez de form-data
* ❌ No usar `request.FILES`
* ❌ No configurar MEDIA_URL
* ❌ No configurar urls.py
* ❌ Devolver rutas relativas en vez de URL completa
