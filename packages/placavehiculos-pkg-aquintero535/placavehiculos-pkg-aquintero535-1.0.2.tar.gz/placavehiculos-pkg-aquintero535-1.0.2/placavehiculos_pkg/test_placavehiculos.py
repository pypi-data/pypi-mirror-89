# encoding: utf-8

import unittest
import placavehiculos

class TestPlacaVehiculos(unittest.TestCase):
	
	def test_comprobarPlacaValida(self):
		self.assertIsInstance(
		placavehiculos.Vehiculo.comprobarPlaca("338978"),
		placavehiculos.Vehiculo)
		
		self.assertIsInstance(
		placavehiculos.Vehiculo.comprobarPlaca("BD8976"),
		placavehiculos.Vehiculo)
		
		self.assertIsInstance(
		placavehiculos.Vehiculo.comprobarPlaca("HS8976"),
		placavehiculos.Vehiculo)
		
		
	def test_comprobarPlaca(self):
		self.assertEqual(
		placavehiculos.Vehiculo.comprobarPlaca("888769").placa,
		"888769")
		
		self.assertEqual(
		placavehiculos.Vehiculo.comprobarPlaca("KJ8976").placa,
		"KJ8976")
		
		self.assertEqual(
		placavehiculos.Vehiculo.comprobarPlaca("F94516").placa,
		"F94516")
	
	def test_comprobarTipoVehiculo(self):
		self.assertEqual(
		placavehiculos.Vehiculo.comprobarPlaca("TA9865").tipoVehiculo,
		"Taxi")
		
		self.assertEqual(
		placavehiculos.Vehiculo.comprobarPlaca("MF6487").tipoVehiculo,
		"Motocicleta")
		
		self.assertEqual(
		placavehiculos.Vehiculo.comprobarPlaca("MB3345").tipoVehiculo,
		"Metrobus")
		
		self.assertEqual(
		placavehiculos.Vehiculo.comprobarPlaca("GO7654").tipoVehiculo,
		"Vehículo gubernamental")
		
		self.assertEqual(
		placavehiculos.Vehiculo.comprobarPlaca("J83256").tipoVehiculo,
		"Vehículo convencional")
		

if __name__ == "__main__":
	unittest.main()
