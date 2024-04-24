from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('enviar-archivo/', views.cargarXML, name='enviar_archivo'),
]