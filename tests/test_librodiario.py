import unittest
from librodiario import LibroDiario, MontoInvalidoError
from unittest.mock import patch, mock_open

class TestLibroDiario(unittest.TestCase):
    """Pruebas unitarias para la clase LibroDiario."""

    def setUp(self):
        """Configuración inicial antes de cada prueba."""
        self.libro = LibroDiario()

    def test_agregar_transaccion(self):
        """Prueba agregar una transacción de tipo 'ingreso' y 'egreso'."""
        self.libro.agregar_transaccion("2025-06-15", "Venta de producto", 1000.0, "ingreso")
        self.libro.agregar_transaccion("2025-06-16", "Pago de servicios", 500.0, "egreso")
        
        resumen = self.libro.calcular_resumen()
        
        self.assertEqual(resumen["ingresos"], 1000.0)
        self.assertEqual(resumen["egresos"], 500.0)

    def test_cargar_transacciones_desde_archivo(self):
        """Prueba cargar transacciones desde un archivo CSV simulado."""
        archivo_csv = "2025-06-15;Venta de producto;1000.0;ingreso\n2025-06-16;Pago de servicios;500.0;egreso\n"
        
        with patch("builtins.open", mock_open(read_data=archivo_csv)):
            self.libro.cargar_transacciones_desde_archivo("test_transacciones.csv")

        resumen = self.libro.calcular_resumen()
        
        self.assertEqual(resumen["ingresos"], 1000.0)
        self.assertEqual(resumen["egresos"], 500.0)

    def test_exportar_resumen(self):
        """Prueba exportar el resumen contable a un archivo."""
        self.libro.agregar_transaccion("2025-06-15", "Venta de producto", 1000.0, "ingreso")
        self.libro.agregar_transaccion("2025-06-16", "Pago de servicios", 500.0, "egreso")

        with patch("builtins.open", mock_open()) as mock_file:
            self.libro.exportar_resumen("test_resumen.txt")
            
            mock_file.assert_called_once_with("test_resumen.txt", "w", encoding="utf-8")
            mock_file().write.assert_any_call("Resumen contable:\n")
            mock_file().write.assert_any_call("Total ingresos: 1000.00\n")
            mock_file().write.assert_any_call("Total egresos: 500.00\n")

    def test_resumen_inicial(self):
        """Prueba el resumen contable inicial (debería ser cero en ingresos y egresos)."""
        resumen = self.libro.calcular_resumen()

        self.assertEqual(resumen["ingresos"], 0.0)
        self.assertEqual(resumen["egresos"], 0.0)

if __name__ == '__main__':
    unittest.main()
