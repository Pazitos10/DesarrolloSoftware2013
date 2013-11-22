from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404,redirect
from django.template import RequestContext
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory

from gestionServicios.models import *
from gestionServicios.forms import *

from django.views.generic.edit import FormView
from django.views.generic.list import ListView

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
        formulario = TipoDeServicioAltaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/')
    else:
        formulario=TipoDeServicioAltaForm()
    return render_to_response('tiposDeServicio/alta.html', {'formulario': formulario}, context_instance=RequestContext(request))

#NUEVO
def modificar_tipo_de_servicio(request):
    if request.method=='POST':
        tipo_de_servicio = str(request.REQUEST["tipoDeServicio_1"])
        tipo_de_servicio = get_object_or_404(TipoDeServicio, pk = tipo_de_servicio)
        formulario = TipoDeServicioAltaForm(request.POST, instance=tipo_de_servicio)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/')
    else:
        if "tipoDeServicio_1" in request.REQUEST:
            tipo_de_servicio = str(request.REQUEST["tipoDeServicio_1"])
            tipo_de_servicio = get_object_or_404(TipoDeServicio, pk = tipo_de_servicio)
            buscador = BuscadorTipoDeServicioForm(request.REQUEST)
            formulario = TipoDeServicioAltaForm(instance = tipo_de_servicio)
        else:
            buscador = BuscadorTipoDeServicioForm()
            formulario = TipoDeServicioAltaForm()
    return render_to_response('tiposDeServicio/modificar.html', {'formulario': formulario, 'buscar':buscador}, context_instance=RequestContext(request))
#END NUEVO

def baja_tipo_de_servicio(request):
    if request.method=='POST':
        tipo_de_servicio = str(request.REQUEST["tipoDeServicio_1"])
        tipo_de_servicio = get_object_or_404(TipoDeServicio, pk = tipo_de_servicio)
        formulario = TipoDeServicioBajaForm(request.POST, instance=tipo_de_servicio)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/')
    else:
        if "tipoDeServicio_1" in request.REQUEST:
            tipo_de_servicio = str(request.REQUEST["tipoDeServicio_1"])# SAQUE EL CAST,NOSE PORQUE NO FUNCIONABA
            tipo_de_servicio = get_object_or_404(TipoDeServicio, pk = tipo_de_servicio)
            buscador = BuscadorTipoDeServicioForm(request.REQUEST)
            formulario = TipoDeServicioBajaForm(instance = tipo_de_servicio)
        else:
            buscador = BuscadorTipoDeServicioForm()
            formulario = ""
    return render_to_response('tiposDeServicio/baja.html', {'formulario': formulario, 'buscar':buscador}, context_instance=RequestContext(request))


def alta_cliente(request):
    if request.method=='POST':
        formulario = ClienteAltaForm(request.POST)
        if formulario.is_valid():

            #from ipdb import set_trace; set_trace()
            
            #TODO TRATAR LOS CAMPOS QUE NO SON OBLIGATORIOS
            tipo_documento = formulario.cleaned_data['tipo_documento']
            nro_documento = formulario.cleaned_data['nro_documento']
            apellido = formulario.cleaned_data['apellido']
            nombre = formulario.cleaned_data['nombre'] 
            domicilio = formulario.cleaned_data['domicilio']
            telefono = formulario.cleaned_data['telefono']
            #TODO HACER VALIDACIONES DEL EMAIL Y OTROS CAMPOS SI FUERA NECESARIO
            email = formulario.cleaned_data['email']
            
            persona = Persona()
            persona.tipo_documento = tipo_documento
            persona.nro_documento = nro_documento
            persona.apellido = apellido
            persona.nombre = nombre
            persona.domicilio = domicilio
            persona.telefono = telefono
            persona.email = email
            persona.save()

            cliente = Cliente()
            cliente.persona = persona
            cliente.save()

            return HttpResponseRedirect('/')
    else:
        formulario=ClienteAltaForm()
    return render_to_response('clientes/alta.html', {'formulario': formulario}, context_instance=RequestContext(request))

#NUEVO
def modificar_cliente(request):
    if request.method=='POST':
        cliente = int(request.REQUEST["persona_1"])
        cliente = get_object_or_404(Persona, pk = cliente)
        formulario = ClienteModificarForm(request.POST, instance = cliente)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/')
    else:
        if "persona_1" in request.REQUEST:
            cliente = int(request.REQUEST["persona_1"])
            cliente = get_object_or_404(Persona, pk = cliente)
            buscador = BuscadorClienteForm(request.REQUEST)
            formulario = ClienteModificarForm(instance = cliente)
        else:
            buscador = BuscadorClienteForm()
            formulario = ClienteModificarForm()
    return render_to_response('clientes/modificar.html', {'formulario': formulario, 'buscar':buscador}, context_instance=RequestContext(request))

