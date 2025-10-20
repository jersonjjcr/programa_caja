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

class InterfazCajaModerna:
    def __init__(self, root):
        self.root = root
        self.root.title("URBAN VIVES - Sistema POS")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Configurar estilos
        self.configurar_estilos()
        
        # Inicializar base de datos y generador de facturas
        self.db = DatabaseManager()
        self.db.connect()  # Establecer conexión persistente
        self.generador_facturas = GeneradorFacturas()
        
        # Variables
        self.pedido_actual = None
        self.productos = []
        self.categoria_actual = "Todos"
        
        # Configurar interfaz
        self.configurar_interfaz()
        self.cargar_productos()
        self.nuevo_pedido()
    
    def configurar_estilos(self):
        """Configura estilos modernos para la aplicación"""
        style = ttk.Style()
        
        # Configurar tema
        style.theme_use('clam')
        
        # Estilos personalizados
        style.configure('Title.TLabel', font=('Segoe UI', 18, 'bold'), background='#2c3e50', foreground='white')
        style.configure('Header.TLabel', font=('Segoe UI', 12, 'bold'), background='#34495e', foreground='white')
        style.configure('Product.TFrame', background='white', relief='raised', borderwidth=1)
        style.configure('Category.TButton', font=('Segoe UI', 10, 'bold'))
        style.configure('Action.TButton', font=('Segoe UI', 11, 'bold'))
        style.configure('Total.TLabel', font=('Segoe UI', 14, 'bold'), foreground='#27ae60')
        style.configure('Checkout.TButton', font=('Segoe UI', 12, 'bold'), foreground='white')
        
        # Mapas de estilos
        style.map('Checkout.TButton',
                 background=[('active', '#e74c3c'), ('!active', '#c0392b')])
    
    def configurar_interfaz(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#ecf0f1')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.crear_header(main_frame)
        
        # Contenido principal
        content_frame = tk.Frame(main_frame, bg='#ecf0f1')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Dividir en tres secciones
        self.crear_seccion_productos(content_frame)
        self.crear_seccion_pedido(content_frame)
        self.crear_seccion_totales(content_frame)
    
    def crear_header(self, parent):
        """Crea la barra de título superior"""
        header_frame = tk.Frame(parent, bg='#2c3e50', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Logo y título
        title_label = tk.Label(header_frame, text="☕ URBAN VIVES", 
                              font=('Segoe UI', 24, 'bold'), 
                              bg='#2c3e50', fg='white')
        title_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Botones de navegación
        nav_frame = tk.Frame(header_frame, bg='#2c3e50')
        nav_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        ttk.Button(nav_frame, text="🏠 Nuevo Pedido", command=self.nuevo_pedido,
                  style='Category.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text="🍳 Cocina", command=self.abrir_cocina,
                  style='Category.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text="� Productos", command=self.abrir_gestion_productos,
                  style='Category.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text="�📁 Facturas", command=self.ver_facturas_generadas,
                  style='Category.TButton').pack(side=tk.LEFT, padx=5)
    
    def crear_seccion_productos(self, parent):
        """Crea la sección de productos (izquierda)"""
        productos_frame = tk.Frame(parent, bg='white', relief='raised', borderwidth=1)
        productos_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Header de productos
        header = tk.Frame(productos_frame, bg='#34495e', height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Productos", font=('Segoe UI', 14, 'bold'),
                bg='#34495e', fg='white').pack(side=tk.LEFT, padx=15, pady=10)
        
        # Filtro de categorías
        self.crear_filtro_categorias(productos_frame)
        
        # Lista de productos con scroll
        self.crear_lista_productos(productos_frame)
    
    def crear_filtro_categorias(self, parent):
        """Crea los botones de filtro por categoría"""
        filter_frame = tk.Frame(parent, bg='white', pady=10)
        filter_frame.pack(fill=tk.X, padx=10)
        
        categorias = ["Todos", "Cafés Clásicos", "Bebidas Frías", "Frappés", "Tés", 
                     "Postres", "Panadería", "Comida", "Especiales"]
        
        self.categoria_buttons = {}
        
        # Primera fila
        fila1 = tk.Frame(filter_frame, bg='white')
        fila1.pack(fill=tk.X, pady=2)
        
        # Segunda fila
        fila2 = tk.Frame(filter_frame, bg='white')
        fila2.pack(fill=tk.X, pady=2)
        
        for i, categoria in enumerate(categorias):
            parent_frame = fila1 if i < 5 else fila2
            
            btn = tk.Button(parent_frame, text=categoria, 
                           font=('Segoe UI', 9, 'bold'),
                           bg='#3498db' if categoria == "Todos" else '#bdc3c7',
                           fg='white' if categoria == "Todos" else '#2c3e50',
                           relief='flat', borderwidth=0, pady=5, padx=10,
                           command=lambda c=categoria: self.filtrar_por_categoria(c))
            btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
            self.categoria_buttons[categoria] = btn
    
    def crear_lista_productos(self, parent):
        """Crea la lista scrollable de productos"""
        # Frame para la lista con scroll
        list_frame = tk.Frame(parent, bg='white')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(list_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='white')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind para scroll con mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)
    
    def crear_seccion_pedido(self, parent):
        """Crea la sección del pedido actual (centro)"""
        pedido_frame = tk.Frame(parent, bg='white', relief='raised', borderwidth=1)
        pedido_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5)
        pedido_frame.configure(width=400)
        
        # Header del pedido
        header = tk.Frame(pedido_frame, bg='#34495e', height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Pedido Actual", font=('Segoe UI', 14, 'bold'),
                bg='#34495e', fg='white').pack(side=tk.LEFT, padx=15, pady=10)
        
        # Número de pedido
        info_frame = tk.Frame(pedido_frame, bg='white', pady=10)
        info_frame.pack(fill=tk.X, padx=15)
        
        tk.Label(info_frame, text="No. Pedido:", font=('Segoe UI', 10, 'bold'),
                bg='white').pack(side=tk.LEFT)
        self.lbl_numero_pedido = tk.Label(info_frame, text="", font=('Segoe UI', 10),
                                         bg='white', fg='#e74c3c')
        self.lbl_numero_pedido.pack(side=tk.LEFT, padx=(10, 0))
        
        # Lista de items del pedido
        self.crear_lista_pedido(pedido_frame)
        
        # Información del cliente
        self.crear_info_cliente(pedido_frame)
    
    def crear_lista_pedido(self, parent):
        """Crea la lista de items del pedido"""
        # Frame para lista de pedido
        lista_frame = tk.Frame(parent, bg='white')
        lista_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        # Headers
        header_frame = tk.Frame(lista_frame, bg='#ecf0f1', height=30)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="Producto", font=('Segoe UI', 9, 'bold'),
                bg='#ecf0f1', anchor='w').place(x=5, y=5, width=150)
        tk.Label(header_frame, text="Cant.", font=('Segoe UI', 9, 'bold'),
                bg='#ecf0f1', anchor='center').place(x=160, y=5, width=40)
        tk.Label(header_frame, text="Precio", font=('Segoe UI', 9, 'bold'),
                bg='#ecf0f1', anchor='e').place(x=205, y=5, width=70)
        tk.Label(header_frame, text="Total", font=('Segoe UI', 9, 'bold'),
                bg='#ecf0f1', anchor='e').place(x=280, y=5, width=80)
        
        # Frame scrollable más simple para items del pedido
        scroll_container = tk.Frame(lista_frame, bg='white')
        scroll_container.pack(fill=tk.BOTH, expand=True)
        
        # Crear frame directo para items (sin canvas por ahora para simplificar)
        self.items_frame = tk.Frame(scroll_container, bg='white')
        self.items_frame.pack(fill=tk.BOTH, expand=True)
    
    def crear_info_cliente(self, parent):
        """Crea la sección de información del cliente"""
        cliente_frame = tk.LabelFrame(parent, text="Información del Cliente", 
                                     font=('Segoe UI', 10, 'bold'),
                                     bg='white', fg='#2c3e50')
        cliente_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # Campos del cliente
        tk.Label(cliente_frame, text="Nombre:", bg='white').grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.entry_cliente_nombre = tk.Entry(cliente_frame, font=('Segoe UI', 9), width=25)
        self.entry_cliente_nombre.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(cliente_frame, text="NIT/CC:", bg='white').grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.entry_cliente_nit = tk.Entry(cliente_frame, font=('Segoe UI', 9), width=25)
        self.entry_cliente_nit.grid(row=1, column=1, padx=5, pady=2)
    
    def crear_seccion_totales(self, parent):
        """Crea la sección de totales y checkout (derecha)"""
        totales_frame = tk.Frame(parent, bg='white', relief='raised', borderwidth=1)
        totales_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        totales_frame.configure(width=300)
        
        # Header
        header = tk.Frame(totales_frame, bg='#34495e', height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Resumen", font=('Segoe UI', 14, 'bold'),
                bg='#34495e', fg='white').pack(side=tk.LEFT, padx=15, pady=10)
        
        # Totales
        self.crear_totales(totales_frame)
        
        # Métodos de pago
        self.crear_metodos_pago(totales_frame)
        
        # Botones de acción
        self.crear_botones_accion(totales_frame)
    
    def crear_totales(self, parent):
        """Crea la sección de totales"""
        totales_container = tk.Frame(parent, bg='white', pady=20)
        totales_container.pack(fill=tk.X, padx=15)
        
        # Items count
        items_frame = tk.Frame(totales_container, bg='white')
        items_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(items_frame, text="Items:", font=('Segoe UI', 11),
                bg='white').pack(side=tk.LEFT)
        self.lbl_items_count = tk.Label(items_frame, text="0", font=('Segoe UI', 11, 'bold'),
                                       bg='white', fg='#7f8c8d')
        self.lbl_items_count.pack(side=tk.RIGHT)
        
        # Subtotal
        subtotal_frame = tk.Frame(totales_container, bg='white')
        subtotal_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(subtotal_frame, text="Subtotal:", font=('Segoe UI', 11),
                bg='white').pack(side=tk.LEFT)
        self.lbl_subtotal = tk.Label(subtotal_frame, text="$0", font=('Segoe UI', 11, 'bold'),
                                    bg='white', fg='#34495e')
        self.lbl_subtotal.pack(side=tk.RIGHT)
        
        # IVA
        iva_frame = tk.Frame(totales_container, bg='white')
        iva_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(iva_frame, text="IVA (19%):", font=('Segoe UI', 11),
                bg='white').pack(side=tk.LEFT)
        self.lbl_iva = tk.Label(iva_frame, text="$0", font=('Segoe UI', 11, 'bold'),
                               bg='white', fg='#e67e22')
        self.lbl_iva.pack(side=tk.RIGHT)
        
        # Separador
        separator = tk.Frame(totales_container, bg='#bdc3c7', height=2)
        separator.pack(fill=tk.X, pady=10)
        
        # Total
        total_frame = tk.Frame(totales_container, bg='white')
        total_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(total_frame, text="TOTAL:", font=('Segoe UI', 14, 'bold'),
                bg='white', fg='#2c3e50').pack(side=tk.LEFT)
        self.lbl_total = tk.Label(total_frame, text="$0", font=('Segoe UI', 18, 'bold'),
                                 bg='white', fg='#27ae60')
        self.lbl_total.pack(side=tk.RIGHT)
    
    def crear_metodos_pago(self, parent):
        """Crea los métodos de pago"""
        pago_frame = tk.LabelFrame(parent, text="Método de Pago", 
                                  font=('Segoe UI', 10, 'bold'),
                                  bg='white', fg='#2c3e50')
        pago_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.metodo_pago_var = tk.StringVar(value="EFECTIVO")
        
        # Efectivo
        tk.Radiobutton(pago_frame, text="💵 Efectivo", variable=self.metodo_pago_var,
                      value="EFECTIVO", font=('Segoe UI', 10), bg='white',
                      activebackground='white').pack(anchor='w', padx=10, pady=5)
        
        # Transferencia
        tk.Radiobutton(pago_frame, text="🏦 Transferencia", variable=self.metodo_pago_var,
                      value="TRANSFERENCIA", font=('Segoe UI', 10), bg='white',
                      activebackground='white').pack(anchor='w', padx=10, pady=5)
        
        # Tarjeta
        tk.Radiobutton(pago_frame, text="💳 Tarjeta", variable=self.metodo_pago_var,
                      value="TARJETA", font=('Segoe UI', 10), bg='white',
                      activebackground='white').pack(anchor='w', padx=10, pady=5)
    
    def crear_botones_accion(self, parent):
        """Crea los botones principales de acción"""
        botones_frame = tk.Frame(parent, bg='white', pady=20)
        botones_frame.pack(fill=tk.X, padx=15)
        
        # Botón de Checkout principal
        self.btn_checkout = tk.Button(botones_frame, text="🛒 PROCESAR PEDIDO",
                                     font=('Segoe UI', 12, 'bold'),
                                     bg='#27ae60', fg='white', relief='flat',
                                     borderwidth=0, pady=15, cursor='hand2',
                                     command=self.procesar_pedido)
        self.btn_checkout.pack(fill=tk.X, pady=(0, 10))
        
        # Botón de cancelar
        tk.Button(botones_frame, text="❌ Cancelar Pedido",
                 font=('Segoe UI', 10), bg='#e74c3c', fg='white',
                 relief='flat', borderwidth=0, pady=8, cursor='hand2',
                 command=self.cancelar_pedido).pack(fill=tk.X, pady=2)
    
    def cargar_productos(self):
        """Carga los productos desde la base de datos y los muestra"""
        todos_los_productos = self.db.obtener_productos()
        # Filtrar solo productos disponibles para la interfaz de caja
        self.productos = [p for p in todos_los_productos if p.disponible]
        self.mostrar_productos()
    
    def mostrar_productos(self, filtro_categoria=None):
        """Muestra los productos en la interfaz"""
        # Limpiar productos anteriores
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Filtrar productos por categoría
        productos_filtrados = self.productos
        if filtro_categoria and filtro_categoria != "Todos":
            productos_filtrados = [p for p in self.productos if p.categoria == filtro_categoria]
        
        # Mostrar productos en grid
        columnas = 2
        for i, producto in enumerate(productos_filtrados):
            row = i // columnas
            col = i % columnas
            
            self.crear_tarjeta_producto(self.scrollable_frame, producto, row, col)
    
    def crear_tarjeta_producto(self, parent, producto, row, col):
        """Crea una tarjeta visual para cada producto"""
        # Frame principal de la tarjeta
        card = tk.Frame(parent, bg='white', relief='raised', borderwidth=1,
                       cursor='hand2', padx=10, pady=10)
        card.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
        
        # Configurar grid del parent
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        
        # Emoji según categoría
        emojis = {
            "Cafés Clásicos": "☕",
            "Bebidas Frías": "🧊",
            "Frappés": "🥤",
            "Tés": "🍵",
            "Postres": "🧁",
            "Panadería": "🥐",
            "Comida": "🥪",
            "Especiales": "⭐"
        }
        emoji = emojis.get(producto.categoria, "🍽️")
        
        # Emoji del producto
        emoji_label = tk.Label(card, text=emoji, font=('Segoe UI', 20),
                              bg='white', fg='#3498db')
        emoji_label.pack(pady=(0, 5))
        
        # Nombre del producto
        nombre_label = tk.Label(card, text=producto.nombre, 
                               font=('Segoe UI', 10, 'bold'),
                               bg='white', fg='#2c3e50', wraplength=120,
                               justify='center')
        nombre_label.pack()
        
        # Precio
        precio_label = tk.Label(card, text=f"${producto.precio:,.0f}",
                               font=('Segoe UI', 11, 'bold'),
                               bg='white', fg='#27ae60')
        precio_label.pack(pady=(5, 0))
        
        # ID del producto (oculto)
        id_label = tk.Label(card, text=f"ID: {producto.id}",
                           font=('Segoe UI', 7), bg='white', fg='#95a5a6')
        id_label.pack()
        
        # Bind para doble clic
        def on_double_click(event):
            self.agregar_producto_pedido(producto)
        
        # Bind para hover effect
        def on_enter(event):
            card.configure(relief='solid', borderwidth=2)
        
        def on_leave(event):
            card.configure(relief='raised', borderwidth=1)
        
        # Aplicar binds a la tarjeta y todos sus hijos
        widgets = [card, emoji_label, nombre_label, precio_label, id_label]
        for widget in widgets:
            widget.bind("<Double-Button-1>", on_double_click)
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
    
    def filtrar_por_categoria(self, categoria):
        """Filtra productos por categoría"""
        self.categoria_actual = categoria
        
        # Actualizar estilo de botones
        for cat, btn in self.categoria_buttons.items():
            if cat == categoria:
                btn.configure(bg='#3498db', fg='white')
            else:
                btn.configure(bg='#bdc3c7', fg='#2c3e50')
        
        # Mostrar productos filtrados
        self.mostrar_productos(categoria)
    
    def nuevo_pedido(self):
        """Crea un nuevo pedido"""
        numero_pedido = self.db.generar_numero_pedido()
        self.pedido_actual = Pedido(numero_pedido)
        
        self.lbl_numero_pedido.config(text=numero_pedido)
        
        # Limpiar lista de items
        for widget in self.items_frame.winfo_children():
            widget.destroy()
        
        # Limpiar campos de cliente
        self.entry_cliente_nombre.delete(0, tk.END)
        self.entry_cliente_nit.delete(0, tk.END)
        
        # Resetear totales
        self.actualizar_totales()
        
        # Habilitar botón de procesar
        self.btn_checkout.config(state="normal", bg='#27ae60')
    
    def agregar_producto_pedido(self, producto):
        """Agrega un producto al pedido actual (llamado con doble clic)"""
        if not self.pedido_actual:
            messagebox.showwarning("Advertencia", "No hay un pedido activo")
            return
        
        print(f"Debug: Agregando producto {producto.nombre} al pedido")
        
        # Agregar con cantidad 1 por defecto (sin ventana de diálogo)
        cantidad = 1
        print(f"Debug: Cantidad por defecto: {cantidad}")
        
        self.pedido_actual.agregar_item(producto, cantidad)
        print(f"Debug: Items en pedido después de agregar: {len(self.pedido_actual.items)}")
        
        # Forzar actualización
        self.actualizar_lista_pedido()
        self.actualizar_totales()
        
        # Actualizar la vista del canvas
        self.root.update_idletasks()
    
    def actualizar_lista_pedido(self):
        """Actualiza la lista visual de items del pedido"""
        # Limpiar lista actual
        for widget in self.items_frame.winfo_children():
            widget.destroy()
        
        # Agregar items
        if self.pedido_actual and self.pedido_actual.items:
            print(f"Debug: Actualizando lista con {len(self.pedido_actual.items)} items")
            for i, item in enumerate(self.pedido_actual.items):
                print(f"Debug: Agregando item {i}: {item.producto.nombre} x{item.cantidad}")
                self.crear_item_pedido(self.items_frame, item, i)
            
            # Forzar actualización visual
            self.items_frame.update()
            self.root.update_idletasks()
        else:
            print("Debug: No hay items en el pedido actual")
            # Mostrar mensaje cuando no hay items
            mensaje_frame = tk.Frame(self.items_frame, bg='white', height=50)
            mensaje_frame.pack(fill=tk.X, pady=20)
            
            tk.Label(mensaje_frame, text="No hay productos en el pedido", 
                    font=('Segoe UI', 10, 'italic'), bg='white', fg='#7f8c8d').pack()
    
    def crear_item_pedido(self, parent, item, index):
        """Crea un elemento visual para cada item del pedido"""
        item_frame = tk.Frame(parent, bg='white' if index % 2 == 0 else '#f8f9fa', 
                             height=40, relief='flat', borderwidth=1)
        item_frame.pack(fill=tk.X, padx=2, pady=1)
        item_frame.pack_propagate(False)
        
        # Nombre del producto (truncado si es muy largo)
        nombre = item.producto.nombre
        if len(nombre) > 18:
            nombre = nombre[:15] + "..."
        
        tk.Label(item_frame, text=nombre, font=('Segoe UI', 9),
                bg=item_frame['bg'], anchor='w').place(x=5, y=12, width=130)
        
        # Botones de cantidad (- y +)
        btn_menos = tk.Button(item_frame, text="-", font=('Segoe UI', 8, 'bold'),
                             bg='#95a5a6', fg='white', relief='flat',
                             borderwidth=0, cursor='hand2', width=1,
                             command=lambda: self.cambiar_cantidad(item.producto.id, -1))
        btn_menos.place(x=140, y=10, width=15, height=20)
        
        # Cantidad
        tk.Label(item_frame, text=str(item.cantidad), font=('Segoe UI', 9, 'bold'),
                bg=item_frame['bg'], anchor='center').place(x=157, y=12, width=25)
        
        btn_mas = tk.Button(item_frame, text="+", font=('Segoe UI', 8, 'bold'),
                           bg='#3498db', fg='white', relief='flat',
                           borderwidth=0, cursor='hand2', width=1,
                           command=lambda: self.cambiar_cantidad(item.producto.id, 1))
        btn_mas.place(x=184, y=10, width=15, height=20)
        
        # Precio unitario
        tk.Label(item_frame, text=f"${item.producto.precio:,.0f}", font=('Segoe UI', 9),
                bg=item_frame['bg'], anchor='e').place(x=205, y=12, width=60)
        
        # Subtotal
        tk.Label(item_frame, text=f"${item.subtotal:,.0f}", font=('Segoe UI', 9, 'bold'),
                bg=item_frame['bg'], fg='#27ae60', anchor='e').place(x=270, y=12, width=70)
        
        # Botón para eliminar (X pequeño)
        btn_eliminar = tk.Button(item_frame, text="×", font=('Segoe UI', 10, 'bold'),
                                bg='#e74c3c', fg='white', relief='flat',
                                borderwidth=0, cursor='hand2', width=2,
                                command=lambda: self.eliminar_item_pedido(item.producto.id))
        btn_eliminar.place(x=345, y=10, width=20, height=20)
    def cambiar_cantidad(self, producto_id, cambio):
        """Cambia la cantidad de un producto en el pedido"""
        try:
            if not self.pedido_actual:
                return
                
            # Buscar el item en el pedido
            for item in self.pedido_actual.items:
                if item.producto.id == producto_id:
                    nueva_cantidad = item.cantidad + cambio
                    
                    # No permitir cantidad menor a 1
                    if nueva_cantidad < 1:
                        # Si llega a 0, eliminar el item
                        self.eliminar_item_pedido(producto_id)
                        return
                    
                    # Actualizar cantidad
                    item.cantidad = nueva_cantidad
                    item.calcular_subtotal()
                    break
            
            # Actualizar totales del pedido
            self.pedido_actual.calcular_totales()
            
            # Refrescar la lista del pedido
            self.actualizar_lista_pedido()
            self.actualizar_totales()
            
            print(f"Cantidad cambiada. Producto ID: {producto_id}, Cambio: {cambio}")
            
        except Exception as e:
            print(f"Error cambiando cantidad: {e}")
    
    def eliminar_item_pedido(self, producto_id):
        """Elimina un item del pedido"""
        if not self.pedido_actual:
            return
        
        # Buscar y remover el producto
        for i, item_pedido in enumerate(self.pedido_actual.items):
            if item_pedido.producto.id == producto_id:
                self.pedido_actual.items.pop(i)
                break
        
        self.pedido_actual.calcular_totales()
        self.actualizar_lista_pedido()
        self.actualizar_totales()
    
    def actualizar_totales(self):
        """Actualiza los labels de totales"""
        if self.pedido_actual:
            # Contar items
            total_items = sum(item.cantidad for item in self.pedido_actual.items)
            self.lbl_items_count.config(text=str(total_items))
            
            # Totales
            self.lbl_subtotal.config(text=f"${self.pedido_actual.subtotal:,.0f}")
            self.lbl_iva.config(text=f"${self.pedido_actual.total_impuestos:,.0f}")
            self.lbl_total.config(text=f"${self.pedido_actual.total:,.0f}")
        else:
            self.lbl_items_count.config(text="0")
            self.lbl_subtotal.config(text="$0")
            self.lbl_iva.config(text="$0")
            self.lbl_total.config(text="$0")
    
    def cancelar_pedido(self):
        """Cancela el pedido actual"""
        if messagebox.askyesno("Confirmar", "¿Está seguro de cancelar el pedido actual?"):
            self.nuevo_pedido()
    
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
            self.btn_checkout.config(state="disabled", bg='#95a5a6')
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar pedido: {str(e)}")
    
    def abrir_cocina(self):
        """Abre la ventana de cocina"""
        ventana_cocina = tk.Toplevel(self.root)
        InterfazCocina(ventana_cocina, self.db)
    
    def ver_facturas_generadas(self):
        """Abre la carpeta de facturas generadas"""
        import subprocess
        
        try:
            # Crear la carpeta si no existe
            carpeta_facturas = "facturas_generadas"
            if not os.path.exists(carpeta_facturas):
                os.makedirs(carpeta_facturas)
            
            # Abrir la carpeta en el explorador de Windows
            subprocess.run(f'explorer "{os.path.abspath(carpeta_facturas)}"', shell=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la carpeta de facturas: {str(e)}")
    
    def abrir_gestion_productos(self):
        """Abre la ventana de gestión de productos"""
        GestionProductos(self.root, self.db, self.cargar_productos)
    
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

# Mantener la clase InterfazCocina original pero mejorarla un poco
class InterfazCocina:
    def __init__(self, root, db_manager):
        self.root = root
        self.db = db_manager
        self.root.title("URBAN VIVES - Sistema de Cocina")
        self.root.geometry("900x700")
        self.root.configure(bg='#ecf0f1')
        
        self.configurar_interfaz()
        self.actualizar_pedidos()
        
        # Auto-actualizar cada 30 segundos
        self.auto_actualizar()
    
    def configurar_interfaz(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        titulo = tk.Label(header_frame, text="🍳 URBAN VIVES - COCINA", 
                         font=('Segoe UI', 20, 'bold'), 
                         bg='#2c3e50', fg='white')
        titulo.pack(pady=15)
        
        # Contenido principal
        main_frame = tk.Frame(self.root, bg='#ecf0f1', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título de pedidos pendientes
        tk.Label(main_frame, text="Pedidos Pendientes y En Preparación", 
                font=('Segoe UI', 14, 'bold'), bg='#ecf0f1', fg='#2c3e50').pack(pady=(0, 15))
        
        # Lista de pedidos
        pedidos_frame = tk.Frame(main_frame, bg='white', relief='raised', borderwidth=1)
        pedidos_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("Pedido", "Fecha", "Estado", "Items", "Total")
        self.pedidos_tree = ttk.Treeview(pedidos_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.pedidos_tree.heading(col, text=col)
            self.pedidos_tree.column(col, width=150)
        
        pedidos_scroll = ttk.Scrollbar(pedidos_frame, orient="vertical", command=self.pedidos_tree.yview)
        self.pedidos_tree.configure(yscrollcommand=pedidos_scroll.set)
        
        self.pedidos_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        pedidos_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Botones
        botones_frame = tk.Frame(main_frame, bg='#ecf0f1', pady=20)
        botones_frame.pack()
        
        tk.Button(botones_frame, text="✅ Marcar como Listo", 
                 font=('Segoe UI', 11, 'bold'), bg='#27ae60', fg='white',
                 relief='flat', borderwidth=0, pady=10, padx=20, cursor='hand2',
                 command=self.marcar_listo).pack(side=tk.LEFT, padx=10)
        
        tk.Button(botones_frame, text="🔄 Actualizar", 
                 font=('Segoe UI', 11, 'bold'), bg='#3498db', fg='white',
                 relief='flat', borderwidth=0, pady=10, padx=20, cursor='hand2',
                 command=self.actualizar_pedidos).pack(side=tk.LEFT, padx=10)
        
        tk.Button(botones_frame, text="📋 Ver Detalles", 
                 font=('Segoe UI', 11, 'bold'), bg='#9b59b6', fg='white',
                 relief='flat', borderwidth=0, pady=10, padx=20, cursor='hand2',
                 command=self.ver_detalles).pack(side=tk.LEFT, padx=10)
    
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
        self.root.after(30000, self.auto_actualizar)


class GestionProductos:
    def __init__(self, parent, db, callback_actualizar=None):
        self.parent = parent
        self.db = db
        self.callback_actualizar = callback_actualizar
        
        # Crear ventana
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("URBAN VIVES - Gestión de Productos")
        self.ventana.geometry("1000x700")
        self.ventana.configure(bg='#f0f0f0')
        
        # Variables
        self.productos = []
        self.categorias = [
            "Cafés Calientes", "Cafés Fríos", "Bebidas Especiales", 
            "Frappés", "Tés", "Postres", "Comidas", "Otros"
        ]
        
        # Configurar interfaz
        self.configurar_interfaz()
        self.cargar_productos()
        
    def configurar_interfaz(self):
        """Configura la interfaz de gestión de productos"""
        # Header
        header_frame = tk.Frame(self.ventana, bg='#2c3e50', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="📦 GESTIÓN DE PRODUCTOS", 
                font=('Segoe UI', 20, 'bold'), 
                bg='#2c3e50', fg='white').pack(pady=15)
        
        # Botones de acción
        botones_frame = tk.Frame(self.ventana, bg='#f0f0f0')
        botones_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(botones_frame, text="➕ Agregar Producto", 
                 font=('Segoe UI', 11, 'bold'), bg='#27ae60', fg='white',
                 relief='flat', borderwidth=0, cursor='hand2', padx=20, pady=8,
                 command=self.agregar_producto).pack(side=tk.LEFT, padx=5)
        
        tk.Button(botones_frame, text="🔄 Actualizar Lista", 
                 font=('Segoe UI', 11, 'bold'), bg='#3498db', fg='white',
                 relief='flat', borderwidth=0, cursor='hand2', padx=20, pady=8,
                 command=self.cargar_productos).pack(side=tk.LEFT, padx=5)
        
        # Lista de productos con scrollbar
        lista_frame = tk.Frame(self.ventana, bg='#f0f0f0')
        lista_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Treeview para mostrar productos
        columns = ('ID', 'Nombre', 'Categoría', 'Precio', 'Disponible')
        self.tree = ttk.Treeview(lista_frame, columns=columns, show='headings', height=20)
        
        # Configurar columnas
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre del Producto')
        self.tree.heading('Categoría', text='Categoría')
        self.tree.heading('Precio', text='Precio')
        self.tree.heading('Disponible', text='Disponible')
        
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Nombre', width=300)
        self.tree.column('Categoría', width=150)
        self.tree.column('Precio', width=100, anchor='center')
        self.tree.column('Disponible', width=100, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(lista_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack del treeview y scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones de acción para productos seleccionados
        acciones_frame = tk.Frame(self.ventana, bg='#f0f0f0')
        acciones_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(acciones_frame, text="✏️ Editar", 
                 font=('Segoe UI', 10, 'bold'), bg='#f39c12', fg='white',
                 relief='flat', borderwidth=0, cursor='hand2', padx=15, pady=5,
                 command=self.editar_producto).pack(side=tk.LEFT, padx=5)
        
        tk.Button(acciones_frame, text="🗑️ Eliminar", 
                 font=('Segoe UI', 10, 'bold'), bg='#e74c3c', fg='white',
                 relief='flat', borderwidth=0, cursor='hand2', padx=15, pady=5,
                 command=self.eliminar_producto).pack(side=tk.LEFT, padx=5)
        
        tk.Button(acciones_frame, text="🔄 Cambiar Estado", 
                 font=('Segoe UI', 10, 'bold'), bg='#9b59b6', fg='white',
                 relief='flat', borderwidth=0, cursor='hand2', padx=15, pady=5,
                 command=self.cambiar_estado_producto).pack(side=tk.LEFT, padx=5)
        
    def cargar_productos(self):
        """Carga la lista de productos desde la base de datos"""
        try:
            # Limpiar el treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Obtener productos de la base de datos
            self.productos = self.db.obtener_productos()
            
            # Agregar productos al treeview
            for producto in self.productos:
                estado = "Sí" if producto.disponible else "No"
                precio_formateado = f"${producto.precio:,.0f}"
                
                self.tree.insert('', 'end', values=(
                    producto.id,
                    producto.nombre,
                    producto.categoria,
                    precio_formateado,
                    estado
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando productos: {str(e)}")
    
    def agregar_producto(self):
        """Abre el formulario para agregar un nuevo producto"""
        FormularioProducto(self.ventana, self.db, self.cargar_productos)
    
    def editar_producto(self):
        """Edita el producto seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto para editar")
            return
        
        # Obtener datos del producto seleccionado
        item = self.tree.item(seleccion[0])
        producto_id = item['values'][0]
        
        # Buscar el producto completo
        producto = None
        for p in self.productos:
            if p.id == producto_id:
                producto = p
                break
        
        if producto:
            FormularioProducto(self.ventana, self.db, self.cargar_productos, producto)
        else:
            messagebox.showerror("Error", "No se pudo encontrar el producto")
    
    def eliminar_producto(self):
        """Elimina el producto seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar")
            return
        
        # Obtener datos del producto
        item = self.tree.item(seleccion[0])
        producto_id = item['values'][0]
        producto_nombre = item['values'][1]
        
        # Confirmar eliminación
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar el producto:\n'{producto_nombre}'?\n\nEsta acción no se puede deshacer."
        )
        
        if respuesta:
            try:
                # Eliminar de la base de datos
                self.db.cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
                self.db.conn.commit()
                
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                self.cargar_productos()
                
                # Actualizar la interfaz principal
                if self.callback_actualizar:
                    self.callback_actualizar()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error eliminando producto: {str(e)}")
    
    def cambiar_estado_producto(self):
        """Cambia el estado (disponible/no disponible) del producto seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto para cambiar estado")
            return
        
        # Obtener datos del producto
        item = self.tree.item(seleccion[0])
        producto_id = item['values'][0]
        producto_nombre = item['values'][1]
        estado_actual = item['values'][4] == "Sí"
        
        nuevo_estado = not estado_actual
        estado_texto = "disponible" if nuevo_estado else "no disponible"
        
        respuesta = messagebox.askyesno(
            "Cambiar Estado",
            f"¿Cambiar el estado del producto '{producto_nombre}' a {estado_texto}?"
        )
        
        if respuesta:
            try:
                # Actualizar en la base de datos
                self.db.cursor.execute(
                    "UPDATE productos SET disponible = ? WHERE id = ?", 
                    (nuevo_estado, producto_id)
                )
                self.db.conn.commit()
                
                messagebox.showinfo("Éxito", f"Estado cambiado a {estado_texto}")
                self.cargar_productos()
                
                # Actualizar la interfaz principal
                if self.callback_actualizar:
                    self.callback_actualizar()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error cambiando estado: {str(e)}")


class FormularioProducto:
    def __init__(self, parent, db, callback_actualizar, producto_editar=None):
        self.parent = parent
        self.db = db
        self.callback_actualizar = callback_actualizar
        self.producto_editar = producto_editar
        
        # Crear ventana
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Agregar Producto" if not producto_editar else "Editar Producto")
        self.ventana.geometry("500x400")
        self.ventana.configure(bg='#f0f0f0')
        self.ventana.grab_set()  # Modal
        
        # Variables
        self.categorias = [
            "Cafés Calientes", "Cafés Fríos", "Bebidas Especiales", 
            "Frappés", "Tés", "Postres", "Comidas", "Otros"
        ]
        
        # Configurar interfaz
        self.configurar_interfaz()
        
        # Si estamos editando, llenar los campos
        if self.producto_editar:
            self.llenar_campos_edicion()
    
    def configurar_interfaz(self):
        """Configura la interfaz del formulario"""
        # Header
        header_frame = tk.Frame(self.ventana, bg='#34495e', height=50)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        titulo = "➕ AGREGAR PRODUCTO" if not self.producto_editar else "✏️ EDITAR PRODUCTO"
        tk.Label(header_frame, text=titulo, 
                font=('Segoe UI', 16, 'bold'), 
                bg='#34495e', fg='white').pack(pady=15)
        
        # Formulario
        form_frame = tk.Frame(self.ventana, bg='#f0f0f0')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Nombre del producto
        tk.Label(form_frame, text="Nombre del Producto:", 
                font=('Segoe UI', 11, 'bold'), bg='#f0f0f0').pack(anchor='w', pady=(0, 5))
        self.entry_nombre = tk.Entry(form_frame, font=('Segoe UI', 11), width=40)
        self.entry_nombre.pack(fill=tk.X, pady=(0, 15))
        
        # Categoría
        tk.Label(form_frame, text="Categoría:", 
                font=('Segoe UI', 11, 'bold'), bg='#f0f0f0').pack(anchor='w', pady=(0, 5))
        self.combo_categoria = ttk.Combobox(form_frame, values=self.categorias, 
                                           font=('Segoe UI', 11), state='readonly')
        self.combo_categoria.pack(fill=tk.X, pady=(0, 15))
        
        # Precio
        tk.Label(form_frame, text="Precio (COP):", 
                font=('Segoe UI', 11, 'bold'), bg='#f0f0f0').pack(anchor='w', pady=(0, 5))
        self.entry_precio = tk.Entry(form_frame, font=('Segoe UI', 11), width=40)
        self.entry_precio.pack(fill=tk.X, pady=(0, 15))
        
        # Estado disponible
        self.var_disponible = tk.BooleanVar(value=True)
        self.check_disponible = tk.Checkbutton(form_frame, text="Producto disponible", 
                                              variable=self.var_disponible,
                                              font=('Segoe UI', 11), bg='#f0f0f0')
        self.check_disponible.pack(anchor='w', pady=(0, 20))
        
        # Botones
        botones_frame = tk.Frame(form_frame, bg='#f0f0f0')
        botones_frame.pack(fill=tk.X, pady=(20, 0))
        
        tk.Button(botones_frame, text="💾 Guardar", 
                 font=('Segoe UI', 11, 'bold'), bg='#27ae60', fg='white',
                 relief='flat', borderwidth=0, cursor='hand2', padx=20, pady=8,
                 command=self.guardar_producto).pack(side=tk.LEFT, padx=5)
        
        tk.Button(botones_frame, text="❌ Cancelar", 
                 font=('Segoe UI', 11, 'bold'), bg='#95a5a6', fg='white',
                 relief='flat', borderwidth=0, cursor='hand2', padx=20, pady=8,
                 command=self.ventana.destroy).pack(side=tk.LEFT, padx=5)
    
    def llenar_campos_edicion(self):
        """Llena los campos con los datos del producto a editar"""
        if self.producto_editar:
            self.entry_nombre.insert(0, self.producto_editar.nombre)
            self.combo_categoria.set(self.producto_editar.categoria)
            self.entry_precio.insert(0, str(int(self.producto_editar.precio)))
            self.var_disponible.set(self.producto_editar.disponible)
    
    def guardar_producto(self):
        """Guarda el producto en la base de datos"""
        try:
            # Validar campos
            nombre = self.entry_nombre.get().strip()
            categoria = self.combo_categoria.get()
            precio_texto = self.entry_precio.get().strip()
            disponible = self.var_disponible.get()
            
            # Validaciones
            if not nombre:
                messagebox.showerror("Error", "El nombre del producto es obligatorio")
                return
            
            if not categoria:
                messagebox.showerror("Error", "Debe seleccionar una categoría")
                return
            
            try:
                precio = float(precio_texto)
                if precio <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "El precio debe ser un número válido mayor a 0")
                return
            
            # Verificar que el nombre no esté duplicado (excepto si estamos editando el mismo producto)
            productos_existentes = self.db.obtener_productos()
            for p in productos_existentes:
                if p.nombre.lower() == nombre.lower():
                    if not self.producto_editar or p.id != self.producto_editar.id:
                        messagebox.showerror("Error", f"Ya existe un producto con el nombre '{nombre}'")
                        return
            
            # Guardar en la base de datos
            if self.producto_editar:
                # Actualizar producto existente
                self.db.cursor.execute("""
                    UPDATE productos 
                    SET nombre = ?, categoria = ?, precio = ?, disponible = ?
                    WHERE id = ?
                """, (nombre, categoria, precio, disponible, self.producto_editar.id))
                mensaje = "Producto actualizado correctamente"
            else:
                # Agregar nuevo producto
                self.db.cursor.execute("""
                    INSERT INTO productos (nombre, categoria, precio, disponible)
                    VALUES (?, ?, ?, ?)
                """, (nombre, categoria, precio, disponible))
                mensaje = "Producto agregado correctamente"
            
            self.db.conn.commit()
            messagebox.showinfo("Éxito", mensaje)
            
            # Actualizar la lista de productos
            if self.callback_actualizar:
                self.callback_actualizar()
            
            # Cerrar ventana
            self.ventana.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando producto: {str(e)}")


def main():
    root = tk.Tk()
    app = InterfazCajaModerna(root)
    root.mainloop()

if __name__ == "__main__":
    main()