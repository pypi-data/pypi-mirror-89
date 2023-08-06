# encoding: utf-8
## Adrián Quintero

import re

class Vehiculo:
	
	placa = ""
	tipoVehiculo = ""
	
	def __init__(self, placa, tipoVehiculo):
		self.placa = placa
		self.tipoVehiculo = tipoVehiculo
	
	def comprobarPlaca(codigoPlaca):
		if re.match("\w\w\d\d\d\d\Z", codigoPlaca):
			if re.match("T\w\d\d\d\d\Z", codigoPlaca):
				vehiculo = Vehiculo(codigoPlaca, "Taxi")
				return vehiculo
			elif re.match("M[^B]\d\d\d\d\Z", codigoPlaca):
				vehiculo = Vehiculo(codigoPlaca, "Motocicleta")
				return vehiculo
			elif re.match("MB\d\d\d\d\Z", codigoPlaca):
				vehiculo = Vehiculo(codigoPlaca, "Metrobus")
				return vehiculo
			elif re.match("GO\d\d\d\d\Z", codigoPlaca):
				vehiculo = Vehiculo(codigoPlaca, "Vehículo gubernamental")
				return vehiculo
			else:
				vehiculo = Vehiculo(codigoPlaca, "Vehículo convencional")
				return vehiculo
		else:
			return None
		
## Función principal ##
def ingresarPlaca():
	while (True):
		codigoPlaca = input("Introduzca la matrícula de la placa de su vehículo: ")
		print("\n")
		if (codigoPlaca == 'salir'):
			break
		else:
			vehiculo = Vehiculo.comprobarPlaca(codigoPlaca)
			if (vehiculo != None):
				print("Esta placa es válida: "+vehiculo.placa)
				print("Esta placa pertenece a: "+vehiculo.tipoVehiculo)
			else:
				print("Esta placa no es válida")
		print("\n")
		
if __name__ == "__main__":
	ingresarPlaca()
