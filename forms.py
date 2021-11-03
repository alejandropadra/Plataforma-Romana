from wtforms import Form
from wtforms import StringField
from wtforms import IntegerField
from wtforms import PasswordField
from wtforms import RadioField
from wtforms import TextField, TextAreaField
from wtforms import SelectField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from wtforms import IntegerField
from wtforms import FloatField, DecimalField
from wtforms import BooleanField
from wtforms.fields.html5 import TimeField
from wtforms.fields.html5 import DateField
from wtforms import HiddenField
from wtforms import SubmitField

def length_honeypot(form, field):
    if len(field.data) > 0:
        raise validators.ValidationError('El campo debe estar vacio.')

class VigilanciaForm(Form):
    nombre_apellido = StringField("Nombre y Apellido: ")
    cedula = IntegerField("Cédula: ")
    telefono = StringField("Teléfono: ", [validators.Required(message='')])
    empresa = StringField("Empresa: ")
    modelo = StringField("Modelo: ")
    marca = StringField("Marca: ")
    clasificacion = StringField("Clasificación: ")
    placa = StringField("Placa: ")
    num_transporte = IntegerField("Número de transporte: ")
    direccion = StringField("Dirección: ")
    motivo = StringField("Motivo de Visita: ")
    ingresa_con = TextAreaField("El vehículo ingresa con: ")
    peso_transporte = DecimalField("Peso Transporte (Kg): ")
    fecha = DateField("Fecha de Ingreso")
    num_pase = IntegerField("Nº de pase asignado: ")
    sello = BooleanField("Sello ", [validators.Required(message='')])
    uniforme = BooleanField("Uniforme ", [validators.Required(message='')])
    epp = BooleanField("EPP ", [validators.Required(message='')])
    vehiculo_condicion = BooleanField("Vehiculo", [validators.Required(message='')])
    gasoil = BooleanField("Gasoil ", [validators.Required(message='')])
    bandera = HiddenField("")

class PreingresoForm(Form):
    nombre_apellido = StringField("Nombre y Apellido: ", [validators.Required(message='')])
    cedula = IntegerField("Cédula: ", [validators.Required(message='')])
    telefono = StringField("Teléfono: ")
    empresa = StringField("Empresa: ", [validators.Required(message='')])
    modelo = StringField("Modelo: ", [validators.Required(message='')])
    marca = StringField("Marca: ", [validators.Required(message='')])
    clasificacion = StringField("Clasificación: ")
    placa = StringField("Placa: ")
    num_transporte = IntegerField("Número de Transporte: ", [validators.Required(message='')])
    peso_transporte = FloatField("Peso Transporte (Kg): ", [validators.Required(message='')])
    motivo = SelectField("Motivo de Visita: ", choices = [("Retiro","Retiro"),("Devoluciones","Devoluciones"),("Retiro y devoluciones","Retiro y devoluciones")])
    fecha = DateField("Fecha de Ingreso", [validators.Required(message='')])


class RomanaForm(Form):
    reconteo = RadioField("RECONTEO",choices = [("Si","Si"),("No","No")])

class DistribucionForm(Form):
    carga = BooleanField("Carga Vehiculo")
    verificar = BooleanField('¿Considieron los pesajes?   Sí')
    reconteo = BooleanField("No")
    usuario_carga = StringField("")
    usuario_verifica = StringField("")
    date_carga = StringField("")
    date_verifica = StringField("")

class LoginForm(Form):
    username = StringField("",
                            [
                                validators.Required(message='El usuario es requerido!.'),
                                validators.length(min=4, max=25,message='Ingrese usuario valido!.')
                            ])        
    password = PasswordField("")
    honeypot = HiddenField('',[length_honeypot])

class RegistroForm(Form):
    nombre =  StringField("",
                            [
                                validators.Required(message='Nombre es requerido!.')
                            ])
    apellido = StringField("",
                            [
                                validators.Required(message='Apellido es requerido!.')
                            ])
    cedula = IntegerField("",
                            [
                                validators.Required(message='Cédula es requerida!.')
                            ])
    ficha = IntegerField("",
                            [
                                validators.Required(message='Ficha es requerido!.')
                            ])
    email = EmailField("",
                            [
                                validators.Required(message='Correo Electrónico es requerido!.')
                            ])
    area_asignada = SelectField("", choices = [('10','Vigilancia'),('20','Distribución, Supervisor'),('21','Distribución, Superintendente')])
    password = PasswordField("",
                            [
                                validators.Required(message='Contraseña es requerida!.')
                            ])
    password_repetir = PasswordField("")
    nacionalidad = SelectField("", choices = [('venezolano','V'),('extranjero','E')])

