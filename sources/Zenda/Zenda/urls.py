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
    url(r'^presupuesto/agregar_servicios$','gestionServicios.views.agregarTS', name="servicios_agregar"),
    url(r'^presupuesto/valorizar$','gestionServicios.views.valorizar_presupuesto', name="presupuesto_valorizar"),
    url(r'^presupuesto/confirmar$','gestionServicios.views.confirmar_presupuesto', name="presupuesto_confirmar"),
    url(r'^presupuesto/valorizar/servicios_contratados$','gestionServicios.views.servicios_contratados', name="presupuesto_servicios_contratados"),
    
    url(r'^persona/alta$', 'gestionServicios.views.personaView', name='persona_alta'),
    # url(r'^Zenda/', include('Zenda.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tiposDeServicio/alta$','gestionServicios.views.alta_tipo_de_servicio', name="tipo_servicio_alta"),
    url(r'^tiposDeServicio/modificar$','gestionServicios.views.modificar_tipo_de_servicio', name="tipo_servicio_modificar"),
    url(r'^tiposDeServicio/baja$','gestionServicios.views.baja_tipo_de_servicio', name="tipo_servicio_baja"),
    url(r'^cliente/alta$','gestionServicios.views.alta_cliente', name="cliente_alta"),
    url(r'^cliente/modificar$','gestionServicios.views.modificar_cliente', name="cliente_modificar"),
    url(r'^empleado/alta$','gestionServicios.views.alta_empleado', name="empleado_alta"),
    url(r'^empleado/modificar$','gestionServicios.views.modificar_empleado', name="empleado_modificar"),
    url(r'^turno/alta$','gestionServicios.views.alta_turnos', name="turno_alta"),

    (r'^selectable/', include('selectable.urls')),
)
