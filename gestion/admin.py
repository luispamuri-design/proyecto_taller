from django.contrib import admin
from .models import Cliente, Tecnico, Dispositivo, Repuesto, Reparacion, RepuestosUsados

admin.site.register(Cliente)
admin.site.register(Tecnico)
admin.site.register(Dispositivo)
admin.site.register(Repuesto)
admin.site.register(Reparacion)
admin.site.register(RepuestosUsados)
