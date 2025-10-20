import sqlite3
import os
from datetime import datetime
from typing import List, Optional
from models.models import Producto, Pedido, ItemPedido, Cliente, Factura, FormaPago

class DatabaseManager:
    def __init__(self, db_path: str = "cafeteria.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def connect(self):
        """Establece una conexión persistente"""
        if not self.conn:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        return self.conn
    
    def close(self):
        """Cierra la conexión persistente"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
    
    def init_database(self):
        """Inicializa la base de datos con las tablas necesarias"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de productos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL,
                categoria TEXT DEFAULT '',
                disponible BOOLEAN DEFAULT 1
            )
        ''')
        
        # Migración: agregar columna disponible si no existe
        try:
            cursor.execute("ALTER TABLE productos ADD COLUMN disponible BOOLEAN DEFAULT 1")
            print("✓ Columna 'disponible' agregada a la tabla productos")
        except sqlite3.OperationalError:
            # La columna ya existe
            pass
        
        # Migración: copiar datos de activo a disponible si existe la columna activo
        try:
            cursor.execute("SELECT activo FROM productos LIMIT 1")
            # Si llegamos aquí, la columna activo existe
            cursor.execute("UPDATE productos SET disponible = activo WHERE disponible IS NULL")
            print("✓ Datos migrados de 'activo' a 'disponible'")
        except sqlite3.OperationalError:
            # La columna activo no existe, esto es normal
            pass
        
        # Tabla de clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nit TEXT,
                nombre TEXT,
                direccion TEXT
            )
        ''')
        
        # Tabla de pedidos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_pedido TEXT UNIQUE NOT NULL,
                fecha DATETIME NOT NULL,
                estado TEXT NOT NULL,
                cliente_id INTEGER,
                subtotal REAL NOT NULL,
                total_impuestos REAL NOT NULL,
                total REAL NOT NULL,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            )
        ''')
        
        # Tabla de items de pedido
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items_pedido (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pedido_id INTEGER NOT NULL,
                producto_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (pedido_id) REFERENCES pedidos (id),
                FOREIGN KEY (producto_id) REFERENCES productos (id)
            )
        ''')
        
        # Tabla de formas de pago
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS formas_pago (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pedido_id INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                valor REAL NOT NULL,
                FOREIGN KEY (pedido_id) REFERENCES pedidos (id)
            )
        ''')
        
        # Tabla de facturas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS facturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT UNIQUE NOT NULL,
                pedido_id INTEGER NOT NULL,
                fecha_facturacion DATETIME NOT NULL,
                caja_numero INTEGER NOT NULL,
                FOREIGN KEY (pedido_id) REFERENCES pedidos (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Insertar productos de ejemplo si no existen
        self.insertar_productos_ejemplo()
    
    def insertar_productos_ejemplo(self):
        """Inserta productos de ejemplo si la tabla está vacía"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM productos")
        count = cursor.fetchone()[0]
        
        if count == 0:
            productos_ejemplo = [
                # CAFÉS CLÁSICOS
                ("Espresso Simple", 5000, "Cafés Clásicos"),
                ("Espresso Doble", 7000, "Cafés Clásicos"),
                ("Americano", 6000, "Cafés Clásicos"),
                ("Latte", 8000, "Cafés Clásicos"),
                ("Cappuccino", 8500, "Cafés Clásicos"),
                ("Macchiato", 7500, "Cafés Clásicos"),
                ("Mocha", 9000, "Cafés Clásicos"),
                ("White Mocha", 9000, "Cafés Clásicos"),
                ("Flat White", 9500, "Cafés Clásicos"),
                
                # BEBIDAS FRÍAS Y CON HIELO
                ("Cold Brew", 9000, "Bebidas Frías"),
                ("Iced Latte", 8500, "Bebidas Frías"),
                ("Iced Mocha", 9000, "Bebidas Frías"),
                ("Iced White Mocha", 9000, "Bebidas Frías"),
                ("Caramel Macchiato Frío", 9500, "Bebidas Frías"),
                ("Affogato", 10000, "Bebidas Frías"),
                
                # FRAPPÉS Y BEBIDAS CON CREMA
                ("Frappé de Café Clásico", 9000, "Frappés"),
                ("Mocha Frappé", 10000, "Frappés"),
                ("Caramel Frappé", 10000, "Frappés"),
                ("Cookies & Cream Frappé", 10500, "Frappés"),
                ("Matcha Frappé", 11000, "Frappés"),
                ("Choco Menta Frappé", 10500, "Frappés"),
                
                # TÉS Y BEBIDAS ESPECIALES
                ("Té Verde", 6000, "Tés"),
                ("Té Negro", 6000, "Tés"),
                ("Té Frutos Rojos", 6000, "Tés"),
                ("Manzanilla", 6000, "Tés"),
                ("Matcha Latte Caliente", 9000, "Tés"),
                ("Matcha Latte Frío", 9000, "Tés"),
                ("Chai Latte", 9000, "Tés"),
                ("Golden Milk (Cúrcuma Latte)", 9500, "Tés"),
                
                # POSTRES Y PANADERÍA
                ("Muffin de Arándanos", 5500, "Postres"),
                ("Muffin de Chocolate", 5500, "Postres"),
                ("Muffin de Vainilla", 5500, "Postres"),
                ("Croissant de Mantequilla", 6500, "Panadería"),
                ("Croissant de Chocolate", 6500, "Panadería"),
                ("Croissant Jamón y Queso", 6500, "Panadería"),
                ("Brownie con Nueces", 6000, "Postres"),
                ("Torta de Zanahoria", 8000, "Postres"),
                ("Red Velvet", 8000, "Postres"),
                ("Cheesecake", 8000, "Postres"),
                ("Galleta Chips de Chocolate", 5000, "Postres"),
                ("Pan de Banano", 5500, "Panadería"),
                
                # SANDWICHES Y SALADOS
                ("Sandwich Pollo a la Parrilla", 10000, "Comida"),
                ("Bagel Queso Crema y Salmón", 11000, "Comida"),
                ("Panini Caprese", 9000, "Comida"),
                ("Wrap Pollo Espinaca", 9500, "Comida"),
                
                # EDICIONES ESPECIALES
                ("Pumpkin Spice Latte", 10000, "Especiales"),
                ("Caramel Apple Latte", 9500, "Especiales"),
                ("Coconut Mocha Frappé", 10500, "Especiales"),
                ("Frappé Café con Panela", 9000, "Especiales")
            ]
            
            cursor.executemany(
                "INSERT INTO productos (nombre, precio, categoria) VALUES (?, ?, ?)",
                productos_ejemplo
            )
            conn.commit()
        
        conn.close()
    
    # CRUD para Productos
    def obtener_productos(self) -> List[Producto]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, precio, categoria, disponible FROM productos ORDER BY categoria, nombre")
        productos = []
        for row in cursor.fetchall():
            producto = Producto(row[0], row[1], row[2], row[3])
            producto.disponible = bool(row[4])
            productos.append(producto)
        conn.close()
        return productos
    
    def obtener_producto_por_id(self, producto_id: int) -> Optional[Producto]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, precio, categoria, disponible FROM productos WHERE id = ?", (producto_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            producto = Producto(row[0], row[1], row[2], row[3])
            producto.disponible = bool(row[4])
            return producto
        return None
    
    def guardar_producto(self, producto: Producto) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        if producto.id == 0:  # Nuevo producto
            cursor.execute(
                "INSERT INTO productos (nombre, precio, categoria) VALUES (?, ?, ?)",
                (producto.nombre, producto.precio, producto.categoria)
            )
            producto_id = cursor.lastrowid
        else:  # Actualizar producto
            cursor.execute(
                "UPDATE productos SET nombre = ?, precio = ?, categoria = ? WHERE id = ?",
                (producto.nombre, producto.precio, producto.categoria, producto.id)
            )
            producto_id = producto.id
        conn.commit()
        conn.close()
        return producto_id
    
    # CRUD para Pedidos
    def guardar_pedido(self, pedido: Pedido) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Guardar cliente si tiene datos
            cliente_id = None
            if pedido.cliente.nit or pedido.cliente.nombre:
                cursor.execute(
                    "INSERT INTO clientes (nit, nombre, direccion) VALUES (?, ?, ?)",
                    (pedido.cliente.nit, pedido.cliente.nombre, pedido.cliente.direccion)
                )
                cliente_id = cursor.lastrowid
            
            # Guardar pedido
            cursor.execute('''
                INSERT INTO pedidos (numero_pedido, fecha, estado, cliente_id, subtotal, total_impuestos, total)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                pedido.numero_pedido,
                pedido.fecha,
                pedido.estado,
                cliente_id,
                pedido.subtotal,
                pedido.total_impuestos,
                pedido.total
            ))
            pedido_id = cursor.lastrowid
            
            # Guardar items del pedido
            for item in pedido.items:
                cursor.execute('''
                    INSERT INTO items_pedido (pedido_id, producto_id, cantidad, subtotal)
                    VALUES (?, ?, ?, ?)
                ''', (pedido_id, item.producto.id, item.cantidad, item.subtotal))
            
            # Guardar formas de pago
            for pago in pedido.formas_pago:
                cursor.execute('''
                    INSERT INTO formas_pago (pedido_id, tipo, valor)
                    VALUES (?, ?, ?)
                ''', (pedido_id, pago.tipo, pago.valor))
            
            conn.commit()
            return pedido_id
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def obtener_pedidos_pendientes(self) -> List[Pedido]:
        """Obtiene pedidos que están pendientes o en preparación para la cocina"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.id, p.numero_pedido, p.fecha, p.estado, p.subtotal, p.total_impuestos, p.total,
                   c.nit, c.nombre, c.direccion
            FROM pedidos p
            LEFT JOIN clientes c ON p.cliente_id = c.id
            WHERE p.estado IN ('PENDIENTE', 'EN_PREPARACION')
            ORDER BY p.fecha
        ''')
        
        pedidos = []
        for row in cursor.fetchall():
            pedido = Pedido(row[1])  # numero_pedido
            pedido.fecha = datetime.fromisoformat(row[2])
            pedido.estado = row[3]
            pedido.subtotal = row[4]
            pedido.total_impuestos = row[5]
            pedido.total = row[6]
            
            # Cliente
            if row[7]:  # nit
                pedido.cliente = Cliente(row[7], row[8], row[9])
            
            # Cargar items del pedido
            cursor.execute('''
                SELECT ip.producto_id, ip.cantidad, ip.subtotal, pr.nombre, pr.precio
                FROM items_pedido ip
                JOIN productos pr ON ip.producto_id = pr.id
                WHERE ip.pedido_id = ?
            ''', (row[0],))
            
            for item_row in cursor.fetchall():
                producto = Producto(item_row[0], item_row[3], item_row[4])
                item = ItemPedido(producto, item_row[1])
                pedido.items.append(item)
            
            pedidos.append(pedido)
        
        conn.close()
        return pedidos
    
    def actualizar_estado_pedido(self, numero_pedido: str, nuevo_estado: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE pedidos SET estado = ? WHERE numero_pedido = ?",
            (nuevo_estado, numero_pedido)
        )
        conn.commit()
        conn.close()
    
    def guardar_factura(self, factura: Factura) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Primero obtener el ID del pedido
        cursor.execute("SELECT id FROM pedidos WHERE numero_pedido = ?", (factura.pedido.numero_pedido,))
        pedido_row = cursor.fetchone()
        
        if pedido_row:
            pedido_id = pedido_row[0]
            cursor.execute('''
                INSERT INTO facturas (numero, pedido_id, fecha_facturacion, caja_numero)
                VALUES (?, ?, ?, ?)
            ''', (factura.numero, pedido_id, factura.fecha_facturacion, factura.caja_numero))
            
            factura_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return factura_id
        else:
            conn.close()
            raise ValueError(f"No se encontró el pedido {factura.pedido.numero_pedido}")
    
    def generar_numero_pedido(self) -> str:
        """Genera un número único para el pedido"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM pedidos")
        count = cursor.fetchone()[0]
        conn.close()
        return f"UV-{count + 100001:06d}"
    
    def generar_numero_factura(self) -> str:
        """Genera un número único para la factura"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM facturas")
        count = cursor.fetchone()[0]
        conn.close()
        return f"UV-F{count + 10001:05d}"