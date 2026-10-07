from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('prestamo/nuevo/', views.registrar_prestamo, name='registrar_prestamo'),
    path('devolucion/<int:prestamo_id>/', views.registrar_devolucion, name='registrar_devolucion'),
    path('usuarios/nuevo/', views.registrar_usuario, name='registrar_usuario'),
    path('usuarios/historial/', views.historial_usuario, name='historial_usuario'),
    path('libros/nuevo/', views.registrar_libro, name='registrar_libro'),
    path('ejemplares/nuevo/', views.registrar_ejemplar, name='registrar_ejemplar'),
]