#END NUEVO

#NUEVO
def alta_empleado(request):
    if request.method=='POST':
        formulario = EmpleadoAltaForm(request.POST)
        if formulario.is_valid():
            #TODO TRATAR LOS CAMPOS QUE NO SON OBLIGATORIOS
            tipo_documento = formulario.cleaned_data['tipo_documento']
            nro_documento = formulario.cleaned_data['nro_documento']
            apellido = formulario.cleaned_data['apellido']
            nombre = formulario.cleaned_data['nombre'] 
            domicilio = formulario.cleaned_data['domicilio']
            telefono = formulario.cleaned_data['telefono']
            #TODO HACER VALIDACIONES DEL EMAIL Y OTROS CAMPOS SI FUERA NECESARIO
            email = formulario.cleaned_data['email']
            cuil = formulario.cleaned_data['cuil']
            fecha_nacimiento = formulario.cleaned_data['fecha_nacimiento']
            tipo_de_servicio = formulario.cleaned_data['tipo_de_servicio'] #devuelve objeto
            
            persona = Persona()
            persona.tipo_documento = tipo_documento
            persona.nro_documento = nro_documento
            persona.apellido = apellido
            persona.nombre = nombre
            persona.domicilio = domicilio
            persona.telefono = telefono
            persona.email = email
            persona.save()

            empleado = Empleado()
            empleado.CUIL = cuil
            empleado.nacimiento = fecha_nacimiento
            empleado.especialidad = tipo_de_servicio
            empleado.persona = persona
            empleado.save()
            #tipo_de_servicio.empleado_set.add(empleado)
            
            return HttpResponseRedirect('/')
    else:
        formulario=EmpleadoAltaForm()
    return render_to_response('empleados/alta.html', {'formulario': formulario}, context_instance=RequestContext(request))

#END NUEVO

#NUEVO
def modificar_empleado(request):
    if request.method=='POST':
        empleado = int(request.REQUEST["persona_1"])
        empleado = get_object_or_404(Persona, pk = empleado)
        formulario = EmpleadoModificarForm(request.POST, instance = empleado)
        if formulario.is_valid():
            e = empleado.empleado_set.get()
            e.CUIL = formulario.cleaned_data['cuil']
            e.nacimiento = formulario.cleaned_data['fecha_nacimiento']
            e.especialidad = formulario.cleaned_data['tipo_de_servicio']
            e.save()
            formulario.save()
            return HttpResponseRedirect('/')
    else:
        if "persona_1" in request.REQUEST:
            empleado = int(request.REQUEST["persona_1"])
            empleado = get_object_or_404(Persona, pk = empleado)
            buscador = BuscadorEmpleadoForm(request.REQUEST)
            formulario = EmpleadoModificarForm(instance=empleado)
            formulario.fields['cuil'].initial = empleado.empleado_set.get().CUIL
            formulario.fields['fecha_nacimiento'].initial = empleado.empleado_set.get().nacimiento
            formulario.fields['tipo_de_servicio'].initial = empleado.empleado_set.get().especialidad
        else:
            buscador = BuscadorEmpleadoForm()
            formulario = EmpleadoModificarForm()
    return render_to_response('empleados/modificar.html', {'formulario': formulario, 'buscar':buscador}, context_instance=RequestContext(request))

#END NUEVO



def presupuesto(request):
    buscador = BuscadorClienteForm(request.GET)
    if "cliente_1" in request.GET and request.GET["cliente_1"].isdigit():
        cliente = int(request.GET["cliente_1"])
        cliente = get_object_or_404(Cliente, pk = cliente)
    else:
        cliente = None
    if request.method=='POST':
        formulario = PresupuestoForm(request.POST)
        if formulario.is_valid():
            presupuesto = formulario.save()
            return redirect('servicios_agregar', id_presupuesto = presupuesto.id)
        print formulario.is_valid() 
    else:
        formulario = PresupuestoForm(initial = {"cliente": cliente})
    return render_to_response('presupuestos/alta.html', {
        'formulario': formulario, 
        'buscar':buscador, 
        'cliente': cliente
        }, context_instance=RequestContext(request))


def agregarTS(request, id_presupuesto):
    presupuesto = get_object_or_404(Presupuesto, pk = id_presupuesto)
    buscar = BuscadorTipoDeServicioForm()
    servicios = FrecuenciaFormset()
    if request.method == 'POST':
        tipo_de_servicio = str(request.REQUEST["tipoDeServicio_1"])
        tipo_de_servicio = get_object_or_404(TipoDeServicio, pk = tipo_de_servicio)
        formset = servicios(request.POST)
        buscar = BuscadorTipoDeServicioForm(request.POST)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/')
    elif "tipoDeServicio_1" in request.GET:
        tipo_de_servicio = get_object_or_404(TipoDeServicio, 
                pk = request.GET["tipoDeServicio_1"])
        presupuesto.contratar_servicio(tipo_de_servicio)
    servicios_contratados = ServicioContratadoFormset(queryset = presupuesto.serviciocontratado_set.all())
    return render_to_response('presupuestos/datosTS.html', {'servicios':servicios,
        'presupuesto': presupuesto,
        'buscar':buscar,
        'contratados': servicios_contratados }, context_instance=RequestContext(request))
    
