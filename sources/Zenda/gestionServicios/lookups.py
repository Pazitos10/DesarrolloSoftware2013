from selectable.base import ModelLookup
from selectable.registry import registry

#MODIF
from gestionServicios.models import *
#END MODIF

class EmpleadoLookup(ModelLookup):
    model = Persona
    search_fields = ('nombre__icontains', 'apellido__icontains' )

    def get_item_label(self, item):
        if len(item.empleado_set.all()) > 0:
           return str(item)

    def get_item_id(self, item):
        if len(item.empleado_set.all()) > 0:
           return item.pk

class ClienteLookup(ModelLookup): 
    model = Persona
    search_fields = ('nombre__icontains', 'apellido__icontains' )

    def get_item_label(self, item):
        if len(item.cliente_set.all()) > 0:
           return str(item)
        print 'uiiii'
        return None   

    def get_item_id(self, item):
        if len(item.cliente_set.all()) > 0:
            return item.pk
        print 'uiiii X2'    
        return None

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