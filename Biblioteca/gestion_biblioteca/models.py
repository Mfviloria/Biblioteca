from django.db import models

class Autor(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    isbn = models.CharField(max_length=20, unique=True)
    titulo = models.CharField(max_length=200)
    autores = models.ManyToManyField(Autor)
    editorial = models.CharField(max_length=100)
    anio = models.IntegerField()
    categoria = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.titulo

class Ejemplar(models.Model):
    ESTADOS_EJEMPLAR = [
        ('disponible', 'Disponible'),
        ('prestado', 'Prestado'),
        ('perdido', 'Perdido'),
    ]
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    codigo_barras = models.CharField(max_length=50, unique=True)
    ubicacion = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=ESTADOS_EJEMPLAR, default='disponible')

    def __str__(self):
        return f"{self.libro.titulo} - {self.codigo_barras}"

class UsuarioBiblioteca(models.Model):
    ROLES = [('estudiante', 'Estudiante'), ('docente', 'Docente')]
    ESTADOS_USUARIO = [('activo', 'Activo'), ('bloqueado', 'Bloqueado')]

    codigo = models.CharField(max_length=50, unique=True)
    identificacion = models.CharField(max_length=50, unique=True)
    nombres = models.CharField(max_length=200)
    correo = models.EmailField(unique=True)
    rol = models.CharField(max_length=20, choices=ROLES)
    carrera = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_USUARIO, default='activo')

    def __str__(self):
        return self.nombres

# Prestamo must be at the bottom because it references UsuarioBiblioteca and Ejemplar
class Prestamo(models.Model):
    usuario = models.ForeignKey(UsuarioBiblioteca, on_delete=models.CASCADE)
    ejemplar = models.ForeignKey(Ejemplar, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_vencimiento = models.DateField()
    devuelto = models.BooleanField(default=False)
    multa = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    observaciones = models.TextField(blank=True, null=True, help_text="Ej: dañado, páginas faltantes")

    def __str__(self):
        return f"Préstamo: {self.ejemplar} a {self.usuario}"