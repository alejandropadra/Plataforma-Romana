import os

class Config(object):
	SECRET_KEY = 'mi_clave'

class DevelopmentConfig(Config):
	DEBUG = True

class DireccionDb():
	USUARIOS = r'C:\\Users\\Corimon\\OneDrive - Corimon\\CORIMON\\CRP\\ROMANA CRP\\PLATAFORMA\\SERVIDOR_PESAJE\\static\\db\\usuarios.db'
	LISTA_PASE = r'C:\\Users\\Corimon\\OneDrive - Corimon\\CORIMON\\CRP\\ROMANA CRP\\PLATAFORMA\\SERVIDOR_PESAJE\\static\\db\\lista_pase.db'
	CONTENIDO_CARGA = r'C:\\Users\\Corimon\\OneDrive - Corimon\\CORIMON\\CRP\\ROMANA CRP\\PLATAFORMA\\SERVIDOR_PESAJE\\static\\db\\contenido_carga.db'