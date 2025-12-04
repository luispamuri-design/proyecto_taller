from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.dashboard, name='dashboard'),
    path('clientes/', views.clientes_list, name='clientes_list'),
    path('clientes/nuevo/', views.cliente_create, name='cliente_create'),
    path('clientes/editar/<int:pk>/', views.cliente_edit, name='cliente_edit'),
    path('clientes/eliminar/<int:pk>/', views.cliente_delete, name='cliente_delete'),
        
        # DISPOSITIVOS
    path('dispositivos/', views.dispositivos_list, name='dispositivos_list'),
    path('dispositivos/nuevo/', views.dispositivo_create, name='dispositivo_create'),
    path('dispositivos/editar/<int:pk>/', views.dispositivo_edit, name='dispositivo_edit'),
    path('dispositivos/eliminar/<int:pk>/', views.dispositivo_delete, name='dispositivo_delete'),
    

        
        # TÉCNICOS
    path('tecnicos/', views.tecnicos_list, name='tecnicos_list'),
    path('tecnicos/nuevo/', views.tecnico_create, name='tecnico_create'),
    path('tecnicos/editar/<int:pk>/', views.tecnico_edit, name='tecnico_edit'),
    path('tecnicos/eliminar/<int:pk>/', views.tecnico_delete, name='tecnico_delete'),
        
        # REPUESTOS
    path('repuestos/', views.repuestos_list, name='repuestos_list'),
    path('repuestos/nuevo/', views.repuesto_create, name='repuesto_create'),
    path('repuestos/editar/<int:pk>/', views.repuesto_edit, name='repuesto_edit'),
    path('repuestos/eliminar/<int:pk>/', views.repuesto_delete, name='repuesto_delete'),
        
        # REPARACIONES
    path('reparaciones/', views.reparaciones_list, name='reparaciones_list'),
    path('reparaciones/nuevo/', views.reparacion_create, name='reparacion_create'),
    path('reparaciones/editar/<int:pk>/', views.reparacion_edit, name='reparacion_edit'),
    path('reparaciones/eliminar/<int:pk>/', views.reparacion_delete, name='reparacion_delete'),
        # AGREGAR REPUESTO A REPARACIÓN
    path('reparaciones/<int:reparacion_id>/repuestos/', views.agregar_repuesto, name='agregar_repuesto'),

        #PDF
    path('reparaciones/<int:reparacion_id>/nota/', views.nota_ingreso_pdf, name='nota_ingreso_pdf'),

        # DETALLES
    path('clientes/<int:pk>/', views.cliente_detail, name='cliente_detail'),
    path('reparaciones/<int:pk>/', views.reparacion_detail, name='reparacion_detail'),
        # CREAR USUARIO
    path('registro-admin/', views.registro_admin, name='registro_admin'),
   
    
    

]
