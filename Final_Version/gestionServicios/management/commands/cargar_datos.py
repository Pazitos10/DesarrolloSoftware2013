from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from gestionServicios.models import *
from datetime import datetime
import random
from django.contrib.auth.models import Group,User, Permission
from django.core.mail import send_mail
PERSONAS = [ { 
"nombre": "Bruno",
"apellido": "Rodrigez",
"email": "brunor@hotmail.com",
"telefono": 1234567,
"tipo_documento": "dni",
"domicilio": "25 de Mayo",
"nro_documento": 12345698
}, { 
"nombre": "Roberto",
"apellido": "Rod",
"email": "rr@hotmail.com",
"telefono": 444555,
"tipo_documento": "dni",
"domicilio": "Belgrano 994",
"nro_documento": 34567887
},{ 
"nombre": "Pedro",
"apellido": "Lopez",
"email": "pl@hotmail.com",
"telefono": 556213,
"tipo_documento": "dni",
"domicilio": "Marconi 212",
"nro_documento": 34123765
},{ 
"nombre": "Ricardo",
"apellido": "Lanz",
"email": "rl@hotmail.com",
"telefono": 675443,
"tipo_documento": "dni",
"domicilio": "Uruguay 280",
"nro_documento": 32567098
},{ 
"nombre": "Gaston",
"apellido": "Casas",
"email": "gc@hotmail.com",
"telefono": 433111,
"tipo_documento": "dni",
"domicilio": "Gregorio 892",
"nro_documento": 23456666
},{ 
"nombre": "Gabriel",
"apellido": "San",
"email": "gs@hotmail.com",
"telefono": 988772,
"tipo_documento": "dni",
"domicilio": "Belgrano 872",
"nro_documento": 21554995
},{ 
"nombre": "Emanuel",
"apellido": "Pereyra",
"email": "ep@hotmail.com",
"telefono": 998772,
"tipo_documento": "dni",
"domicilio": "25 de mayo 993",
"nro_documento": 36995433
},{ 
"nombre": "Miguel",
"apellido": "Perg",
"email": "mp@hotmail.com",
"telefono": 356443,
"tipo_documento": "dni",
"domicilio": "Torne 223",
"nro_documento": 37885553
},{ 
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
"apellido": "Chango",
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

PRODUCTOS = ["Detergente", "Lavandina", "Jabon", "Abrillantador de piso", "Esponja", "Cera para piso",""]
SERVICIOS = ["Limpieza vidrios", "Limpieza alfombra", "Limpieza oficina", "Limpieza sillones", "Limpieza salon", "Limpieza casa"]





## creo los grupos
grupo_empleados, created = Group.objects.get_or_create(name='empleados')
grupo_clientes, created = Group.objects.get_or_create(name='clientes')
#asigno permisos a los grupos
grupo_clientes.permissions.add(Permission.objects.get(codename='change_user'))
grupo_clientes.permissions.add(Permission.objects.get(codename='change_cliente'))
grupo_clientes.permissions.add(Permission.objects.get(codename='add_presupuesto'))



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
                passwd = User.objects.make_random_password()   
                u = User.objects.create_user(username=empleado.persona.email, password=passwd)         
                u.save()
                send_mail('Usuario creado exitosamente',
                      "Bienvenido! Usted ha sido dado de alta en el sistema.\n\n"+
                      "Utilize estos datos para iniciar sesion la primera vez:\n"+
                      "Usuario: %s\nPass: %s\n\n" % (empleado.persona.email, passwd)+
                      "Una vez que halla ingresado, cambie su clave por favor.\n\n\n\n"
                      "ZENDA - La higiene es salud",
                      'admin@zenda.com',
                      [empleado.persona.email])
                grupo_empleados.user_set.add(u)

            else:
                Cliente.objects.create(persona = personas.pop(index))

