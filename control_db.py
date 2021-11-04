import sqlite3
from sqlite3 import Error

"""-----------UBICACIONES DE LAS BASES DE DATOS------------------------"""
usuarios_db = r'C:\\Users\\Corimon\\OneDrive - Corimon\\CORIMON\\CRP\\ROMANA CRP\\PLATAFORMA\\SERVIDOR_PESAJE\\static\\db\\usuarios.db'
lista_pase_db = r'C:\\Users\\Corimon\\OneDrive - Corimon\\CORIMON\\CRP\\ROMANA CRP\\PLATAFORMA\\SERVIDOR_PESAJE\\static\\db\\lista_pase.db'
transportistas_db = r'C:\\Users\\Corimon\\OneDrive - Corimon\\CORIMON\\CRP\\ROMANA CRP\\PLATAFORMA\\SERVIDOR_PESAJE\\static\\db\\transportistas.db'
procesos = r'C:\\Users\\Corimon\\OneDrive - Corimon\\CORIMON\\CRP\\ROMANA CRP\\PLATAFORMA\\SERVIDOR_PESAJE\\static\\db\\procesos.db'

def crear_conexion(db_file):
	"""-----CREAR CONEXION CON BASE DE DATOS----"""
	conn = None
	try:
		conn = sqlite3.connect(db_file)
	except Error as e:
		print(e)
	return conn

def cerrar_conexion(conexion):
	"""-----CERRAR CONEXION CON BASES DE DATOS----"""
	
	conexion.commit()
	conexion.close()

def insertar_datos(argumentos, titulo):
	"""-----INSERTAR DATOS EN UNA BASE DE DATOS----"""
	sentencia , ubicacion = sentenciasSQL(titulo)
	conexion = crear_conexion(ubicacion)
	consulta = conexion.cursor()
	if (consulta.execute(sentencia, argumentos)):
		estado = True
	else:
		estado = False
	consulta.close()
	conexion.commit()
	conexion.close()
	return estado

def seleccionar_tabla(titulo):
	"""-----SELECCIONAR TABLA EN UNA BASE DE DATOS----"""
	sentencia, ubicacion = sentenciasSQL(titulo)
	conexion = crear_conexion(ubicacion)
	consulta = conexion.cursor()
	rows = consulta.execute(sentencia)
	return rows

def seleccionar_fila(fila, titulo):
	"""----SELECCION DE UNA FILA EN UNA BASE DE DATOS-----"""
	sentencia, ubicacion = sentenciasSQL(titulo)
	conexion = crear_conexion(ubicacion)
	consulta = conexion.cursor()
	row = consulta.execute(sentencia, (fila,))
	return row

def update(dato, titulo):
	"""----ACTUALIZAR DATO EN UNA BASE DE DATOS----"""
	sentencia, ubicacion = sentenciasSQL(titulo)
	conexion = crear_conexion(ubicacion)
	consulta = conexion.cursor()
	consulta.execute(sentencia, dato)
	conexion.commit()
	#conexion.close()

def seleccionar_dato_tabla(dato, titulo):
	sql = """
	SELECT * FROM vehiculos WHERE transporte = '"""+dato+"""'
	"""
	database = transportistas_db
	conexion = crear_conexion(database)
	consulta = conexion.cursor()
	rows = consulta.execute(sql)
	return rows

def eliminar_fila(fila, titulo):
	"""----ELIMINAR DE UNA FILA EN UNA BASE DE DATOS-----"""
	sentencia, ubicacion = sentenciasSQL(titulo)
	conexion = crear_conexion(ubicacion)
	consulta = conexion.cursor()
	consulta.execute(sentencia, (fila,))
	conexion.commit()

