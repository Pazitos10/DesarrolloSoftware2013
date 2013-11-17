#! /usr/bin/python2
# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime


def listar_clientes():
	return Cliente.objects.all()

def listar_empleados():
	return Empleado.objects.all()

def listar_presupuestos():
	return Presupuesto.objects.all()

def seleccionar_un_cliente(nroDni):
	unaPersona = Persona.objects.get(nro_documento = nroDni)
	if len(unaPersona.cliente_set.all()) != 0:
		return unaPersona.cliente_set.all()[0]

def seleccionar_un_empleado(nroDni):
	unaPersona = Persona.objects.get(nro_documento = nroDni)
	if len(unaPersona.empleado_set.all()) != 0:
		return unaPersona.empleado_set.all()[0]

def listar_presupuestos_de_cliente(nroDni):
	unCliente = seleccionar_un_cliente(nroDni)
	return unCliente.presupuestos

def listar_empleados_especializados(codServicio):
	return TipoDeServicio.objects.get(pk = codServicio).empleado_set.all()

def alta_persona(tipoDocumento, nroDocumento, apellido, nombre, domicilio, telefono, email, CUIL=None, nacimiento=None, especialidad= None):
	persona = Persona.objects.create(tipo_documento = tipoDocumento, nro_documento = nroDocumento,
									 apellido = apellido, domicilio = domicilio,
									 telefono = telefono, email = email)
	if CUIL != None and nacimiento != None:
		persona.empleado_set.add(Empleado.objects.create(CUIL = CUIL, nacimiento = nacimiento, especialidad = especialidad))
	elif nombre != "":
		persona.nombre = nombre
		persona.cliente_set.add(Cliente.objects.create())
	persona.save()


#----- Zenda
class Pais(models.Model):
	nombre	= models.CharField(max_length=10)

	def __str__(self):
		return self.nombre

class Provincia(models.Model):
	pais 	= models.ForeignKey('Pais')
	nombre	= models.CharField(max_length=10)

	def __str__(self):
		return self.nombre

class Localidad(models.Model):
	provincia 	= models.ForeignKey('Provincia')
	nombre		= models.CharField(max_length=10)

	def __str__(self):
		return "%s - %s" % (self.nombre, self.provincia)

#----- Gestion Personas
class Persona(models.Model):
	"""Esta clase define el objeto Persona""" 

	le = 'le'
	dni = 'dni'
	TIPO_DOC_CHOICES=(
		(dni, 'documento nacional de identidad'),
		(le, 'libreta de enrrolamiento')
	)
	tipo_documento = models.CharField(max_length=5, choices=TIPO_DOC_CHOICES)
	nro_documento = models.IntegerField(primary_key=True,max_length=8,unique=True)
	apellido = models.CharField(max_length=20)
	nombre = models.CharField(max_length=20, blank=True,null=True)
	domicilio = models.CharField(max_length=20)
	telefono = models.IntegerField()
	email = models.EmailField()
	baja = models.DateTimeField(blank=True, null=True)
	motivo = models.TextField(max_length= 100, blank=True, null=True)


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

class Rol(models.Model):
	"""Esta clase define el objeto abstracto Rol""" 
	persona = models.ForeignKey(Persona)

	class Meta:
		abstract = True


class Empleado(Rol):
	"""Esta clase define el objeto Rol Empleado""" 
	especialidad = models.ForeignKey('TipoDeServicio')
	nro_legajo = models.AutoField(primary_key=True)
	CUIL = models.IntegerField(max_length=11)
	nacimiento = models.DateTimeField('fecha_nacimiento')

	def __str__(self):
		return "CUIL = %s" %  (self.CUIL)	


class Cliente(Rol):
	"""Esta clase define el objeto Rol Cliente"""
	#nro_cliente	= models.AutoField(primary_key=True)

	def obtener_presupuestos(self):
		return self.presupuestos

	def seleccionar_presupuesto(self,nroPresupuesto):
		return Presupuesto.objects.get(id=nroPresupuesto)

	def __str__(self):
		return "%s" %  (self.persona)

#MODIFICADO
# === Gestion Tipos de servicio ============
class TipoDeServicio(models.Model):
	"""docstring for TipoDeServicio"""
	productos = models.ManyToManyField('Producto', related_name = "servicios")
 	codigo_servicio = models.CharField(max_length=4,primary_key=True)
	nombre = models.CharField('nombre',max_length=50)
	creacion = models.DateTimeField('creacion', auto_now=True)
	modificacion = models.DateTimeField('modificacion', auto_now_add=True)
	baja = models.DateTimeField('baja', blank=True, null=True)
	valorM2 = models.FloatField('valorM1')
	
	def __str__(self):
		return "%s" %(self.nombre) 
#END MODIFICADO 


#=== Gestion Presupuestos ============
 
