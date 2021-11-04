from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import redirect
from flask import flash
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask import jsonify

from responses import response
from responses import bad_request

import sqlite3
import forms
import control_db
import time

app = Flask(__name__)
app.secret_key = 'mi_clave'
csrf = CSRFProtect(app)

@app.errorhandler(404)
def error_page(e):

	return render_template("error404.html"), 404

@app.before_request
def before_request():
    if "username" not in session and request.endpoint in ["ReporteVigilancia", "distribucion lista", "configuracion", "gestionTransportistas", "listaUsuarios", "vigilanciaLista", "distribucionLista", "preingreso", "listaTransporte", "reporteDistribucion"]:
    	return redirect(url_for("index"))
    elif "username" in session and request.endpoint in ["index"]:
       	return redirect(url_for("distribucionLista"))

@app.after_request
def arfer_request(response):
	try:
		if int(session['nivel']) == 10 and request.endpoint in ["distribucionLista", "configuracion", "gestionTransporte", "distribucionLista", "preingresoTipo", "reporteDistribucion", "gestionTransportistas"]:
			success_message = " No posee los permisos necesarios para ingresar"
			flash(success_message, 'error')
			return redirect(url_for("vigilanciaLista"))
		elif int(session['nivel']) == 20 and request.endpoint in ["registro", "usuarioEditar", "listaUsuarios","gestionTransportistas"]:
			success_message = " No posee los permisos necesarios para ingresar."
			flash(success_message, 'error')
			return redirect(url_for("distribucionLista"))
	except:
		pass
	return(response)

@app.route("/logout")
def logout():
	if "username" in session:
   		session.pop("username")
	return redirect(url_for("index"))

@app.route("/", methods = ["GET","POST"])
def index():
	tittle = "index"
	acceso_form = forms.LoginForm(request.form)
	user = None
	if request.method == "POST" and acceso_form.validate():
		username = acceso_form.username.data.lower()
		password = acceso_form.password.data
		tabla = control_db.seleccionar_fila(username, tittle)
		for row in tabla:
			clave = row[6]
			user = username
			usuario = row [2] +" "+row[3]
			nivel =int(row[8])
		if user is not None and check_password_hash(clave,password):
			session['username'] = acceso_form.username.data
			session['nivel'] = nivel
			print(session['nivel'])
			success_message = "Bienvenido {}".format(usuario.title())
			flash(str(success_message))
			if nivel == 10:
				return redirect( url_for( 'vigilanciaLista'))
			elif nivel >= 20:
				return redirect( url_for( 'distribucionLista'))
		else:
			success_message = "Datos incorrectos!."
			flash(success_message, 'error')
	return render_template("index.html", form = acceso_form)

@app.route("/configuracion", methods = ["GET"])
def configuracion():
     
	return render_template("configuracion.html")

@app.route("/gestion-transporte", methods = ["GET"])
def gestionTransportistas():
     
	return render_template("gestion_transporte.html")

@app.route("/registro", methods = ["GET","POST"])
def registro():
	tittle = "registro usuarios"
	registro_form = forms.RegistroForm(request.form)
	if request.method == "POST" and registro_form.validate():
		nombre = registro_form.nombre.data.lower()
		apellido = registro_form.apellido.data.lower()
		cedula = registro_form.cedula.data
		nacionalidad = registro_form.nacionalidad.data
		ficha = registro_form.ficha.data
		correo = registro_form.email.data
		area = registro_form.area_asignada.data
		password = generate_password_hash(registro_form.password.data)
		repetir = generate_password_hash(registro_form.password_repetir.data)
		usuario = nombre+"_"+apellido
		#Crear en forms condicional para igualdad de password
		argumentos = (usuario,nombre,apellido,cedula,ficha,password,correo,area)
		try:
			control_db.insertar_datos(argumentos, tittle)
			success_message = "Usuario registrado correctamente!."
			flash(success_message)

		except:
			success_message = "Datos existentes!."
			flash(success_message,'error')
	return render_template("ingreso.html", form = registro_form, tittle = tittle)

