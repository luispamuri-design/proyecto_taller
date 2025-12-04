from django import forms
from .models import Cliente, Dispositivo, Tecnico, Repuesto, Reparacion, RepuestosUsados


# Aplicamos widgets de Bootstrap para que los formularios se vean bien
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono', 'correo', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
        }

class DispositivoForm(forms.ModelForm):
    class Meta:
        model = Dispositivo
        fields = ['cliente', 'marca', 'modelo', 'imei', 'descripcion_falla', 'estado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'imei': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_falla': forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

class TecnicoForm(forms.ModelForm):
    class Meta:
        model = Tecnico
        fields = ['nombre', 'especialidad', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RepuestoForm(forms.ModelForm):
    class Meta:
        model = Repuesto
        fields = ['nombre', 'descripcion', 'stock', 'precio']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows':2}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class ReparacionForm(forms.ModelForm):
    class Meta:
        model = Reparacion
        fields = ['dispositivo', 'tecnico', 'diagnostico', 'costo_mano_obra', 'estado', 'fecha_fin']
        widgets = {
            'dispositivo': forms.Select(attrs={'class': 'form-select'}),
            'tecnico': forms.Select(attrs={'class': 'form-select'}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows':4}),
            'costo_mano_obra': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'fecha_fin': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

class RepuestosUsadosForm(forms.ModelForm):
    class Meta:
        model = RepuestosUsados
        fields = ['repuesto', 'cantidad']
        widgets = {
            'repuesto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

