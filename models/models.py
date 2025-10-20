from datetime import datetime
from typing import List, Optional

class Producto:
    def __init__(self, id: int, nombre: str, precio: float, categoria: str = ""):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.disponible = True
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio:,.0f}"

class ItemPedido:
    def __init__(self, producto: Producto, cantidad: int):
        self.producto = producto
        self.cantidad = cantidad
        self.subtotal = producto.precio * cantidad
    
    def calcular_subtotal(self):
        """Recalcula el subtotal basado en cantidad y precio"""
        self.subtotal = self.producto.precio * self.cantidad
    
    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad} = ${self.subtotal:,.0f}"

class Cliente:
    def __init__(self, nit: str = "", nombre: str = "", direccion: str = ""):
        self.nit = nit
        self.nombre = nombre
        self.direccion = direccion

class Impuesto:
    def __init__(self, nombre: str, porcentaje: float, base: float):
        self.nombre = nombre
        self.porcentaje = porcentaje
        self.base = base
        self.valor = base * (porcentaje / 100)

class FormaPago:
    def __init__(self, tipo: str, valor: float):
        self.tipo = tipo  # "CONTADO", "Puntos JV", "APP JUANVALDEZ"
        self.valor = valor

class Pedido:
    def __init__(self, numero_pedido: str):
        self.numero_pedido = numero_pedido
        self.items: List[ItemPedido] = []
        self.fecha = datetime.now()
        self.estado = "PENDIENTE"  # PENDIENTE, EN_PREPARACION, LISTO, ENTREGADO
        self.cliente = Cliente()
        self.subtotal = 0.0
        self.impuestos: List[Impuesto] = []
        self.total_impuestos = 0.0
        self.total = 0.0
        self.formas_pago: List[FormaPago] = []
        
    def agregar_item(self, producto: Producto, cantidad: int):
        for item in self.items:
            if item.producto.id == producto.id:
                item.cantidad += cantidad
                item.subtotal = item.producto.precio * item.cantidad
                self.calcular_totales()
                return
        
        nuevo_item = ItemPedido(producto, cantidad)
        self.items.append(nuevo_item)
        self.calcular_totales()
    
    def remover_item(self, producto_id: int):
        self.items = [item for item in self.items if item.producto.id != producto_id]
        self.calcular_totales()
    
    def calcular_totales(self):
        self.subtotal = sum(item.subtotal for item in self.items)
        
        # Calcular IVA 19%
        if self.subtotal > 0:
            iva_base = self.subtotal
            iva_19 = Impuesto("Iva 19%", 19.0, iva_base)
            self.impuestos = [iva_19]
            self.total_impuestos = sum(imp.valor for imp in self.impuestos)
        else:
            self.impuestos = []
            self.total_impuestos = 0.0
        
        self.total = self.subtotal + self.total_impuestos
    
    def agregar_forma_pago(self, tipo: str, valor: float):
        self.formas_pago.append(FormaPago(tipo, valor))
    
    def total_pagado(self) -> float:
        return sum(pago.valor for pago in self.formas_pago)
    
    def cambio(self) -> float:
        return max(0, self.total_pagado() - self.total)

class Factura:
    def __init__(self, numero: str, pedido: Pedido):
        self.numero = numero
        self.pedido = pedido
        self.fecha_facturacion = datetime.now()
        self.caja_numero = 1
        
    def obtener_datos_empresa(self):
        return {
            "nombre": "URBAN VIVES",
            "tienda": "CAFETERIA URBAN VIVES",
            "direccion": "Calle Principal Centro",
            "nit": "NIT:900.123.456-7"
        }