@app.route("/usuario-<int:ci>", methods = ["GET","POST"])
def usuarioEditar(ci):
	tittle = "usuario editar"
	registro_form = forms.EditarUserForm(request.form)
	user = control_db.seleccionar_fila(ci, "seleccionar user")
	for row in user:
		nombreu = row[2]
		apellidou = row[3]
		cedulau = row[4]
		fichau = row[5]
		correou = row[7]
		areau = row[8]
	usuario_fila = (nombreu, apellidou, fichau, correou, areau, cedulau)
	if request.method == "POST" and registro_form.validate():
		nombre = registro_form.nombre.data.lower()
		apellido = registro_form.apellido.data.lower()
		cedula = registro_form.cedula.data
		nacionalidad = registro_form.nacionalidad.data
		ficha = registro_form.ficha.data
		email = registro_form.email.data
		area = registro_form.area_asignada.data
		usuario = nombre+"_"+apellido
		#Crear en forms condicional para igualdad de password
		argumentos = (usuario,nombre,apellido,ficha,email,area,cedula)
		#try:
		control_db.update(argumentos, tittle)
			#success_message = "Usuario registrado correctamente!."
			#flash(success_message)
		#except:
		#	success_message = "Datos existentes!."
		#	flash(success_message,'error')
	return render_template("usuario_update.html", form = registro_form, tittle = tittle, usuario = usuario_fila)

@app.route("/lista-usuarios", methods = ["GET","POST"])
def listaUsuarios():
	tittle = "lista usuarios"
	tabla_usuarios = control_db.seleccionar_tabla(tittle)
	return render_template("lista_usuarios.html", tittle = tittle, usuarios = tabla_usuarios)


@app.route("/cambio-clave", methods = ["GET","POST"])
def actClave():
	tittle = "cambio clave"
	actpass_form = forms.ActpassForm(request.form)
	if request.method == "POST" and actpass_form.validate():
		password = generate_password_hash(actpass_form.password.data)
		repetir = generate_password_hash(actpass_form.password.data)
		usuario = session['username']
		control_db.update((password, usuario), tittle)
		print(usuario)
		success_message = "Cambio de clave exitoso!"
		flash(success_message)
	return render_template("cambio_clave.html", form = actpass_form, tittle = tittle)

@app.route("/vigilancia-lista", methods = ["GET","POST"])
def vigilanciaLista():
	tittle = "vigilancia lista" #luego colocar vigilancia todas las listas
	rows = control_db.seleccionar_tabla(tittle)
	lista_coordinador = control_db.seleccionar_tabla("coordinadores preingreso")
	date = time.strftime("%Y-%m-%d")
	return render_template( "vigilancia_lista.html",  tittle = tittle, rows = rows, date = date, lista_coordinador = lista_coordinador)

@app.route("/romana", methods = ["GET","POST"])
def hmi():
	tittle = "hmi"
	return render_template( "romana.html",tittle = tittle)

@app.route("/vigilancia-<int:n>", methods = ["GET","POST"])
def vigilancia(n):
	tittle = "vigilancia"
	vigilancia_form = forms.VigilanciaForm(request.form)
	salida_form = forms.SalidaForm(request.form)
	if request.method == "POST" and vigilancia_form.validate():
		ingresa = vigilancia_form.ingresa_con.data
		direccion = vigilancia_form.direccion.data
		pase = vigilancia_form.num_pase.data
		guia = vigilancia_form.num_transporte.data
		bandera = vigilancia_form.bandera.data
		estado = int(bandera)
		date = time.strftime("%Y-%m-%d %H:%M:%S")
		argumentos = (guia, direccion, ingresa, pase, estado, date)
		repartos = salida_form.repartos.data
		bultos = salida_form.bultos.data
		#try:
		if estado == 7:
			print((estado, date, guia, repartos, bultos))
			control_db.update((estado, date, repartos, bultos, guia), tittle + " fin")
			success_message = "Proceso numero de pase: " + str(pase) + " finalizado, numero de guia: " + str(guia) + " ha salido de planta!"
		else:
			control_db.insertar_datos(argumentos,tittle+" ingreso")
			control_db.update((pase,guia),"proceso distribucion num pase")
			success_message = "Se ha registrado!"
		control_db.update((estado,guia),"proceso distribucion")
		flash(success_message)
		return redirect( url_for( 'vigilanciaLista'))
		#except:
		#	success_message = " No se ha registrado la información."
		#	flash(success_message, 'error')
	row = control_db.seleccionar_fila(n, tittle)
	row_proceso = control_db.seleccionar_fila(n, "proceso")
	return render_template("vigilancia.html", form2 = salida_form, form= vigilancia_form, row = row, tittle = tittle, row_proceso = row_proceso)

