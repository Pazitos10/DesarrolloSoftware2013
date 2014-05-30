from gestionServicios.models import *
from django import forms
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django.forms.formsets import BaseFormSet

from gestionServicios.lookups import *
from selectable import forms as sforms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django.contrib.auth.models import User

from django.contrib.auth.models import Group 
from django.forms import ModelForm

from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field


class BuscadorClienteForm(forms.Form):
    cliente = sforms.AutoCompleteSelectField(
        lookup_class = ClienteLookup,
        label = 'Buscar:',
        required=False, allow_new = False)
    cliente.widget.attrs['placeholder'] = "Ingrese nombre y/o apellido"

    def __init__(self, *args, **kwargs):
        super(BuscadorClienteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-lg-1'
        self.helper.field_class='col-lg-6'
        self.helper.form_method = 'get'

        #self.helper.layout = FormActions(Submit('save_changes', 'Save changes', css_class="btn-primary")))

class BuscadorPersonaForm(forms.Form):
    persona = sforms.AutoCompleteSelectField(
        lookup_class = PersonaLookup,
        label = 'Buscar:',
        required=False, allow_new = False)
    persona.widget.attrs['placeholder'] = "Ingrese nombre y/o apellido"

    def __init__(self, *args, **kwargs):
        super(BuscadorPersonaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-lg-1'
        self.helper.field_class='col-lg-6'
        self.helper.form_method = 'get'


class BuscadorEmpleadoForm(forms.Form):
    empleado = sforms.AutoCompleteSelectField(
        lookup_class = EmpleadoLookup,
        label = 'Buscar:',
        required=True, allow_new = True)
    empleado.widget.attrs['placeholder'] = "Ingrese nombre y/o apellido"

    def __init__(self, *args, **kwargs):
        super(BuscadorEmpleadoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'get'
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-lg-1'
        self.helper.field_class='col-lg-6'
        
class BuscadorTipoDeServicioForm(forms.Form):
    tipoDeServicio = sforms.AutoCompleteSelectField(
        lookup_class = TipoDeServicioLookup,
        label = 'Buscar:',
        required=False, allow_new = True)
    tipoDeServicio.widget.attrs['placeholder'] = "Ingrese nombre de servicio"

    def __init__(self, *args, **kwargs):
        super(BuscadorTipoDeServicioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'get'
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-lg-1'
        self.helper.field_class='col-lg-6'

class PresupuestoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PresupuestoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'formulario'
        self.helper.form_method = 'post'
        self.helper.form_class='form-horizontal'
        self.helper.add_input(Submit('submit', 'Crear'))
        self.helper.label_class='col-lg-2'
        self.helper.field_class='col-lg-6'

    class Meta:
        model = Presupuesto
        exclude = ['contrato']
        widgets = {
            "cliente": forms.HiddenInput()
        }

#--- Written by Bruno ---
class DatosTSForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DatosTSForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'formulario'
        self.helper.form_method = 'post'

    class Meta:
        model = TipoDeServicio
        exclude = ['productos', 'creacion','modificacion','baja','alta']
    
    def clean(self):
        return self.cleaned_data

#--- Written by Bruno ---
class FrecuenciasForm(forms.ModelForm):
    hora_inicio = forms.TimeField(widget=forms.TimeInput(format='%H:%M %a'))   
    hora_fin = forms.TimeField(widget=forms.TimeInput(format='%H:%M %a'))    
    class Meta: 
        model = Frecuencia
        exclude = ['servicio_contratado']

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

class TipoDeServicioModificaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TipoDeServicioModificaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'formulario'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Confirmar'))
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-lg-1'
        self.helper.field_class='col-lg-6'
        
    class Meta:
        model = TipoDeServicio
        exclude = ['alta', 'baja','codigo_servicio']



class TipoDeServicioBajaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TipoDeServicioBajaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'formulario'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Confirmar'))
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-lg-1'
        self.helper.field_class='col-lg-6'

    class Meta:
        model = TipoDeServicio
        exclude = ['productos','codigo_servicio','nombre','creacion','modificacion','valorM2']
        widgets = {
            "baja": forms.DateInput(
                attrs={'class':'datepicker', 
                        'date-date-format':'dd-mm-yyyy',
                        'date-date-language':'es'}),
        }




class ServicioContratadoForm(forms.ModelForm):
    class Meta:
        model = ServicioContratado
        widgets = {
            "tipo_servicio": forms.TextInput(),
            "fin": forms.DateInput(
                attrs={
                    'class': 'form-control datepicker',
                    'data-date-format': 'dd-mm-yyyy',
                    'data-date-language':'es',
                    }),
        }
        fields = ("tipo_servicio", "fin")

    def __init__(self, *largs, **kwargs):
        super(ServicioContratadoForm, self).__init__(*largs, **kwargs)
        self.fields["tipo_servicio"].widget.attrs["class"] = "form-control"
        self.fields["tipo_servicio"].widget.attrs["disabled"] = "true"

class ServicioContratadoBaseFormset(BaseFormSet):
     def clean(self):
        return super(ServicioContratadoBaseFormset, self).clean()

ServicioContratadoFormset = modelformset_factory(ServicioContratado,
    form=ServicioContratadoForm,
    #formset=ServicioContratadoBaseFormset,
    extra=0)

class PersonaAltaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PersonaAltaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'persona-formulario'
        self.helper.form_class='form-horizontal'
        self.helper.form_method = 'POST'
        self.helper.label_class='col-lg-2'
        self.helper.field_class='col-lg-6'
        self.helper.form_tag=False
        

    class Meta:
        model = Persona
        exclude = ['user','baja','motivo']
    
    def clean(self):
        return self.cleaned_data

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
        exclude = ['user','baja','motivo']

    
    #NUEVO
    #- La redefinicion del metodo clean de ModelForm hace que se sobreescriba/duplique datos de un cliente cargado cuak!
    #def clean(self):
    #   return self.cleaned_data

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
        exclude = ['tipo_documento', 'nro_documento', 'user','baja', 'motivo']
    
    def clean(self):
        return self.cleaned_data

class EmpleadoAltaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EmpleadoAltaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'formulario'
        #self.helper.form_method = 'post'
        #self.helper.add_input(Submit('submit', 'Confirmar'))
        #self.helper.form_class='form-horizontal'
        self.helper.label_class='col-lg-2'
        self.helper.field_class='col-lg-6'
        self.helper.form_tag=False

    class Meta:
        model = Empleado
        exclude = ['persona','baja','motivo','especialidad']


class EmpleadoModificarForm(forms.ModelForm):
    cuil = forms.IntegerField()
    #fecha_nacimiento = forms.DateTimeField()
    #tipo_de_servicio = forms.ModelChoiceField(queryset = TipoDeServicio.objects.all())

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
        exclude = ['tipo_documento', 'nro_documento','especialidad','baja','motivo','user']



class EmpleadoBajaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmpleadoBajaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'formulario'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Confirmar'))
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-lg-1'
        self.helper.field_class='col-lg-6'

    class Meta:
        model = Persona
        fields = ('baja', 'motivo')
        widgets = {
            "baja": forms.DateInput(
                attrs={'class':'datepicker', 
                        'date-date-format':'dd-mm-yyyy',
                        'date-date-language':'es'}),
        }

class TurnosForm(forms.ModelForm):
    class Meta:
        model = Turno
        widgets = {
            "hora_inicio": forms.DateInput(attrs={ 'class': 'form-control timepicker'}),
            "hora_fin": forms.DateInput(attrs={ 'class': 'form-control timepicker'}),
        }
        fields = ("hora_inicio", "hora_fin") 

    def __init__(self, *largs, **kwargs):
        super(TurnosForm, self).__init__(*largs, **kwargs)
        self.fields["hora_inicio"].widget.attrs["timepicker"] = 'tabindex:2'
        self.fields["hora_fin"].widget.attrs["timepicker"] = 'tabindex:2'

class TurnoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TurnoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'formulario'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Confirmar'))
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-lg-2'
        self.helper.field_class='col-lg-6'
        
    class Meta:
        model = Turno
        

class RegisterForm(forms.Form):
    username=forms.CharField(label="nombre de usuario", widget=forms.TextInput())
    password_uno= forms.CharField(label="Password", widget=forms.PasswordInput(render_value=False))
    password_dos= forms.CharField(label="Confirmar Password", widget=forms.PasswordInput(render_value=False))
    grupo=forms.ModelChoiceField(queryset=Group.objects.all())

    def clean_username(self):
        username=self.cleaned_data["username"]
        try:
            u=User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("usuario ya existe")


    def clean_password_dos(self):
        password_uno=self.cleaned_data["password_uno"]
        password_dos=self.cleaned_data["password_dos"]
        if password_uno == password_dos:
            pass
        else:
            raise forms.ValidationError("claves iguales")


    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Registrar'))
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-lg-2'
        self.helper.field_class='col-lg-4'

#NUEVO
class ContratoForm(forms.ModelForm):

    class Meta:
        model=Contrato
        exclude = ['creacion', 'baja', 'motivo', 'fecha_fin_real']

    def __init__(self, *args, **kwargs):
        super(ContratoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form'
        #self.helper.form_method = 'post'
        #self.helper.add_input(Submit('submit', 'Crear'))
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-lg-2'
        self.helper.field_class='col-lg-4'