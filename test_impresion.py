#!/usr/bin/env python3
"""
Script de prueba para el sistema de impresión de facturas
Genera una factura de prueba y la imprime
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.models import Producto, Pedido, Cliente, Factura
from utils.factura_generator import GeneradorFacturas
from database.db_manager import DatabaseManager

def crear_factura_prueba():
    """Crea una factura de prueba para verificar la impresión"""
    
    # Crear productos de prueba
    cafe = Producto(1, "Café Drip Sierra Pie", 17900, "Café")
    
    # Crear pedido de prueba
    pedido = Pedido("APP-TJV1300159")
    pedido.agregar_item(cafe, 1)
    
    # Agregar cliente
    cliente = Cliente("1005569038", "JERSON CONTRERAS", "None")
    pedido.cliente = cliente
    
    # Agregar forma de pago
    pedido.agregar_forma_pago("APP JUANVALDEZ", 14436)
    pedido.agregar_forma_pago("Puntos JV", 3464)
    
    # Crear factura
    factura = Factura("F314-64456", pedido)
    
    return factura

def main():
    print("=== Prueba del Sistema de Impresión ===")
    print("Generando factura de prueba...")
    
    # Crear generador
    generador = GeneradorFacturas()
    
    # Mostrar impresoras disponibles
    print(f"Impresoras disponibles: {generador.obtener_impresoras_disponibles()}")
    
    # Crear factura de prueba
    factura_prueba = crear_factura_prueba()
    
    # Generar PDF
    print("Generando PDF...")
    archivo_pdf = generador.generar_factura_pdf(factura_prueba)
    print(f"PDF generado: {archivo_pdf}")
    
    # Generar texto
    print("Generando archivo de texto...")
    contenido_texto = generador.generar_factura_texto(factura_prueba)
    
    # Mostrar vista previa
    print("\n" + "="*60)
    print("VISTA PREVIA DE LA FACTURA:")
    print("="*60)
    print(contenido_texto)
    print("="*60)
    
    # Preguntar si quiere imprimir
    respuesta = input("\n¿Desea probar la impresión? (s/n): ").lower().strip()
    
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        print("Intentando imprimir...")
        resultado = generador.imprimir_factura(factura_prueba)
        
        if resultado:
            print("✓ Impresión exitosa")
        else:
            print("✗ Error en la impresión")
    else:
        print("Prueba de impresión cancelada")
    
    print("\nPrueba completada. Los archivos se encuentran en la carpeta 'facturas_generadas'")

if __name__ == "__main__":
    main()