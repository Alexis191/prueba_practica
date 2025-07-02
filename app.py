from librodiario import LibroDiario

libro = LibroDiario()

#Exportar resumen
#libro.agregar_transaccion('2025-06-19', 'Venta de disco SSD', 80, 'InGrEso') 
#libro.agregar_transaccion('2025-06-18', 'Compra de teclado Polaroid', 50, 'EGreSO')  
#libro.agregar_transaccion('2025-06-19', 'Venta de pantalla ENV', 200, 'ingreso') 
#libro.agregar_transaccion('2025-06-16', 'Compra de mouse Logitech', 100, 'egreso') 
#libro.exportar_resumen("resumen_contable.txt")

# Cargar desde archivo csv
libro.cargar_transacciones_desde_archivo("transacciones.csv")
print(libro.calcular_resumen())


#Probar código sin archivo csv
#libro.agregar_transaccion('2025-06-19', 'Venta de disco SSD', 80, 'InGrEso') 
#libro.agregar_transaccion('2025-06-18', 'Compra de teclado Polaroid', -50, 'EGreSO')  
#libro.agregar_transaccion('19-06-2025', 'Venta de pantalla ENV', 200, 'ingreso') 
#libro.agregar_transaccion('2025-06-16', 'Compra de mouse Logitech', 100, 'gasto')  
#print(libro.calcular_resumen())