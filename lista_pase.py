import sqlite3



#conexion
conexion= sqlite3.connect('C:\\Users\\Corimon\\OneDrive - Corimon\\CORIMON\\CRP\\ROMANA CRP\\PLATAFORMA\\SERVIDOR_PESAJE\\static\\db\\lista_pase.db')

#seleccionar cursor
consulta= conexion.cursor()

#insersiom 

sql= """
CREATE TABLE IF NOT EXISTS preingresodis(
numguia INTEGER PRIMARY KEY NOT NULL,
nombre VARCHAR(20) NOT NULL,
cedula INTEGER NOT NULL,
telefono VARCHAR(20) NOT NULL,
empresa VARCHAR(20) NOT NULL,
marca VARCHAR(20) NOT NULL,
modelo VARCHAR(20) NOT NULL,
clasificacion VARCHAR(20) NOT NULL,
placa VARCHAR(20) NOT NULL,
motivo VARCHAR(66) NOT NULL,
fecha VARCHAR(20) NOT NULL,
pesoguia DECIMAL NOT NULL,
status INTEGER NOT NULL,
acompanante VARCHAR(66))"""

sql2= """
CREATE TABLE IF NOT EXISTS preingresocoordinador(
id INTEGER PRIMARY KEY NOT NULL,
cedula INTEGER NOT NULL,
nombre VARCHAR(20) NOT NULL,
telefono VARCHAR(20) NOT NULL,
empresa VARCHAR(20) NOT NULL,
direccion VARCHAR(20) NOT NULL,
fecha VARCHAR(20) NOT NULL,
tipo_in VARCHAR(20) NOT NULL,
fecha_limite VARCHAR(20) NOT NULL)"""

#EJECUTAR CONSULTA
if(consulta.execute(sql)): 
	print("registrado")
	
else: 
	print("no registrado")

#EJECUTAR CONSULTA
if(consulta.execute(sql2)): 
	print("registrado coordinador")
	
else: 
	print("no registrado")

#fin de consulta
conexion.commit()

#cerrar conexion
conexion.close()