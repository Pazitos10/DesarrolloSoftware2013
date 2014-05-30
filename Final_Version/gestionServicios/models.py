#! /usr/bin/python2
# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from datetime import timedelta

#----- Zenda
class Pais(models.Model):
    nombre  = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre

class Provincia(models.Model):
    pais    = models.ForeignKey('Pais')
    nombre  = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre

class Localidad(models.Model):
    provincia   = models.ForeignKey('Provincia')
    nombre      = models.CharField(max_length=10)

    def __str__(self):
        return "%s - %s" % (self.nombre, self.provincia)


#----- Gestion Personas
class Persona(models.Model):
    """Esta clase define el objeto Persona""" 

    le = 'le'
    dni = 'dni'
    TIPO_DOC_CHOICES=(
        (dni, 'DNI'),
        (le, 'LE')
    )
    tipo_documento = models.CharField(max_length=5, choices=TIPO_DOC_CHOICES)
    nro_documento = models.BigIntegerField(primary_key=True,max_length=8,unique=True)
    apellido = models.CharField(max_length=20)
    nombre = models.CharField(max_length=20, blank=True,null=True)
    domicilio = models.CharField(max_length=20)
    telefono = models.BigIntegerField(max_length=10)
    email = models.EmailField(unique=True)
    baja = models.DateTimeField(blank=True, null=True)
    motivo = models.TextField(max_length= 100, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)


    def guardar(self):
        documento = self.nro_documento
        if Persona.objects.get(nro_documento = documento) != []:
            print "error, la persona con el documento ingresado ya existe"
        else:
            self.save()

    def buscar_roles(self):
        empleado = ""
        cliente = ""
        if self.empleado_set.all() != []:
            empleado = self.empleado_set.all()
        if self.cliente_set.all() != []:
            cliente = self.cliente_set.all()
        return "La persona %s %s tiene los roles: %s %s" %(self.apellido, self.nombre, empleado, cliente)

    def dar_de_baja(self, fecha, motivo):
        self.baja = fecha
        self.motivo = motivo

    def dado_de_baja(self):
        if self.baja:
            return self.baja

    def __str__(self):
        return "%s %s" % (self.apellido, self.nombre)   

class LineaDeTiempo(models.Model):
    info = 'info'
    warning = 'warning'
    danger = 'danger'
    success = 'success'
    TIPO_ACTIVIDAD = (
        (info, 'info'),
        (warning, 'warning'),
        (danger, 'danger'),
        (success, 'success'),
    )
    titulo = models.CharField(max_length=200)
    tiempo_de_actividad = models.DateTimeField()
    descripcion = models.TextField(max_length=200,blank=True,null=True)
    tipo_actividad = models.CharField(max_length=30,choices=TIPO_ACTIVIDAD)
    persona = models.ForeignKey(Persona)

class Mensaje(models.Model):
    remitente = models.EmailField()
    destinatario = models.ForeignKey(User)
    asunto = models.CharField(max_length=20)
    descripcion = models.TextField(max_length=150)
    fecha_envio = models.DateTimeField()
    leido = models.BooleanField(default=False)


class Rol(models.Model):
    """Esta clase define el objeto abstracto Rol""" 
    persona = models.ForeignKey(Persona)

    class Meta:
        abstract = True


class Empleado(Rol):
    """Esta clase define el objeto Rol Empleado""" 
    especialidad = models.ForeignKey('TipoDeServicio')
    nro_legajo = models.AutoField(primary_key=True)
    CUIL = models.BigIntegerField(max_length=11)
    nacimiento = models.DateTimeField('fecha_nacimiento')
    baja = models.DateTimeField(blank=True, null=True)
    motivo = models.TextField(max_length= 100, blank=True, null=True)

    def dado_de_baja(self):
        if self.baja:
            return self.baja
        else:
            return False

    def __str__(self):
        return "%s" %  (self.persona)   

    class Meta:
        permissions = ( 
            ( "asignar_empleado", "Asignar Empleado" ),
            )


class Cliente(Rol):
    """Esta clase define el objeto Rol Cliente"""
    def obtener_presupuestos(self):
        return self.presupuestos

    def seleccionar_presupuesto(self,nroPresupuesto):
        return Presupuesto.objects.get(id=nroPresupuesto)

    def get_confirmados_vigentes(self):
        confirmados = Presupuesto.objects.filter(cliente=self).filter(confirmado__nombre = 'Confirmado')    #Tomo los presupuestos CONFIRMADOS del cliente
        confirmados_vigentes = []
        for c in confirmados:
            if c.contrato.baja is None:
                confirmados_vigentes.append(c)
        return confirmados_vigentes

    def get_solicitados(self):
        solicitados = Presupuesto.objects.filter(cliente=self).filter(
                        solicitado__nombre = 'Solicitado').exclude(
                        valorizado__nombre = 'Valorizado')    #Tomo solo los presupuestos solicitados del cliente
        return solicitados


    def get_valorizados(self):
        valorizados = Presupuesto.objects.filter(cliente=self).filter(
                        valorizado__nombre = 'Valorizado').exclude(
                        confirmado__nombre = 'Confirmado')     #Tomo solo los presupuestos valorizados del cliente
        return valorizados

    def __str__(self):
        return "%s" %  (self.persona)

