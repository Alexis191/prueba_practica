import unittest
from librodiario import LibroDiario

class TestLibro(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.librodiario = LibroDiario("transacciones.csv")

    def test_agregar_transaccion(self):
        resumen = self.analizador.agregar_transaccion()
        self.assertIsInstance(resumen, dict)

    def test_cargar_transacciones_desde_archivo(self):
        resumen = self.analizador.ventas_totales_por_provincia()
        total_provincias = len(resumen)
        self.assertEqual(total_provincias, 24)