class EditarUserForm(Form):
    nombre =  StringField("",
                            [
                                validators.Required(message='Nombre es requerido!.')
                            ])
    apellido = StringField("",
                            [
                                validators.Required(message='Apellido es requerido!.')
                            ])
    cedula = IntegerField("",
                            [
                                validators.Required(message='Cédula es requerida!.')
                            ])
    ficha = IntegerField("",
                            [
                                validators.Required(message='Ficha es requerido!.')
                            ])
    email = EmailField("",
                            [
                                validators.Required(message='Correo Electrónico es requerido!.')
                            ])
    area_asignada = SelectField("", choices = [('10','Vigilancia'),('20','Distribución, Supervisor'),('21','Distribución, Superintendente')])
    nacionalidad = SelectField("", choices = [('venezolano','V'),('extranjero','E')])

class ActpassForm(Form):
    password = PasswordField("",
                            [
                                validators.Required(message='Contraseña es requerida!.')
                            ])
    password_repetir = PasswordField("")

class ContenidoCarga(Form):
    material = SelectField("", choices = [('270 600 01','270 600 01'),('897 320 01','897 320 01'),('271 147b01','271 147b01'),('867 153 01','867 153 01')])
    presentacion = SelectField("", choices = [('cuñetes','Cuñetes'),('cajas galones','Cajas Galones'),('cajas cuartos','Cajas Cuartos'),('otros','Otros')])
    diferencia = IntegerField("")
    total = IntegerField("")

class ConductorForm(Form):
    nombre_apellido = StringField("Nombre y Apellido: ", [validators.Required(message='')])
    cedula = IntegerField("Cédula: ", [validators.Required(message='')])
    transporte = StringField("Transporte: ", [validators.Required(message='')])
    telefono = StringField("Teléfono: ", [validators.Required(message='Número telefonico requerido!.')])
    licencia_fecha = DateField("Expiración licencia: ", [validators.Required(message='')])
    certifica_fecha = DateField("Expiración certificado médico: ", [validators.Required(message='')])

class VehiculoForm(Form):
    transporte = StringField("Transporte: ", [validators.Required(message='')])
    modelo = StringField("Modelo: ", [validators.Required(message='')])
    marca = StringField("Marca: ", [validators.Required(message='')])
    clasificacion = SelectField("Clasificación: ", choices = [("Particular","Particular (40gal.)"),("Pick Up","Pick Up (100gal.)"),("350","350 (500gal.)"),("450","450 (700gal.)"),("750","750 (1500gal.)"),("Toronto","Toronto (2000gal.)"),("Gandola","Gandola (4000gal.)")])
    placa = StringField("Placa: ", [validators.Required(message='')])

class CoordinadorForm(Form):
    nombre_apellido = StringField("Nombre y Apellido: ")
    cedula = IntegerField("Cédula: ")
    empresa = StringField("Empresa: ")
    telefono = StringField("Teléfono: ", [ validators.Required(message='Número telefonico requerido!.')])
    direccion = StringField("Dirección de habitacion: ")
    transporte = StringField("Transporte: ")
    seleccionar = SelectField("Seleccionar tipo de ingreso: ", choices = [("coordinador","Coordinador"),("acompañante","Acompañante")])

class CoordinadorPreingresoForm(Form):
    nombre_apellido = StringField("Nombre y Apellido: ", [validators.Required(message='')])
    cedula = IntegerField("Cédula: ", [validators.Required(message='')])
    empresa = StringField("Empresa: ", [validators.Required(message='')])
    telefono = StringField("Teléfono: ")
    direccion = StringField("Dirección de habitacion: ", [validators.Required(message='')])
    transporte = StringField("Transporte: ", [validators.Required(message='')])
    fecha = DateField("Fecha limite de pase: ", [validators.Required(message='')])
    fecha_limite = DateField("", [validators.Required(message='')])

class CancelarForm(Form):
    cedula = IntegerField("Cédula: ")
    placa = StringField("Placa: ")
    num_transporte = IntegerField("Número de transporte: ")
    motivo_cancelar = TextAreaField("Motivo por el cual se cancela el preingreso:")
    fecha_reporte = DateField()
    fecha_preingreso = DateField()

class SalidaForm(Form):
    repartos = IntegerField("Repartos: ")
    bultos = IntegerField("Bultos: ")

    #def validate_username(form,field):
     #   username = field.data
      #  conexion = sqlite3.connect('C:\\Users\\Corimon\\OneDrive - Corimon\\CORIMON\\CRP\\ROMANA CRP\\PLATAFORMA\\SERVIDOR_PESAJE\\static\\db\\usuarios.db')
       # consulta = conexion.cursor()
        #argumentos = (username)
        #sql = """
        #SELECT * FROM tabla WHERE usuario = ? limit 1
        #"""
        #tabla = consulta.execute(sql,argumentos)
        #user = username
        #if user is not None:
         #   raise validators.ValidationError("El usuario ya existe!.")