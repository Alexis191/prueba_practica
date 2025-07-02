from datetime import datetime
from typing import List, Dict
import logging
import traceback

#Configuración de logging
logging.basicConfig(
    filename='logs/log_contable.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)

class MontoInvalidoError(Exception):
    """Excepción lanzada cuando el monto es cero o negativo."""
    pass

class LibroDiario:
    """Gestión contable básica de ingresos y egresos."""

    def __init__(self):
        self.transacciones: List[Dict] = []

    def agregar_transaccion(self, fecha: str, descripcion: str, monto: float, tipo: str) -> None:
        """Agrega una transacción con manejo de errores."""

        try:
            #Controla si el tipo es ingreso o egreso.
            if tipo.lower() not in ("ingreso", "egreso"):
                raise ValueError("Tipo de transaccion invalido, debe poner 'ingreso' o 'egreso'.")

            #Controla si el formato correcto de fecha año-mes-día (2025-06-19).
            try:
                fecha_dt = datetime.strptime(fecha, "%Y-%m-%d") 
            except ValueError:
                raise ValueError("Formato de fecha invalido, debe usar el formato: yyyy-mm-dd.")

            #Controla si el monto el mayor o menos a 0.
            if monto <= 0:
                raise MontoInvalidoError("El monto debe ser mayor a cero.")

            #Registra la transacción.
            transaccion = {
                "fecha": fecha_dt,
                "descripcion": descripcion,
                "monto": monto,
                "tipo": tipo.lower()
            }
            self.transacciones.append(transaccion)

            #Registrar transacción exitosa
            logging.info(f"Transaccion registrada: {fecha} | {descripcion} | {monto} | {tipo}")

        except (ValueError, MontoInvalidoError) as e:
            error_line = traceback.format_exc().strip().splitlines()[-1]
            logging.error(f"{e} - Linea: {error_line}")
            print(f"[ERROR] {e}")

    def cargar_transacciones_desde_archivo(self, path: str) -> None:
        """Carga transacciones desde un archivo .csv (separado por ;) y registra errores."""

        try:
            with open(path, "r", encoding="utf-8") as archivo:
                linea_nro = 0
                for linea in archivo:
                    linea_nro += 1
                    partes = linea.strip().split(";")

                    # Verificar que tenga 4 columnas
                    if len(partes) != 4:
                        logging.error(f"Linea {linea_nro}: Formato incorrecto -> {linea.strip()}")
                        continue

                    fecha, descripcion, monto_str, tipo = partes

                    try:
                        monto = float(monto_str)
                        self.agregar_transaccion(fecha, descripcion, monto, tipo)
                    except Exception as e:
                        import traceback
                        error_line = traceback.format_exc().strip().splitlines()[-1]
                        logging.error(f"Linea {linea_nro}: {e} - Linea: {error_line}")

        except FileNotFoundError:
            logging.critical(f"No se encontro el archivo: {path}")
            print(f"[CRITICO] No se encontro el archivo: {path}")

    def calcular_resumen(self) -> Dict[str, float]:
        """Devuelve el resumen total de ingresos y egresos."""
        resumen = {"ingresos": 0.0, "egresos": 0.0}
        for transaccion in self.transacciones:
            if transaccion["tipo"] == "ingreso":
                resumen["ingresos"] += transaccion["monto"]
            else:
                resumen["egresos"] += transaccion["monto"]
        return resumen
    
    def exportar_resumen(self, path: str) -> None:
        """Exporta el resumen contable a un archivo especificado."""
        resumen = self.calcular_resumen()
        try:
            with open(path, "w", encoding="utf-8") as archivo:
                archivo.write("Resumen contable:\n")
                archivo.write(f"Total ingresos: {resumen['ingresos']}\n")
                archivo.write(f"Total egresos: {resumen['egresos']}\n")
            logging.info(f"Resumen exportado correctamente a {path}")
        except Exception as e:
            import traceback
            error_line = traceback.format_exc().strip().splitlines()[-1]
            logging.error(f"Error al exportar resumen: {e} - Línea: {error_line}")
            print(f"[ERROR] No se pudo exportar el resumen: {e}")