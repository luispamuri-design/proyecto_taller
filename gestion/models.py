from django.db import models

# -----------------------------------------
# CLIENTE
# -----------------------------------------
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


# -----------------------------------------
# TÉCNICO
# -----------------------------------------
class Tecnico(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre


# -----------------------------------------
# DISPOSITIVO
# -----------------------------------------
class Dispositivo(models.Model):
    ESTADOS = [
        ('ingresado', 'Ingresado'),
        ('diagnostico', 'En Diagnóstico'),
        ('reparacion', 'En Reparación'),
        ('finalizado', 'Reparado'),
        ('entregado', 'Entregado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=100)
    imei = models.CharField(max_length=50, blank=True, null=True)
    descripcion_falla = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='ingresado')
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.cliente})"


# -----------------------------------------
# REPUESTO (INVENTARIO)
# -----------------------------------------
class Repuesto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    stock = models.IntegerField(default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} – Stock: {self.stock}"


# -----------------------------------------
# REPARACIÓN
# -----------------------------------------
class Reparacion(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('trabajando', 'Trabajando'),
        ('espera_repuesto', 'Esperando Repuesto'),
        ('finalizado', 'Finalizado'),
        ('entregado', 'Entregado'),
    ]

    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.SET_NULL, null=True)
    diagnostico = models.TextField()
    costo_mano_obra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=30, choices=ESTADOS, default='pendiente')
    notificado = models.BooleanField(default=False)

    def __str__(self):
        return f"Reparación #{self.id} – {self.dispositivo}"


# -----------------------------------------
# REPUESTOS USADOS
# -----------------------------------------
class RepuestosUsados(models.Model):
    reparacion = models.ForeignKey(Reparacion, on_delete=models.CASCADE)
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.repuesto.nombre} x{self.cantidad}"
