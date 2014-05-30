#! /usr/bin/python2
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404,redirect
from django.template import RequestContext
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django.core.urlresolvers import reverse

from gestionServicios.models import *
from gestionServicios.forms import *

from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.contrib.auth.models import Group 

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

#NUEVO
from django.contrib.auth.models import User
#END NUEVO
import time
import datetime
import qsstats
import dateutil

# from datetime import date #--- Written by Bruno import ---
from datetime import datetime, timedelta, date
import re #--- Written by Bruno import---

#NUEVO by chiqui
import simplejson
from django.core.mail import send_mail
#END NUEVO by chiqui

#NUEVO CHIQUI DALEEEEE
import collections

def personaView(request):
    if request.method=='POST':
        formulario = Persona(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/')
    else:
        formulario=PersonaForm()
    return render_to_response('personas/alta.html', {'formulario': formulario}, context_instance=RequestContext(request))

def alta_tipo_de_servicio(request):
    if request.method=='POST':
        tipo_de_servicio = str(request.POST["nombre"])
        formulario = TipoDeServicioAltaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            request.notifications.success('Servicio '+tipo_de_servicio+' dado de alta.')
            return HttpResponseRedirect('/home')
    else:
        formulario=TipoDeServicioAltaForm()
    return render_to_response('tiposDeServicio/alta.html', {'formulario': formulario}, context_instance=RequestContext(request))


def modificar_tipo_de_servicio(request):
    buscador = BuscadorTipoDeServicioForm()
    formulario = ""
    if request.method=='POST':
        tipo_de_servicio = str(request.REQUEST["tipoDeServicio_1"])
        tipo_de_servicio = get_object_or_404(TipoDeServicio, pk = tipo_de_servicio)
        formulario = TipoDeServicioModificaForm(request.POST, instance=tipo_de_servicio)
        if formulario.is_valid():
            formulario.save()
            request.notifications.success('Datos del servicio ' +tipo_de_servicio.nombre+" modificados.")
            return HttpResponseRedirect('/home')

    else:
        if "tipoDeServicio_1" in request.REQUEST:
            if not request.REQUEST["tipoDeServicio_1"] == "":
                tipo_de_servicio = str(request.REQUEST["tipoDeServicio_1"])
                tipo_de_servicio = get_object_or_404(TipoDeServicio, pk = tipo_de_servicio)
                buscador = BuscadorTipoDeServicioForm(request.REQUEST)
                formulario = TipoDeServicioModificaForm(instance = tipo_de_servicio)
    return render_to_response('tiposDeServicio/modificar.html', {'formulario': formulario, 'buscar':buscador}, context_instance=RequestContext(request))


def alta_cliente(request):
    formulario = ""
    existe='no'
    if request.method=='POST':
        tipo_documento = request.POST['tipo_documento']
        nro_documento = request.POST['nro_documento']
        apellido = request.POST['apellido']
        nombre = request.POST['nombre'] 
        domicilio = request.POST['domicilio']
        telefono = request.POST['telefono']
        email = request.POST['email']

        try:
            persona = Persona.objects.get(pk=nro_documento)
        except Persona.DoesNotExist:
            persona = None

        if persona == None:          
            persona = Persona()
            persona.tipo_documento = tipo_documento
            persona.nro_documento = nro_documento
            persona.apellido = apellido
            persona.nombre = nombre
            persona.domicilio = domicilio
            persona.telefono = telefono
            persona.email = email

            formulario=ClienteAltaForm(request.POST)
            if formulario.is_valid():
                persona.save()

        try:
            print persona
            persona = Persona.objects.get(pk=persona.nro_documento)
        except Persona.DoesNotExist:
            persona = None
        if persona != None:
            cliente = Cliente()
            cliente.persona = persona
            cliente.save()

            LineaDeTiempo.objects.create(titulo="Dado de alta como cliente",
                                        tiempo_de_actividad=datetime.now(),
                                        descripcion="",
                                        persona = cliente.persona,
                                        tipo_actividad = "info")

            request.notifications.success('Cliente ' + cliente.persona.nombre +" "+ cliente.persona.apellido+" dado de alta.")

            return HttpResponseRedirect('/home')
    else:
        formulario=""
        if 'Documento' in request.GET:
            dni = request.GET['Documento']
            
            if not dni == ''and not(dni.isalpha()) and dni.isdigit():
                try:
                    cliente = Cliente.objects.get(persona__pk=dni)
                except Cliente.DoesNotExist:
                    cliente = None
                try:
                    persona = Persona.objects.get(pk=dni)
                except Persona.DoesNotExist:
                    persona = None

                if cliente != None:
                    request.notifications.success(cliente.persona.nombre+' '+cliente.persona.apellido+' ya es cliente')
                    return redirect('/home')
                else:
                    if persona != None:
                        existe = 'si'
                        formulario = ClienteAltaForm(instance = persona)
                    else:
                        p = Persona()
                        p.nro_documento = dni
                        formulario = ClienteAltaForm(instance = p)
    return render_to_response('clientes/alta.html', {'existe':existe,'formulario': formulario}, context_instance=RequestContext(request))

def modificar_cliente(request):
    buscador = BuscadorClienteForm()
    formulario = ""
    if request.method=='POST':
        cliente = int(request.REQUEST["cliente_1"])
        cliente = get_object_or_404(Cliente, pk = cliente)
        formulario = ClienteModificarForm(request.POST, instance = cliente.persona)
        if formulario.is_valid():
            formulario.save()
            LineaDeTiempo.objects.create(titulo="Datos modificados",
                                        tiempo_de_actividad=datetime.now(),
                                        descripcion="Consulte su perfil para consultar las modificaciones",
                                        persona = cliente.persona,
                                        tipo_actividad = "success")
            request.notifications.success('Datos del cliente ' +cliente.persona.nombre+" "+cliente.persona.apellido+" modificados.")
            return HttpResponseRedirect('/home')
    else:
        if "cliente_1" in request.REQUEST:
            if not request.REQUEST["cliente_1"] == '':
                cliente = int(request.REQUEST["cliente_1"])
                cliente = get_object_or_404(Cliente, pk = cliente)
                buscador = BuscadorClienteForm(request.REQUEST)
                formulario = ClienteModificarForm(instance = cliente.persona)
    return render_to_response('clientes/modificar.html', {'formulario': formulario, 'buscar':buscador}, context_instance=RequestContext(request))


def alta_empleado(request):
    existe = 'no'
    formpersona =""
    servicios = TipoDeServicio.objects.filter(baja=None)
    if request.method=='POST':
        tipo_de_servicio = request.POST['especialidad']    
        tipo_documento = request.POST['tipo_documento']
        nro_documento = request.POST['nro_documento']
        apellido = request.POST['apellido']
        nombre = request.POST['nombre'] 
        domicilio = request.POST['domicilio']
        telefono = request.POST['telefono']
        email = request.POST['email']
        cuil = request.POST['CUIL']
        fecha_nacimiento = request.POST['nacimiento']
        try:
            persona = Persona.objects.get(pk=nro_documento)
        except Persona.DoesNotExist:
            persona = None

        if persona == None:
            persona = Persona()
            persona.tipo_documento = tipo_documento
            persona.nro_documento = nro_documento
            persona.apellido = apellido
            persona.nombre = nombre
            persona.domicilio = domicilio
            persona.telefono = telefono
            persona.email = email

            formpersona=PersonaAltaForm(request.POST)
            if formpersona.is_valid():
                persona.save()

        empleado = Empleado()
        empleado.CUIL = cuil
        empleado.nacimiento = fecha_nacimiento
        
        
        
        tipo_servicio = get_object_or_404(TipoDeServicio,pk=tipo_de_servicio)
        
        empleado.especialidad = tipo_servicio            
        empleado.persona = persona
        formpersona =PersonaAltaForm(request.POST, instance=persona)
        formulario = EmpleadoAltaForm(request.POST,instance=empleado)
        
        if formulario.is_valid():
            if persona.user:
                user = User.objects.filter(username=persona.email)[0]
                grupo = Group.objects.filter(name='empleados')[0]
                print(grupo)
                user.groups.add(grupo)
                user.save()
            else:
                passwd = User.objects.make_random_password()
                user = User.objects.create_user(username=persona.email, password='123456')         
                user.save()
                grupo = Group.objects.filter(name='empleados')[0]
                user.groups.add(grupo)
                persona.user =  user
                persona.save()
                # send_mail('Usuario creado exitosamente',
                #       "Bienvenido! Usted ha sido dado de alta en el sistema.\n\n"+
                #       "Utilize estos datos para iniciar sesion la primera vez:\n"+
                #       "Usuario: %s\nPass: %s\n\n" % (persona.email, passwd)+
                #       "Una vez que halla ingresado, cambie su clave por favor.\n\n\n\n"
                #       "ZENDA - La higiene es salud",
                #       'admin@zenda.com',
                #       [persona.email])
                request.notifications.success('Usuario ' + persona.email+ ' dado de alta' )
            empleado.save()
            LineaDeTiempo.objects.create(titulo="Dado de alta como empleado",
                                        tiempo_de_actividad=datetime.now(),
                                        descripcion="",
                                        persona = empleado.persona,
                                        tipo_actividad = "info")

            request.notifications.success('Empleado ' + empleado.persona.nombre +" "+ empleado.persona.apellido+" dado de alta.")
            return HttpResponseRedirect('/home')
    else:
        formulario=""
        #servicios = TipoDeServicio.objects.filter(baja=None)
        
        if 'Documento' in request.GET:
            dni = request.GET['Documento']
            if not dni == '' and not(dni.isalpha()) and dni.isdigit():
                # try:
                #     empleado = Empleado.objects.get(persona__pk=dni)
                # except Empleado.DoesNotExist:
                #     empleado = None
                try:
                    persona = Persona.objects.get(pk=dni)
                    count = persona.empleado_set.all().count()
                    if count >= 1:
                        empleado = persona.empleado_set.all()[count-1]
                    else: 
                        empleado = None
                except Persona.DoesNotExist:
                    persona = None
                    empleado = None
                if empleado != None and empleado.dado_de_baja() == False:
                    request.notifications.success(empleado.persona.nombre+' '+empleado.persona.apellido+' ya es empleado')
                    return redirect('/home')
                else:
                    if persona != None:
                        existe = 'si'
                        formpersona = PersonaAltaForm(instance=persona)
                    else:
                        p = Persona()
                        p.nro_documento = dni
                        formpersona = PersonaAltaForm(instance = p)
                    formulario = EmpleadoAltaForm()
    return render_to_response('empleados/alta.html', {'existe':existe,'formulario': formulario, 'formpersona':formpersona, 'servicios':servicios}, context_instance=RequestContext(request))

def modificar_empleado(request):
    buscador = BuscadorEmpleadoForm()
    formulario = ""
    if request.method=='POST':
        empleado = int(request.REQUEST["empleado_1"])
        empleado = get_object_or_404(Empleado, pk = empleado)
        formulario = EmpleadoModificarForm(request.POST, instance = empleado.persona)
        if formulario.is_valid():
            empleado.CUIL = formulario.cleaned_data['cuil']
            #empleado.nacimiento = formulario.cleaned_data['fecha_nacimiento']
            #empleado.especialidad = formulario.cleaned_data['tipo_de_servicio']
            empleado.save()
            formulario.save()
            LineaDeTiempo.objects.create(titulo="Datos modificados",
                                        tiempo_de_actividad=datetime.now(),
                                        descripcion="Consulte su perfil para consultar las modificaciones",
                                        persona = empleado.persona,
                                        tipo_actividad = "success")
            request.notifications.success('Datos del empleado ' +empleado.persona.nombre+" "+empleado.persona.apellido  +" modificados.")
            return HttpResponseRedirect('/home')
    else:
        if "empleado_1" in request.REQUEST:
            empleado = request.REQUEST['empleado_1']
            if empleado != "":
                empleado = int(request.REQUEST["empleado_1"])
                empleado = get_object_or_404(Empleado, pk = empleado)
                buscador = BuscadorEmpleadoForm(request.REQUEST)
                formulario = EmpleadoModificarForm(instance=empleado.persona)
                formulario.fields['cuil'].initial = empleado.CUIL
                #formulario.fields['fecha_nacimiento'].initial = empleado.nacimiento
                #formulario.fields['tipo_de_servicio'].initial = empleado.especialidad
    return render_to_response('empleados/modificar.html', {'formulario': formulario, 'buscar':buscador}, context_instance=RequestContext(request))


#--- Written by Bruno ---
def presupuesto(request):
    request.session['pre_data'] = {}
    request.session['frecuencias'] = {}
    request.session['cant_frec'] = {}
    #NUEVO CHIQUI
    request.session['presupuesto'] = {}
    buscador = BuscadorClienteForm(request.GET)
    #formulario = ""
    cliente = None
    if "cliente_1" in request.REQUEST:
        if not request.GET["cliente_1"] == "":
            cliente = int(request.GET["cliente_1"])
            cliente = get_object_or_404(Cliente, pk = cliente)
    if request.method=='POST':
        formulario = PresupuestoForm(request.POST)
        if formulario.is_valid():
            # Controlamos que esten todos para borrarlos de request.session cada vez que se crea un presup nuevo
            if request.session['pre_data'].has_key('serv'):
                request.session['pre_data'].pop('serv')
            if request.session['pre_data'].has_key('valorM2'):
                request.session['pre_data'].pop('valorM2')             
            
            request.session['pre_data'].update({'cliente': formulario.instance.cliente.pk, 'domicilio_servicio':formulario.instance.domicilio_servicio}) #inserto los datos en el diccionario que formara un presupuesto en un futuro
            #NUEVO CHIQUI
            request.session['presupuesto']['1'] = None
            request.session.modified = True
            return redirect('seleccion_servicios',0)
    else:
        formulario = PresupuestoForm(initial = {"cliente": cliente})
    return render_to_response('presupuestos/alta.html', {
        'formulario': formulario, 
        'buscar':buscador, 
        'cliente': cliente
        }, context_instance=RequestContext(request))


#--- Written by Bruno ---
def ensamble_presupuesto(request):
    #Creacion de presupuesto basico
    ok = True
    nro_pres = 0 # NO LO CREE
    cliente = get_object_or_404(Cliente, pk=request.session['pre_data']['cliente']) 
    dom_serv = request.session['pre_data']['domicilio_servicio']
    presupuesto = Presupuesto()
    presupuesto.cliente = cliente
    presupuesto.domicilio_servicio = dom_serv
    presupuesto.save()
    nro_pres = presupuesto.pk
    #import ipdb; ipdb.set_trace()
    
    #Adicion de servicios y fechas fin
    for pkTS,nombreTS in request.session['pre_data']['serv'].iteritems(): #este diccionario guarda por ej: {'L002':'limpieza de alfombras'}
        ##### fecha_fin = request.session['fechas'][pkTS]
        ##### mes,dia,anio = fecha_fin.split('/')
        ##### fecha_fin = date(int(anio),int(mes),int(dia))
        tipo_servicio = get_object_or_404(TipoDeServicio, pk=pkTS)
        presupuesto.contratar_servicio(tipo_servicio)
    #Adicion de frecuencias a cada servicio
    for sc in presupuesto.listar_servicios_contratados():
        pkTS = sc.tipo_servicio.pk 
        if pkTS in request.session['frecuencias']:
            for pk_frec,frec in request.session['frecuencias'][pkTS].iteritems():
                frecuencia = Frecuencia()
                frecuencia.dia = dia_choice(frec[0])
                frecuencia.hora_inicio = frec[1]
                frecuencia.hora_fin = frec[2]
                frecuencia.servicio_contratado = sc
                print '%s %s' % ("dia: ", frec[0])
                print '%s %s' % ("hora_inicio: ", frec[1])
                print '%s %s' % ("hora_fin: ", frec[2])
                frecuencia.save()
        else:
            ok = False
            request.notifications.error('Error servicio no encontrado.')
    return ok, nro_pres
#--- Written by Bruno ---
def seleccion_servicios(request, id_presupuesto):               #administra el agregado de servicios en un diccionario temporal hasta que entre por post.
    puedoArmar = True   #Esta hablando del fasooooo(?)
    frecuencias = FrecuenciasForm()
    buscar = BuscadorTipoDeServicioForm()
    #NUEVO CHIQUI
    presupuesto = None
    if (int(id_presupuesto) != 0):
            presupuesto = get_object_or_404(Presupuesto, pk = int(id_presupuesto)) 
    if request.method == 'POST':
        if len(request.session['pre_data']['serv']) <= 0 :
            request.notifications.error('No ha elegido ningun servicio, para continuar busque y agregue al menos uno, luego configure su frecuencia.')
        else:
            for pk,frec in request.session['frecuencias'].iteritems():
                if len(frec)==0:
                    request.notifications.error('Algunos de los servicios no cuentan con frecuencias,para continuar complete al menos una frecuencia para cada servicio.')
                    puedoArmar = False
                    break
            if puedoArmar:
                resultado, nro_pres = ensamble_presupuesto(request) #Crea Presupuesto,serviciosContratados,frecuencias y asocia todos los datos pertinentes
                if resultado:
                    #NUEVO CHIQUI
                    if (int(id_presupuesto) != 0):
                        if request.session.has_key('modificado'):
                            print "HOLAAAAAAAAaa"
                            print request.session['modificado']
                            #nuevo_jueves
                            if request.session['modificado']['1'] == True:
                                print request.POST['motivo']
                                motivo = request.POST['motivo']
                                print id_presupuesto, type(id_presupuesto)
                                print ("hice cambios, ahora si renegociar")
                                presupuesto_renegociar = get_object_or_404(Presupuesto,pk= int(id_presupuesto))
                                #nuevo_jueves
                                if motivo == '':
                                    presupuesto_renegociar.confirmado.dar_de_baja("Baja por renegociación.")
                                    request.notifications.success('Presupuesto renegociado exitosamente')       
                                    return HttpResponseRedirect('/home')
                                else:
                                    presupuesto_renegociar.confirmado.dar_de_baja(motivo)
                                    request.notifications.success('Presupuesto renegociado exitosamente')       
                                    return HttpResponseRedirect('/home')
                            else:
                                request.notifications.error('No realizo cambios.')       
                    else:
                        presupuesto = get_object_or_404(Presupuesto, pk = int(nro_pres))
                        LineaDeTiempo.objects.create(titulo="Presupuesto Nro:"+str(nro_pres)+" solicitado",
                                            tiempo_de_actividad=datetime.now(),
                                            descripcion="",
                                            persona = presupuesto.cliente.persona,
                                            tipo_actividad = "success")
                        request.notifications.success('Presupuesto creado exitosamente')       
                        return HttpResponseRedirect('/home')
                    #END NUEVO CHIQUI
                else :
                    request.notifications.error('Ha ocurrido un error, intente nuevamente')
            else:
                request.notifications.error('Algunos de los servicios no cuentan con frecuencias o fecha de fin, complete los datos para continuar.')
    else:
        if not request.session['pre_data'].has_key('serv') and not request.session['pre_data'].has_key('valorM2'):
            servicio = {}
            valorM2 = {} 
            request.session['pre_data']['serv'] = servicio
            request.session['pre_data']['valorM2'] = valorM2
            request.session.modified = True
        
        if "tipoDeServicio_1" in request.GET:
            if not request.GET["tipoDeServicio_1"] == "":
                if not request.session['pre_data']['serv'].has_key(str(request.GET["tipoDeServicio_1"])):    
                    servicio = request.session['pre_data']['serv']
                    valorM2 = request.session['pre_data']['valorM2']
                    pk = str(request.GET["tipoDeServicio_1"])
                    tipo_de_servicio = get_object_or_404(TipoDeServicio, pk = pk) 
                    servicio.update({pk:tipo_de_servicio.nombre})
                    valorM2.update({pk:tipo_de_servicio.valorM2})               
                    request.session['pre_data']['serv'] = servicio
                    request.session['pre_data']['valorM2'] = valorM2
                    request.session['frecuencias'][pk] = {}               
                    request.session['cant_frec'][pk] = 0 #inicializamos en 0 el indice de frecuencias para el servicio
                    #NUEVO CHIQUI
                if (int(id_presupuesto) != 0):
                    request.session['modificado']['1'] = True
                request.session.modified = True # Linea necesaria para que la sesion guarde los cambios entre request
        if (int(id_presupuesto) != 0):
            presupuesto = get_object_or_404(Presupuesto, pk = int(id_presupuesto)) 
    return render_to_response('presupuestos/datosTS.html', {
        'buscar':buscar,
        'presupuesto':presupuesto,
        'servicios': request.session['pre_data']['serv'],
        'valores' : request.session['pre_data']['valorM2'],
        'frecuencias': frecuencias
        }, context_instance=RequestContext(request))

    
#--- Written by Bruno ---    
def quitarSC(request, pk_servicio):
    request.session['pre_data']['serv'].pop(pk_servicio)
    request.session['pre_data']['valorM2'].pop(pk_servicio)
    request.session['frecuencias'].pop(pk_servicio)
    request.session['cant_frec'].pop(pk_servicio)
    presupuesto_pk = 0
    #NUEVO CHIQUI
    if request.session['presupuesto'].has_key('1'):
        if (request.session['presupuesto']['1'] != None):
            request.session['modificado']['1'] = True
            print "¿}?"
            print request.session['presupuesto']['1']
            presupuesto_pk = request.session['presupuesto']['1']
    request.session.modified = True
    return redirect('seleccion_servicios', presupuesto_pk)

#--- Written by Bruno - hay otro metodo que se llama frecuencias_servicio charlar nombre---
def frecuencias_de_servicio(request, pk_servicio):
    frecuencias_de_servicio = request.session['frecuencias'][pk_servicio] #obtengo las frecuencias del servicio seleccionado    
    request.session.modified = False
    return render_to_response('presupuestos/frecuencias.html', {"frecuencias": frecuencias_de_servicio,"pk_servicio":pk_servicio}, context_instance=RequestContext(request))

#--- Written by Bruno ---
def agregar_frecuencia(request, pk_servicio):
    if request.method == "POST":
        form = FrecuenciasForm(request.POST)
        if form.is_valid():
            dia =  dia_string(form.cleaned_data['dia'])
            hora_inicio = form.cleaned_data['hora_inicio']
            hora_fin =  form.cleaned_data['hora_fin']
            print hora_inicio       
            if hora_inicio < hora_fin:
                if not existe_frecuencia(request,pk_servicio,dia,hora_inicio,hora_fin):
                    frecuencias_de_servicio = request.session['frecuencias'][pk_servicio]
                    pk_frec = request.session['cant_frec'][pk_servicio]
                    pk_frec += 1
                    frecuencias_de_servicio.update({pk_frec : [dia,str(hora_inicio),str(hora_fin)]})
                    request.session['cant_frec'].update({pk_servicio:pk_frec})
                    request.session['frecuencias'][pk_servicio] = frecuencias_de_servicio
                    #NUEVO CHIQUI
                    if request.session['presupuesto'].has_key('1'):
                        if (request.session['presupuesto']['1'] != None):
                            request.session['modificado']['1'] = True
                            print "MODIFIQUE TRUE LOCO"
                    request.session.modified = True
                # else:
                #     request.notifications.error('Ya existe una frecuencia con estos datos, intente realizar alguna modificacion')
            print "frecuencias de servicio: "+str(request.session['frecuencias'][pk_servicio])
            print "indice "+str(request.session['cant_frec'][pk_servicio])
        else:
            print form.errors
        request.session.modified = True
    return redirect('frecuencias_de_servicio',pk_servicio)

#--- Written by Bruno ---
def dia_string(dia): #Devuelve el nombre real del choice ingresado
    for d in Frecuencia.DIA_DE_LA_SEMANA_CHOICES:
        if d[0] == dia:
            return d[1]

#--- Written by Bruno ---
def dia_choice(dia):
    for d in Frecuencia.DIA_DE_LA_SEMANA_CHOICES:
        if d[1] == dia:
            return d[0]

#--- Written by Bruno ---
def existe_frecuencia(request,pk_servicio, d, hi , hf ):
    if request.session['frecuencias'].has_key(pk_servicio):
        for pk_frec, frec in request.session['frecuencias'][pk_servicio].iteritems():
            if frec == [d,str(hi),str(hf)]:
                print 'es la misma'
                return True
            else:
                print 'es otra'
                return False
    else:
        return False

#--- Written by Bruno ---
def quitarFrec(request,pk_servicio,pk_frec):
    print pk_frec, type(pk_frec)
    request.session['frecuencias'][pk_servicio].pop(pk_frec)
    request.session['cant_frec'][pk_servicio]-=1
    request.session.modified = True
    #NUEVO CHIQUI
    if request.session['presupuesto'].has_key('1'):
        if (request.session['presupuesto']['1'] != None):
            request.session['modificado']['1'] = True
    return redirect('frecuencias_de_servicio',pk_servicio)

#--- Written by Bruno ---
def valorizar_presupuesto(request):
    buscador = BuscadorClienteForm(request.GET)
    if "cliente_1" in request.GET and request.GET["cliente_1"].isdigit():
        cliente = int(request.GET["cliente_1"])
        cliente = get_object_or_404(Cliente, pk = cliente)
        presupuestos = cliente.get_solicitados()
    else:
        cliente = None
        presupuestos = None   
    if request.method=='POST':
        request.session['id_presupuesto'] = request.POST['id_presupuesto'] 
        return HttpResponseRedirect('valorizar/servicios_contratados')
    return render_to_response('presupuestos/valorizar.html', { 
        'buscar':buscador, 
        'cliente': cliente,
        'presupuestos': presupuestos
        }, context_instance=RequestContext(request))

#--- Written by Bruno ---
def servicios_contratados(request):
    presupuesto = get_object_or_404(Presupuesto, id = request.session['id_presupuesto'])
    sc = presupuesto.serviciocontratado_set.all() #todos los SC de un presupuesto
    total = 0
    if request.method == 'POST':
        if "id_serv" in request.POST:
            id_serv = request.POST['id_serv']
            if "ConfirmoVal-"+str(id_serv) in request.POST:
                if "False" == request.POST["ConfirmoVal-"+str(id_serv)]:
                    return HttpResponseRedirect('./servicios_contratados')
                else:
                    serv_contratado =get_object_or_404(ServicioContratado, pk = int(request.POST['servicio_contratado']))#un SC del presupuesto
                    print str(request.POST['cantidadM2'])
                    if request.POST['cantidadM2'] != None:
                        print "cant m2"
                        print request.POST['cantidadM2']
                        if (not (request.POST['cantidadM2'].isalpha())) and request.POST['cantidadM2'].isnumeric():
                            serv_contratado.metros_cuad = float(request.POST['cantidadM2'].replace(',','.'))
                        else:
                            request.notifications.error('El valor ingresado debe ser un número')
                            print "esta malllll es letra"
                            return HttpResponseRedirect('./servicios_contratados')
                    else:
                        serv_contratado.metros_cuad = 0
                    serv_contratado.calcularImporte(serv_contratado.tipo_servicio.valorM2)
                    total = presupuesto.calcularTotal()
        else:
            if "False" == request.POST['Confirmo']:
                return HttpResponseRedirect('./servicios_contratados')
            else:
                if request.POST["nuevoValor"] != '':
                    presupuesto.solicitado.valorizar(float(request.POST["nuevoValor"].replace(',','.')))
                else:
                    presupuesto.solicitado.valorizar(request.POST["total"])
                request.notifications.success('Presupuesto Nro. %s Valorizado' % (presupuesto.pk))
                return HttpResponseRedirect('/home')
        
    return render_to_response('presupuestos/servicios_contratados.html',
     {'servicios': sc, 'total':total}, context_instance=RequestContext(request))


def renegociar(request):
    buscador = BuscadorClienteForm(request.GET)

    request.session['pre_data'] = {}
    request.session['pre_data']['serv'] = {}
    request.session['pre_data']['valorM2'] = {}
    request.session['frecuencias'] = {}
    request.session['cant_frec'] = {}
    #NUEVO CHIQUI
    request.session['modificado'] = {}
    request.session['presupuesto'] = {}

 
    if "cliente_1" in request.GET and request.GET["cliente_1"].isdigit():
        cliente = int(request.GET["cliente_1"])
        cliente = get_object_or_404(Cliente, pk = cliente)
        presupuestosConfirmados = cliente.get_confirmados_vigentes()#Presupuesto.objects.filter(cliente=cliente).filter(confirmado__nombre = 'Confirmado')    #Tomo los presupuestos CONFIRMADOS del cliente
    else:
        cliente = None
        presupuestosConfirmados = None
    if request.method=='POST':
        presupuesto_renegociar = get_object_or_404(Presupuesto, pk = int(request.POST['id_presupuesto']))

        request.session['pre_data'].update({'cliente': presupuesto_renegociar.cliente.pk, 'domicilio_servicio':presupuesto_renegociar.domicilio_servicio}) #inserto los datos en el diccionario que formara un presupuesto en un futuro

        for sc in presupuesto_renegociar.serviciocontratado_set.all():
            dicc_servicios = request.session['pre_data']['serv']
            dicc_valoresM2 = request.session['pre_data']['valorM2']

            dicc_servicios.update({sc.tipo_servicio.pk:sc.tipo_servicio.nombre})
            dicc_valoresM2.update({sc.tipo_servicio.pk:sc.tipo_servicio.valorM2})

            request.session['pre_data']['serv'] = dicc_servicios
            request.session['pre_data']['valorM2'] = dicc_valoresM2
            request.session.modified = True
    
            request.session['frecuencias'][sc.tipo_servicio.pk] = {}               
            request.session['cant_frec'][sc.tipo_servicio.pk] = 0
            request.session.modified = True
                
            for f in sc.frecuencia_set.all():
                frecuencias_de_servicio = request.session['frecuencias'][sc.tipo_servicio.pk]
                pk_frec = request.session['cant_frec'][sc.tipo_servicio.pk]

                pk_frec += 1
                frecuencias_de_servicio.update({pk_frec: [dia_string(f.dia),str(f.hora_inicio),str(f.hora_fin)]})
                request.session['cant_frec'].update({sc.tipo_servicio.pk: pk_frec})
                request.session['frecuencias'][sc.tipo_servicio.pk] = frecuencias_de_servicio
                request.session.modified = True
                print (pk_frec)
                print request.session['frecuencias'][sc.tipo_servicio.pk]
            request.session.modified = True
        
        request.session['modificado']['1'] = False
        request.session['presupuesto']['1'] = presupuesto_renegociar.pk  #objetos no se pueden meter en sesion sin serializar
        request.session.modified = True
        return redirect('seleccion_servicios', presupuesto_renegociar.pk)
    return render_to_response('contratos/renegociar.html', { 
        'buscar':buscador, 
        'cliente': cliente,
        'presupuestos': presupuestosConfirmados
        }, context_instance=RequestContext(request))

#LO USAMOS¡?¡?¡?¡?¡
def confirmar_presupuesto(request):
    buscador = BuscadorClienteForm(request.GET)
    if "cliente_1" in request.GET and request.GET["cliente_1"].isdigit():
        fecha_actual = datetime.now()
        cliente = int(request.GET["cliente_1"])
        cliente = get_object_or_404(Cliente, pk = cliente)
        presupuestos_aux = cliente.get_valorizados()
        presupuestos = []
        for presupuesto in presupuestos_aux:
            if presupuesto.valorizado.fecha_vigencia >= fecha_actual:
                presupuestos.append(presupuesto)
    else:
        cliente = None
        presupuestos = None
    if request.method=='POST':
        request.session['id_presupuesto'] = request.POST['id_presupuesto'] 
        #NUEVO by chiqui
        request.session['id_persona'] = cliente.persona.pk
        #END NUEVO by chiqui
        return HttpResponseRedirect('contrato')
    return render_to_response('presupuestos/confirmar.html', { 
        'buscar':buscador, 
        'cliente': cliente,
        'presupuestos': presupuestos
        }, context_instance=RequestContext(request))



#################---------------------ASIGNACION DE EMPLEADO

def alta_turnos(request):
    """Busca los presupuestos confirmados de un cliente"""
    buscador = BuscadorClienteForm(request.GET)
    cliente = None
    presupuestos = None  
    if "cliente_1" in request.GET and request.GET["cliente_1"].isdigit():
        cliente = int(request.GET["cliente_1"])
        cliente = get_object_or_404(Cliente, pk = cliente)
        presupuestos = cliente.get_confirmados_vigentes()
    if request.method=='POST':
        request.session['id_presupuesto'] = request.POST['id_presupuesto'] 
        return HttpResponseRedirect('asignar/frecuencias_servicio_contratado')
    return render_to_response('turnos/alta.html', { 
        'buscar':buscador, 
        'cliente': cliente,
        'presupuestos': presupuestos
        }, context_instance=RequestContext(request))


def frecuencias_servicio_contratado(request):
    """Lista los servicios contratados de un presupuesto"""
    presupuesto = get_object_or_404(Presupuesto, id = request.session['id_presupuesto'] )  
    sc = presupuesto.serviciocontratado_set.all() #todos los SC de un presupuesto
    if request.method == 'POST':
        return redirect('frecuencias_servicio', id_presupuesto = presupuesto.id, id_sc = request.POST['servicio_contratado'] )
    return render_to_response('turnos/servicios_contratados.html',
     {'servicios': sc}, context_instance=RequestContext(request))

def frecuencias_servicio(request,id_presupuesto, id_sc):
    """Lista las frecuencias de un servicio contratado"""
    presupuesto =  get_object_or_404(Presupuesto,pk=id_presupuesto)
    sc = get_object_or_404(ServicioContratado, pk = id_sc )  
    frecuencias = sc.frecuencia_set.all()
    servicios_contratados = presupuesto.serviciocontratado_set.all()
    if request.method == 'POST':
        if "Es_servicio" in request.POST :
            return redirect('frecuencias_servicio', id_presupuesto = presupuesto.id, id_sc = request.POST['servicio_contratado'])
        else:
            sc_id = request.POST['servicio_contratado']
            frecuencia_id = request.POST['frecuencia_id']
            return redirect('crear_turno',sc_id, frecuencia_id)
    return render_to_response('turnos/servicios_contratados.html',
     {'frecuencias': frecuencias,
     'servicios':servicios_contratados,
     'servicio_contratado':sc}, context_instance=RequestContext(request))

def turnos_de_empleado(request,id_empleado,id_frecuencia):
    """Busca los turnos para un dia de un empleado"""
    empleado = get_object_or_404(Empleado, pk = id_empleado)
    frecuencia = get_object_or_404(Frecuencia, pk= id_frecuencia)
    turnos = empleado.turno_set.filter(frecuencia__dia = frecuencia.dia)
    return render_to_response('turnos/frecuencias_empleado.html', { 
        'empleado': empleado,
        'turnos':turnos,
        }, context_instance=RequestContext(request))

def turnos_de_empleado_eliminar(request,id_empleado,id_frecuencia):
    """Busca los turnos para un dia de un empleado"""
    empleado = get_object_or_404(Empleado, pk = id_empleado)
    frecuencia = get_object_or_404(Frecuencia, pk= id_frecuencia)
    turnos = empleado.turno_set.filter(frecuencia__dia = frecuencia.dia)
    return render_to_response('turnos/eliminar_turno.html', { 
        'empleado': empleado,
        'turnos':turnos,
        }, context_instance=RequestContext(request))

def turnos_frecuencia(request,id_frecuencia):   
    frecuencia = get_object_or_404(Frecuencia, pk = id_frecuencia)
    turnos_frecuencia = frecuencia.turno_set.all()
    return render_to_response('turnos/turnos_frecuencia.html', {
        'turnos_frecuencia':turnos_frecuencia,
        }, context_instance=RequestContext(request))

def empleados_de_tipo_servicio(request,id_tipo_servicio,id_frecuencia):
    tipo_servicio = get_object_or_404(TipoDeServicio, pk=id_tipo_servicio)
    empleado_tipo_servicio = tipo_servicio.empleado_set.all()
    frecuencia = get_object_or_404(Frecuencia,pk=id_frecuencia)
    return render_to_response('turnos/empleados_servicio.html', {
        'empleados_disponibles':empleado_tipo_servicio,
        'frecuencia':frecuencia
        }, context_instance=RequestContext(request))

def crear_turno_empleado(request,id_empleado, id_frecuencia):
    turno = TurnosForm()
    empleado = get_object_or_404(Empleado,pk=id_empleado)
    if request.method == 'POST':
        formulario = TurnoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
    return render_to_response('turnos/crear_turno_empleado.html', { 
        'turno':turno,
        'empleado':empleado,
        'frecuencia':id_frecuencia,
        }, context_instance=RequestContext(request))

def quitar_turno(request,id_turno):
    turno = get_object_or_404(Turno,pk=id_turno)
    turno.delete()
    return HttpResponse('ok')


#--------------- LISTADOS

def listado_empleados(request):
    empleados_aux = Empleado.objects.all()
    empleados = []
    for empleado in empleados_aux:
        if empleado.dado_de_baja() == False:
            empleados.append(empleado)
    return render_to_response('listados/empleados.html', { 
        'empleados':empleados,
        }, context_instance=RequestContext(request))

#NUEVO by chiqui
def listado_presupuestos(request):
    presupuestos = []
    personal = ""   #PARA QUE??
    #NUEVO
    if request.user.is_superuser or request.session['rol_empleado']:#request.user.groups.filter(name='empleados'):

        presupuestoss = Presupuesto.objects.all()
        confirmados_vigentes = []
        for p in presupuestoss:
            if p.obtener_estado_actual() is not None:
                presupuestos.append(p)

        solicitados = Presupuesto.objects.filter(solicitado__nombre = 'Solicitado').exclude(
                                                valorizado__nombre = 'Valorizado').exclude(
                                                confirmado__nombre = 'Confirmado')

        valorizados = Presupuesto.objects.filter(valorizado__nombre = 'Valorizado').exclude(rechazado__nombre='Rechazado').exclude(
                                                confirmado__nombre = 'Confirmado')    

        confirmados = Presupuesto.objects.filter(confirmado__nombre = 'Confirmado')    #Tomo los presupuestos CONFIRMADOS

        for c in confirmados:
            if c.contrato.baja is None:
                confirmados_vigentes.append(c)
    else: 
        if request.user.groups.filter(name='clientes'): #Se puede ir este if???? gran pregunta... :O
            presupuestos = Presupuesto.objects.all().filter(cliente = request.user.persona_set.get().cliente_set.get())
            solicitados = request.user.persona_set.get().cliente_set.get().get_solicitados()
            valorizados = request.user.persona_set.get().cliente_set.get().get_valorizados()
            confirmados_vigentes = request.user.persona_set.get().cliente_set.get().get_confirmados_vigentes

    return render_to_response('listados/presupuestos.html', { 
        'presupuestos':presupuestos,
        'solicitados':solicitados,
        'valorizados':valorizados,
        'confirmados':confirmados_vigentes,
        'personal':personal,
        }, context_instance=RequestContext(request))
#END NUEVO by chiqui

def listado_clientes(request):
    clientes = Cliente.objects.all()
    return render_to_response('listados/clientes.html', { 
        'clientes':clientes,
        }, context_instance=RequestContext(request))

def info_cliente(request,id_cliente):
    cliente = get_object_or_404(Cliente, pk= id_cliente)
    return render_to_response('listados/cliente_info.html', { 
        'cliente':cliente,
        }, context_instance=RequestContext(request))


#------------------ LOGIN

def register_view(request):
    if request.method=="POST":
        form=RegisterForm(request.POST) 
        if form.is_valid():
            username=form.cleaned_data["username"]
            password_uno=form.cleaned_data["password_uno"]       
            password_dos=form.cleaned_data["password_dos"]    
            user = User.objects.create_user(username=username, password=password_uno)          
            user.save()     
            form.cleaned_data['grupo'].user_set.add(user)
            persona = int(request.REQUEST["persona_1"])
            persona = get_object_or_404(Persona, pk = persona)
            persona.user = user
            persona.save()
            request.notifications.success('Usuario ' + username+ ' dado de alta' )
            return redirect('/home')
        else:
            request.notifications.error('Las contraseñas no coinciden')

    if "persona_1" in request.REQUEST:
            persona = int(request.REQUEST["persona_1"])
            persona = get_object_or_404(Persona, pk = persona)
            buscador = BuscadorPersonaForm(request.REQUEST)
            if persona.user:
                request.notifications.success('Cliente ' + persona.nombre + ' ya posee un usuario' )
                return redirect('/home')
            else:
                form = RegisterForm() #si el cliente no tiene usuario,mostrar formulario de nuevo usuario
    else:
        buscador = BuscadorPersonaForm()
        form = ""
        persona = ""  
    return render_to_response("usuarios/register.html",{'form':form, 'buscador':buscador,'cliente':persona}, context_instance = RequestContext(request))


def alta_contrato(request): 
    presupuesto = get_object_or_404(Presupuesto, id = request.session['id_presupuesto'])
    if request.method=='POST':
        servicios = presupuesto.listar_servicios_contratados()
        pattern_fechas = r'fechaFin-\d+' #Las fechas vienen como por ej: fechaFin-1
        re_fechas = re.compile(pattern_fechas)
        if (request.POST['id_inicio'] != ''):
            if (request.POST['id_fin'] != ''):
                result = re_fechas.findall(str(request.POST)) #hago el matcheo de la re con lo que venga por post
                puedoCrear = True
                for fecha in result:
                    if request.POST[fecha] == u'':  #encontre una fecha fin sin valor
                        request.notifications.error('Falta ingresar fecha fin para uno o mas servicios.')
                        puedoCrear = False
                        print("Debe ingresar una fecha fin de servicio.")
                        break   #con que encuentre una fecha que no tiene valor no puede continuar
                if puedoCrear:
                        print("Todo ok, a crear el contrato man")        
                        print("Tengo estos sc: ")        
                        i = 1
                        for sc in servicios:
                            print 'al sc %s le corresponde la fecha fin %s' % (sc, request.POST['fechaFin-'+str(i)])
                            fechaFinSC = request.POST['fechaFin-'+str(i)]
                            sc.set_fecha_fin_sc(datetime(int (fechaFinSC.split('/')[2]), int(fechaFinSC.split('/')[1]), int(fechaFinSC.split('/')[0])))
                            i += 1
                        contrato = Contrato()
                        contrato.creacion = datetime.now()
                        fecha_inicio_contrato = request.POST['id_inicio']
                        contrato.inicio = (datetime(int(fecha_inicio_contrato.split('/')[2]), int(fecha_inicio_contrato.split('/')[1]), int(fecha_inicio_contrato.split('/')[0])))
                        fecha_fin_contrato = request.POST['id_fin']
                        contrato.fin = (datetime(int(fecha_fin_contrato.split('/')[2]), int(fecha_fin_contrato.split('/')[1]), int(fecha_fin_contrato.split('/')[0])))
                        contrato.save()
                        presupuesto.contrato = contrato
                        presupuesto.save()
                        presupuesto.valorizado.confirmar()
                        #NUEVO by chiqui
                        persona = get_object_or_404(Persona, pk = int(request.session['id_persona']))
                        if persona.user:
                            #nuevo_jueves
                            print("estemmm ya tiene usuario este cliente :P")
                            user = User.objects.filter(username=persona.email)[0]
                            grupo = Group.objects.filter(name='clientes')[0]
                            print(grupo)
                            user.groups.add(grupo)
                            user.save()
                        else:
                            print("a crearle usuario che")
                            passwd = User.objects.make_random_password()
                            user = User.objects.create_user(username=persona.email, password='123456')          
                            user.save()
                            grupo = Group.objects.filter(name='clientes')[0]
                            print(grupo)
                            user.groups.add(grupo)
                            persona.user =  user
                            persona.save()
                            '''
                            send_mail('Bienvenido a Zenda!',
                                      "Bienvenido! Usted ya esta registrado como cliente.\n\n"+
                                      "Utilize estos datos para iniciar sesion la primera vez:\n"+
                                      "Usuario: %s\nPass: %s\n\n" % (persona.email, passwd) +                                   
                                      "Una vez que halla ingresado, cambie su clave por favor.\n\n"+
                                      "GRACIAS POR ELEGIRNOS!!\n\n\n\n"+
                                      "ZENDA - La higiene es salud",
                                      'admin@zenda.com',
                                      [persona.email])
                            request.notifications.success('Usuario ' + persona.email+ ' dado de alta' )
                            '''
                        #END NUEVO by chiqui
                        LineaDeTiempo.objects.create(titulo="Presupuesto Nro:"+str(presupuesto.pk)+" contratado",
                                            tiempo_de_actividad=datetime.now(),
                                            descripcion="",
                                            persona = presupuesto.cliente.persona,
                                            tipo_actividad = "success")
                        request.notifications.success('Nuevo contrato generado')
                        return HttpResponseRedirect('/home')
            else:
                request.notifications.error('No ha establecido fecha de fin de contrato.')
                print("No ha definido ninguna fecha de fin de servicio.")
        else:
            request.notifications.error('No ha establecido fecha de inicio de contrato.')
            print("No ha definido una fecha de inicio de contrato.")
    else:
        servicios = presupuesto.listar_servicios_contratados()
    return render_to_response('contratos/alta.html', {'servicios': servicios}, context_instance=RequestContext(request))


def baja_tipo_de_servicio(request):
    buscador = BuscadorTipoDeServicioForm(request.REQUEST)
    if request.method=='POST':
        tipo_de_servicio = str(request.REQUEST["tipoDeServicio_1"])
        tipo_de_servicio = get_object_or_404(TipoDeServicio, pk = tipo_de_servicio)
        sc= tipo_de_servicio.serviciocontratado_set.all()

        print tipo_de_servicio, sc
        if len(sc) == 0: 
            formulario = TipoDeServicioBajaForm(request.POST, instance=tipo_de_servicio)
            print formulario.errors
            if formulario.is_valid():
                formulario.save()
                request.notifications.success('Servicio ' +tipo_de_servicio.nombre+" dado de baja.")
                return HttpResponseRedirect('/home')
        else:
            request.notifications.success('Servicio ' +tipo_de_servicio.nombre+" no se puede dar de baja ya que hay presupuestos asociados al mismo.")
            return HttpResponseRedirect('baja')
    else:
        if "tipoDeServicio_1" in request.REQUEST:
            tipo_de_servicio = str(request.REQUEST["tipoDeServicio_1"])
            tipo_de_servicio = get_object_or_404(TipoDeServicio, pk = tipo_de_servicio)
            buscador = BuscadorTipoDeServicioForm(request.REQUEST)
            formulario = TipoDeServicioBajaForm(instance = tipo_de_servicio)
        else:
            buscador = BuscadorTipoDeServicioForm()
            formulario = ""
    return render_to_response('tiposDeServicio/baja.html', {'formulario': formulario, 'buscar':buscador}, context_instance=RequestContext(request))


def baja_empleado(request):
    formulario = ""
    buscador = BuscadorEmpleadoForm()
    if request.method == 'POST':
        empleado = int(request.REQUEST["empleado_1"])
        empleado = get_object_or_404(Empleado, pk = empleado)
        turnos = empleado.turno_set.all()
        if len(turnos) != 0:
            request.notifications.success('Empleado ' + empleado.persona.nombre +" "+ empleado.persona.apellido+" no se puede dar de eliminar, por poseer turnos vigentes.")
            return redirect('/empleado/baja')
        formulario = EmpleadoBajaForm(request.POST, instance = empleado)
        if formulario.is_valid():
            formulario.save()
            request.notifications.success('Empleado ' + empleado.persona.nombre +" "+ empleado.persona.apellido+" dado de baja.")
            return redirect('/home')
    else:   
        if "empleado_1" in request.REQUEST:
            if not request.REQUEST["empleado_1"] == '':
                empleado = int(request.REQUEST["empleado_1"])
                empleado = get_object_or_404(Empleado, pk = empleado)
                formulario = EmpleadoBajaForm()
                buscador = BuscadorEmpleadoForm(request.REQUEST)
    return render_to_response('empleados/baja.html', {'formulario': formulario, 'buscar':buscador}, context_instance=RequestContext(request))


#ALAN LO ULTIMO 6/2

def estadistica_presupuestos(request):
    tiempo = date.today()
    hoy = date.today() + timedelta(days=1)
    if request.method == 'GET':
        tiempo = hoy - timedelta(weeks=2)
    else:
        filtro = request.POST['filtrar_por']
        cantidad = request.POST['cantidad']
        if cantidad.isdigit():
            if filtro == "semana":
                tiempo = hoy - timedelta(weeks=int(cantidad))
            elif filtro == "mes":
                tiempo = date.today() - dateutil.relativedelta.relativedelta(months=int(cantidad))
            elif filtro == "anio":
                tiempo = hoy - timedelta(days=int(cantidad)*365)
        
    solicitadoQs = Solicitado.objects.all()
    if len(solicitadoQs) > 0:
        solicitadoQss = qsstats.QuerySetStats(solicitadoQs, 'fecha_creacion')
        solicitado_stats = solicitadoQss.time_series(tiempo, hoy)
    else:
        solicitado_stats = []
        
    confirmadoQs = Confirmado.objects.all()
    if len(confirmadoQs) > 0:
        confirmadoQss = qsstats.QuerySetStats(confirmadoQs, 'confirmacion')
        confirmado_stats = confirmadoQss.time_series(tiempo, hoy)
    else:
        confirmado_stats = []    

    rechazadoQs = Rechazado.objects.all()
    if len(rechazadoQs) >0:
        rechazadoQss = qsstats.QuerySetStats(rechazadoQs, 'rechazado')
        rechazado_stats = rechazadoQss.time_series(tiempo, hoy)
    else:
        rechazado_stats = []

    cantidad_solicitados = 0
    cantidad_confirmados = 0
    cantidad_rechazados = 0

    solicitados = []
    print solicitado_stats
    for s in solicitado_stats:
        fecha = str(s[0]).split('-')
        lista = []
        for numero in fecha:
            lista.append(int(numero)-1)
        lista.append(s[1])
        solicitados.append(lista)
        if s[1]>0:
            cantidad_solicitados +=s[1]

    confirmados = []
    for s in confirmado_stats:
        fecha = str(s[0]).split('-')
        lista = []
        for numero in fecha:
            lista.append(int(numero)-1)
        lista.append(s[1])
        confirmados.append(lista)
        if s[1]>0:
            cantidad_confirmados +=s[1]

    rechazados = []
    for s in rechazado_stats:
        fecha = str(s[0]).split('-')
        lista = []
        for numero in fecha:
            lista.append(int(numero)-1)
        lista.append(s[1])
        rechazados.append(lista)
        if s[1]>0:
            cantidad_rechazados +=s[1]

    return render_to_response("estadisticas/estadistica_presupuestos.html",
        {'solicitados':solicitados,
        'confirmados':confirmados,
        'rechazados':rechazados,
        'cantidad_solicitados':cantidad_solicitados,
        'cantidad_confirmados':cantidad_confirmados,
        'cantidad_rechazados':cantidad_rechazados},context_instance = RequestContext(request))


def estadistica_empleados(request):
    servicios = TipoDeServicio.objects.all()
    empleados_por_servicio = []
    for servicio in servicios:
        cantidad_empleados = servicio.empleado_set.count()
        empleados_por_servicio.append([servicio.nombre,cantidad_empleados])

    hoy = date.today() + timedelta(days=1)
    tiempo = hoy - timedelta(weeks=4)
       
    solicitadoQs = Solicitado.objects.all()
    if len(solicitadoQs) > 0:
        solicitadoQss = qsstats.QuerySetStats(solicitadoQs, 'fecha_creacion')
        solicitado_stats = solicitadoQss.time_series(tiempo, hoy)
    else:
        solicitado_stats = []
    return render_to_response("estadisticas/estadistica_empleados.html",
        {'empleados_por_servicio':empleados_por_servicio},context_instance = RequestContext(request))

#VISTA DE USUARIO

def listado_presupuestos_usuario(request):
    cliente = Cliente.objects.get(persona__user=request.user)
    presupuestos = Presupuesto.objects.filter(cliente = cliente)
    solicitados = []
    valorizados = []
    confirmados = []
    personal = "si"
    
    for presupuesto in presupuestos:
        estado = presupuesto.obtener_estado_actual()
        if str(estado) == 'Confirmado':
            confirmados.append(presupuesto)
        elif str(estado) == 'Valorizado':
            valorizados.append(presupuesto)
        elif str(estado) == 'Solicitado':
            solicitados.append(presupuesto)

    return render_to_response('listados/presupuestos.html', { 
        'presupuestos':presupuestos,
        'solicitados':solicitados,
        'valorizados':valorizados,
        'confirmados':confirmados,
        'personal':personal,
        }, context_instance=RequestContext(request))

def info_presupuesto(request,id_presupuesto):
    presupuesto= get_object_or_404(Presupuesto, pk= id_presupuesto)
    sc = presupuesto.serviciocontratado_set.all() #todos los SC de un presupuesto
    return render_to_response('listados/presupuesto_info.html', { 
        'presupuesto':presupuesto,
        'servicios_contratados':sc,
        }, context_instance=RequestContext(request))

def servicio_frecuencias(request,id_servicio):
    servicio = get_object_or_404(ServicioContratado,pk=id_servicio)
    frecuencias = servicio.frecuencia_set.all()

    return render_to_response('listados/presupuesto_info_frecuencias.html', { 
        'frecuencias':frecuencias,
        }, context_instance=RequestContext(request))


def estadistica_cliente(request):
    hoy = date.today() + timedelta(days=1)
    if request.method == 'GET':
        tiempo = hoy - timedelta(weeks=2)
    else:
        filtro = request.POST['filtrar_por']
        cantidad = request.POST['cantidad']
        if filtro == "semana":
            tiempo = hoy - timedelta(weeks=int(cantidad))
        elif filtro == "mes":
            tiempo = date.today() - dateutil.relativedelta.relativedelta(months=int(cantidad))
        elif filtro == "anio":
            tiempo = hoy - timedelta(days=int(cantidad)*365)

    cliente = Cliente.objects.get(persona__user=request.user)

    solicitadoQs = Solicitado.objects.filter(presupuesto__cliente__persona__nro_documento= cliente.persona.nro_documento)
    if len(solicitadoQs) > 0:
        solicitadoQss = qsstats.QuerySetStats(solicitadoQs, 'fecha_creacion')
        solicitado_stats = solicitadoQss.time_series(tiempo, hoy)
    else:
        solicitado_stats = []
        
    confirmadoQs = Confirmado.objects.filter(presupuesto__cliente__persona__nro_documento= cliente.persona.nro_documento)
    if len(confirmadoQs) > 0:
        confirmadoQss = qsstats.QuerySetStats(confirmadoQs, 'confirmacion')
        confirmado_stats = confirmadoQss.time_series(tiempo, hoy)
    else:
        confirmado_stats = []    

    rechazadoQs = Rechazado.objects.filter(presupuesto__cliente__persona__nro_documento= cliente.persona.nro_documento)
    if len(rechazadoQs) >0:
        rechazadoQss = qsstats.QuerySetStats(rechazadoQs, 'rechazado')
        rechazado_stats = rechazadoQss.time_series(tiempo, hoy)
    else:
        rechazado_stats = []

    cantidad_solicitados = 0
    cantidad_confirmados = 0
    cantidad_rechazados = 0

    solicitados = []
    for s in solicitado_stats:
        fecha = str(s[0]).split('-')
        lista = []
        for numero in fecha:
            lista.append(int(numero)-1)
        lista.append(s[1])
        solicitados.append(lista)
        if s[1]>0:
            cantidad_solicitados +=s[1]

    confirmados = []
    for s in confirmado_stats:
        fecha = str(s[0]).split('-')
        lista = []
        for numero in fecha:
            lista.append(int(numero)-1)
        lista.append(s[1])
        confirmados.append(lista)
        if s[1]>0:
            cantidad_confirmados +=s[1]

    rechazados = []
    for s in rechazado_stats:
        fecha = str(s[0]).split('-')
        lista = []
        for numero in fecha:
            lista.append(int(numero)-1)
        lista.append(s[1])
        rechazados.append(lista)
        if s[1]>0:
            cantidad_rechazados +=s[1]

    return render_to_response("estadisticas/estadistica_presupuestos.html",
        {'solicitados':solicitados,
        'confirmados':confirmados,
        'rechazados':rechazados,
        'cantidad_solicitados':cantidad_solicitados,
        'cantidad_confirmados':cantidad_confirmados,
        'cantidad_rechazados':cantidad_rechazados},context_instance = RequestContext(request))


def valorizar_estadistica_cliente(request,id_cliente):
    hoy = datetime.date.today() + datetime.timedelta(days=1)
    tiempo = hoy - datetime.timedelta(days=int(1)*365)

    cliente = get_object_or_404(Cliente, pk=id_cliente)

    solicitadoQs = Solicitado.objects.filter(presupuesto__cliente__persona__nro_documento= cliente.persona.nro_documento)
    if len(solicitadoQs) > 0:
        solicitadoQss = qsstats.QuerySetStats(solicitadoQs, 'fecha_creacion')
        solicitado_stats = solicitadoQss.time_series(tiempo, hoy)
    else:
        solicitado_stats = []
        
    confirmadoQs = Confirmado.objects.filter(presupuesto__cliente__persona__nro_documento= cliente.persona.nro_documento)
    if len(confirmadoQs) > 0:
        confirmadoQss = qsstats.QuerySetStats(confirmadoQs, 'confirmacion')
        confirmado_stats = confirmadoQss.time_series(tiempo, hoy)
    else:
        confirmado_stats = []    

    rechazadoQs = Rechazado.objects.filter(presupuesto__cliente__persona__nro_documento= cliente.persona.nro_documento)
    if len(rechazadoQs) >0:
        rechazadoQss = qsstats.QuerySetStats(rechazadoQs, 'rechazado')
        rechazado_stats = rechazadoQss.time_series(tiempo, hoy)
    else:
        rechazado_stats = []

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
        
    rechazados = []
    for s in rechazado_stats:
        fecha = str(s[0]).split('-')
        lista = []
        for numero in fecha:
            lista.append(int(numero)-1)
        lista.append(s[1])
        rechazados.append(lista)
        
    return render_to_response("presupuestos/estadistica_cliente.html",
        {'solicitados':solicitados,
        'confirmados':confirmados,
        'rechazados':rechazados,
        },context_instance = RequestContext(request))

#NUEVO by chiqui
def casilla_mensaje(request):
    #persona = get_object_or_404(Persona, user = request.user)
    user = get_object_or_404(User,username=request.user)
    #if request.method == 'POST':
        #mensaje = request.POST['id_mensaje']
        #return redirect('leer_mensaje',id_mensaje = mensaje)
    if user.username != "admin":
        #MODIFIQUE LA LINEA DE ABAJO by chiqui
        #if str(user.groups.get()) == "Empleado":         
        if request.session['rol_empleado']:
            #MODIFIQUE LA LINEA DE ABAJO by chiqui
            #user = get_object_or_404(User,username="admin")
            user = get_object_or_404(User,username=request.user)
    mensajes = user.mensaje_set.all()
    leidos =[]
    noLeidos = []
    for msj in mensajes:
        if msj.leido:
            leidos.append(msj)
        else:
            noLeidos.append(msj)
    cantidad_mensajes = mensajes.count()
    cantidad_leidos = len(leidos)
    cantidad_no_leidos = len(noLeidos)

    return render_to_response("mensajes/listado_mensaje.html",{
        'mensajes':reversed(mensajes),
        'cantidad_mensajes':cantidad_mensajes,
        'cantidad_leidos':cantidad_leidos,
        'cantidad_no_leidos':cantidad_no_leidos,
        },context_instance = RequestContext(request))
#END NUEVO by chiqui

#NUEVO by chiqui
def mensajes_leidos(request):
    #if request.method == 'POST':
        #mensaje = request.POST['id_mensaje']
        #return redirect('leer_mensaje',id_mensaje = mensaje)
    #persona = get_object_or_404(Persona, user = request.user)
    user = get_object_or_404(User,username=request.user)
    if user.username != "admin":
        #MODIFIQUE LA LINEA DE ABAJO by chiqui
        #if str(user.groups.get()) == "Empleado":         
        if request.session['rol_empleado']:
            #MODIFIQUE LA LINEA DE ABAJO by chiqui
            #user = get_object_or_404(User,username="admin")
            user = get_object_or_404(User,username=request.user)
    mensajes = user.mensaje_set.all()
    leidos =[]
    noLeidos = []
    for msj in mensajes:
        if msj.leido:
            leidos.append(msj)
        else:
            noLeidos.append(msj)
    cantidad_mensajes = mensajes.count()
    cantidad_leidos = len(leidos)
    cantidad_no_leidos = len(noLeidos)

    return render_to_response("mensajes/leidos.html",{
        'leidos':reversed(leidos),
        'cantidad_mensajes':cantidad_mensajes,
        'cantidad_leidos':cantidad_leidos,
        'cantidad_no_leidos':cantidad_no_leidos,
        },context_instance = RequestContext(request))
#END NUEVO by chiqui

#NUEVO by chiqui
def mensajes_no_leidos(request):
    #if request.method == 'POST':
        #mensaje = request.POST['id_mensaje']
        #return redirect('leer_mensaje',id_mensaje = mensaje)
    #persona = get_object_or_404(Persona, user = request.user)
    user = get_object_or_404(User,username=request.user)
    if user.username != "admin":
        #MODIFIQUE LA LINEA DE ABAJO by chiqui
        #if str(user.groups.get()) == "Empleado":         
        if request.session['rol_empleado']:
            #MODIFIQUE LA LINEA DE ABAJO by chiqui
            #user = get_object_or_404(User,username="admin")
            user = get_object_or_404(User,username=request.user)
    mensajes = user.mensaje_set.all()
    leidos =[]
    noLeidos = []
    for msj in mensajes:
        if msj.leido:
            leidos.append(msj)
        else:
            noLeidos.append(msj)
    cantidad_mensajes = mensajes.count()
    cantidad_leidos = len(leidos)
    cantidad_no_leidos = len(noLeidos)

    return render_to_response("mensajes/no_leidos.html",{
        'noLeidos':reversed(noLeidos),
        'cantidad_mensajes':cantidad_mensajes,
        'cantidad_leidos':cantidad_leidos,
        'cantidad_no_leidos':cantidad_no_leidos,
        },context_instance = RequestContext(request))
#END NUEVO by chiqui

#NUEVO by chiqui
def enviar_mail(request):
    user = get_object_or_404(User,username=request.user)
    if request.method =='POST':
        mensaje = request.POST['message']
        asunto = request.POST['asunto']
        adminuser = User.objects.get(username="admin")
        if user.username != "admin":
            persona = get_object_or_404(Persona,user = request.user)
            #MODIFICO LA LINEA DE ABAJO
            #if str(request.user.groups.get()) == "Usuario":
            if request.session['rol_cliente']:
                Mensaje.objects.create(remitente=persona.email,
                                        destinatario=adminuser,
                                        asunto=asunto,
                                        descripcion=mensaje,
                                        fecha_envio=datetime.now())
                LineaDeTiempo.objects.create(titulo="Envio de mensaje a administrador",
                                            tiempo_de_actividad=datetime.now(),
                                            descripcion="Asunto: " +asunto,
                                            persona = persona,
                                            tipo_actividad = "info")
                return redirect('/privado')
            else:
                destinatario = request.POST['destinatario']
                persona = get_object_or_404(Persona,email=destinatario)
                usuario = persona.user
                Mensaje.objects.create(remitente=persona.email,
                                        destinatario=usuario,
                                        asunto=asunto,
                                        descripcion="Asunto: " +asunto,
                                        fecha_envio=datetime.datetime.now())
                return redirect('/privado')
        else:
            destinatario = request.POST['destinatario']
            persona = get_object_or_404(Persona,email=destinatario)
            usuario = persona.user
            Mensaje.objects.create(remitente=user.email,
                                    destinatario=usuario,
                                    asunto=asunto,
                                    descripcion="Asunto: " +asunto,
                                    fecha_envio=datetime.datetime.now())
            return redirect('/home')
    persona = ""
    usuario = "admin"
    destinatario_msj = "" #Se utiliza cuando se responde a un mensaje desde el mismo mensaje
    #Se utiliza cuando se responde a un mensaje desde el mismo mensaje
    if 'destinatario_msj' in request.session: 
        #usuario = "destinatario" 
        destinatario_msj = request.session['destinatario_msj']
        destinatario_msj = get_object_or_404(Mensaje,pk=destinatario_msj)
        request.session.pop('destinatario_msj')
        request.session.modified = True 

    if user.username != "admin":
        persona = persona = get_object_or_404(Persona, user = request.user)
        #MODIFICO LA LINEA DE ABAJO
        #if str(user.groups.get()) == "Empleado":         
        if request.session['rol_empleado']:
            usuario = "empleado"
        #MODIFICO LA LINEA DE ABAJO
        #elif str(user.groups.get()) == "Usuario":
        elif request.session['rol_cliente']:
            usuario = "cliente"
    mensajes = user.mensaje_set.all()
    leidos =[]
    noLeidos = []
    for msj in mensajes:
        if msj.leido:
            leidos.append(msj)
        else:
            noLeidos.append(msj)
    cantidad_mensajes = mensajes.count()
    cantidad_leidos = len(leidos)
    cantidad_no_leidos = len(noLeidos)
    return render_to_response("mensajes/enviar_mail.html",{
        'persona':persona,
        'usuario':usuario,
        'destinatario_msj':destinatario_msj, #Se utiliza cuando se responde a un mensaje desde el mismo mensaje
        'cantidad_mensajes':cantidad_mensajes,
        'cantidad_leidos':cantidad_leidos,
        'cantidad_no_leidos':cantidad_no_leidos,
        },context_instance = RequestContext(request))
#END NUEVO by chiqui

def leer_mensaje(request,id_mensaje):
    if request.method == 'POST':
        mensaje = get_object_or_404(Mensaje,pk=request.POST['id_mensaje'])
        request.session['destinatario_msj'] = mensaje.pk # quien nos mandó el mensaje, es nuestro mas probable destinatario
        request.session.modified = True 
        return redirect('enviar_mail')
    mensaje = get_object_or_404(Mensaje,pk=id_mensaje)
    if not mensaje.leido:
        mensaje.leido = True
    mensaje.save()
    user = mensaje.destinatario
    mensajes = user.mensaje_set.all()
    leidos =[]
    noLeidos = []
    for msj in mensajes:
        if msj.leido:
            leidos.append(msj)
        else:
            noLeidos.append(msj)
    cantidad_mensajes = mensajes.count()
    cantidad_leidos = len(leidos)
    cantidad_no_leidos = len(noLeidos)
    return render_to_response("mensajes/info_mensaje.html",{
        'mensaje':mensaje,
        'persona':user,
        'cantidad_mensajes':cantidad_mensajes,
        'cantidad_leidos':cantidad_leidos,
        'cantidad_no_leidos':cantidad_no_leidos,
        },context_instance = RequestContext(request))

def eliminar_mensaje(request,id_mensaje):
    #id_mensaje = request.GET['id_mensaje']
    mensaje = get_object_or_404(Mensaje,pk=id_mensaje)
    mensaje.delete()
    return redirect('casilla_mensaje')

from wkhtmltopdf.views import PDFTemplateView, PDFTemplateResponse

def clientes_pdf(request):
    clientes = Cliente.objects.all()
    hoy = datetime.now()
    context = {'cliente':clientes, 'hoy':hoy}
    return PDFTemplateResponse(request=request, 
        context=context, 
        template='pdf/listado_clientes.html', 
        filename='listado_clientes.pdf')







'''    
def clientes_pdf(request):
    empleados = Empleado.objects.all()
    context = {'empleados':empleados}
    return render_to_response("pdf/listado_clientes.html", context, context_instance = RequestContext(request))

'''
'''
from django.utils import timezone

date_created = models.DateTimeField(default=timezone.now)
def presupuesto_pdf(request, id_presupuesto):
    nro = get_object_or_404(Presupuesto, pk = id_presupuesto)
    
    sc = nro.serviciocontratado_set.all()
    valor=sc.count()
    valor = nro.calcularTotal()
    #hoy = models.DateTimeField(default=timezone.now)
    hoy = datetime.now()
    
    #hoy = datetime.date.today() + datetime.timedelta(days=1)
    return render_to_response("pdf/presupuesto_pdf.html",{'nro':nro, 'valor': valor, 'sc':sc, 'hoy':hoy },context_instance = RequestContext(request))
'''

def presupuesto_pdf(request, id_presupuesto):
    nro = get_object_or_404(Presupuesto, pk = id_presupuesto)
    sc = nro.serviciocontratado_set.all()
    hoy = datetime.now()
    context= {'nro':nro, 'sc':sc, 'hoy':hoy}
    return PDFTemplateResponse(request=request, 
        context=context, 
        template='pdf/presupuesto_pdf.html', 
        filename='presupuesto.pdf')



#NUEVO CHIQUI
def eliminar_contrato(request):
    buscador = BuscadorClienteForm(request.GET)
    if "cliente_1" in request.GET and request.GET["cliente_1"].isdigit():
        cliente = int(request.GET["cliente_1"])
        cliente = get_object_or_404(Cliente, pk = cliente)
        presupuestosConfirmados = cliente.get_confirmados_vigentes()#Presupuesto.objects.filter(cliente=cliente).filter(confirmado__nombre = 'Confirmado')    #Tomo los presupuestos CONFIRMADOS del cliente
    else:
        cliente = None
        presupuestosConfirmados = None
    if request.method=='POST':        
        presupuesto_eliminar = get_object_or_404(Presupuesto, pk = int(request.POST['id_presupuesto']))
        request.session['id_presupuesto'] = int(request.POST['id_presupuesto'])
        #return redirect('detalle_servicios', presupuesto_eliminar.pk)
        return redirect('detalle_servicios')
    return render_to_response('contratos/eliminar.html', { 
        'buscar':buscador, 
        'cliente': cliente,
        'presupuestos': presupuestosConfirmados
        }, context_instance=RequestContext(request))


def detalle_servicios(request):
    """Lista los servicios contratados de un presupuesto"""
    presupuesto = get_object_or_404(Presupuesto, id = request.session['id_presupuesto'] )  
    sc = presupuesto.serviciocontratado_set.all() #todos los SC de un presupuesto
    if "presupuesto_id" in request.POST:
        #nuevo_jueves
        print("heloooww")
        print request.POST['motivo']
        motivo = request.POST['motivo']
        presupuesto_eliminar = get_object_or_404(Presupuesto, pk = int(request.POST['presupuesto_id']))
        if motivo == '':
            presupuesto_eliminar.confirmado.dar_de_baja("Baja por eliminación.")
            request.notifications.success('Contrato eliminado.' )
            return HttpResponseRedirect('/home')
        else:
            presupuesto_eliminar.confirmado.dar_de_baja(motivo)
            request.notifications.success('Contrato eliminado.' )
            return HttpResponseRedirect('/home')
    else:
        if request.method == 'POST':
            return redirect('detalle_frecuencias_servicio', id_presupuesto = presupuesto.id, id_sc = request.POST['servicio_contratado'] )
    return render_to_response('contratos/detalle.html',
     {'presupuesto': presupuesto, 
     'servicios': sc}, context_instance=RequestContext(request))

def detalle_frecuencias_servicio(request,id_presupuesto, id_sc):
    """Lista las frecuencias de un servicio contratado"""
    presupuesto =  get_object_or_404(Presupuesto,pk=id_presupuesto)
    sc = get_object_or_404(ServicioContratado, pk = id_sc )  
    frecuencias = sc.frecuencia_set.all()
    servicios_contratados = presupuesto.serviciocontratado_set.all()
    if "presupuesto_id" in request.POST:
        #nuevo_jueves
        print "ole ole ole cada dia eliminanos mas"
        print request.POST['motivo']
        motivo = request.POST['motivo']
        presupuesto_eliminar = get_object_or_404(Presupuesto, pk = int(request.POST['presupuesto_id']))
        if motivo == '':
            presupuesto_eliminar.confirmado.dar_de_baja("Baja por eliminación.")
            request.notifications.success('Contrato eliminado.' )
            return HttpResponseRedirect('/home')
        else:
            presupuesto_eliminar.confirmado.dar_de_baja(motivo)
            request.notifications.success('Contrato eliminado.' )
            return HttpResponseRedirect('/home')
    else:
        if request.method == 'POST':
            if "Es_servicio" in request.POST :
                return redirect('detalle_frecuencias_servicio', id_presupuesto = presupuesto.id, id_sc = request.POST['servicio_contratado'])            
    return render_to_response('contratos/detalle.html',
     {'presupuesto': presupuesto, 
     'frecuencias': frecuencias,
     'servicios':servicios_contratados,
     'servicio_contratado':sc}, context_instance=RequestContext(request))

def frecuencias_servicio(request,id_presupuesto, id_sc):
    """Lista las frecuencias de un servicio contratado"""
    presupuesto =  get_object_or_404(Presupuesto,pk=id_presupuesto)
    sc = get_object_or_404(ServicioContratado, pk = id_sc )  
    frecuencias = sc.frecuencia_set.all()
    servicios_contratados = presupuesto.serviciocontratado_set.all()
    if request.method == 'POST':
        if "Es_servicio" in request.POST :
            return redirect('frecuencias_servicio', id_presupuesto = presupuesto.id, id_sc = request.POST['servicio_contratado'])
        else:
            sc_id = request.POST['servicio_contratado']
            frecuencia_id = request.POST['frecuencia_id']
            return redirect('crear_turno',sc_id, frecuencia_id)
    return render_to_response('turnos/servicios_contratados.html',
     {'frecuencias': frecuencias,
     'servicios':servicios_contratados,
     'servicio_contratado':sc}, context_instance=RequestContext(request))

#NUEVO CHIQUI DALEEEEE
def turnos_de_frecuencia(request,id_frecuencia):   
    frecuencia = get_object_or_404(Frecuencia, pk = id_frecuencia)
    turnos_frecuencia = frecuencia.turno_set.all()
    
    turno_empleado_dicc = {}    

    for turno in turnos_frecuencia:
        empleado = turno.empleado
        turno_empleado_dicc.update({turno.pk: [turno.hora_inicio, turno.hora_fin, empleado]})
    print("eoeoeoeoeo")
    od = collections.OrderedDict(sorted(turno_empleado_dicc.items()))
    return render_to_response('contratos/turnos_frecuencia.html', {
        'turno_empleado':od,
        }, context_instance=RequestContext(request))


#NUEVO
def listar_servicios(request, id_presupuesto):
    if request.method=='POST':
        presupuesto = get_object_or_404(Presupuesto, pk = id_presupuesto)
        presupuesto.confirmado.dar_de_baja('Baja por eliminación')

        return HttpResponseRedirect('/home')

    else:
        presupuesto = get_object_or_404(Presupuesto, pk = id_presupuesto)
        servicios = FrecuenciaFormset()
        contratados = ServicioContratadoFormset(queryset = presupuesto.serviciocontratado_set.all())
    return render_to_response('contratos/lista_servicios.html', {
        'presupuesto':presupuesto,
        'contratados':contratados,
        'servicios':servicios
        }, context_instance=RequestContext(request))



from datetime import datetime, date
from django.http import HttpResponse
import xlwt
from xlwt import Workbook



def exportar_excel(request):
    clientes = xlwt.Workbook(encoding='utf8')
    sheet = clientes.add_sheet('untitled')

    default_style = xlwt.Style.default_style
    datetime_style = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm')
    date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')

# Adding style for cell
    # Create Alignment
    alignment = xlwt.Alignment()
    # horz May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT,    
    # HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL,
    # HORZ_DISTRIBUTED
    alignment.horz = xlwt.Alignment.HORZ_LEFT
    # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED,
    # VERT_DISTRIBUTED
    alignment.vert = xlwt.Alignment.VERT_TOP
    style = xlwt.XFStyle() # Create Style
    style.alignment = alignment # Add Alignment to Style

    # write the header
    header = ['Nro Legajo', 'Nombre', 'Apellido', 'Especialidad']
    for hcol, hcol_data in enumerate(header): # [(0,'Header 1'), (1, 'Header 2'), (2,'Header 3'), (3,'Header 4')]
        sheet.write(0, hcol, hcol_data, style=xlwt.Style.default_style)

    lista =[]
    for empleado in Empleado.objects.all():
        lista.append( [empleado.nro_legajo,empleado.persona.nombre, empleado.persona.apellido,empleado.especialidad.nombre] )
    
    print(len(lista))
    for i in range(0,len(lista)):
        for j in range(0,len(lista[i])):
            print 'i %s, j %s' %(i,j)
            print lista[i][j]
            sheet.write(i+1,j,lista[i][j],style=xlwt.Style.default_style)

    # print lista
    # for row, rowdata in enumerate(lista, start=1):
    #     for col, val in enumerate(rowdata):
    #         if isinstance(val, datetime):
    #             style = datetime_style
    #         elif isinstance(val, date):
    #             style = date_style
    #         else:
    #             style = default_style
    #         print row 
    #         sheet.write(row, col, val, style=style)

    response = HttpResponse(mimetype='gestionServicios/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=ptro.xls'
    clientes.save(response)
    return response






'''

from django.http import HttpResponse
import xlwt
from django.utils.html import strip_tags

def exportar_excel(request):
    empleado = xlwt.Workbook(encoding='utf8')
    sheet = empleado.add_sheet('my_sheet')  

    # Adding style for cell
    # Create Alignment
    alignment = xlwt.Alignment()
    # horz May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT,    
    # HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL,
    # HORZ_DISTRIBUTED
    alignment.horz = xlwt.Alignment.HORZ_LEFT
    # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED,
    # VERT_DISTRIBUTED
    alignment.vert = xlwt.Alignment.VERT_TOP
    style = xlwt.XFStyle() # Create Style
    style.alignment = alignment # Add Alignment to Style

    #data = ['genius', 'super', 'gorgeous', 'awesomeness']
    #for row, row_data in enumerate(data, start=1): # start from row no.1
     #  for col, col_data in enumerate(row_data):
      #       sheet.write(row, col, col_data, style=xlwt.Style.default_style)
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=my_data.xls'
    empleado.save(response)
    return response



def export_to_excel(request):
    empleados = Empleado.objects.all()

    # your excel html format
    template_name = "excel/empleados_excel.html"
    
    response = render_to_response(template_name, {'empleados': empleados})
    
    # this is the output file
    filename = "model.csv"

    response['Content-Disposition'] = 'attachment; filename='+filename
    response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-16'
    return response



from django.http import HttpResponse
import xlwt

def exportar_excel(request):
  normal_style = xlwt.easyxf("""
     font:
         name Verdana
     """) 
  response = HttpResponse(mimetype='application/vnd.ms-excel')
  wb = xlwt.Workbook()
  ws0 = wb.add_sheet('Worksheet')
  ws0.write(0, 0, "something", normal_style)
  wb.save(response)
  return response



from django.http import HttpResponse, HttpResponseRedirect

from django.utils.html import strip_tags
from django.contrib import messages


def exportar_excel(request):

    queryset=Empleado.objects.all()

    wb = Workbook()
    ws0 = wb.add_sheet('0')
    col = 0
    field_names = []

    extras = ['']
    fields = []

    # write header row
    for field in fields:
        ws0.write(0, col, field)
        field_names.append(field)
        col = col + 1
    row = 1

    # Write data rows
    for obj in queryset:
        col = 0
        for field in field_names:
            
            ws0.write(row, col, str(strip_tags(val[-1])).strip())
            col = col + 1
        
        row = row + 1

    wb.save('/tmp/output.xls')
    response = HttpResponse(open('/tmp/output.xls','r').read(),
                  mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s.xls' % unicode('').replace('.', '_')
    return response


import csv
from django.http import HttpResponse

def exportar_excel(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response
'''

def ayuda_online(request):
    return render_to_response("ayuda_online.html",context_instance = RequestContext(request))

def empleados_por_fecha(request):
    dias_semana=['lu','ma','mi','ju','vi','sa','do']
    fecha = datetime.today().strftime("%Y/%m/%d")
    anio,mes = fecha.split('/',1)
    mes,dia = mes.split('/',1)       
    if request.method=='POST':
        fecha = request.POST['id_inicio']
        print "holi", fecha
        if fecha != '':
            dia,mes = fecha.split('/',1)
            mes,anio = mes.split('/',1)
    fecha=(int(anio),int(mes),int(dia),0,0,0,0,0,0)
    dia_semana = time.localtime(time.mktime(fecha))[6]
    fecha_a_comparar= date(int(anio),int(mes),int(dia))

    request.session['dia'] = dias_semana[dia_semana]
    print dias_semana[dia_semana], fecha
    frecuencias = (Frecuencia.objects.filter(dia=dias_semana[dia_semana]))
    empleados = []
    for frecuencia in frecuencias:
        if frecuencia.servicio_contratado.fin > fecha_a_comparar:
            turnos = frecuencia.turno_set.all()
            for turno in turnos:
                if turno.fin == None:
                    empleados.append(turno.empleado)
    return render_to_response("listados/empleados_por_fecha.html",{'empleados':empleados},context_instance = RequestContext(request))

def turnos_empleados_por_fecha(request,id_empleado):
    empleado = get_object_or_404(Empleado,pk=id_empleado)
    dia = request.session['dia']
    turnos = empleado.turno_set.all()
    turnos_filtrados=[]
    for turno in turnos:
        if turno.frecuencia.dia == dia and turno.fin == None:
            turnos_filtrados.append(turno)
    print turnos_filtrados
    # frecuencias = (Frecuencia.objects.filter(dia=dia))
    # turnos = []
    # for frecuencia in frecuencias:
    #     turnos.append(frecuencia.turno_set.all())
    return render_to_response("listados/turnos_empleado.html",{'turnos_frecuencia':turnos_filtrados},context_instance = RequestContext(request))


def parte_diario(request):
    dias_semana=['lu','ma','mi','ju','vi','sa','do']
    fecha = datetime.today().strftime("%Y/%m/%d")
    print 'fecha de tipo',type(fecha)
    anio,mes = fecha.split('/',1)
    mes,dia = mes.split('/',1)       
    if request.method=='POST':
        fecha = request.POST['id_inicio']
        if fecha != '':
            dia,mes = fecha.split('/',1)
            mes,anio = mes.split('/',1)
    fecha=(int(anio),int(mes),int(dia),0,0,0,0,0,0)
    dia_semana = time.localtime(time.mktime(fecha))[6]
    fecha_a_comparar= date(int(anio),int(mes),int(dia))
    fecha_a_comparar1= datetime(int(anio),int(mes),int(dia))
    dia_aux = dia
    
    #frecuencias = (Frecuencia.objects.filter(dia=dias_semana[dia_semana]))
    dia = dias_semana[dia_semana]
    print fecha, dia

    lista = []
    confirmados = Presupuesto.objects.filter(confirmado__nombre = 'Confirmado')
      
    for c in confirmados:
        print "zzzzzzzzzz",c.contrato.baja
        if c.contrato.baja is None:
            print "compararrrr"
            print c.contrato.inicio <= fecha_a_comparar1
            if c.contrato.inicio <= fecha_a_comparar1:
                print c.contrato.inicio, "aaaaaaaaaaaaaaaaaaaaaa", fecha_a_comparar1
                aux = c.serviciocontratado_set.all()
                for a in aux:
                    print a.fin,"cccccccccccccccc", fecha_a_comparar
                    if a.fin > fecha_a_comparar:
                        print a.fin, "bbbbbbbbbbbbbbb", fecha_a_comparar
                        var = a.frecuencia_set.all()
                        for v in var:
                            print v.dia, "vs", dia    
                            if v.dia == dia:
                                t = v.turno_set.all()
                                for z in t:
                                    #if z is not None and z.frecuencia.dia==dia:
                                    if z is not None and c not in lista:                       
                                        lista.append(c)
                                        
    print "la listen ", lista
    request.session['control_parte_diario'] = {'dia':dia, 'fecha': {'dia':dia_aux,'mes':mes,'anio':anio}}
    presupuestos, datos_cabeceras = obtener_diccionarios(lista, fecha_a_comparar, dia)   
    request.session['datos_cabeceras'] = datos_cabeceras
    request.session['presup_parte_diario'] = presupuestos
    request.session['fecha_a_comparar'] = str(dia_aux)+"/"+str(mes)+"/"+str(anio)
    request.session.modified = True

    return render_to_response("listados/p_diario.html",{'presupuestos':presupuestos,'cabeceras':datos_cabeceras,'fecha': str(dia_aux)+"/"+str(mes)+"/"+str(anio) } ,context_instance = RequestContext(request))



def parte_diario_pdf(request):
    dia_semana = request.session['control_parte_diario']['dia']
    dia_num = request.session['control_parte_diario']['fecha']['dia']
    mes = request.session['control_parte_diario']['fecha']['mes']
    anio = request.session['control_parte_diario']['fecha']['anio']
    fecha_a_comparar= date(int(anio),int(mes),int(dia_num))    
    datos_cabeceras = request.session['datos_cabeceras'] 
    presupuestos = request.session['presup_parte_diario']
    hoy = datetime.now()
    context= {'presupuestos':presupuestos, 'cabeceras':datos_cabeceras,'fecha': str(dia_num)+"/"+str(mes)+"/"+str(anio), 'hoy': hoy }
    return PDFTemplateResponse(request=request, 
        context=context, 
        template='listados/p_diario_diccionario.html', 
        filename='sin_nombre.pdf')




def obtener_diccionarios(lista,fecha_a_comparar, dia_semana):
    presupuestos = {}
    datos_cabeceras = {}
    for p in lista:
        datos_cabeceras.update({p.pk: "Presupuesto Nro.:"+str(p.pk)+"/ Cliente: "+p.cliente.persona.apellido+" "+p.cliente.persona.nombre+"/ Domicilio Servicio:"+p.domicilio_servicio })
        presupuestos.update({p.pk:{}})
        sc = p.serviciocontratado_set.all()
        for s in sc:
            presupuestos[p.pk].update({s.tipo_servicio.nombre:{}})
            print s.tipo_servicio.nombre
            if s.fin > fecha_a_comparar:
                frecs = s.frecuencia_set.all()
                for f in frecs:
                    print f.pk, f.dia, f.hora_inicio, f.hora_fin
                    if f.dia == dia_semana:
                        turnos = f.turno_set.all()
                        for t in turnos:
                            print t.hora_inicio,t.hora_fin , t.empleado.persona.nombre
                            if t.fin == None:
                                presupuestos[p.pk][s.tipo_servicio.nombre].update( { t.pk:[ t.empleado.persona.nombre+' '+t.empleado.persona.apellido, str(t.hora_inicio),str(t.hora_fin)] } )
    #Eliminar ts que no tienen turnos en ese dia
    a_eliminar = {}
    for k,v in presupuestos.iteritems():
        lista_serv = []
        for ks,vs in v.iteritems():
            if not v[ks]:
                print 'pr: %s este servicio no tiene turnos: %s' % (k,ks)
                lista_serv.append(ks)
                a_eliminar.update({k:lista_serv})
                

    print "presup %s \n" % (presupuestos)
    print " "
    print "a eliminar %s \n" % (a_eliminar)
    for k,v in a_eliminar.iteritems():
        print 'eliminando %s de presupuesto %s' % (v,k)
        if presupuestos.has_key(k):
            for s in v: # s es un servicio que esta en la lista de servicios a eliminar v
                presupuestos[k].pop(s)
    print "presupuesto %s " % (presupuesto)
    return presupuestos,datos_cabeceras


def turnos_empleado(request):
    #fecha_a_comparar = datetime.today()
    empleado = Empleado.objects.get(persona__user=request.user)
    turnos_empleado = empleado.turno_set.all()
    dias_semana=['lu','ma','mi','ju','vi','sa','do']
    fecha = datetime.today().strftime("%Y/%m/%d")
    anio,mes = fecha.split('/',1)
    mes,dia = mes.split('/',1) 
    if request.method == 'POST':
        fecha = request.POST['id_inicio']
        if fecha != '':
            dia,mes = fecha.split('/',1)
            mes,anio = mes.split('/',1)
            #fecha_a_comparar = date(int(anio), int(mes), int(dia))
    fecha_a_comparar = date(int(anio), int(mes), int(dia))
    fecha_a_comparar1 = datetime(int(anio), int(mes), int(dia))
    fecha=(int(anio),int(mes),int(dia),0,0,0,0,0,0)
    dia_semana = time.localtime(time.mktime(fecha))[6]
    turnos = []
    for turno in turnos_empleado:
        if turno.fin == None:
            print turno.frecuencia.servicio_contratado.fin, "contra", fecha_a_comparar 
            if turno.frecuencia.servicio_contratado.fin >= fecha_a_comparar and turno.frecuencia.servicio_contratado.presupuesto.contrato.inicio <= fecha_a_comparar1 and turno.frecuencia.dia == dias_semana[dia_semana]:
                turnos.append(turno)
    return render_to_response("empleados/consulta_turno.html",{'turnos':turnos},context_instance = RequestContext(request))

def turnos_empleado_pdf(request):
    empleado = Empleado.objects.get(persona__user=request.user)
    turnos_empleado = empleado.turno_set.all()
    dias_semana=['lu','ma','mi','ju','vi','sa','do']
    fecha = datetime.today().strftime("%Y/%m/%d")
    anio,mes = fecha.split('/',1)
    mes,dia = mes.split('/',1) 
    if request.method == 'POST':
        fecha = request.POST['id_inicio']
        if fecha != '':
            dia,mes = fecha.split('/',1)
            mes,anio = mes.split('/',1)
            #fecha_a_comparar = date(int(anio), int(mes), int(dia))
    fecha_a_comparar = date(int(anio), int(mes), int(dia))
    fecha_a_comparar1 = datetime(int(anio), int(mes), int(dia))
    fecha=(int(anio),int(mes),int(dia),0,0,0,0,0,0)
    dia_semana = time.localtime(time.mktime(fecha))[6]
    turnos = []
    for turno in turnos_empleado:
        if turno.fin == None:
            print turno.frecuencia.servicio_contratado.fin, "contra", fecha_a_comparar 
            if turno.frecuencia.servicio_contratado.fin >= fecha_a_comparar and turno.frecuencia.servicio_contratado.presupuesto.contrato.inicio <= fecha_a_comparar1 and turno.frecuencia.dia == dias_semana[dia_semana]:
                turnos.append(turno)

    context = {'turnos':turnos}

    return PDFTemplateResponse(request=request, 
        context=context, 
        template='listados/turnos_empleado_pdf.html', 
        filename='sin_nombre.pdf')