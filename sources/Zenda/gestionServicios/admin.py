from gestionServicios.models import *
from django.contrib import admin

class PersonaAdmin(admin.ModelAdmin):
	search_fields = ("nombre", "apellido")

admin.site.register(Presupuesto)
admin.site.register(ServicioContratado)
admin.site.register(TipoDeServicio)
admin.site.register(Producto)
admin.site.register(Frecuencia)
admin.site.register(Persona, PersonaAdmin)
admin.site.register(Cliente)
admin.site.register(Turno)
admin.site.register(Empleado)
admin.site.register(Localidad)
admin.site.register(Provincia)
admin.site.register(Pais)
admin.site.register(Contrato)