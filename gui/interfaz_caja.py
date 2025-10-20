import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import sys
import os

# Agregar el directorio padre al path para importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.models import Producto, Pedido, Cliente, Factura
from database.db_manager import DatabaseManager
from utils.factura_generator import GeneradorFacturas

class InterfazCajero:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Cafetería - Caja")
        self.root.geometry("1200x800")
        
        # Inicializar base de datos y generador de facturas
        self.db = DatabaseManager()
        self.generador_facturas = GeneradorFacturas()
        
        # Variables
        self.pedido_actual = None
        self.productos = []
        
        # Configurar interfaz
        self.configurar_interfaz()
        self.cargar_productos()
        self.nuevo_pedido()
    
    def configurar_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="URBAN VIVES - Sistema de Caja", font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame izquierdo - Lista de productos
        productos_frame = ttk.LabelFrame(main_frame, text="Productos", padding="10")
        productos_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Lista de productos
        productos_columns = ("ID", "Nombre", "Precio")
        self.productos_tree = ttk.Treeview(productos_frame, columns=productos_columns, show="headings", height=15)
        
        for col in productos_columns:
            self.productos_tree.heading(col, text=col)
            self.productos_tree.column(col, width=80 if col == "ID" else 150)
        
        # Scrollbar para productos
        productos_scroll = ttk.Scrollbar(productos_frame, orient="vertical", command=self.productos_tree.yview)
        self.productos_tree.configure(yscrollcommand=productos_scroll.set)
        
        self.productos_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        productos_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        productos_frame.columnconfigure(0, weight=1)
        productos_frame.rowconfigure(0, weight=1)
        
        # Botón agregar producto
        btn_agregar = ttk.Button(productos_frame, text="Agregar al Pedido", command=self.agregar_producto_pedido)
        btn_agregar.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky=(tk.W, tk.E))
        
        # Frame central - Pedido actual
        pedido_frame = ttk.LabelFrame(main_frame, text="Pedido Actual", padding="10")
        pedido_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Información del pedido
        info_frame = ttk.Frame(pedido_frame)
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(info_frame, text="No. Pedido:").grid(row=0, column=0, sticky=tk.W)
        self.lbl_numero_pedido = ttk.Label(info_frame, text="", font=("Arial", 10, "bold"))
        self.lbl_numero_pedido.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Lista de items del pedido
        pedido_columns = ("Producto", "Cantidad", "Precio Unit.", "Subtotal")
        self.pedido_tree = ttk.Treeview(pedido_frame, columns=pedido_columns, show="headings", height=10)
        
        for col in pedido_columns:
            self.pedido_tree.heading(col, text=col)
            self.pedido_tree.column(col, width=120)
        
        pedido_scroll = ttk.Scrollbar(pedido_frame, orient="vertical", command=self.pedido_tree.yview)
        self.pedido_tree.configure(yscrollcommand=pedido_scroll.set)
        
        self.pedido_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        pedido_scroll.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        pedido_frame.columnconfigure(0, weight=1)
        pedido_frame.rowconfigure(1, weight=1)
        
        # Botones del pedido
        botones_pedido_frame = ttk.Frame(pedido_frame)
        botones_pedido_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky=(tk.W, tk.E))
        
        ttk.Button(botones_pedido_frame, text="Quitar Item", command=self.quitar_item_pedido).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(botones_pedido_frame, text="Nuevo Pedido", command=self.nuevo_pedido).grid(row=0, column=1, padx=5)
        
        # Frame derecho - Totales y pago
        pago_frame = ttk.LabelFrame(main_frame, text="Totales y Pago", padding="10")
        pago_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        # Totales
        totales_frame = ttk.Frame(pago_frame)
        totales_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(totales_frame, text="Subtotal:").grid(row=0, column=0, sticky=tk.W)
        self.lbl_subtotal = ttk.Label(totales_frame, text="$0", font=("Arial", 12))
        self.lbl_subtotal.grid(row=0, column=1, sticky=tk.E)
        
        ttk.Label(totales_frame, text="IVA (19%):").grid(row=1, column=0, sticky=tk.W)
        self.lbl_iva = ttk.Label(totales_frame, text="$0", font=("Arial", 12))
        self.lbl_iva.grid(row=1, column=1, sticky=tk.E)
        
        ttk.Label(totales_frame, text="TOTAL:", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky=tk.W)
        self.lbl_total = ttk.Label(totales_frame, text="$0", font=("Arial", 14, "bold"))
        self.lbl_total.grid(row=2, column=1, sticky=tk.E)
        
        totales_frame.columnconfigure(1, weight=1)
        
        # Cliente
        cliente_frame = ttk.LabelFrame(pago_frame, text="Cliente", padding="5")
        cliente_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(cliente_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W)
        self.entry_cliente_nombre = ttk.Entry(cliente_frame, width=20)
        self.entry_cliente_nombre.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        ttk.Label(cliente_frame, text="NIT/CC:").grid(row=1, column=0, sticky=tk.W)
        self.entry_cliente_nit = ttk.Entry(cliente_frame, width=20)
        self.entry_cliente_nit.grid(row=1, column=1, sticky=(tk.W, tk.E))
        
        cliente_frame.columnconfigure(1, weight=1)
        
        # Pago
        pago_metodo_frame = ttk.LabelFrame(pago_frame, text="Método de Pago", padding="5")
        pago_metodo_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.metodo_pago_var = tk.StringVar(value="EFECTIVO")
        ttk.Radiobutton(pago_metodo_frame, text="Efectivo", variable=self.metodo_pago_var, value="EFECTIVO").grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(pago_metodo_frame, text="Transferencia", variable=self.metodo_pago_var, value="TRANSFERENCIA").grid(row=1, column=0, sticky=tk.W)
        ttk.Radiobutton(pago_metodo_frame, text="Tarjeta", variable=self.metodo_pago_var, value="TARJETA").grid(row=2, column=0, sticky=tk.W)
        
        # Botones principales
        botones_frame = ttk.Frame(pago_frame)
        botones_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        self.btn_procesar = ttk.Button(botones_frame, text="Procesar Pedido", command=self.procesar_pedido, style="Accent.TButton")
        self.btn_procesar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Button(botones_frame, text="Ver Cocina", command=self.abrir_cocina).grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Button(botones_frame, text="Ver Facturas", command=self.ver_facturas_generadas).grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        botones_frame.columnconfigure(0, weight=1)
        pago_frame.columnconfigure(0, weight=1)
        
    def cargar_productos(self):
        """Carga los productos desde la base de datos"""
        self.productos = self.db.obtener_productos()
        
        # Limpiar la lista
        for item in self.productos_tree.get_children():
            self.productos_tree.delete(item)
        
        # Agregar productos
        for producto in self.productos:
            self.productos_tree.insert("", "end", values=(
                producto.id,
                producto.nombre,
                f"${producto.precio:,.0f}"
            ))
    
    def nuevo_pedido(self):
        """Crea un nuevo pedido"""
        numero_pedido = self.db.generar_numero_pedido()
        self.pedido_actual = Pedido(numero_pedido)
        
        self.lbl_numero_pedido.config(text=numero_pedido)
        
        # Limpiar lista de items
        for item in self.pedido_tree.get_children():
            self.pedido_tree.delete(item)
        
        # Limpiar campos de cliente
        self.entry_cliente_nombre.delete(0, tk.END)
        self.entry_cliente_nit.delete(0, tk.END)
        
        # Resetear totales
        self.actualizar_totales()
        
        # Habilitar botón de procesar
        self.btn_procesar.config(state="normal")
    
    def agregar_producto_pedido(self):
        """Agrega un producto al pedido actual"""
        if not self.pedido_actual:
            messagebox.showwarning("Advertencia", "No hay un pedido activo")
            return
        
        seleccion = self.productos_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return
        
        # Obtener producto seleccionado
        item = self.productos_tree.item(seleccion[0])
        producto_id = int(item['values'][0])
        
        # Buscar el producto
        producto = None
        for p in self.productos:
            if p.id == producto_id:
                producto = p
                break
        
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado")
            return
        
        # Pedir cantidad
        cantidad = simpledialog.askinteger("Cantidad", f"Cantidad de {producto.nombre}:", minvalue=1, maxvalue=99)
        if cantidad:
            self.pedido_actual.agregar_item(producto, cantidad)
            self.actualizar_lista_pedido()
            self.actualizar_totales()
    
    def quitar_item_pedido(self):
        """Quita un item del pedido actual"""
        if not self.pedido_actual:
            return
        
        seleccion = self.pedido_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un item para quitar")
            return
        
        # Obtener el item seleccionado
        item = self.pedido_tree.item(seleccion[0])
        nombre_producto = item['values'][0]
        
        # Buscar y remover el producto
        for i, item_pedido in enumerate(self.pedido_actual.items):
            if item_pedido.producto.nombre == nombre_producto:
                self.pedido_actual.items.pop(i)
                break
        
        self.pedido_actual.calcular_totales()
        self.actualizar_lista_pedido()
        self.actualizar_totales()
    
    def actualizar_lista_pedido(self):
        """Actualiza la lista de items del pedido"""
        # Limpiar lista
        for item in self.pedido_tree.get_children():
            self.pedido_tree.delete(item)
        
        # Agregar items
        if self.pedido_actual:
            for item in self.pedido_actual.items:
                self.pedido_tree.insert("", "end", values=(
                    item.producto.nombre,
                    item.cantidad,
                    f"${item.producto.precio:,.0f}",
                    f"${item.subtotal:,.0f}"
                ))
    
    def actualizar_totales(self):
        """Actualiza los labels de totales"""
        if self.pedido_actual:
            self.lbl_subtotal.config(text=f"${self.pedido_actual.subtotal:,.0f}")
            self.lbl_iva.config(text=f"${self.pedido_actual.total_impuestos:,.0f}")
            self.lbl_total.config(text=f"${self.pedido_actual.total:,.0f}")
        else:
            self.lbl_subtotal.config(text="$0")
            self.lbl_iva.config(text="$0")
            self.lbl_total.config(text="$0")
    
    def procesar_pedido(self):
        """Procesa el pedido actual"""
        if not self.pedido_actual or not self.pedido_actual.items:
            messagebox.showwarning("Advertencia", "No hay items en el pedido")
            return
        
        try:
            # Configurar cliente
            nombre_cliente = self.entry_cliente_nombre.get().strip()
            nit_cliente = self.entry_cliente_nit.get().strip()
            
            if nombre_cliente or nit_cliente:
                self.pedido_actual.cliente = Cliente(nit_cliente, nombre_cliente)
            
            # Configurar forma de pago
            metodo_pago = self.metodo_pago_var.get()
            self.pedido_actual.agregar_forma_pago(metodo_pago, self.pedido_actual.total)
            
            # Cambiar estado a EN_PREPARACION
            self.pedido_actual.estado = "EN_PREPARACION"
            
            # Guardar en base de datos
            self.db.guardar_pedido(self.pedido_actual)
            
            # Generar factura
            numero_factura = self.db.generar_numero_factura()
            factura = Factura(numero_factura, self.pedido_actual)
            self.db.guardar_factura(factura)
            
            # Generar e imprimir factura
            archivo_pdf = self.generador_facturas.generar_factura_pdf(factura)
            
            # Mostrar vista previa y preguntar si quiere imprimir
            self.mostrar_vista_previa_factura(factura)
            
            if messagebox.askyesno("Imprimir", "¿Desea imprimir la factura?"):
                resultado_impresion = self.generador_facturas.imprimir_factura(factura)
                if resultado_impresion:
                    messagebox.showinfo("Impresión", "Factura enviada a impresión correctamente")
                else:
                    messagebox.showwarning("Impresión", "Hubo un problema con la impresión.\nRevise la consola para más detalles.\nLa factura se guardó en archivo.")
            
            # Mostrar información de archivos generados
            mensaje_exito = f"Pedido procesado exitosamente\nFactura: {numero_factura}\n\nArchivos generados:\n- PDF: facturas_generadas/factura_{numero_factura}.pdf\n- Texto: facturas_generadas/factura_{numero_factura}.txt"
            messagebox.showinfo("Éxito", mensaje_exito)
            
            # Deshabilitar botón de procesar
            self.btn_procesar.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar pedido: {str(e)}")
    
    def abrir_cocina(self):
        """Abre la ventana de cocina"""
        ventana_cocina = tk.Toplevel(self.root)
        InterfazCocina(ventana_cocina, self.db)
    
    def ver_facturas_generadas(self):
        """Abre la carpeta de facturas generadas"""
        import subprocess
        import os
        
        try:
            # Crear la carpeta si no existe
            carpeta_facturas = "facturas_generadas"
            if not os.path.exists(carpeta_facturas):
                os.makedirs(carpeta_facturas)
            
            # Abrir la carpeta en el explorador de Windows
            subprocess.run(f'explorer "{os.path.abspath(carpeta_facturas)}"', shell=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la carpeta de facturas: {str(e)}")
    
    def mostrar_vista_previa_factura(self, factura):
        """Muestra una vista previa de la factura en una ventana"""
        ventana_previa = tk.Toplevel(self.root)
        ventana_previa.title(f"Vista Previa - Factura {factura.numero}")
        ventana_previa.geometry("600x700")
        
        # Frame con scrollbar
        main_frame = ttk.Frame(ventana_previa)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Generar contenido de la factura
        contenido_factura = self.generador_facturas.generar_factura_texto(factura)
        
        # Mostrar contenido en un Text widget
        text_widget = tk.Text(scrollable_frame, wrap=tk.WORD, font=("Courier", 10), 
                             width=70, height=40, bg="white", fg="black")
        text_widget.insert(tk.END, contenido_factura)
        text_widget.config(state=tk.DISABLED)  # Solo lectura
        text_widget.pack(padx=10, pady=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botones
        botones_frame = ttk.Frame(ventana_previa)
        botones_frame.pack(pady=10)
        
        ttk.Button(botones_frame, text="Cerrar", command=ventana_previa.destroy).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_frame, text="Imprimir Ahora", 
                  command=lambda: self.imprimir_desde_previa(factura, ventana_previa)).pack(side=tk.LEFT, padx=5)
    
    def imprimir_desde_previa(self, factura, ventana):
        """Imprime la factura desde la vista previa"""
        resultado = self.generador_facturas.imprimir_factura(factura)
        if resultado:
            messagebox.showinfo("Impresión", "Factura enviada a impresión")
        else:
            messagebox.showwarning("Impresión", "Hubo un problema con la impresión")
        ventana.destroy()

class InterfazCocina:
    def __init__(self, root, db_manager):
        self.root = root
        self.db = db_manager
        self.root.title("Sistema de Cafetería - Cocina")
        self.root.geometry("800x600")
        
        self.configurar_interfaz()
        self.actualizar_pedidos()
        
        # Auto-actualizar cada 30 segundos
        self.auto_actualizar()
    
    def configurar_interfaz(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(main_frame, text="COCINA - Pedidos Pendientes", font=("Arial", 16, "bold"))
        titulo.pack(pady=(0, 20))
        
        # Lista de pedidos
        pedidos_frame = ttk.Frame(main_frame)
        pedidos_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("Pedido", "Fecha", "Estado", "Items", "Total")
        self.pedidos_tree = ttk.Treeview(pedidos_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.pedidos_tree.heading(col, text=col)
            self.pedidos_tree.column(col, width=120)
        
        pedidos_scroll = ttk.Scrollbar(pedidos_frame, orient="vertical", command=self.pedidos_tree.yview)
        self.pedidos_tree.configure(yscrollcommand=pedidos_scroll.set)
        
        self.pedidos_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        pedidos_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones
        botones_frame = ttk.Frame(main_frame)
        botones_frame.pack(pady=(20, 0))
        
        ttk.Button(botones_frame, text="Marcar como Listo", command=self.marcar_listo).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(botones_frame, text="Actualizar", command=self.actualizar_pedidos).pack(side=tk.LEFT, padx=10)
        ttk.Button(botones_frame, text="Ver Detalles", command=self.ver_detalles).pack(side=tk.LEFT, padx=10)
    
    def actualizar_pedidos(self):
        """Actualiza la lista de pedidos pendientes"""
        # Limpiar lista
        for item in self.pedidos_tree.get_children():
            self.pedidos_tree.delete(item)
        
        # Obtener pedidos pendientes
        pedidos = self.db.obtener_pedidos_pendientes()
        
        for pedido in pedidos:
            items_str = ", ".join([f"{item.producto.nombre} x{item.cantidad}" for item in pedido.items])
            
            self.pedidos_tree.insert("", "end", values=(
                pedido.numero_pedido,
                pedido.fecha.strftime("%H:%M:%S"),
                pedido.estado,
                items_str[:50] + "..." if len(items_str) > 50 else items_str,
                f"${pedido.total:,.0f}"
            ))
    
    def marcar_listo(self):
        """Marca un pedido como listo"""
        seleccion = self.pedidos_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un pedido")
            return
        
        item = self.pedidos_tree.item(seleccion[0])
        numero_pedido = item['values'][0]
        
        try:
            self.db.actualizar_estado_pedido(numero_pedido, "LISTO")
            messagebox.showinfo("Éxito", f"Pedido {numero_pedido} marcado como listo")
            self.actualizar_pedidos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar pedido: {str(e)}")
    
    def ver_detalles(self):
        """Muestra los detalles de un pedido"""
        seleccion = self.pedidos_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un pedido")
            return
        
        item = self.pedidos_tree.item(seleccion[0])
        numero_pedido = item['values'][0]
        
        # Buscar el pedido completo
        pedidos = self.db.obtener_pedidos_pendientes()
        pedido = None
        for p in pedidos:
            if p.numero_pedido == numero_pedido:
                pedido = p
                break
        
        if pedido:
            detalles = f"Pedido: {pedido.numero_pedido}\n"
            detalles += f"Estado: {pedido.estado}\n"
            detalles += f"Cliente: {pedido.cliente.nombre if pedido.cliente.nombre else 'Sin nombre'}\n\n"
            detalles += "Items:\n"
            
            for item in pedido.items:
                detalles += f"- {item.producto.nombre} x{item.cantidad}\n"
            
            detalles += f"\nTotal: ${pedido.total:,.0f}"
            
            messagebox.showinfo("Detalles del Pedido", detalles)
    
    def auto_actualizar(self):
        """Auto-actualiza los pedidos cada 30 segundos"""
        self.actualizar_pedidos()
        self.root.after(30000, self.auto_actualizar)  # 30000 ms = 30 segundos

def main():
    root = tk.Tk()
    app = InterfazCajero(root)
    root.mainloop()

if __name__ == "__main__":
    main()