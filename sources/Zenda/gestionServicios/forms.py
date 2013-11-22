from gestionServicios.models import *
from django import forms
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django.forms.formsets import BaseFormSet

from gestionServicios.lookups import *
from selectable import forms as sforms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class BuscadorClienteForm(forms.Form):
    cliente = sforms.AutoCompleteSelectField(
        lookup_class = ClienteLookup,
        label = 'Buscar:',
        required=False, allow_new = False)

    def __init__(self, *args, **kwargs):
        super(BuscadorClienteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'get'
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-lg-1'
        self.helper.field_class='col-lg-6'

class BuscadorEmpleadoForm(forms.Form):
    persona = sforms.AutoCompleteSelectField(
        lookup_class = EmpleadoLookup,
        label = 'Buscar:',
        required=False, allow_new = False)

    def __init__(self, *args, **kwargs):
        super(BuscadorEmpleadoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'get'
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-lg-1'
        self.helper.field_class='col-lg-6'




#NUEVO
class BuscadorTipoDeServicioForm(forms.Form):
    tipoDeServicio = sforms.AutoCompleteSelectField(
        lookup_class = TipoDeServicioLookup,
        label = 'Buscar:',
        required=False, allow_new = True)

    def __init__(self, *args, **kwargs):
        super(BuscadorTipoDeServicioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'get'
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-lg-1'
        self.helper.field_class='col-lg-6'
        
#END NUEVO

class PresupuestoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PresupuestoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'formulario'
        self.helper.form_method = 'post'
        self.helper.form_class='form-horizontal'
        self.helper.add_input(Submit('submit', 'Confirmar'))
        self.helper.label_class='col-lg-2'
        self.helper.field_class='col-lg-6'

    class Meta:
        model = Presupuesto
        exclude = ['contrato','servicios_contratados']
        widgets = {
            "cliente": forms.HiddenInput()
        }

class DatosTSForm(forms.ModelForm ):
    class Meta:
        model = TipoDeServicio
        exclude = ['productos','codigo_servicio','nombre','creacion','modificacion','baja']


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona


class TipoDeServicioAltaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TipoDeServicioAltaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'formulario'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Confirmar'))
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-lg-1'
        self.helper.field_class='col-lg-6'
        
    class Meta:
        model = TipoDeServicio
        exclude = ['alta', 'baja']

class TipoDeServicioBajaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TipoDeServicioBajaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'formulario'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Confirmar'))

    class Meta:
        model = TipoDeServicio
        exclude = ['productos','codigo_servicio','nombre','creacion','modificacion','valorM2']

class DatosTSForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DatosTSForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'formulario'
        self.helper.form_method = 'post'

    class Meta:
        model = TipoDeServicio
        exclude = ['productos', 'codigo_servicio', 'creacion','modificacion','baja']
    
    def clean(self):
        return self.cleaned_data


class FrecuenciasForm(forms.ModelForm):
    class Meta: 
        model = Frecuencia
        widgets = {
            "servicio_contratado": forms.HiddenInput()
        } 

FrecuenciaFormset = formset_factory(FrecuenciasForm)        


class ServicioContratadoForm(forms.ModelForm):
    class Meta:
        model = ServicioContratado
        widgets = {
            "tipo_servicio": forms.TextInput()
        }
        fields = ("tipo_servicio", "fin")

    def __init__(self, *largs, **kwargs):
        super(ServicioContratadoForm, self).__init__(*largs, **kwargs)
        self.fields["fin"].widget.attrs["class"] = "datepicker"

class ServicioContratadoBaseFormset(BaseFormSet):
     def clean(self):
        return super(ServicioContratadoBaseFormset, self).clean()

ServicioContratadoFormset = modelformset_factory(ServicioContratado,
    form=ServicioContratadoForm,
    #formset=ServicioContratadoBaseFormset,
    extra=0)

class ClienteAltaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ClienteAltaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'formulario'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Confirmar'))
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-lg-2'
        self.helper.field_class='col-lg-6'

    class Meta:
        model = Persona
        exclude = ['baja', 'motivo']
    
    def clean(self):
        return self.cleaned_data

class ClienteModificarForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ClienteModificarForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'formulario'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Confirmar'))
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-lg-1'
        self.helper.field_class='col-lg-6'

    class Meta:
        model = Persona
        exclude = ['tipo_documento', 'nro_documento', 'baja', 'motivo']
    
    def clean(self):
        return self.cleaned_data

class EmpleadoAltaForm(forms.ModelForm):
    cuil = forms.IntegerField()
    fecha_nacimiento = forms.DateTimeField()
    tipo_de_servicio = forms.ModelChoiceField(queryset = TipoDeServicio.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(EmpleadoAltaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'formulario'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Confirmar'))
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-lg-2'
        self.helper.field_class='col-lg-6'

    class Meta:
        model = Persona
        exclude = ['baja', 'motivo']

class EmpleadoModificarForm(forms.ModelForm):
    cuil = forms.IntegerField()
    fecha_nacimiento = forms.DateTimeField()
    tipo_de_servicio = forms.ModelChoiceField(queryset = TipoDeServicio.objects.all())

    def __init__(self, *args, **kwargs):
        super(EmpleadoModificarForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'formulario'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Confirmar'))
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-lg-2'
        self.helper.field_class='col-lg-6'

    class Meta:
        model = Persona
        exclude = ['tipo_documento', 'nro_documento', 'baja', 'motivo']


class TurnosForm(forms.ModelForm):
    class Meta:
        model = Turno
        
