from django.db.models import Count
from datetime import datetime
from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from .forms import ClienteForm
from .models import Dispositivo
from .forms import DispositivoForm
from .models import Tecnico
from .forms import TecnicoForm
from .models import Repuesto
from .forms import RepuestoForm
from .models import Reparacion
from .forms import ReparacionForm
from .forms import RepuestosUsadosForm
from .forms import RepuestosUsados
from utils.pdf_utils import generar_pdf, generar_qr
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm




#  PAGINA PRINCIPAL
@login_required
def dashboard(request):

    total_clientes = Cliente.objects.count()
    total_dispositivos = Dispositivo.objects.count()
    rep_en_proceso = Reparacion.objects.filter(estado="En proceso").count()
    rep_finalizadas = Reparacion.objects.filter(estado="Finalizado").count()

    # Alerta de stock bajo
    repuestos_bajo_stock = Repuesto.objects.filter(stock__lt=3)

    # Últimas 5 reparaciones
    ultimas_reparaciones = Reparacion.objects.select_related("dispositivo", "tecnico").order_by('-fecha_inicio')[:5]

    # Gráfico: Reparaciones por mes
    reparaciones_por_mes = (
        Reparacion.objects
        .annotate(mes=TruncMonth('fecha_inicio'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )

    context = {
        'total_clientes': total_clientes,
        'total_dispositivos': total_dispositivos,
        'rep_en_proceso': rep_en_proceso,
        'rep_finalizadas': rep_finalizadas,
        'repuestos_bajo_stock': repuestos_bajo_stock,
        'ultimas_reparaciones': ultimas_reparaciones,
        'reparaciones_por_mes': reparaciones_por_mes,
    }

    return render(request, 'gestion/dashboard.html', context)


# -----------------------------
# CLIENTES
# -----------------------------

@login_required
def clientes_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'gestion/clientes_list.html', {'clientes': clientes})

@login_required
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes_list')
    else:
        form = ClienteForm()
    return render(request, 'gestion/cliente_form.html', {'form': form})

@login_required
def cliente_edit(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'gestion/cliente_form.html', {'form': form})

@login_required
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.delete()
    return redirect('clientes_list')


# Detalle Cliente
@login_required
def cliente_detail(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    # Corregido: usar filter para evitar errores por related_name inexistente
    dispositivos = Dispositivo.objects.filter(cliente=cliente)
    reparaciones = Reparacion.objects.filter(dispositivo__cliente=cliente)

    return render(request, 'gestion/cliente_detail.html', {
        'cliente': cliente,
        'dispositivos': dispositivos,
        'reparaciones': reparaciones
    })


# -----------------------------
# DISPOSITIVOS
# -----------------------------

@login_required
def dispositivos_list(request):
    dispositivos = Dispositivo.objects.select_related('cliente').all()
    return render(request, 'gestion/dispositivos_list.html', {'dispositivos': dispositivos})

@login_required
def dispositivo_create(request):
    if request.method == 'POST':
        form = DispositivoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dispositivos_list')
    else:
        form = DispositivoForm()
    return render(request, 'gestion/dispositivo_form.html', {'form': form})

@login_required
def dispositivo_edit(request, pk):
    dispositivo = get_object_or_404(Dispositivo, pk=pk)
    if request.method == 'POST':
        form = DispositivoForm(request.POST, instance=dispositivo)
        if form.is_valid():
            form.save()
            return redirect('dispositivos_list')
    else:
        form = DispositivoForm(instance=dispositivo)
    return render(request, 'gestion/dispositivo_form.html', {'form': form})

@login_required
def dispositivo_delete(request, pk):
    dispositivo = get_object_or_404(Dispositivo, pk=pk)
    dispositivo.delete()
    return redirect('dispositivos_list')


# -----------------------------
# TÉCNICOS
# -----------------------------

@login_required
def tecnicos_list(request):
    tecnicos = Tecnico.objects.all()
    return render(request, 'gestion/tecnicos_list.html', {'tecnicos': tecnicos})

@login_required
def tecnico_create(request):
    if request.method == 'POST':
        form = TecnicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tecnicos_list')
    else:
        form = TecnicoForm()
    return render(request, 'gestion/tecnico_form.html', {'form': form})

@login_required
def tecnico_edit(request, pk):
    tecnico = get_object_or_404(Tecnico, pk=pk)
    if request.method == 'POST':
        form = TecnicoForm(request.POST, instance=tecnico)
        if form.is_valid():
            form.save()
            return redirect('tecnicos_list')
    else:
        form = TecnicoForm(instance=tecnico)
    return render(request, 'gestion/tecnico_form.html', {'form': form})

@login_required
def tecnico_delete(request, pk):
    tecnico = get_object_or_404(Tecnico, pk=pk)
    tecnico.delete()
    return redirect('tecnicos_list')


# -----------------------------
# REPUESTOS
# -----------------------------

@login_required
def repuestos_list(request):
    repuestos = Repuesto.objects.all()
    return render(request, 'gestion/repuestos_list.html', {'repuestos': repuestos})

@login_required
def repuesto_create(request):
    if request.method == 'POST':
        form = RepuestoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('repuestos_list')
    else:
        form = RepuestoForm()
    return render(request, 'gestion/repuesto_form.html', {'form': form})

@login_required
def repuesto_edit(request, pk):
    repuesto = get_object_or_404(Repuesto, pk=pk)
    if request.method == 'POST':
        form = RepuestoForm(request.POST, instance=repuesto)
        if form.is_valid():
            form.save()
            return redirect('repuestos_list')
    else:
        form = RepuestoForm(instance=repuesto)
    return render(request, 'gestion/repuesto_form.html', {'form': form})

@login_required
def repuesto_delete(request, pk):
    repuesto = get_object_or_404(Repuesto, pk=pk)
    repuesto.delete()
    return redirect('repuestos_list')


# -----------------------------
# REPARACIONES
# -----------------------------

@login_required
def reparaciones_list(request):
    reparaciones = Reparacion.objects.select_related('dispositivo', 'tecnico').all()
    return render(request, 'gestion/reparaciones_list.html', {'reparaciones': reparaciones})

@login_required
def reparacion_create(request):
    if request.method == 'POST':
        form = ReparacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reparaciones_list')
    else:
        form = ReparacionForm()
    return render(request, 'gestion/reparacion_form.html', {'form': form})

@login_required
def reparacion_edit(request, pk):
    reparacion = get_object_or_404(Reparacion, pk=pk)
    if request.method == 'POST':
        form = ReparacionForm(request.POST, instance=reparacion)
        if form.is_valid():
            form.save()
            return redirect('reparaciones_list')
    else:
        form = ReparacionForm(instance=reparacion)
    return render(request, 'gestion/reparacion_form.html', {'form': form})

@login_required
def reparacion_delete(request, pk):
    reparacion = get_object_or_404(Reparacion, pk=pk)
    reparacion.delete()
    return redirect('reparaciones_list')


# Detalle Reparación
@login_required
def reparacion_detail(request, pk):
    reparacion = get_object_or_404(Reparacion, pk=pk)
    repuestos_usados = RepuestosUsados.objects.filter(reparacion=reparacion)
    return render(request, 'gestion/reparacion_detail.html', {
        'reparacion': reparacion,
        'repuestos_usados': repuestos_usados
    })


# -----------------------------
# REPUESTOS USADOS
# -----------------------------

@login_required
def agregar_repuesto(request, reparacion_id):
    reparacion = get_object_or_404(Reparacion, pk=reparacion_id)

    if request.method == 'POST':
        form = RepuestosUsadosForm(request.POST)
        if form.is_valid():
            repu = form.cleaned_data['repuesto']
            cantidad = form.cleaned_data['cantidad']

            # stock
            if repu.stock < cantidad:
                messages.error(request, f"Stock insuficiente para {repu.nombre}. Disponible: {repu.stock}")
                return redirect('agregar_repuesto', reparacion_id=reparacion_id)

            repu.stock -= cantidad
            repu.save()

            repuesto_usado = form.save(commit=False)
            repuesto_usado.reparacion = reparacion
            repuesto_usado.save()

            messages.success(request, "Repuesto agregado correctamente.")
            return redirect('reparaciones_list')
    else:
        form = RepuestosUsadosForm()

    return render(request, 'gestion/repuestos_usados_form.html', {
        'form': form,
        'reparacion': reparacion
    })


# -----------------------------
# PDF
# -----------------------------

@login_required
def nota_ingreso_pdf(request, reparacion_id):
    reparacion = get_object_or_404(Reparacion, pk=reparacion_id)
    repuestos = RepuestosUsados.objects.filter(reparacion=reparacion)

    qr_texto = f"Reparación #{reparacion.id} - Cliente: {reparacion.dispositivo.cliente.nombre}"
    qr_base64 = generar_qr(qr_texto)

    contexto = {
        'reparacion': reparacion,
        'repuestos': repuestos,
        'qr_base64': qr_base64,
    }

    return generar_pdf('gestion/nota_ingreso.html', contexto)


# ----------------------------------------------------
# VISTA PARA CREAR NUEVOS ADMINISTRADORES
# ----------------------------------------------------
@login_required
def registro_admin(request):
    """Permite a un administrador crear nuevos usuarios del sistema."""
    # Solo permite a superusuarios crear otros administradores (Opcional, pero recomendado)
    if not request.user.is_superuser:
         messages.error(request, "Solo un Superusuario puede crear nuevos administradores.")
         return redirect('dashboard')
         
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Configuramos el nuevo usuario como personal (Staff)
            # Esto les da acceso si usaras el panel de administración, 
            # y es una buena práctica para diferenciar administradores de usuarios comunes.
            user.is_staff = True 
            user.save()
            
            messages.success(request, f'¡Usuario "{user.username}" creado con éxito!')
            return redirect('dashboard') 
    else:
        form = UserCreationForm()
        
    return render(request, 'gestion/registro_admin.html', {'form': form})