def sentenciasSQL(titulo):
	"""----FUNCION PARA SELECCIONAR SENTENCIA SQL DE ACUERDO AL TITULO DE LA PAGINA-----"""
	if titulo == "registro usuarios":
		sql = """
		INSERT INTO usuarios(usuario,nombre,apellido,cedula,ficha,password,email,area)
		values(?,?,?,?,?,?,?,?)"""
		database = usuarios_db
	elif titulo == "registro conductor":
		sql = """
		INSERT INTO conductores(cedula,nombre,telefono,transporte,explicencia,expsalud)
		values(?,?,?,?,?,?)"""
		database = transportistas_db
	elif titulo == "preingreso":
		sql = """
		INSERT INTO preingresodis(numguia, nombre, cedula, telefono, empresa, marca, modelo, clasificacion, placa, motivo, fecha, pesoguia, status)
		values(?,?,?,?,?,?,?,?,?,?,?,?,?)"""
		database = lista_pase_db
	elif titulo == "registro vehiculo":
		sql = """
		INSERT INTO vehiculos(placa, Marca, modelo, clasificacion, transporte)
		values(?,?,?,?,?)"""
		database = transportistas_db
	elif titulo == "distribucion lista" or titulo == "vigilancia lista":
		sql ="""
		SELECT * FROM preingresodis ORDER BY numguia DESC"""
		database = lista_pase_db
	elif titulo == "distribucion reportes":
		sql = """
		SELECT * FROM distribucion ORDER BY numguia DESC"""
		database = procesos
	elif titulo == "distribucion" or titulo == "vigilancia":
		sql = """
		SELECT * FROM preingresodis WHERE  numguia = ?"""
		database = lista_pase_db
	elif titulo == "cambio clave":
		sql = """
		UPDATE usuarios
		SET password = ?
		WHERE usuario = ?"""
		database = usuarios_db
	elif titulo == "index":
		sql = """
		SELECT * FROM usuarios WHERE usuario = ? limit 1
		"""
		database =usuarios_db
	elif titulo == "conductores":
		sql = """
		SELECT * FROM conductores"""
		database = transportistas_db
	elif titulo == "vehiculos":
		sql = """
		SELECT * FROM vehiculos"""
		database = transportistas_db
	elif titulo == "lista usuarios":
		sql = """
		SELECT * FROM usuarios"""
		database = usuarios_db
	elif titulo == "preingreso vehiculos":
		sql = """
		SELECT * FROM conductores WHERE cedula = ?"""
		database = transportistas_db
	elif titulo == "preingreso fin":
		sql = """
		SELECT * FROM vehiculos WHERE placa = ?"""
		database = transportistas_db
	elif titulo == "vigilancia ingreso":
		sql = """
		INSERT INTO distribucion(numguia, direccion, ingresa_con, num_pase, estatus, date_registro)
		values(?,?,?,?,?,?)"""
		database = procesos
	elif titulo == "distribucion ingreso":
		sql = """
		UPDATE distribucion
		SET carga_vehiculo = ?, carga_verificada = ?, reconteo = ?, estatus = ?, user_carga = ?, date_carga= ?, user_verificar= ?, date_verificar= ?
		WHERE numguia = ?"""
		database = procesos
	elif titulo == "proceso":
		sql = """
		SELECT * FROM distribucion WHERE numguia = ?"""
		database = procesos
	elif titulo == "proceso distribucion":
		sql = """
		UPDATE preingresodis
		SET status = ?
		WHERE numguia = ?"""
		database = lista_pase_db
	elif titulo == "proceso distribucion num pase":
		sql = """
		UPDATE preingresodis
		SET num_pase = ?
		WHERE numguia = ?"""
		database = lista_pase_db
	elif titulo == "registro vehiculo editar":
		sql = """
		UPDATE vehiculos
		SET Marca = ?, modelo = ?, clasificacion = ?, transporte = ?
		WHERE placa = ?"""
		database = transportistas_db
	elif titulo == "conductor editar":
		sql = """
		UPDATE conductores
		SET nombre = ?, telefono = ?, transporte = ?, explicencia = ?, expsalud = ?
		WHERE cedula =? """
		database = transportistas_db
	elif titulo == "usuario editar":
		sql ="""
		UPDATE usuarios
		SET usuario = ?, nombre = ?, apellido = ?, ficha = ?, email = ?, area = ?
		WHERE cedula = ?"""
		database = usuarios_db
	elif titulo == "seleccionar user":
		sql = """
		SELECT * FROM usuarios  WHERE cedula = ?"""
		database = usuarios_db
	elif titulo == "registro coordinador":
		sql = """
		INSERT INTO coordinadores(cedula, nombre, telefono, transporte, direccion, seleccionar)
		values(?,?,?,?,?,?)"""
		database = transportistas_db
	elif titulo == "coordinadores":
		sql = """
		SELECT * FROM coordinadores"""
		database = transportistas_db
	elif titulo == "preingreso coordinadores":
		sql = """
		SELECT * FROM coordinadores WHERE cedula = ?"""
		database = transportistas_db
	elif titulo == "coordinador editar":
		sql = """
		UPDATE coordinadores
		SET nombre = ?, telefono = ?, transporte = ?, direccion = ?
		WHERE cedula = ? """
		database = transportistas_db
	elif titulo == "seleccionar coordinador":
		sql = """
		SELECT * FROM coordinadores WHERE cedula = ?"""
		database = transportistas_db
	elif titulo == "preingreso coordinador":
		sql = """
		INSERT INTO preingresocoordinador(cedula, nombre, telefono, empresa, direccion, fecha, tipo_in, fecha_limite)
		values(?,?,?,?,?,?,?,?)"""
		database = lista_pase_db
	elif titulo == "coordinadores preingreso":
		sql = """
		SELECT * FROM preingresocoordinador"""
		database = lista_pase_db
	elif titulo == "distribucion coordinador":
		sql = """
		SELECT * FROM preingresocoordinador WHERE cedula = ?"""
		database = lista_pase_db
	elif titulo == "vigilancia fin":
		sql = """
		UPDATE distribucion
		SET estatus = ?, date_reconteo = ?, repartos = ?, bultos = ?
		WHERE numguia = ?
		"""
		database = procesos
	elif titulo == "Ficha":
		sql = """
		SELECT * FROM preingresocoordinador WHERE id = ?"""
		database = lista_pase_db
	elif titulo == "cancelar preingreso":
		sql = """
		DELETE FROM preingresodis WHERE numguia = ?"""
		database = lista_pase_db
	elif titulo == "cancelar ingresar":
		sql = """
		INSERT INTO alarmas(fecha_reportado, motivo_alarma, num_guia, cedula, placa, fecha_creado)
		values(?,?,?,?,?,?)"""
		database = procesos
	elif titulo == "lista alarmas":
		sql = """
		SELECT * FROM alarmas"""
		database = procesos
	elif titulo == "romana":
		sql = """
		SELECT num_pase, cedula, nombre, empresa, clasificacion, placa, motivo, pesoguia, status FROM preingresodis WHERE fecha = date('now')
		"""
		database = lista_pase_db
	elif titulo == "conductor delete":
		sql = """
		DELETE FROM conductores WHERE cedula = ?"""
		database = transportistas_db
	elif titulo == "vehiculo delete":
		sql = """
		DELETE FROM vehiculos WHERE placa = ?"""
		database = transportistas_db
	elif titulo == "coordinador delete":
		sql = """
		DELETE FROM coordinadores WHERE cedula = ?"""
		database = transportistas_db
	elif titulo == "romana peso 2":
		sql ="""
		UPDATE distribucion
		SET estatus = ?
		WHERE num_pase = ?
		"""
		database = procesos
	elif titulo == "romana peso":
		sql ="""
		INSERT INTO romana(peso_bruto, peso_tara, peso_neto, num_pase)
		values(?,?,?,?)"""
		database = procesos
	elif titulo == "romana peso 3":
		sql = """
		UPDATE romana
		SET peso_bruto = ?, peso_neto = ?
		WHERE num_pase = ?
		"""
		database = procesos
	elif titulo == "seleccionar":
		sql = """
		SELECT numguia FROM distribucion WHERE num_pase = ?
		"""
		database = procesos
	elif titulo == "act status":
		sql ="""
		UPDATE preingresodis
		SET status = ?
		WHERE numguia = ?
		"""
		database = lista_pase_db
	return sql, database