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


SERVICIOS = ["Limpieza vidrios","Limpieza alfombra","Limpieza oficiona","limpieza sillones","limpieza salon","limpieza casa"]

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--long', '-l', dest='long',
            help='Help for the long options'),
    )
    help = 'Help text goes here'

    def handle(self, **options):
    	for prod,cap  in zip(["Detergente", "Lavandina","Jabon","Abrillantador de piso","Esponja","Cera para piso"],[200,260,280,580,102,460]):
			Producto.objects.create(
				nombre= prod,
				marca = 'generica',
				unidad_medida='cm3',
				capacidad=cap
            )

        print Producto.objects.get(pk=random.randint(1, 2))
        for cod,nombre  in zip(["L001", "L002", "L003"],["Limpieza de vidrios", "Limpieza de alfombras", "Limpieza de pared"]):
            ts = TipoDeServicio()
            ts
            ts.productos.add(Producto.objects.get(pk=random.randint(1, 2)))
            ts.codigo_servicio = cod,
            ts.nombre = nombre,
            ts.valorM2=random.randint(15, 70)
            ts.save()
            '''TipoDeServicio.objects.create(
                #productos = Producto.objects.get(pk=random.randint(1, 2)),
                codigo_servicio = cod,
                nombre = nombre,
                valorM2=random.randint(15, 70)
            )'''

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
                empleado.especialidad = TipoDeServicio.objects.get(pk=random.randint(1, 3))
                empleado.persona = personas.pop(index)
                empleado.save()    
            else:
                Cliente.objects.create(persona = personas.pop(index))


        productos = Producto.objects.all()
        cod = 01
        for producto,servicio in zip(productos,SERVICIOS):
            ts = TipoDeServicio()
            ts.codigo_servicio = "L0"+str(cod)
            ts.nombre = servicio
            ts.valorM2 = 10
            ts.save()
            ts.productos.add(producto)
            cod = cod + 1 
