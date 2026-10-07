from django import forms
from .models import Prestamo, UsuarioBiblioteca, Libro, Ejemplar

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['usuario', 'ejemplar', 'fecha_vencimiento']
        widgets = {
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'})
        }

class DevolucionForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        # Registrar observaciones del ejemplar al devolver: “dañado”, “páginas faltantes”[cite: 1].
        fields = ['observaciones']


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = UsuarioBiblioteca
        fields = ['codigo', 'identificacion', 'nombres', 'correo', 'rol', 'carrera']

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = '__all__'

class EjemplarForm(forms.ModelForm):
    class Meta:
        model = Ejemplar
        fields = ['libro', 'codigo_barras', 'ubicacion', 'estado']