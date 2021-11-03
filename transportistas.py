import sqlite3



#conexion
conexion= sqlite3.connect('C:\\Users\\Corimon\\OneDrive - Corimon\\CORIMON\\CRP\\ROMANA CRP\\PLATAFORMA\\SERVIDOR_PESAJE\\static\\db\\transportistas.db')

#seleccionar cursor
consulta= conexion.cursor()

#insersiom 

sql= """
CREATE TABLE IF NOT EXISTS conductores(
cedula INTEGER PRIMARY KEY NOT NULL,
nombre VARCHAR(20) NOT NULL,
telefono VARCHAR(20) NOT NULL,
transporte VARCHAR(20) NOT NULL,
explicencia VARCHAR(66) NOT NULL,
expsalud VARCHAR(66) NOT NULL)"""

sql2= """
CREATE TABLE IF NOT EXISTS vehiculos(
placa VARCHAR(10) PRIMARY KEY NOT NULL,
Marca VARCHAR(20) NOT NULL,
modelo VARCHAR(20) NOT NULL,
clasificacion VARCHAR(20) NOT NULL,
transporte VARCHAR(20) NOT NULL)"""

sql3= """
CREATE TABLE IF NOT EXISTS coordinadores(
cedula INTEGER PRIMARY KEY NOT NULL,
nombre VARCHAR(20) NOT NULL,
telefono VARCHAR(20) NOT NULL,
transporte VARCHAR(20) NOT NULL,
direccion VARCHAR(20) NOT NULL)"""

#EJECUTAR CONSULTA
if(consulta.execute(sql)): 
	print("tabla conductores creada con exito")
else: 
	print("No se a creado tabla conductores")

if(consulta.execute(sql2)):
	print("tabla vehiculo creada")
else:
	print("No se ha creada tabla vehiculos")

if(consulta.execute(sql3)):
	print("tabla coordinadores creada")
else:
	print("No se ha creada tabla vehiculos")


#fin de consulta
conexion.commit()

#cerrar conexion
conexion.close()