from rest_framework.views import APIView
from rest_framework.response import Response
# Importaremos la funcion propia de Django para enviar correos
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .models import Suscripciones

# Aqui vamos a crear la logica basica de nuestro envio de correos

class EnviarCorreoView(APIView):
   # Cuando trabajamos con APIView, la forma en como definimos
   # los metodos HTTP es a traves de funciones
   # def get
   # def post
   # def put
   # def delete

   def post(self, request):
      # Debemos de solicitar mediante el request
      # El nombre y el correo del usuario
      # {
      #    "nombre": "Demo",
      #    "correo": "arnold.gallegos@demo.edu.pe"
      # }

      nombre = request.data.get('nombre')
      correo = request.data.get('correo')


      # Vamos a renderizar el html, que tenemos
      # dentro de la carpeta templates

      html_content = render_to_string('correo/bienvenida.html', {
         'nombre': nombre
      })

      email = EmailMessage(
         subject='Correo de prueba',
         body=html_content,
         from_email="tucorreo@gmail.com",
         to=[correo]
      )

      email.content_subtype = 'html' # Esto es para indicar que el contenido es HTML
      email.send()


      return Response(
         {'msg': 'Correo enviado exitosamente'}
      )
   
class SubirImagenView(APIView):
   # Aqui vamos a esperar que el usuario envie
   # Un nombre  -> data (texto)
   # Una imagen -> file (imagen)

   def post(self, request):
      nombre = request.data.get('nombre')
      imagen = request.FILES.get('imagen')

      suscripcion = Suscripciones.objects.create(
         nombre=nombre,
         imagen=imagen
      )

      url_completa = request.build_absolute_uri(suscripcion.imagen.url)
      # http://127.0.0.1:8000/media/suscripciones/Wallpaper_AdventureTime.jpg
      return Response({
         "msg": "Imagen subida exitosamente",
         "url_imagen": url_completa
      })