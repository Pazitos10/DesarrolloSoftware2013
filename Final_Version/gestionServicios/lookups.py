from selectable.base import ModelLookup
from selectable.registry import registry

from gestionServicios.models import *


class EmpleadoLookup(ModelLookup):
    model = Empleado
    search_fields = ('persona__nombre__icontains', 'persona__apellido__icontains' )
    filters = {'baja': None, }

class ClienteLookup(ModelLookup): 
    model = Cliente
    search_fields = ('persona__nombre__icontains', 'persona__apellido__icontains' )

class PersonaLookup(ModelLookup): 
    model = Persona
    search_fields = ('nombre__icontains', 'apellido__icontains' )

class TipoDeServicioLookup(ModelLookup):
    model = TipoDeServicio
    search_fields = ('nombre__icontains', )
    filters = {'baja': None, }

    def get_item_label(self, item):
        return str(item)

    def get_item_id(self, item):
        return item.pk

registry.register(TipoDeServicioLookup)  
registry.register(ClienteLookup)
registry.register(EmpleadoLookup)
registry.register((PersonaLookup))