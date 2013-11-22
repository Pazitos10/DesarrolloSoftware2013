from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from gestionServicios.models import *
from datetime import datetime
import random

PERSONAS = [ { 
"nombre": "Bruno",
"apellido": "Rodrigez",
"email": "bruno@hotmail.com",
"telefono": 1234567,
"tipo_documento": "dni",
"domicilio": "25 de Mayo",
"nro_documento": 12345678
}, { 
"nombre": "Alberto",
"apellido": "Perez",
"email": "alberto@hotmail.com",
"telefono": 3344567,
"tipo_documento": "dni",
"domicilio": "Pellegrini",
"nro_documento": 44345678
}, { 
"nombre": "Rodrigo",
"apellido": "Jaramillo",
"email": "rodrigo@hotmail.com",
"telefono": 1234567,
"tipo_documento": "dni",
"domicilio": "9 de Julio",
"nro_documento": 15455678
}, { 
"nombre": "Andy",
"apellido": "Cahngo",
"email": "toxicboy@hotmail.com",
"telefono": 1234567,
"tipo_documento": "dni",
"domicilio": "9 de Julio",
"nro_documento": 11235678
}, { 
"nombre": "Pep",
"apellido": "Guardiola",
"email": "pg@hotmail.com",
"telefono": 463251,
"tipo_documento": "dni",
"domicilio": "9 de Julio",
"nro_documento": 3534615
}, { 
"nombre": "Marcelo",
"apellido": "Tinelli",
"email": "mt@hotmail.com",
"telefono": 643562,
"tipo_documento": "dni",
"domicilio": "9 de Julio",
"nro_documento": 6854329
}   ]

PRODUCTOS = ["Detergente", "Lavandina", "Jabon", "Abrillantador de piso", "Esponja", "Cera para piso"]
SERVICIOS = ["Limpieza vidrios", "Limpieza alfombra", "Limpieza oficina", "Limpieza sillones", "Limpieza salon", "Limpieza casa"]


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--long', '-l', dest='long',
            help='Help for the long options'),
    )
    help = 'Help text goes here'

    def handle(self, **options):
            for prod,cap in zip(PRODUCTOS, [200, 260, 280, 580, 102, 460]):
                        Producto.objects.create(
                                nombre= prod,
                                marca = 'generica',
                                unidad_medida='cm3',
                                capacidad=cap
            )

        count = 1
        for nombre in SERVICIOS:
            ts = TipoDeServicio()
            ts.codigo_servicio = "L00" + str(count)
            ts.nombre = nombre
            ts.valorM2 = random.randint(15, 70)
            ts.save()
            ts.productos.add(Producto.objects.get(pk=random.randint(1, Producto.objects.count())))
            count+=1

        personas = []       
        for persona in PERSONAS:
            personas.append(Persona.objects.create(**persona))

        while personas:
            index = random.randint(0, len(personas)-1)

            r = random.randint(0, 1)
            if r:
                empleado = Empleado()
                empleado.CUIL = random.randint(0, 9999999999)
                empleado.nacimiento = datetime.now()
                empleado.especialidad = TipoDeServicio.objects.get(pk='L00'+str(random.randint(1, TipoDeServicio.objects.count())))
                empleado.persona = personas.pop(index)
                empleado.save()    
            else:
                Cliente.objects.create(persona = personas.pop(index))