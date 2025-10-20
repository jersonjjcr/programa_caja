#!/usr/bin/env python3
"""
Sistema de Cafetería - URBAN VIVES
Sistema completo de ventas y pedidos para cafetería

Características:
- Gestión de productos y precios
- Interfaz de caja para tomar pedidos
- Cálculo automático de impuestos (IVA 19%)
- Múltiples métodos de pago (Efectivo, Transferencia, Tarjeta)
- Generación e impresión de facturas
- Sistema de cocina para preparar pedidos
- Base de datos SQLite para persistencia

Autor: Sistema desarrollado para URBAN VIVES
Fecha: 2025
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from gui.interfaz_moderna import InterfazCajaModerna
    from database.db_manager import DatabaseManager
except ImportError as e:
    print(f"Error al importar módulos: {e}")
    sys.exit(1)

def main():
    """Función principal del sistema"""
    try:
        # Verificar que se puede acceder a la base de datos
        db = DatabaseManager()
        print("✓ Base de datos inicializada correctamente")
        
        # Crear ventana principal
        root = tk.Tk()
        
        # Configurar el tema
        try:
            root.tk.call("source", "azure.tcl")
            root.tk.call("set_theme", "light")
        except:
            pass  # Si no se puede cargar el tema, usar el por defecto
        
        # Inicializar la aplicación
        app = InterfazCajaModerna(root)
        
        print("✓ Sistema de cafetería iniciado correctamente")
        print("✓ Interfaz de caja lista")
        print("\n=== URBAN VIVES - Sistema de Cafetería ===")
        print("Funcionalidades disponibles:")
        print("• Gestión de productos (Menú completo estilo café premium)")
        print("• Toma de pedidos")
        print("• Cálculo de impuestos (IVA 19%)")
        print("• Procesamiento de pagos (Efectivo, Transferencia, Tarjeta)")
        print("• Generación de facturas")
        print("• Sistema de cocina")
        print("==========================================\n")
        
        # Ejecutar la aplicación
        root.mainloop()
        
    except Exception as e:
        error_msg = f"Error al iniciar el sistema: {str(e)}"
        print(f"❌ {error_msg}")
        
        # Mostrar error en ventana si es posible
        try:
            root = tk.Tk()
            root.withdraw()  # Ocultar ventana principal
            messagebox.showerror("Error del Sistema", error_msg)
        except:
            pass
        
        sys.exit(1)

if __name__ == "__main__":
    main()