class Presupuesto(models.Model):
	"""Esta clase define el objeto Presupuesto"""
	contrato = models.OneToOneField('Contrato',blank=True,null=True)
	cliente = models.ForeignKey('Cliente')
	domicilio_servicio = models.CharField(max_length=30)
	#Basado en el CU de Alta presupuesto necesita:
	#foreignKey's al cliente para obtener sus datos
 
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
		#self.solicitado_set.add(estado)
 
	def obtener_estado_actual(self):
		if len(self.confirmado_set.all()) != 0:
			return self.confirmado_set.all()[0] 
		elif len(self.valorizado_set.all()) != 0:
			return self.valorizado_set.all()[0]
		else:
			return self.solicitado_set.all()[0] 

	def listar_servicios_contratados(self):
		return self.servicios_contratados.all()

	def obtener_contrato(self):
		return self.contrato
 
	def __str__(self):
		return  str(self.id)   

class ServicioContratado(models.Model):
	"""docstring for ServicioContratado"""
	presupuesto = models.ForeignKey(Presupuesto)
	tipo_servicio = models.ForeignKey(TipoDeServicio)
	fin= models.DateTimeField('fin')
	metros_cuad = models.FloatField('metros_cuad')
	importe = models.FloatField('importe')
 
	def asignar_tipo_servicio(self):
		pass
 
	def asignar_frecuencia(self):
		pass
		 
	def get_frecuencia(self):
		pass

	def calcularImporte(self, valorM2):
		return self.metros_cuad*valorM2
 
	def __str__(self):
		return str(self.tipo_servicio.nombre)


class EstadosPresupuesto(models.Model):
	"""Esta clase define el estado de un Presupuesto"""
	nombre = models.CharField(max_length=30)
	presupuesto = models.OneToOneField('Presupuesto')
 
	def __str__(self):
		return self.nombre
 
	class Meta:
		abstract = True
 
class Solicitado(EstadosPresupuesto):
	"""docstring for Solicitado"""
	fecha_creacion = models.DateTimeField('fecha_creacion')
	fecha_fin_programada = models.DateTimeField('fecha_fin_programada')
 
	def cambiar_estado(self):
		estado = Valorizado(
							nombre = "Valorizado",
							presupuesto = self.presupuesto,
							valorizacion = datetime.now(),
							valor_final = self.calcular_valor_final(), 
							)   
		estado.save()
		self.presupuesto.valorizado_set.add(estado)

	def calcular_valor_final(self):
		valor_total = 0
		for sc in self.presupuesto.servicios_contratados.all():
			valorMetro = sc.tipodeservicio_set.all()[0].valorM2 
			valor_total += sc.calcularImporte(valorMetro)
		return valor_total                        
				 
 
class Valorizado(EstadosPresupuesto):
	"""Esta clase define el estado Valorizado para el objeto Presupuesto"""
	valorizacion = models.DateTimeField('fecha_valorizacion')
	valor_final = models.FloatField('valor_final')
 
	def cambiar_estado(self):
		estado = Confirmado.objects.create(	nombre = "Confirmado",
											presupuesto = self.presupuesto,
											confirmacion = datetime.now(),
											inicio_servicio = datetime.now(), 
											)   
		self.presupuesto.confirmado_set.add(estado)
		if self.presupuesto.contrato == None:
			contrato = Contrato.objects.create(inicio = datetime.now(),
												fin = datetime.now(),
												creacion = datetime.now(), 
												)
			contrato.presupuesto_set.add(self.presupuesto)#self.presupuesto.contrato.add(contrato)   
 
 
class Confirmado(EstadosPresupuesto):
	"""Esta clase define el estado Confirmado para el objeto Presupuesto"""
	confirmacion = models.DateTimeField('confirmacion')
	inicio_servicio = models.DateTimeField('inicio_servicio')
 		
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

	def dar_de_baja(self, fecha, motivo):
		self.baja = fecha
		self.motivo = motivo

	def renegociar_contrato(self):
		pass
 
 
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
        (mi,'Miércoles'),
        (ju,'Jueves'),
        (vi,'Viernes'),
        (sa,'Sábado')
    )
    
    dia = models.CharField('dia',max_length=2,choices=DIA_DE_LA_SEMANA_CHOICES)
    hora_inicio = models.TimeField('hora_inicio')
    hora_fin = models.TimeField('hora_fin')
    servicio_contratado = models.ForeignKey(ServicioContratado)

    def crear_turno(self, hora_inicio_turno, hora_fin_turno, empleado):
        #TODO validar que las hs de inicio y fin de turno a crear esten dentro de la frecuencia
        #TODO validar que no haya un turno creado en el rango de horario del turno a crear
        t = Turno.objects.create(hora_inicio=hora_inicio_turno, hora_fin=hora_fin_turno, frecuencia = self, empleado = empleado)

    def __str__(self):
        return 'Dia %s - Hora inicio: %s - Hora fin: %s' %(self.dia, self.hora_inicio, self.hora_fin)

class Turno(models.Model):
    frecuencia = models.ForeignKey(Frecuencia)
    empleado = models.ForeignKey(Empleado)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
    	return "turnito"