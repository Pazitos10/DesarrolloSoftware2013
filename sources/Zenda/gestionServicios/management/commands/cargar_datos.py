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
} ]


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
				capacidad=cap)

        personas = []       
        for persona in PERSONAS:
            personas.append(Persona.objects.create(**persona))

        while personas:
            index = random.randint(0, len(personas)-1)
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
