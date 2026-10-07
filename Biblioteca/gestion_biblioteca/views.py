from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Prestamo, Ejemplar, Libro, UsuarioBiblioteca
from .forms import PrestamoForm, DevolucionForm, UsuarioForm, LibroForm, EjemplarForm
from datetime import date
from django.db.models import Count
from decimal import Decimal

# --- 3. Gestión de Préstamos[cite: 1] ---
def registrar_prestamo(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            ejemplar = form.cleaned_data['ejemplar']

            # Validar antes de prestar[cite: 1]:
            # a) que el usuario esté activo[cite: 1]
            if usuario.estado != 'activo':
                messages.error(request, 'El usuario no está activo y no puede pedir préstamos.')
                return render(request, 'prestamo.html', {'form': form})

            # b) que el ejemplar esté disponible[cite: 1]
            if ejemplar.estado != 'disponible':
                messages.error(request, 'Este ejemplar no se encuentra disponible actualmente.')
                return render(request, 'prestamo.html', {'form': form})

            # Si pasa las validaciones, guardamos
            prestamo = form.save()
            # Actualizamos el estado del ejemplar a 'prestado'
            ejemplar.estado = 'prestado'
            ejemplar.save()
            
            messages.success(request, 'Préstamo registrado correctamente.')
            return redirect('registrar_prestamo')
    else:
        form = PrestamoForm()
    
    return render(request, 'prestamo.html', {'form': form})


# --- 4. Gestión de Devolución[cite: 1] ---
def registrar_devolucion(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    
    if request.method == 'POST':
        form = DevolucionForm(request.POST, instance=prestamo)
        if form.is_valid():
            prestamo_actualizado = form.save(commit=False)
            
            # Si existe retraso, calcular automáticamente sanción/multa[cite: 1]
            hoy = date.today()
            if hoy > prestamo.fecha_vencimiento:
                dias_retraso = (hoy - prestamo.fecha_vencimiento).days
                multa_por_dia = Decimal('5000.00') # Ejemplo: 5000 pesos por día
                prestamo_actualizado.multa = dias_retraso * multa_por_dia

            prestamo_actualizado.devuelto = True
            prestamo_actualizado.save()

            # Registrar la devolución de un ejemplar y actualizar su estado a disponible[cite: 1]
            ejemplar = prestamo.ejemplar
            ejemplar.estado = 'disponible'
            
            # Si en las observaciones (Registrar observaciones del ejemplar al devolver: “dañado”, “páginas faltantes”[cite: 1]) 
            # se indica daño, podrías cambiar el estado a otro valor si lo deseas.
            ejemplar.save()

            messages.success(request, f'Devolución registrada. Multa calculada: ${prestamo_actualizado.multa}')
            return redirect('registrar_prestamo') # Redirigirías al listado o panel
    else:
        form = DevolucionForm(instance=prestamo)

    return render(request, 'devolucion.html', {'form': form, 'prestamo': prestamo})
from django.contrib.auth.decorators import login_required

@login_required(login_url='/cuentas/login/')
def dashboard(request):
    hoy = date.today()
    prestamos_activos = Prestamo.objects.filter(devuelto=False)
    prestamos_vencidos = prestamos_activos.filter(fecha_vencimiento__lt=hoy).count()
    ejemplares_disponibles = Ejemplar.objects.filter(estado='disponible').count()
    ejemplares_prestados = Ejemplar.objects.filter(estado='prestado').count()
    ejemplares_perdidos = Ejemplar.objects.filter(estado='perdido').count()
    
    # 5. Reportes y Consultas (Los que faltaban)
    libros_top = Libro.objects.annotate(num=Count('ejemplar__prestamo')).order_by('-num')[:5]
    usuarios_top = UsuarioBiblioteca.objects.annotate(num=Count('prestamo')).order_by('-num')[:5]
    ultimos_libros = Libro.objects.all().order_by('-id')[:8]

    context = {
        'total_activos': prestamos_activos.count(), 'total_vencidos': prestamos_vencidos,
        'disponibles': ejemplares_disponibles, 'prestados': ejemplares_prestados, 'perdidos': ejemplares_perdidos,
        'ultimos_prestamos': prestamos_activos.order_by('-fecha_prestamo')[:5],
        'ultimos_libros': ultimos_libros, 'libros_top': libros_top, 'usuarios_top': usuarios_top,
    }
    return render(request, 'dashboard.html', context)

# Vistas de creación (Usaremos una sola plantilla genérica para todas)
@login_required(login_url='/cuentas/login/')
def registrar_usuario(request):
    form = UsuarioForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Usuario registrado exitosamente.')
        return redirect('dashboard')
    return render(request, 'formulario_generico.html', {'form': form, 'titulo': 'Registrar Nuevo Usuario'})

@login_required(login_url='/cuentas/login/')
def registrar_libro(request):
    form = LibroForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Libro registrado en el catálogo.')
        return redirect('dashboard')
    return render(request, 'formulario_generico.html', {'form': form, 'titulo': 'Registrar Nuevo Libro'})

@login_required(login_url='/cuentas/login/')
def registrar_ejemplar(request):
    form = EjemplarForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Ejemplar añadido correctamente.')
        return redirect('dashboard')
    return render(request, 'formulario_generico.html', {'form': form, 'titulo': 'Añadir Ejemplar Físico'})

# Consultar historial por usuario
@login_required(login_url='/cuentas/login/')
def historial_usuario(request):
    historial, usuario = None, None
    if 'codigo' in request.GET:
        usuario = UsuarioBiblioteca.objects.filter(codigo=request.GET['codigo']).first()
        if usuario:
            historial = Prestamo.objects.filter(usuario=usuario).order_by('-fecha_prestamo')
        else:
            messages.error(request, 'No se encontró un usuario con ese código.')
    return render(request, 'historial.html', {'historial': historial, 'usuario': usuario})
def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Nuevo usuario registrado exitosamente!')
            return redirect('dashboard')
    else:
        form = UsuarioForm()
    return render(request, 'nuevo_usuario.html', {'form': form})

