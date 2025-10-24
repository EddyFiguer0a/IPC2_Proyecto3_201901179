from django.urls import path
from . import views

app_name = 'sistema_web'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('cargar-xml/', views.cargar_xml, name='cargar_xml'),
    path('ver-datos/', views.ver_datos, name='ver_datos'),
    path('crear-datos/', views.crear_datos, name='crear_datos'),
    path('generar-facturas/', views.generar_facturas, name='generar_facturas'),
    path('ver-facturas/', views.ver_facturas, name='ver_facturas'),
    path('reportes/', views.reportes, name='reportes'),
    path('ayuda/', views.ayuda, name='ayuda'),
    path('reiniciar-sistema/', views.reiniciar_sistema, name='reiniciar_sistema'),
]