@app.route("/distribucion-lista", methods = ["GET","POST"])
def distribucionLista():
	tittle = "distribucion lista"
	lista_preingreso = control_db.seleccionar_tabla(tittle)
	lista_pase = control_db.seleccionar_tabla(tittle)
	lista_coordinador = control_db.seleccionar_tabla("coordinadores preingreso")
	date = time.strftime("%Y-%m-%d")
	return render_template("distribucion_lista.html",tittle = tittle, lista_pase = lista_pase, lista_preingreso = lista_preingreso, lista_coordinador = lista_coordinador, date = date)

@app.route("/distribucion-<int:n>", methods = ["GET","POST"])
def distribucion(n):
	tittle = "distribucion"
	vigilancia_form = forms.VigilanciaForm(request.form)
	distribucion_form = forms.DistribucionForm(request.form)
	romana_form = forms.RomanaForm(request.form)    
	distribucion_form = forms.DistribucionForm(request.form)
	usuario = session['username']
	date = time.strftime("%Y-%m-%d %H:%M:%S")
	if request.method == "POST" and distribucion_form.validate():
		carga = distribucion_form.carga.data
		reconteo = distribucion_form.reconteo.data
		verificar = distribucion_form.verificar.data
		guia = vigilancia_form.num_transporte.data
		usuario_carga = distribucion_form.usuario_carga.data
		date_carga = distribucion_form.date_carga.data
		usuario_verificar = distribucion_form.usuario_verifica.data
		date_verificar = distribucion_form.date_verifica.data
		date = time.strftime("%Y-%m-%d %H:%M:%S")
		if carga == True and verificar == False and reconteo == False:
			estado =  3
		elif (carga == True and verificar == True and reconteo == False) or (carga == True and verificar == False and reconteo == True):
			estado = 6
		try:
			argumentos = (carga, verificar, reconteo, estado, usuario_carga, date_carga, usuario_verificar, date_verificar, guia)
			control_db.update(argumentos, tittle+" ingreso")
			control_db.update((estado,guia),"proceso distribucion")
			success_message = " Informacion actualizada."
			flash(success_message)
			return redirect(url_for('distribucionLista'))
		except:
			success_message = " No se ha registrado la información"
			flash(success_message, 'error')
	row = control_db.seleccionar_fila(n, tittle)
	row_proceso = control_db.seleccionar_fila(n, "proceso")
	return render_template("distribucion.html", form = vigilancia_form, form2 = romana_form, form3 = distribucion_form, tittle = tittle, row = row, row_proceso = row_proceso, user_date = (usuario, date))

@app.route("/preingreso", methods = ["GET","POST"])
def preingreso():
	tittle = "preingreso"
	tabla_conductores = control_db.seleccionar_tabla("conductores")
	return render_template("preingreso.html", tittle = tittle, conductores = tabla_conductores)

@app.route("/preingreso-<int:n>", methods = ["GET","POST"])
def preingresoVehiculo(n):
	tittle = "preingreso vehiculos"
	preingreso_form = forms.PreingresoForm(request.form)
	conductor = control_db.seleccionar_fila(n, tittle)
	for row in conductor:
		cedula = row [0]
		nombre = row [1]
		telefono = row [2]
		empresa = row [3]
	fila_conductor = [cedula, nombre, telefono, empresa]
	print(fila_conductor)
	tabla_vehiculos = control_db.seleccionar_dato_tabla(empresa,"preingresovehiculos")
	return render_template("preingreso_vehiculo.html", tittle = tittle, conductor = fila_conductor, form = preingreso_form, vehiculos = tabla_vehiculos)

