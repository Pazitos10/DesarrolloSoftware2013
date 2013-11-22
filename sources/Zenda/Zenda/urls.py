from django.conf.urls import patterns, include, url

from gestionServicios.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'Zenda.views.home', name='home'),
    url(r'^presupuesto/alta$', 'gestionServicios.views.presupuesto', name='presupuesto_alta'),
    url(r'^presupuesto/listado$','gestionServicios.views.listado_presupuestos', name="presupuesto_listados"),
    # ----- Presupuestar y la puta que te pario
    url(r'^presupuesto/(?P<id_presupuesto>\d+)/agregar_servicios$','gestionServicios.views.agregarTS', name="servicios_agregar"),
    url(r'^presupuesto/(?P<id_presupuesto>\d+)/quitar_servicio/(?P<id_serviciocontratado>\d+)$','gestionServicios.views.quitarSC', name="quitar_servicio_contratado"),
    url(r'^contratado/(?P<id_serviciocontratado>\d+)$','gestionServicios.views.frecuencias_de_servicio', name="motrar_frecuencias"),
    url(r'^contratado/(?P<id_serviciocontratado>\d+)/agregar_frecuencia$','gestionServicios.views.agregar_frecuencia', name="agregar_frecuencia"),

    url(r'^presupuesto/valorizar$','gestionServicios.views.valorizar_presupuesto', name="presupuesto_valorizar"),
    url(r'^presupuesto/confirmar$','gestionServicios.views.confirmar_presupuesto', name="presupuesto_confirmar"),
    url(r'^presupuesto/valorizar/servicios_contratados$','gestionServicios.views.servicios_contratados', name="presupuesto_servicios_contratados"),
    
    url(r'^persona/alta$', 'gestionServicios.views.personaView', name='persona_alta'),
    url(r'^cliente/alta$','gestionServicios.views.alta_cliente', name="cliente_alta"),
    url(r'^cliente/modificar$','gestionServicios.views.modificar_cliente', name="cliente_modificar"),
    url(r'^empleado/alta$','gestionServicios.views.alta_empleado', name="empleado_alta"),
    url(r'^empleado/modificar$','gestionServicios.views.modificar_empleado', name="empleado_modificar"),
   
    url(r'^tiposDeServicio/alta$','gestionServicios.views.alta_tipo_de_servicio', name="tipo_servicio_alta"),
    url(r'^tiposDeServicio/modificar$','gestionServicios.views.modificar_tipo_de_servicio', name="tipo_servicio_modificar"),
    url(r'^tiposDeServicio/baja$','gestionServicios.views.baja_tipo_de_servicio', name="tipo_servicio_baja"),
   
    url(r'^turno/alta$','gestionServicios.views.alta_turnos', name="turno_alta"),
    url(r'^turno/asignar/turno_servicios_contratados$','gestionServicios.views.turno_servicios_contratados', name="turno_servicios_contratados"),
    url(r'^turno/asignar/empleados_disponibles$','gestionServicios.views.empleados_disponibles', name="empleados_disponibles"),
    
    
    # url(r'^Zenda/', include('Zenda.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:

    (r'^selectable/', include('selectable.urls')),
)