# === Gestion Tipos de servicio ============
class TipoDeServicio(models.Model):
    """docstring for TipoDeServicio"""
    codigo_servicio = models.CharField(max_length=4,primary_key=True)
    nombre = models.CharField('nombre',max_length=50)
    valorM2 = models.FloatField('valor M2',blank=True, null=True)
    productos = models.ManyToManyField('Producto')#, related_name = "servicios"
    creacion = models.DateTimeField('creacion', auto_now=True)
    modificacion = models.DateTimeField('modificacion', auto_now_add=True, blank=True, null=True)
    baja = models.DateTimeField('baja', blank=True, null=True)
    
    def __str__(self):
        return "%s" %(self.nombre) 

#=== Gestion Presupuestos ============
 
class Presupuesto(models.Model):
    """Esta clase define el objeto Presupuesto"""
    contrato = models.OneToOneField('Contrato',blank=True,null=True)
    cliente = models.ForeignKey('Cliente')
    domicilio_servicio = models.CharField(max_length=30)
    #--- Written by Bruno only method--- 
    def calcularTotal(self):
        total=0
        servicios = self.serviciocontratado_set.all()
        for servicio in servicios:
            if servicio.importe == None:
                servicio.importe = 0.0
            total += servicio.importe
        return total        
        
    def save(self, *largs, **kwargs):
        nuevo_presupuesto = self.id is None
        super(Presupuesto, self).save(*largs, **kwargs)
        if nuevo_presupuesto:
            self.solicitar()
 
    def solicitar(self):
        estado = Solicitado(
                            nombre = "Solicitado",
                            presupuesto = self,
                            fecha_creacion = datetime.now(),
                            fecha_fin_programada = datetime.now() 
                            )
        estado.save()
 
    def obtener_estado_actual(self):
        if hasattr(self,'confirmado'):
            if self.contrato.baja is None:
                return self.confirmado
            else:
                return 'Dado de baja'
        elif hasattr(self,'rechazado'):
            return self.rechazado
        elif hasattr(self,'valorizado'):
            return self.valorizado
        else:
            return self.solicitado

    #--- Written by Bruno only method---
    def listar_servicios_contratados(self):
        return self.serviciocontratado_set.all()


    def obtener_contrato(self):
        return self.contrato
 
    #--- Written by Bruno only method---
    #NUEVO
    def contratar_servicio(self, tipo_de_servicio):
        contratado = ServicioContratado(presupuesto = self,
            tipo_servicio = tipo_de_servicio)
        self.serviciocontratado_set.add(contratado)

    def __str__(self):
        return  str(self.id)   

    class Meta:
        permissions = ( 
            ( "valorizar_presupuesto", "confirmar_presupuestos" ),
            )

 
class ServicioContratado(models.Model):
    """docstring for ServicioContratado"""
    presupuesto = models.ForeignKey(Presupuesto)
    tipo_servicio = models.ForeignKey(TipoDeServicio)
    #NUEVO
    fin= models.DateField(blank=True, null=True) #CON ESTO INDICAMOS LA BAJA LOGICA DEL SERV CONTRATADO
    #END NUEVO
    metros_cuad = models.DecimalField('metros_cuad', decimal_places=2,max_digits=5, blank=True, null=True) #--- Written by Bruno only field---
    importe = models.FloatField('importe', blank=True, null=True)


    def calcularImporte(self, valorM2):
        self.importe = (self.metros_cuad*valorM2) * self.frecuencia_set.count() 
        self.save()
 
    def __str__(self):
        return str(self.tipo_servicio.nombre)

    def baja_servicio_contratado(self):
        self.fin = datetime.now()
        for f in self.frecuencia_set.all():
            for t in f.turno_set.all():
                t.baja_turno()

    #NUEVO
    def set_fecha_fin_sc(self, fechafin):
        self.fin = fechafin
        self.save()

class EstadoPresupuesto(models.Model):
    """Esta clase define el estado de un Presupuesto"""
    nombre = models.CharField(max_length=30)
    presupuesto = models.OneToOneField('Presupuesto')
 
    def __str__(self):
        return self.nombre
 
    class Meta:
        abstract = True
 
class Solicitado(EstadoPresupuesto):
    """docstring for Solicitado"""
    fecha_creacion = models.DateTimeField('fecha_creacion')
    fecha_fin_programada = models.DateTimeField('fecha_fin_programada')
 
    def valorizar(self, total):
        estado = Valorizado(
                            nombre = "Valorizado",
                            presupuesto = self.presupuesto,
                            valorizacion = datetime.now(),
                            #ACA ABAJO ME TIRO UN ERROR, POR ESO COMENTE
                            fecha_vigencia = datetime.now()+ timedelta(weeks=4),#datetime(datetime.now().year, datetime.now().month+1, datetime.now().day),
                            valor_final = total
                            )   
        estado.save()
        self.presupuesto.valorizado = estado
             
 