@app.route("/preingreso-<int:n>-<plak>", methods = ["GET","POST"])
def preingresoEnvio(n,plak):
	tittle = "preingreso vehiculos"
	preingreso_form = forms.PreingresoForm(request.form)
	conductor = control_db.seleccionar_fila(n, tittle)
	for row in conductor:
		cedula = row [0]
		nombre = row [1]
		telefono = row [2]
		empresa = row [3]
	fila_conductor = [cedula, nombre, telefono, empresa]
	print(fila_conductor)
	vehiculos = control_db.seleccionar_fila(plak,"preingreso fin")
	for row in vehiculos:
		placa = row [0]
		marca = row [1]
		modelo = row [2]
		clasificacion = row [3]
	fila_vehiculos = [placa, marca, modelo, clasificacion]
	print (fila_vehiculos)
	if request.method == "POST" and preingreso_form.validate():
		nombre_conductor = nombre
		cedula_conductor = cedula
		telefono_conductor = telefono
		empresa_conductor = empresa
		modelo_vehiculo = modelo
		clasificacion_vehiculo = clasificacion
		placa = placa
		marca_vehiculo = marca
		num_transporte = preingreso_form.num_transporte.data
		peso_transporte = preingreso_form.peso_transporte.data
		fecha_pase = preingreso_form.fecha.data
		motivo = preingreso_form.motivo.data
		edo = 0
		argumentos = (num_transporte, nombre_conductor, cedula_conductor,telefono_conductor, empresa_conductor,marca_vehiculo, modelo_vehiculo, clasificacion_vehiculo, placa, motivo, fecha_pase, peso_transporte, edo)
		print(argumentos)
		date = time.strftime("%Y-%m-%d")
		print(date)
		if str(fecha_pase) >= date:
			try:
				control_db.insertar_datos(argumentos, "preingreso")
				success_message = "ingreso registrado correctamente!."
				flash(success_message)
				return redirect(url_for('distribucionLista'))
			except:
				success_message = "Datos existentes!."
				flash(success_message, 'error')
		else:
			success_message = "Fecha Invalida"
			flash(success_message, 'error')
	return render_template("preingreso_envio.html", tittle = tittle, conductor = fila_conductor, form = preingreso_form, vehiculos = fila_vehiculos)

@app.route("/registro-conductor", methods = ["GET","POST"])
def registroConductor():
	tittle = "registro conductor"
	conductor_form = forms.ConductorForm(request.form)
	if request.method == "POST" and conductor_form.validate():
		cedula = conductor_form.cedula.data
		nombre = conductor_form.nombre_apellido.data
		telefono = conductor_form.telefono.data
		transporte = conductor_form.transporte.data
		expiracion_licencia = conductor_form.licencia_fecha.data
		expiracion_certificado = conductor_form.certifica_fecha.data
		argumentos = (cedula, nombre, telefono, transporte, expiracion_licencia, expiracion_certificado,)
		try:
			control_db.insertar_datos(argumentos, tittle)
			success_message = "ingreso registrado correctamente!."
			flash(success_message)
			return redirect(url_for('listaTranporte'))
		except:
			success_message = "Datos existentes!."
			flash(success_message, 'error')
	return render_template("registro_conductor.html", form = conductor_form, tittle = tittle)

