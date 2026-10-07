from django.contrib import admin
from .models import Autor, Libro, Ejemplar, UsuarioBiblioteca, Prestamo

# Cambiamos el título del panel
admin.site.site_header = "Administración de la Biblioteca"
admin.site.site_title = "Portal Biblioteca"
admin.site.index_title = "Gestión del Catálogo y Usuarios"

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'isbn', 'editorial', 'anio', 'categoria')
    search_fields = ('titulo', 'isbn', 'categoria')
    list_filter = ('categoria', 'anio')

@admin.register(Ejemplar)
class EjemplarAdmin(admin.ModelAdmin):
    list_display = ('codigo_barras', 'libro', 'ubicacion', 'estado')
    list_filter = ('estado', 'ubicacion')
    search_fields = ('codigo_barras', 'libro__titulo')

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('ejemplar', 'usuario', 'fecha_prestamo', 'fecha_vencimiento', 'devuelto')
    list_filter = ('devuelto', 'fecha_prestamo')
    search_fields = ('usuario__nombres', 'ejemplar__codigo_barras')

@admin.register(UsuarioBiblioteca)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'codigo', 'rol', 'estado')
    list_filter = ('rol', 'estado')
    search_fields = ('nombres', 'codigo', 'identificacion')

admin.site.register(Autor)