def quitarSC(request, id_presupuesto, id_serviciocontratado):
    presupuesto = get_object_or_404(Presupuesto, pk = id_presupuesto)
    presupuesto.serviciocontratado_set.get(pk = id_serviciocontratado).delete()
    return redirect('servicios_agregar', id_presupuesto = presupuesto.id)

def frecuencias_de_servicio(request, id_serviciocontratado):
    serviciocontratado = get_object_or_404(ServicioContratado, pk = id_serviciocontratado)
    return render_to_response('presupuestos/frecuencias.html', { 
        "contratado": serviciocontratado
        }, context_instance=RequestContext(request))

def agregar_frecuencia(request, id_serviciocontratado):
    serviciocontratado = get_object_or_404(ServicioContratado, pk = id_serviciocontratado)
    if request.method == "POST":
        frecuencia = FrecuenciasForm(request.POST)
        if frecuencia.is_valid():
            frecuencia.save()
        print(frecuencia.errors)
    return HttpResponse("ok")

def listado_presupuestos(request):
    return render_to_response('presupuestos/listado.html', {'presupuestos':Presupuesto.objects.all()},context_instance=RequestContext(request))


def alta_turnos(request):
    buscador = BuscadorClienteForm(request.GET)
    if "cliente_1" in request.GET and request.GET["cliente_1"].isdigit():
        cliente = int(request.GET["cliente_1"])
        cliente = get_object_or_404(Cliente, pk = cliente)
        presupuestos = cliente.presupuesto_set.all()
    else:
        cliente = None
        presupuestos = None
    if request.method=='POST':
        formulario = PresupuestoForm(request.POST)
        if formulario.is_valid():
            presupuesto = formulario.save()
            return HttpResponseRedirect('agregar_servicios')
        print formulario.is_valid() 
    else:
        formulario = PresupuestoForm(initial = {"cliente": cliente})
    return render_to_response('turnos/alta.html', {
        'formulario': formulario, 
        'buscar':buscador, 
        'cliente': cliente,
        'presupuestos': presupuestos
        }, context_instance=RequestContext(request))


def confirmar_presupuesto(request):
    buscador = BuscadorClienteForm(request.GET)
    if "cliente_1" in request.GET and request.GET["cliente_1"].isdigit():
        cliente = int(request.GET["cliente_1"])
        cliente = get_object_or_404(Cliente, pk = cliente)
        presupuestos = Presupuesto.objects.filter(cliente=cliente)         #Tomo TODOS los presupuestos del cliente
        presupuestos = presupuestos.filter(valorizado__nombre = 'Valorizado')       #Tomo los presupuestos VALORIZADOS del cliente
    else:
        cliente = None
        presupuestos = None
    if request.method=='POST':
        formulario = PresupuestoForm(request.POST)
        if formulario.is_valid():
            presupuesto = formulario.save()
            return HttpResponseRedirect('agregar_servicios')
        print formulario.is_valid() 
    else:
        formulario = PresupuestoForm(initial = {"cliente": cliente})
    return render_to_response('presupuestos/confirmar.html', {
        'formulario': formulario, 
        'buscar':buscador, 
        'cliente': cliente,
        'presupuestos': presupuestos
            }, context_instance=RequestContext(request))


def valorizar_presupuesto(request):
    buscador = BuscadorClienteForm(request.GET)
    if "cliente_1" in request.GET and request.GET["cliente_1"].isdigit():
        cliente = int(request.GET["cliente_1"])
        cliente = get_object_or_404(Cliente, pk = cliente)
        presupuestos = cliente.presupuesto_set.all()
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


def servicios_contratados(request):
    sc = get_object_or_404(Presupuesto, id = request.session['id_presupuesto']).serviciocontratado_set.all() #todos los SC de un presupuesto
    if request.method == 'POST':
        serv_contratado =get_object_or_404(ServicioContratado, id = int(request.POST['servicio_contratado']))#un SC del presupuesto
        serv_contratado.metros_cuad = float(request.POST['cantidadM2'])
        serv_contratado.calcularImporte(serv_contratado.tipo_servicio.valorM2)
    return render_to_response('presupuestos/servicios_contratados.html', { 
                                                                        'servicios': sc,
                                                                        }, context_instance=RequestContext(request))