@app.route("/conductor-<int:ci>", methods = ["GET","POST"])
def registroConductorEditar(ci):
	tittle = "conductor editar"
	conductor_form = forms.ConductorForm(request.form)
	conductor = control_db.seleccionar_fila(ci, "preingreso vehiculos")
	for row in conductor:
		cedulac = row [0]
		nombrec = row [1]
		telefonoc = row [2]
		empresac = row [3]
		expiracion_licenciac = row[4]
		expiracion_certificadoc = row[5]
	conductor_fila = (nombrec, telefonoc, empresac, expiracion_licenciac, expiracion_certificadoc, cedulac)
	if request.method == "POST" and conductor_form.validate():
		cedula = conductor_form.cedula.data
		nombre = conductor_form.nombre_apellido.data
		telefono = conductor_form.telefono.data
		transporte = conductor_form.transporte.data
		expiracion_licencia = conductor_form.licencia_fecha.data
		expiracion_certificado = conductor_form.certifica_fecha.data
		argumentos = (nombre, telefono, transporte, expiracion_licencia, expiracion_certificado, cedula)
		try:
			control_db.update(argumentos, tittle)
			success_message = "Cambio registrado correctamente!."
			flash(success_message)
			return redirect(url_for('listaTranporte'))
		except:
			success_message = "No se puso realizar el cambio!."
			flash(success_message, 'error')
	return render_template("conductor_update.html", form = conductor_form, tittle = tittle, conductor = conductor_fila, ci = ci)

@app.route("/conductor-delete-<int:ci>", methods = ["GET","POST"])
def conductorDelete(ci):
	tittle = "conductor delete"
	control_db.eliminar_fila(ci, tittle)
	success_message = "Se ha eliminado el conductor correctamente!."
	flash(success_message)
	return redirect(url_for("gestionTransportistas"))

@app.route("/registro-vehiculo", methods = ["GET","POST"])
def registroVehiculo():
	tittle = "registro vehiculo"
	vehiculo_form = forms.VehiculoForm(request.form)
	if request.method == "POST" and vehiculo_form.validate():
		transporte = vehiculo_form.transporte.data
		modelo = vehiculo_form.modelo.data
		marca = vehiculo_form.marca.data
		clasificacion = vehiculo_form.clasificacion.data
		placa = vehiculo_form.placa.data
		argumentos = (placa, marca, modelo, clasificacion, transporte)
		try:
			control_db.insertar_datos(argumentos,tittle)
			success_message = "ingreso registrado correctamente!."
			flash(success_message)
			return redirect(url_for('listaTranporte'))
		except:
			success_message = "Datos existentes!."
			flash(success_message, 'error')
	return render_template("registro_vehiculo.html", form = vehiculo_form, tittle = tittle)

@app.route("/vehiculo-<plak>", methods = ["GET","POST"])
def registroVehiculoEditar(plak):
	tittle = "registro vehiculo editar"
	vehiculo_form = forms.VehiculoForm(request.form)
	vehiculo = control_db.seleccionar_fila(plak, "preingreso fin")
	for row in vehiculo:
		placav = row[0]
		marcav = row[1]
		modelov = row[2]
		clasificacionv = row[3]
		transportev = row[4]
	vehiculo_fila = (placav, marcav, modelov, clasificacionv, transportev)
	if request.method == "POST" and vehiculo_form.validate():
		transporte = vehiculo_form.transporte.data
		modelo = vehiculo_form.modelo.data
		marca = vehiculo_form.marca.data
		clasificacion = vehiculo_form.clasificacion.data
		placa = vehiculo_form.placa.data
		argumentos = (marca, modelo, clasificacion, transporte, placa)
		try:
			control_db.update(argumentos,tittle)
			success_message = "Cambio registrado correctamente!."
			flash(success_message)
			return redirect(url_for('listaTranporte'))
		except:
			success_message = "No se puso realizar el cambio!."
			flash(success_message, 'error')
	return render_template("vehiculo_update.html", form = vehiculo_form, tittle = tittle, vehiculos = vehiculo_fila, placa =plak)

@app.route("/vehiculo-delete-<plak>", methods = ["GET","POST"])
def vehiculoDelete(plak):
	tittle = "vehiculo delete"
	control_db.eliminar_fila(plak, tittle)
	success_message = "Se ha eliminado el vehiculo correctamente!."
	flash(success_message)
	return redirect(url_for("gestionTransportistas"))

