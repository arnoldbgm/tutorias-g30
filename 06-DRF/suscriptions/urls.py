from django.urls import path
from .views import EnviarCorreoView, SubirImagenView

urlpatterns = [
   path('enviar-correo/', EnviarCorreoView.as_view()),
   path('subir-imagen/', SubirImagenView.as_view())
]