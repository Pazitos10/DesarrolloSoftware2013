#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from gestionServicios.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
import datetime
import qsstats
from django.db.models import Q


def index(request):
	return render_to_response("index.html", context_instance = RequestContext(request))

@login_required(login_url="/")
def home(request):
    fecha_actual = datetime.datetime.now()
    presupuestos = Presupuesto.objects.all()
    for presupuesto in presupuestos:
        estado = str(presupuesto.obtener_estado_actual())
        print str(presupuesto.obtener_estado_actual())=='Valorizado'
        if estado == 'Valorizado':
            print presupuesto.valorizado.fecha_vigencia,"con",fecha_actual
            if presupuesto.valorizado.fecha_vigencia < fecha_actual:
                print "expire"
                presupuesto.valorizado.rechazar("Expiró presupuesto")
        if estado == 'Confirmado':
            if presupuesto.contrato.fin < fecha_actual:
                presupuesto.contrato.dar_de_baja(fecha_actual,"Expiró contrato")

    usuarios_totales = User.objects.all().count
    contratos_ultimo_anio = Contrato.objects.filter(baja= None).count
    contratos_terminados_ultimo_anio = Contrato.objects.filter(~ Q(baja=None)).count
  
    hoy = datetime.date.today() + datetime.timedelta(days=1)
    hace_2_semanas = hoy - datetime.timedelta(weeks=2)

    solicitadoQs = Solicitado.objects.all()
    if len(solicitadoQs)>0:
        solicitadoQss = qsstats.QuerySetStats(solicitadoQs, 'fecha_creacion')
        solicitado_stats = solicitadoQss.time_series(hace_2_semanas, hoy)
    else:
        solicitado_stats=[]

    confirmadoQs = Confirmado.objects.all()
    if len(confirmadoQs)>0:
        confirmadoQss = qsstats.QuerySetStats(confirmadoQs, 'confirmacion')
        confirmado_stats = confirmadoQss.time_series(hace_2_semanas, hoy)
    else:
        confirmado_stats=[]

    solicitados = []
    for s in solicitado_stats:
        fecha = str(s[0]).split('-')
        lista = []
        for numero in fecha:
            lista.append(int(numero)-1)
        lista.append(s[1])
        solicitados.append(lista)

    confirmados = []
    for s in confirmado_stats:
        fecha = str(s[0]).split('-')
        lista = []
        for numero in fecha:
            lista.append(int(numero)-1)
        lista.append(s[1])
        confirmados.append(lista)


    servicios = TipoDeServicio.objects.all()
    empleados_por_servicio = []
    for servicio in servicios:
        cantidad_empleados = servicio.empleado_set.count()
        empleados_por_servicio.append([servicio.nombre,cantidad_empleados])

    return render_to_response("home.html",{
        'solicitado_stats':solicitados,
        'confirmado_stats':confirmados,
        'usuarios_totales':usuarios_totales,
        'contratos_ultimo_anio':contratos_ultimo_anio,
        'contratos_terminados_ultimo_anio':contratos_terminados_ultimo_anio,
        'empleados_por_servicio':empleados_por_servicio
        },context_instance = RequestContext(request))

def privado(request):
    cliente = Persona.objects.get(user = request.user)
    linea_de_tiempo = cliente.lineadetiempo_set.all()
    print 'rol empleado:',request.session['rol_empleado']
    print 'rol cliente:',request.session['rol_cliente']
    
    return render_to_response("privado.html",{'linea_de_tiempo':linea_de_tiempo},context_instance = RequestContext(request))

#NUEVO CHIQUI DALEEE
def login_view(request):
    logout(request)
    username = password =''
    nuevo = False
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            #nuevo_jueves
            if user.last_login == user.date_joined:
                print "esste es nuevo cheeeeee"
                nuevo = True
            if user.is_superuser:
                login(request, user)
                return HttpResponseRedirect('home')
            elif user.groups.filter(name='clientes'):        
            #elif str(user.groups.get()) == "Usuario":
                login(request, user)
                request.session['rol_cliente'] = True
                request.session['rol_empleado'] = False
                if nuevo:
                    return HttpResponseRedirect('accounts/password_change/')
                return HttpResponseRedirect('privado')            

            else: #empleado
                login(request, user)
                request.session['rol_cliente'] = False
                request.session['rol_empleado'] = True
                #nuevo_jueves
                if nuevo:
                    return HttpResponseRedirect('accounts/password_change/')
                return HttpResponseRedirect('privado')
        request.notifications.error('Usuario y/o Contraseña incorrecto.')
    return render_to_response('index.html', context_instance=RequestContext(request))
#END NUEVO CHIQUI DALEEE



#NUEVO by chiqui
def change_role(request):

    print "hola"
    username = request.user.username
    password = request.user.password
    is_cliente = request.session['rol_cliente']
    print request.session['rol_cliente']
    #is_empleado = request.session['rol_empleado']

    #user_change = authenticate(username=username, password=password)

    #logout(request)        
    if is_cliente:
        print("cambio a empleado")
        #login(request, user_change)
        request.session['rol_cliente'] = False
        request.session['rol_empleado'] = True
        return HttpResponseRedirect('home')
    else:
        print("cambio a cliente")
        #login(request, user_change)
        request.session['rol_cliente'] = True
        request.session['rol_empleado'] = False
        return HttpResponseRedirect('privado')
'''
def change_to_role_empleado(request):
    username = request.user.username
    password = request.user.password
    user_change = authenticate(username=username, password=password)
    
    logout(request)
    login(request, user_change)
    return HttpResponseRedirect('home_empleado')
'''
#END NUEVO by chiqui


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
'''
def contacto(request):
    persona = Persona.objects.get(user = request.user)
    if request.method == 'POST':
        mensaje = request.POST['message']
        LineaDeTiempo.objects.create(titulo="Envio de mensaje a administrador",
                                    tiempo_de_actividad=datetime.datetime.now(),
                                    descripcion="Mensaje: " +mensaje,
                                    persona = persona,
                                    tipo_actividad = "info")
        return HttpResponseRedirect('privado')
    return render_to_response('contacto.html',{'persona':persona}, context_instance=RequestContext(request))
'''