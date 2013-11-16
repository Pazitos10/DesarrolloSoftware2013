from selectable.base import ModelLookup
from selectable.registry import registry

#MODIF
from gestionServicios.models import *
#END MODIF

class EmpleadoLookup(ModelLookup):
    model = Empleado
    search_fields = ('persona__nombre__icontains', 'persona__apellido__icontains' )

class ClienteLookup(ModelLookup): 
    model = Cliente
    search_fields = ('persona__nombre__icontains', 'persona__apellido__icontains' )

#NUEVO
class TipoDeServicioLookup(ModelLookup):
    model = TipoDeServicio
    search_fields = ('nombre__icontains', )

    def get_item_label(self, item):
        return str(item)

    def get_item_id(self, item):
        return item.pk

registry.register(TipoDeServicioLookup)
#END NUEVO      
registry.register(ClienteLookup)
registry.register(EmpleadoLookup)