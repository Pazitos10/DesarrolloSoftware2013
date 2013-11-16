from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,HttpResponseRedirect, get_object_or_404
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
            cliente.save()
            persona.cliente_set.add(cliente)

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
            tipo_de_servicio.empleado_set.add(empleado)
            empleado.save()
            persona.empleado_set.add(empleado)
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


class AsignarPersonalView(ListView):
    template_name = 'turnos/alta.html'
    model = Presupuesto
    ''' buscar cliente , mostrar presupuestos, selecciona uno, 
        muestra tipos de servicio, selecciona uno , despliega frecuencias, 
        elige una,busca un empleado disponible,escoje a uno,
        crea un turno dentro de esa frecuencia
    '''
    def get_queryset(self):
        return super(AsignarPersonalView,self).get_queryset()

    '''def get(self, request):
        buscador = BuscadorPersonaForm()
        return HttpResponse() '''

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
            return HttpResponseRedirect('agregar_servicios')
        print formulario.is_valid() 
    else:
        formulario = PresupuestoForm(initial = {"cliente": cliente})
    return render_to_response('presupuestos/alta.html', {
        'formulario': formulario, 
        'buscar':buscador, 
        'cliente': cliente
        }, context_instance=RequestContext(request))


def agregarTS(request):
    servicios = datosTSFormset() 
    if request.method == 'POST':
        tipo_de_servicio = str(request.REQUEST["tipoDeServicio_1"])
        tipo_de_servicio = get_object_or_404(TipoDeServicio, pk = tipo_de_servicio)
        formset = servicios(request.POST)
        buscar = BuscadorTipoDeServicioForm(request.POST)
        if formset.is_valid():
            #instance = formset.save()
            return HttpResponseRedirect('/')
    else:
        if "tipoDeServicio_1" in request.REQUEST:
            tipo_de_servicio = str(request.REQUEST["tipoDeServicio_1"])
            tipo_de_servicio = get_object_or_404(TipoDeServicio, pk = tipo_de_servicio)
            buscar = BuscadorTipoDeServicioForm(request.REQUEST)
            formset = ''
        else:        
            formset = datosTSFormset()
            buscar = BuscadorTipoDeServicioForm()
            tipo_de_servicio = ''

    return render_to_response('presupuestos/datosTS.html', {'servicios':servicios,'buscar':buscar,'tipo_de_servicio':tipo_de_servicio}, context_instance=RequestContext(request))


    '''
    def agregarTS(request):
    if request.method == 'POST':
        tipo_de_servicio = str(request.REQUEST["tipoDeServicio_1"])
        tipo_de_servicio = get_object_or_404(TipoDeServicio, pk = tipo_de_servicio)
        datosTSForm = DatosTSForm(request.POST,instance=tipo_de_servicio)
        if datosTSForm.is_valid():
            datosTSForm.save()
            return HttpResponseRedirect('/')
    else:
        if "tipoDeServicio_1" in request.REQUEST:
            tipo_de_servicio = str(request.REQUEST["tipoDeServicio_1"])
            tipo_de_servicio = get_object_or_404(TipoDeServicio, pk = tipo_de_servicio)
            buscador = BuscadorTipoDeServicioForm(request.REQUEST)
            datosTSForm = DatosTSForm(request.POST,instance=tipo_de_servicio)
        else:
            datosTSForm = DatosTSForm()
            buscarTS= BuscadorTipoDeServicioForm() 
    return render_to_response ('presupuesto/datosTS.html',{'datosTSForm':datosTSForm,'buscarTS':buscarTS,'tipo_de_servicio':tipo_de_servicio },context_instance=RequestContext(request))
    '''
    

def listado_presupuestos(request):
    return render_to_response('presupuestos/listado.html', {'presupuestos':Presupuesto.objects.all()},context_instance=RequestContext(request))
