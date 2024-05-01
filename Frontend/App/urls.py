from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('grafico/', views.grafico, name='grafico'),
    path('transac/', views.transac, name='transac'),
    path('peticiones/', views.peticiones, name='peticiones'),
    path('enviar-archivo/', views.cargarXML, name='enviar_archivo'),
    path('enviar-transac/', views.cargaTransac, name='enviar_transac'),
    path('borrar_datos/', views.inicializar, name='inicializar'),
    path('cosulta_estado_cuenta/', views.consultar_estado_cuenta, name='consultaCuenta'),
    path('mostrar_clientes/', views.mostar_clientes, name='listado'),
    path("generar_grafico/", views.generar_grafico, name='grafico'),
]