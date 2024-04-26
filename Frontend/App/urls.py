from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('transac/', views.transac, name='transac'),
    path('enviar-archivo/', views.cargarXML, name='enviar_archivo'),
    path('enviar-transac/', views.cargaTransac, name='enviar_transac'),
]