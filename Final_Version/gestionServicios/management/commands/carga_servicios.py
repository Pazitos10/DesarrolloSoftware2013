from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from gestionServicios.models import *
from datetime import datetime
import random
from django.contrib.auth.models import Group,User, Permission
from django.core.mail import send_mail


PRODUCTOS = ["Detergente", "Lavandina", "Jabon", "Abrillantador de piso", "Esponja", "Cera para piso",""]
SERVICIOS = [
	"Limpieza vidrios", 
	"Limpieza alfombra", 
	"Limpieza oficina", 
	"Limpieza sillones", 
	"Limpieza salon", 
	"Limpieza casa",
	"Limpieza techo"
]

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--long', '-l', dest='long',
            help='Help for the long options'),
    )
    help = 'Este Script carga unicamente Tipos de servicio'

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
