from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from gestionServicios.models import *
from datetime import datetime

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--long', '-l', dest='long',
            help='Help for the long options'),
    )
    help = 'Help text goes here'

    def handle(self, **options):
    	for prod,cap  in zip(["detergente", "lavandina"],[200,260,280]):
			Producto.objects.create(
				nombre= prod,
				marca = 'queseyo',
				unidad_medida='cm3',
				capacidad=cap)