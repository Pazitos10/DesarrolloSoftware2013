from gestionServicios.models import *
from django.contrib import admin

class PersonaAdmin(admin.ModelAdmin):
	search_fields = ("nombre", "apellido")

class ServicioContratadoInline(admin.TabularInline):
	model = ServicioContratado


class PresupuestoAdmin(admin.ModelAdmin):
	list_display = ['nro','cliente','domicilio_servicio','estado']
	def estado(self, obj):
		estado = obj.obtener_estado_actual()
		print estado
		if isinstance(estado,Valorizado):
			return estado.nombre+', Valor final: $'+str(estado.valor_final)
		else: 
			return estado
	def nro(self,obj):
		return obj.pk

	inlines = [
		ServicioContratadoInline
	]

class TipoDeServicioAdmin(admin.ModelAdmin):
	search_fields = ("nombre","codigo_servicio","valorM2","productos__nombre")

class EmpleadoAdmin(admin.ModelAdmin):
	list_display = ['nombre','especialidad']
	search_fields = ("especialidad","persona__nombre")
	def especialidad(self, obj):
		return obj.especialidad
	def nombre(self,obj):
		return obj.persona




admin.site.register(Presupuesto, PresupuestoAdmin)
admin.site.register(ServicioContratado)
admin.site.register(TipoDeServicio,TipoDeServicioAdmin)
admin.site.register(Producto)
admin.site.register(Frecuencia)
admin.site.register(Persona, PersonaAdmin)
admin.site.register(Cliente)
admin.site.register(Turno)
admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Localidad)
admin.site.register(Provincia)
admin.site.register(Pais)
admin.site.register(Contrato)
admin.site.register(Valorizado)