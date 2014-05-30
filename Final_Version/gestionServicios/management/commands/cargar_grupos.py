from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from gestionServicios.models import *
from django.contrib.auth.models import Group,User, Permission




class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--long', '-l', dest='long',
            help='Help for the long options'),
    )
    help = 'Help text goes here'

    def handle(self, **options):
            ## creo los grupos
            grupo_empleados, created = Group.objects.get_or_create(name='empleados')
            grupo_clientes, created = Group.objects.get_or_create(name='clientes')
            #asigno permisos a los grupos
            grupo_clientes.permissions.add(Permission.objects.get(codename='change_user'))
            grupo_clientes.permissions.add(Permission.objects.get(codename='change_cliente'))
            grupo_clientes.permissions.add(Permission.objects.get(codename='add_presupuesto'))
