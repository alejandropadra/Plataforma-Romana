import sqlite3

#conexion
conexion= sqlite3.connect('C:\\Users\\Corimon\\OneDrive - Corimon\\CORIMON\\CRP\\ROMANA CRP\\PLATAFORMA\\SERVIDOR_PESAJE\\static\\db\\procesos.db')

#seleccionar cursor
consulta= conexion.cursor()

sql = """
CREATE TABLE IF NOT EXISTS distribucion(
numguia INTEGER NOT NULL UNIQUE,
direccion VARCHAR(20) NOT NULL,
ingresa_con VARCHAR(60) NOT NULL,
num_pase INTEGER PRIMARY KEY NOT NULL,
carga_vehiculo BOOLEAN,
carga_verificada BOOLEAN,
reconteo BOOLEAN,
estatus INTEGER NOT NULL,
user_carga VARCHAR(20),
date_carga VARCHAR(20),
user_verificar VARCHAR(20),
date_verificar VARCHAR(20),
date_reconteo VARCHAR(20),
date_registro VARCHAR(20),
repartos INTEGER,
bultos INTEGER)"""

sql2 = """
CREATE TABLE IF NOT EXISTS alarmas(
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
fecha_reportado VARCHAR(20),
motivo_alarma VARCHAR(20),
num_guia VARCHAR(20),
cedula INTEGER,
placa VARCHAR(20),
fecha_creado VARCHAR(20))"""


if(consulta.execute(sql)):
	print("registrado vigilancia")
else:
	print("no registrado")

if(consulta.execute(sql2)):
	print("registrado alarmas")
else:
	print("no registrado alarmas")


#fin de consulta
conexion.commit()

#cerrar conexion
conexion.close()