from django.conf.urls import patterns, include, url

from gestionServicios.views import *
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from django.conf.urls.defaults import url, patterns
from django.contrib.auth.forms import AdminPasswordChangeForm

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'Zenda.views.index', name='index'),

    url(r'^pdf/$', 'gestionServicios.views.clientes_pdf', name='pdf'),
    url(r'^pdf_presupuesto/(?P<id_presupuesto>\d+)$', 'gestionServicios.views.presupuesto_pdf', name='presupuesto_pdf'),

    url(r'^listado/parte_diario$','gestionServicios.views.parte_diario', name="parte_diario"),
    url(r'^parte_diario$', 'gestionServicios.views.parte_diario_pdf', name='parte_diario_pdf'),
    url(r'^turnos_empleado_pdf$', 'gestionServicios.views.turnos_empleado_pdf', name='turnos_empleado_pdf'),


    url(r'^excel/$', 'gestionServicios.views.exportar_excel', name='excel'),

    
    url(r'^presupuesto/alta$', 'gestionServicios.views.presupuesto', name='presupuesto_alta'),
    #url(r'^presupuesto/(?P<id_presupuesto>\d+)/agregar_servicios$','gestionServicios.views.agregarTS', name="servicios_agregar"),

    url(r'^presupuesto/seleccion_servicios/(?P<id_presupuesto>\d+)$','gestionServicios.views.seleccion_servicios', name="seleccion_servicios"), #--- Written by Bruno url---

    url(r'^presupuesto/seleccion_servicios/(?P<pk_servicio>\w+)/quitar_servicio$','gestionServicios.views.quitarSC', name="quitar_servicio"), #--- Written by Bruno url---
    url(r'^presupuesto/valorizar$','gestionServicios.views.valorizar_presupuesto', name="presupuesto_valorizar"), #--- Written by Bruno url---
    url(r'^presupuesto/valorizar/servicios_contratados$','gestionServicios.views.servicios_contratados', name="presupuesto_servicios_contratados"),
    url(r'^presupuesto/confirmar$','gestionServicios.views.confirmar_presupuesto', name="presupuesto_confirmar"),
    url(r'^presupuesto/contrato$', 'gestionServicios.views.alta_contrato', name='alta_contrato'),
    url(r'^presupuesto/estadistica/cliente/(?P<id_cliente>\d+)$','gestionServicios.views.valorizar_estadistica_cliente', name="valorizar_estadistica_cliente"),
    

    url(r'^presupuesto/seleccion_servicios/(?P<pk_servicio>\w+)/frecuencias_de_servicio$','gestionServicios.views.frecuencias_de_servicio', name="frecuencias_de_servicio"), #--- Written by Bruno url---
    url(r'^presupuesto/seleccion_servicios/(?P<pk_servicio>\w+)/agregar_frecuencia$','gestionServicios.views.agregar_frecuencia', name="agregar_frecuencia"), #--- Written by Bruno url---
    url(r'^presupuesto/seleccion_servicios/(?P<pk_servicio>\w+)/(?P<pk_frec>\d+)/quitar_frecuencia$','gestionServicios.views.quitarFrec', name="quitar_frecuencia"), #--- Written by Bruno url---


    url(r'^persona/alta$', 'gestionServicios.views.personaView', name='persona_alta'),
    url(r'^cliente/alta$','gestionServicios.views.alta_cliente', name="cliente_alta"),
    url(r'^cliente/modificar$','gestionServicios.views.modificar_cliente', name="cliente_modificar"),
    
    url(r'^empleado/alta$','gestionServicios.views.alta_empleado', name="empleado_alta"),
    url(r'^empleado/modificar$','gestionServicios.views.modificar_empleado', name="empleado_modificar"),
    url(r'^empleado/baja$','gestionServicios.views.baja_empleado', name="empleado_baja"),
    url(r'^empleado/(?P<id_empleado>\d+)/(?P<id_frecuencia>\d+)$','gestionServicios.views.turnos_de_empleado', name="turnos_de_empleado"),
    url(r'^empleado/(?P<id_empleado>\d+)/(?P<id_frecuencia>\d+)/crear_turno_empleado$','gestionServicios.views.crear_turno_empleado', name="crear_turno_empleado"),
    url(r'^empleado/(?P<id_empleado>\d+)/(?P<id_frecuencia>\d+)/eliminar$','gestionServicios.views.turnos_de_empleado_eliminar', name="turnos_de_empleado_eliminar"),
    url(r'^empleado/turnos_empleado$','gestionServicios.views.turnos_empleado', name="turnos_empleado"),
    

    url(r'^tiposDeServicio/alta$','gestionServicios.views.alta_tipo_de_servicio', name="tipo_servicio_alta"),
    url(r'^tiposDeServicio/modificar$','gestionServicios.views.modificar_tipo_de_servicio', name="tipo_servicio_modificar"),
    url(r'^tiposDeServicio/baja$','gestionServicios.views.baja_tipo_de_servicio', name="tipo_servicio_baja"),
    
    url(r'^frecuencia/(?P<id_frecuencia>\d+)$','gestionServicios.views.turnos_frecuencia', name="turnos_frecuencia"),
    
    url(r'^servicio/(?P<id_servicio>\d+)$','gestionServicios.views.servicio_frecuencias', name="servicio_frecuencias"),
    

    url(r'^turno/alta$','gestionServicios.views.alta_turnos', name="turno_alta"),
    url(r'^turno/asignar/frecuencias_servicio_contratado$','gestionServicios.views.frecuencias_servicio_contratado', name="frecuencias_servicio_contratado"),
    url(r'^turno/asignar/frecuencias_servicio/(?P<id_presupuesto>\d+)/(?P<id_sc>\d+)/$','gestionServicios.views.frecuencias_servicio', name="frecuencias_servicio"),
    url(r'^turno/(?P<id_turno>\d+)/quitar_turno$','gestionServicios.views.quitar_turno', name="quitar_turno"),
    url(r'^turno/empleados_de_tipo_servicio/(?P<id_tipo_servicio>\w+)/(?P<id_frecuencia>\d+)$','gestionServicios.views.empleados_de_tipo_servicio', name="empleados_de_tipo_servicio"),


    url(r'^listado/clientes$','gestionServicios.views.listado_clientes', name="listar_clientes"),
    url(r'^listado/cliente/info/(?P<id_cliente>\d+)$','gestionServicios.views.info_cliente', name="info_cliente"),
    url(r'^listado/empleados$','gestionServicios.views.listado_empleados', name="listar_empleados"),
    url(r'^listado/presupuestos$','gestionServicios.views.listado_presupuestos', name="listar_presupuestos"),
    url(r'^listado/presupuesto/info/(?P<id_presupuesto>\d+)$','gestionServicios.views.info_presupuesto', name="info_presupuesto"),
    url(r'^listado/empleados_por_fecha$','gestionServicios.views.empleados_por_fecha', name="empleados_por_fecha"),
    url(r'^listado/turnos_empleados_por_fecha/(?P<id_empleado>\d+)$','gestionServicios.views.turnos_empleados_por_fecha', name="turnos_empleados_por_fecha"),
       

    #VISTA DE USUARIO
    url(r'^usuario/presupuestos$','gestionServicios.views.listado_presupuestos_usuario', name="listar_presupuestos_usuario"),
    
    #NUEVO
    url(r'^contrato/renegociar$','gestionServicios.views.renegociar', name="contrato_renegociar"),
    url(r'^contrato/eliminar$','gestionServicios.views.eliminar_contrato', name="contrato_eliminar"),
    #NUEVO CHIQUI DALEEE
    url(r'^contrato/presupuesto/detalle_servicios/$','gestionServicios.views.detalle_servicios', name="detalle_servicios"),
    url(r'^contrato/presupuesto/(?P<id_presupuesto>\d+)/detalle_frecuencias_servicio/(?P<id_sc>\d+)/$','gestionServicios.views.detalle_frecuencias_servicio', name="detalle_frecuencias_servicio"),
    url(r'^contrato/eliminar/(?P<id_presupuesto>\d+)/servicios_contratados$','gestionServicios.views.listar_servicios', name="listar_servicios"),
    url(r'^turnosDeFrecuencia/(?P<id_frecuencia>\d+)$','gestionServicios.views.turnos_de_frecuencia', name="turnos_de_frecuencia"),
    #END NUEVO CHIQUI DALEEE
    # url(r'^Zenda/', include('Zenda.foo.urls')),

    url(r'^estadistica/presupuestos$','gestionServicios.views.estadistica_presupuestos', name="estadistica_presupuestos"),
    url(r'^estadistica/empleados$','gestionServicios.views.estadistica_empleados', name="estadistica_empleados"),
    url(r'^estadistica/cliente$','gestionServicios.views.estadistica_cliente', name="estadistica_cliente"),
    
    url(r'^casilla_mensaje$','gestionServicios.views.casilla_mensaje', name="casilla_mensaje"),
    url(r'^casilla_mensaje/no_leidos$','gestionServicios.views.mensajes_no_leidos', name="mensajes_no_leidos"),
    url(r'^casilla_mensaje/leidos$','gestionServicios.views.mensajes_leidos', name="mensajes_leidos"),
    url(r'^casilla_mensaje/enviar_mail$','gestionServicios.views.enviar_mail', name="enviar_mail"),
    url(r'^casilla_mensaje/leer_mensaje/(?P<id_mensaje>\d+)$','gestionServicios.views.leer_mensaje', name="leer_mensaje"),
    url(r'^casilla_mensaje/eliminar_mensaje/(?P<id_mensaje>\d+)$','gestionServicios.views.eliminar_mensaje', name="eliminar_mensaje"),
    
    url(r'^ayuda_online$','gestionServicios.views.ayuda_online', name="ayuda_online"),

    url(r'^admin/', include(admin.site.urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:

    url(r'^login$','Zenda.views.login_view', name="vista_login"),    
    url(r'^logout$','Zenda.views.logout_view', name="vista_logout"),    
    #NUEVO by chiqui
    url(r'^change$','Zenda.views.change_role', name="vista_change_rol"),    
    #END NUEVO by chiqui
    url(r'^home$','Zenda.views.home', name="home"),   
    url(r'^privado$','Zenda.views.privado', name="privado"),   
    #url(r'^contacto$','Zenda.views.contacto', name="contacto"),
    url(r'^registro/$','gestionServicios.views.register_view', name="vista_registro"),

    (r'^selectable/', include('selectable.urls')),

    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/password_change/$',  # hijack password_change's url
        'django.contrib.auth.views.password_change',
        {'password_change_form': AdminPasswordChangeForm},
        name="password_change"),


    (r'^$', 'Zenda.views.index'),
)