@app.route("/registro-coordinador", methods = ["GET","POST"])
def registroCoordinador():
	tittle = "registro coordinador"
	coordinador_form = forms.CoordinadorForm(request.form)
	if request.method == "POST" and coordinador_form.validate():
		cedula = coordinador_form.cedula.data
		nombre = coordinador_form.nombre_apellido.data
		telefono = coordinador_form.telefono.data
		direccion = coordinador_form.direccion.data
		transporte = coordinador_form.transporte.data
		seleccionar_tipo = coordinador_form.seleccionar.data
		argumentos = (cedula, nombre, telefono, transporte, direccion, seleccionar_tipo)
		try:
			control_db.insertar_datos(argumentos, tittle)
			success_message = "Registro realizado con exito"
			flash(success_message)
			return redirect(url_for("listaTranporte"))
		except:
			success_message = "Error, datos existentes"
			flash(success_message, "error")
	return render_template("registro_coordinador.html", form = coordinador_form, tittle = tittle)

@app.route("/coordinador-<int:ci>", methods = ["GET","POST"])
def registroCoordinadorEditar(ci):
	tittle = "coordinador editar"
	coordinador_form = forms.CoordinadorForm(request.form)
	coordinador = control_db.seleccionar_fila(ci, "preingreso coordinadores")
	for row in coordinador:
		cedulac = row [0]
		nombrec = row [1]
		telefonoc = row [2]
		empresac = row [3]
		direccionc = row[4]
	coordinador_fila = (cedulac, nombrec, telefonoc, empresac, direccionc)
	if request.method == "POST" and coordinador_form.validate():
		cedula = coordinador_form.cedula.data
		nombre = coordinador_form.nombre_apellido.data
		telefono = coordinador_form.telefono.data
		transporte = coordinador_form.transporte.data
		direccion = coordinador_form.direccion.data
		argumentos = (nombre, telefono, transporte, direccion, cedula)
		#try:
		control_db.update(argumentos, tittle)
		success_message = "Cambio registrado correctamente!."
		flash(success_message)
		return redirect(url_for('listaTranporte'))
		#except:
		#	success_message = "No se puso realizar el cambio!."
		#	flash(success_message, 'error')
	return render_template("coordinador_update.html", form = coordinador_form, tittle = tittle, coordinador = coordinador_fila, ci =ci)

@app.route("/coordinador-delete-<int:ci>", methods = ["GET","POST"])
def coordinadorDelete(ci):
	tittle = "coordinador delete"
	control_db.eliminar_fila(ci, tittle)
	success_message = "Se ha eliminado el coordinador correctamente!."
	flash(success_message)
	return redirect(url_for("gestionTransportistas"))

@app.route("/lista-transportes", methods = ["GET","POST"])
def listaTranporte():
	tittle = "lista Transportes"
	tabla_conductores = control_db.seleccionar_tabla("conductores")
	tabla_vehiculos = control_db.seleccionar_tabla("vehiculos")
	tabla_coordinadores = control_db.seleccionar_tabla("coordinadores")
	return render_template("lista_transporte.html", tittle = tittle, conductores = tabla_conductores, vehiculos = tabla_vehiculos, coordinadores = tabla_coordinadores)

@app.route("/preingreso-tipo", methods = ["GET"])
def preingresoTipo():
	tittle = "preingreso tipo"
	return render_template("tipo_preingreso.html", tittle = tittle)

@app.route("/preingreso-coordinadores", methods = ["GET","POST"])
def preingresoCoordinador():
	tittle = "preingreso coordinador"
	tabla_coordinadores = control_db.seleccionar_tabla("coordinadores")
	return render_template("preingreso_coordinador.html", tittle = tittle, coordinadores = tabla_coordinadores)