class Valorizado(EstadoPresupuesto):
    """Esta clase define el estado Valorizado para el objeto Presupuesto"""
    valorizacion = models.DateTimeField()
    fecha_vigencia = models.DateTimeField()
    valor_final = models.FloatField()
 
    def confirmar(self):
        estado = Confirmado.objects.create( nombre = "Confirmado",
                                            presupuesto = self.presupuesto,
                                            confirmacion = datetime.now(),
                                            inicio_servicio = datetime.now(), 
                                            )   
        self.presupuesto.confirmado = estado

    def rechazar(self, motivo):
        estado = Rechazado.objects.create(nombre = 'Rechazado',
                                                  presupuesto = self.presupuesto,
                                                  rechazado = datetime.now(),
                                                  motivo = motivo 
                                                 )   
        self.presupuesto.rechazado = estado 

    class Meta:
        permissions = ( 
            ( "valorizar_presupuesto", "Valorizar Presupuesto" ),
            )
 
class Confirmado(EstadoPresupuesto):
    """Esta clase define el estado Confirmado para el objeto Presupuesto"""
    confirmacion = models.DateTimeField('confirmacion')
    inicio_servicio = models.DateTimeField('inicio_servicio')

    #NUEVO
    def dar_de_baja(self, motivo):
        self.presupuesto.contrato.dar_de_baja(datetime.now(), motivo)


class Rechazado(EstadoPresupuesto):
    rechazado = models.DateTimeField('rechazado')
    motivo = models.CharField(max_length = 30)

        
#==== Gestion contrato====

class Contrato(models.Model):
    inicio = models.DateTimeField()
    fin = models.DateTimeField()#Programada
    fecha_fin_real = models.DateTimeField('fecha_fin_real', blank=True,null=True)
    creacion = models.DateTimeField()
    baja = models.DateTimeField(blank=True, null=True)
    motivo = models.CharField(max_length=50, blank=True, null=True)


    def asignar_personal(self):
        pass

    #NUEVO
    def dar_de_baja(self, fecha, motivo):
        self.baja = fecha
        self.motivo = motivo
        for sc in self.presupuesto.serviciocontratado_set.all():
            sc.baja_servicio_contratado()
        self.save()

    def renegociar_contrato(self):
        pass

    class Meta:
        permissions = ( 
            ( "renegociar_contrato", "Renegociar Contrato" ),
            )
 
 
class Producto(models.Model):
    """docstring for Producto"""
    cm3 = 'cm3'
    mm3 = 'cm3'
    litro = 'Lt'
    kilogramo = 'Kg'
    gramo = 'Gr'
    UNIDADES_DE_MEDIDA_CHOICES = (
        (cm3, 'centimetro cubico'),
        (mm3, 'milimetro cubico'),
        (litro, 'litro'),
        (kilogramo, 'kilogramo'),
        (gramo, 'gramo'),
    )
    nombre = models.CharField('nombre',max_length=50)
    marca = models.CharField('marca',max_length=50)
    unidad_medida = models.CharField(max_length=3,choices=UNIDADES_DE_MEDIDA_CHOICES)
    capacidad = models.FloatField('valorM2')
 
    def __str__(self):
        return '%s de %s %s' % (self.nombre, self.capacidad, self.unidad_medida)

    class Meta:
        permissions = ( 
            ( "consultar_producto", "Consultar Productos" ),
            )
 

#------- Gestion turnos y frecuencias

class Frecuencia(models.Model):
    """docstring for Frecuencia"""
    lu = 'lu'
    ma = 'ma'
    mi = 'mi'
    ju = 'ju'
    vi = 'vi'
    sa = 'sa'
    DIA_DE_LA_SEMANA_CHOICES = (
        (lu,'Lunes'),
        (ma,'Martes'),
        (mi,'Miercoles'),
        (ju,'Jueves'),
        (vi,'Viernes'),
        (sa,'Sabado')
    )
    
    dia = models.CharField('dia',max_length=2,choices=DIA_DE_LA_SEMANA_CHOICES)
    hora_inicio = models.TimeField('hora_inicio')
    hora_fin = models.TimeField('hora_fin')
    servicio_contratado = models.ForeignKey(ServicioContratado, null=True,blank=True) #--- Written by Bruno only field---

    def __str__(self):
        return 'Dia %s - Hora inicio: %s - Hora fin: %s' %(self.dia, self.hora_inicio, self.hora_fin)

class Turno(models.Model):
    frecuencia = models.ForeignKey(Frecuencia)
    empleado = models.ForeignKey(Empleado)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    #NUEVO
    fin = models.DateTimeField(blank=True, null=True) #CON ESTO INDICAMOS LA BAJA LOGICA DEL TURNO

    class Meta:
        permissions = ( 
            ( "consultar_turnos", "Consultar Turnos" ),
            )

    #NUEVO
    def baja_turno(self):
        self.fin = datetime.now()
        self.save()

