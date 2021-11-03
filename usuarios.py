import sqlite3



#conexion
conexion= sqlite3.connect('C:\\Users\\Corimon\\OneDrive - Corimon\\CORIMON\\CRP\\ROMANA CRP\\PLATAFORMA\\SERVIDOR_PESAJE\\static\\db\\usuarios.db')

#seleccionar cursor
consulta= conexion.cursor()

#insersiom 

sql= """
CREATE TABLE IF NOT EXISTS usuarios(
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
usuario VARCHAR(20) NOT NULL,
nombre VARCHAR(20) NOT NULL,
apellido VARCHAR(20) NOT NULL,
cedula INTEGER NOT NULL UNIQUE,
ficha INTEGER NOT NULL,
password VARCHAR(66) NOT NULL,
email VARCHAR(50) NOT NULL,
area VARCHAR(20) NOT NULL)"""

#EJECUTAR CONSULTA
if(consulta.execute(sql)): 
	print("registrado")
	
else: 
	print("no registrado")
	

#fin de consulta
conexion.commit()

#cerrar conexion
conexion.close()