@app.route("/preingreso-coordinador-<int:ci>", methods = ["GET","POST"])
def preingresoCoordinadorCi(ci):
	tittle = "preingreso coordinador"
	coordinador_form = forms.CoordinadorPreingresoForm(request.form)
	coordinador = control_db.seleccionar_fila(ci, "seleccionar coordinador")
	for row in coordinador:
		cedulac = row[0]
		nombrec = row[1]
		telefonoc = row[2]
		transportec = row[3]
		direccionc = row[4]
		tipo = row[5]
	coordinador_fila = (cedulac, nombrec, telefonoc, transportec, direccionc, tipo)
	if request.method == "POST" and coordinador_form.validate():
		cedula = cedulac
		nombre = nombrec
		telefono = telefonoc
		empresa = transportec
		direccion = direccionc
		fecha = coordinador_form.fecha.data
		fecha_limite = coordinador_form.fecha_limite.data
		argumentos = (cedula, nombre, telefono, empresa, direccion, fecha, tipo, fecha_limite)
		date = time.strftime("%Y-%m-%d")
		if str(fecha) >= date:
			try:
				control_db.insertar_datos(argumentos,tittle)
				success_message = "Preingreso registrado correctamente!."
				flash(success_message)
				return redirect(url_for('distribucionLista'))
			except:
				success_message = "No se puso realizar el registro."
				flash(success_message, 'error')
		else:
			success_message = "Fecha Invalida"
			flash(success_message, 'error')
	return render_template("preingreso_coordinador_fin.html", tittle = tittle, coordinador = coordinador_fila, form = coordinador_form)

@app.route("/distribucion-coordinador-<int:ci>", methods = ["GET","POST"])
def distribucionCoordinadorCi(ci):
	tittle = "distribucion"
	coordinador_form = forms.CoordinadorPreingresoForm(request.form)
	coordinador = control_db.seleccionar_fila(ci, "distribucion coordinador")
	for row in coordinador:
		cedulac = row[0]
		nombrec = row[1]
		telefonoc = row[2]
		transportec = row[3]
		direccionc = row[4]
		fechac = row[5]
	coordinador_fila = (cedulac, nombrec, telefonoc, transportec, direccionc, fechac)
	return render_template("distribucion_coordinador.html", tittle = tittle, coordinador = coordinador_fila, form = coordinador_form)

@app.route("/coordinador-acompañante-<int:id>", methods = ["GET","POST"])
def coordinadorAcompañante(id):
	tittle = "Ficha"
	coordinador_form = forms.CoordinadorPreingresoForm(request.form)
	coordinador_fila = control_db.seleccionar_fila(id, tittle)
	return render_template("coordinador_acompañante.html", tittle = tittle, lista_coordinador = coordinador_fila, form = coordinador_form)


@app.route("/materiaprima", methods = ["GET","POST"])
def materia_prima():
     
	return render_template("completo.html")

@app.route("/vigilancia-reporte", methods = ["GET","POST"])
def ReporteVigilancia():
	tittle = "vigilancia_reporte"
	reporte_vigilancia = control_db.seleccionar_tabla("distribucion lista")
	return render_template("ReporteVigilancia.html", tittle = tittle, reporte_vigilancia = reporte_vigilancia)

@app.route("/romana-reportes", methods = ["GET","POST"])
def reporte_romana():
	tittle = "romana"
	return render_template("reporte_romana.html", tittle = tittle)

@app.route("/distribucion-reportes", methods = ["GET","POST"])
def reporteDistribucion():
	tittle = "distribucion reportes"
	reporte_preingreso = control_db.seleccionar_tabla("distribucion lista")
	reporte_distribucion = control_db.seleccionar_tabla(tittle)
	return render_template("reporte_distribucion.html", tittle = tittle, reporte_distribucion = reporte_distribucion, reporte_preingreso = reporte_preingreso) 

@app.route("/alarmas", methods = ["GET","POST"])
def alarmas_avisos():
	tittle = "lista alarmas"
	rows = control_db.seleccionar_tabla(tittle)
	return render_template("alarmas.html", tittle = tittle, rows = rows)

@app.route("/vigilancia-cancelar", methods = ["GET","POST"])
def vigilanciaCancelar():
	tittle = "vigilancia cancelar" #luego colocar vigilancia todas las listas
	rows = control_db.seleccionar_tabla("vigilancia lista")
	date = time.strftime("%Y-%m-%d")
	return render_template( "vigilancia_cancelar.html",  tittle = tittle, rows = rows, date = date)

