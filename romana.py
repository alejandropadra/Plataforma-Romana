import sqlite3

#conexion
conexion= sqlite3.connect('C:\\Users\\Corimon\\OneDrive - Corimon\\CORIMON\\CRP\\ROMANA CRP\\PLATAFORMA\\SERVIDOR_PESAJE\\static\\db\\procesos.db')

#seleccionar cursor
consulta= conexion.cursor()

#
sql= """
CREATE TABLE IF NOT EXISTS romana(
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
peso_bruto INTEGER,
peso_tara INTEGER,
peso_neto INTEGER,
num_pase INTEGER NOT NULL UNIQUE,
FOREIGN KEY (num_pase) REFERENCES procesos(num_pase))"""

#EJECUTAR CONSULTA
if(consulta.execute(sql)): 
	print("Tabla romana creada")
	
else: 
	print("no se ha creado la tabla")
	

#fin de consulta
conexion.commit()

#cerrar conexion
conexion.close()