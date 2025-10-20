#!/usr/bin/env python3
"""
Script de prueba para URBAN VIVES
Genera una factura de muestra con el nuevo menú y configuración
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.models import Producto, Pedido, Cliente, Factura
from utils.factura_generator import GeneradorFacturas
from database.db_manager import DatabaseManager

def main():
    print("=== URBAN VIVES - Prueba del Sistema ===")
    print("Generando factura de prueba con el nuevo menú...")
    
    # Inicializar base de datos
    db = DatabaseManager()
    
    # Obtener algunos productos del nuevo menú
    productos = db.obtener_productos()
    print(f"\nProductos disponibles: {len(productos)}")
    
    # Mostrar algunos productos por categoría
    print("\n--- MUESTRA DEL MENÚ URBAN VIVES ---")
    categorias = {}
    for producto in productos[:20]:  # Mostrar primeros 20 productos
        categoria = producto.categoria
        if categoria not in categorias:
            categorias[categoria] = []
        categorias[categoria].append(producto)
    
    for categoria, items in categorias.items():
        print(f"\n📍 {categoria.upper()}:")
        for item in items[:5]:  # Mostrar máximo 5 por categoría
            print(f"  • {item.nombre} - ${item.precio:,}")
    
    # Crear pedido de prueba
    numero_pedido = db.generar_numero_pedido()
    pedido = Pedido(numero_pedido)
    
    # Agregar algunos productos al pedido
    if len(productos) > 0:
        # Latte
        pedido.agregar_item(productos[3], 1)  # Latte $8,000
        # Cappuccino  
        pedido.agregar_item(productos[4], 2)  # Cappuccino $8,500 x2
        # Muffin
        if len(productos) > 29:
            pedido.agregar_item(productos[29], 1)  # Muffin $5,500
    
    # Agregar cliente
    cliente = Cliente("1005569038", "CLIENTE EJEMPLO", "Calle 123 #45-67")
    pedido.cliente = cliente
    
    # Agregar formas de pago
    pedido.agregar_forma_pago("TARJETA", pedido.total)
    
    print(f"\n--- RESUMEN DEL PEDIDO ---")
    print(f"Número: {pedido.numero_pedido}")
    print(f"Cliente: {pedido.cliente.nombre}")
    print(f"Items:")
    for item in pedido.items:
        print(f"  • {item.producto.nombre} x{item.cantidad} = ${item.subtotal:,}")
    print(f"Subtotal: ${pedido.subtotal:,}")
    print(f"IVA 19%: ${pedido.total_impuestos:,}")
    print(f"TOTAL: ${pedido.total:,}")
    
    # Generar factura
    numero_factura = db.generar_numero_factura()
    factura = Factura(numero_factura, pedido)
    
    # Generar archivos
    generador = GeneradorFacturas()
    
    # PDF
    archivo_pdf = generador.generar_factura_pdf(factura)
    print(f"\n✓ PDF generado: {archivo_pdf}")
    
    # Texto
    contenido_texto = generador.generar_factura_texto(factura)
    
    # Mostrar vista previa de la factura
    print("\n" + "="*60)
    print("VISTA PREVIA - FACTURA URBAN VIVES")
    print("="*60)
    print(contenido_texto)
    print("="*60)
    
    print(f"\n🎉 Sistema URBAN VIVES funcionando correctamente!")
    print(f"📁 Archivos guardados en: facturas_generadas/")
    print(f"🏪 Empresa: URBAN VIVES")
    print(f"💰 IVA: 19%")
    print(f"💳 Métodos de pago: Efectivo, Transferencia, Tarjeta")
    print(f"☕ Menú: {len(productos)} productos estilo café premium")

if __name__ == "__main__":
    main()