@app.route("/cancelar-<int:n>", methods = ["GET","POST"])
def cancelar(n):
	tittle = "cancelar preingreso"
	cancelar_form = forms.CancelarForm(request.form)
	preingreso_form = forms.PreingresoForm(request.form)
	if request.method == "POST" and cancelar_form.validate():
		fecha_reporte = cancelar_form.fecha_reporte.data
		motivo_cancelar = cancelar_form.motivo_cancelar.data
		num_transporte = preingreso_form.num_transporte.data
		cedula = preingreso_form.cedula.data
		placa = preingreso_form.placa.data
		fecha_preingreso = preingreso_form.fecha.data
		argumentos = (fecha_reporte, motivo_cancelar, num_transporte, cedula, placa, fecha_preingreso)
		print(argumentos)
	#try:
		control_db.insertar_datos(argumentos, "cancelar ingresar")
		control_db.eliminar_fila(n, tittle)
		success_message = "Se ha generado una alarma correctamente!."
		flash(success_message)
		return redirect(url_for("alarmas_avisos"))
	#except:
	#	success_message = "No se pudo crear la alarma!."
	#	flash(success_message, "error")
	#row = control_db.seleccionar_fila(n, tittle)
	#row_proceso = control_db.seleccionar_fila(n, "proceso") GUARDAR INFORMACION EN BASES DE DATOS Y TOMAR LA NECESARIA DE PREINGRESO
	date = time.strftime("%Y-%m-%d")
	row = control_db.seleccionar_fila(n, "vigilancia")
	return render_template("cancelar.html", form2 = cancelar_form, tittle = tittle, form = preingreso_form , row = row, date = date)

@app.route('/lista', methods = ["GET"])
def get_tarea():
	rows = control_db.seleccionar_tabla("romana")
	rows = rows.fetchall()
	return response([
		row for row in rows
	])

@app.route('/lista', methods = ["POST"])
@csrf.exempt
def crear_tarea():
	json = request.get_json(force=True)

	if json.get('num_pase') is None:
		return bad_request()

	if json.get('peso_tara') is None:
		return bad_request()

	if json.get('peso_neto') is None:
		return bad_request()

	if json.get('peso_bruto') is None:
		return bad_request()

	if json.get('estatus') is None:
		return bad_request()

	tarea = (json['peso_bruto'], json['peso_tara'], json['peso_neto'], json['num_pase'])
	status = json['estatus']
	pase = json['num_pase']
	peso2 = (json['peso_bruto'], json['peso_neto'], json['num_pase'])
	print(tarea)
	#try:
	if status == '2':
		control_db.insertar_datos(tarea, "romana peso")
		control_db.update((status, pase), "romana peso 2")
		num_guia = control_db.seleccionar_fila(pase, "seleccionar")
		num_guia = num_guia.fetchone()
		print(num_guia)
		num_guia = num_guia[0]
		print(num_guia)
		control_db.update((status,num_guia), "act status")
		return response(tarea)
	elif status == '4':
		control_db.update(peso2, "romana peso 3")
		control_db.update((status, pase), "romana peso 2")
		num_guia = control_db.seleccionar_fila(pase, "seleccionar")
		num_guia = num_guia.fetchone()
		num_guia = num_guia[0]
		control_db.update((status,num_guia), "act status")
		return response(tarea)
	#except:
	#	return bad_request()
	return bad_request()

def serialize(nombre, placa, transporte, area, capacidad, peso):
  return{
    'nombre': nombre,
    'placa': placa,
    'transporte': transporte,
    'area': area,
    'capacidad': capacidad,
    'peso': peso
  }


if __name__ == "__main__":
	#url_web = 'Corimon.pinturas.produccion.com:8000'
	#app.config['SERVER_NAME'] = url_web
	app.run(debug=True, port=8000, host="0.0.0.0")