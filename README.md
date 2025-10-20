# 🏪 URBAN VIVES - Sistema de Cafetería POS

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows-green.svg)](https://windows.com)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](https://github.com)

Sistema completo de **Punto de Venta (POS)** para cafetería premium con interfaz moderna, gestión de pedidos, facturación automática e impresión térmica. Desarrollado específicamente para **URBAN VIVES** con menú estilo Starbucks y cumplimiento fiscal colombiano.

---

## 📋 Tabla de Contenidos

- [🚀 Características Principales](#-características-principales)
- [🏗️ Arquitectura del Sistema](#️-arquitectura-del-sistema)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)
- [⚡ Instalación Rápida](#-instalación-rápida)
- [🎯 Cómo Usar el Sistema](#-cómo-usar-el-sistema)
- [📦 Gestión de Productos](#-gestión-de-productos)
- [☕ Menú Completo URBAN VIVES](#-menú-completo-urban-vives)
- [🧾 Sistema de Facturación](#-sistema-de-facturación)
- [🖨️ Configuración de Impresión](#️-configuración-de-impresión)
- [💾 Base de Datos](#-base-de-datos)
- [🛠️ Solución de Problemas](#️-solución-de-problemas)
- [🔧 Personalización](#-personalización)
- [📞 Soporte](#-soporte)

---

## 🚀 Características Principales

### 💻 **Interfaz Moderna POS**
- ✅ Diseño profesional estilo café premium
- ✅ Selección de productos con **doble clic**
- ✅ Gestión intuitiva de cantidades con botones **+ / -**
- ✅ Categorías organizadas (8 categorías, 47+ productos)
- ✅ Experiencia de usuario optimizada sin interrupciones
- ✅ Responsive design para diferentes resoluciones

### 🏪 **Sistema de Caja Completo**
- ✅ Toma de pedidos rápida y eficiente
- ✅ Cálculo automático de totales con **IVA 19%**
- ✅ Múltiples métodos de pago:
  - 💵 **Efectivo**
  - 🏦 **Transferencia bancaria**
  - 💳 **Tarjeta de crédito/débito**
- ✅ Gestión de datos del cliente (opcional)
- ✅ Numeración automática de pedidos con prefijo **UV-**

### 🍳 **Sistema de Cocina**
- ✅ Vista en tiempo real de pedidos pendientes
- ✅ Estados de pedidos: Pendiente → En preparación → Listo
- ✅ Auto-actualización cada 30 segundos
- ✅ Vista detallada de items por pedido
- ✅ Interface limpia para el personal de cocina

### 📦 **Gestión de Productos (NUEVO)**
- ✅ **Agregar productos** con formulario completo
- ✅ **Editar productos** existentes (nombre, precio, categoría)
- ✅ **Eliminar productos** con confirmación de seguridad
- ✅ **Cambiar estado** disponible/no disponible
- ✅ **Vista de tabla** con ordenamiento por categoría
- ✅ **Validaciones** para evitar duplicados
- ✅ **Actualización automática** de la interfaz principal
- ✅ **8 categorías predefinidas** + categoría "Otros"

### 🧾 **Facturación Profesional**
- ✅ Generación automática de facturas con formato fiscal
- ✅ Cumplimiento normativo colombiano
- ✅ Datos fiscales completos (NIT, dirección, teléfono)
- ✅ Discriminación detallada de impuestos
- ✅ Exportación a **PDF** para archivo
- ✅ **Impresión térmica** directa
- ✅ Respaldo digital automático

### 💾 **Base de Datos Robusta**
- ✅ **SQLite** para persistencia local confiable
- ✅ Histórico completo de transacciones
- ✅ Gestión de productos, pedidos, clientes y facturas
- ✅ Backup automático de datos críticos
- ✅ Consultas optimizadas para rendimiento

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    URBAN VIVES POS                         │
├─────────────────────────────────────────────────────────────┤
│  main.py (Punto de Entrada)                                │
│  ├── InterfazCajaModerna (GUI Principal)                   │
│  ├── InterfazCocina (Sistema Cocina)                       │
│  └── DatabaseManager (Gestión de Datos)                    │
├─────────────────────────────────────────────────────────────┤
│  MODELOS DE NEGOCIO                                        │
│  ├── Producto (47 items premium)                           │
│  ├── Pedido (Numeración UV-XXXXX)                          │
│  ├── ItemPedido (Cantidades + Subtotales)                  │
│  ├── Factura (Fiscalización IVA 19%)                       │
│  └── Cliente (Datos opcionales)                            │
├─────────────────────────────────────────────────────────────┤
│  PERSISTENCIA                                              │
│  ├── SQLite Database (cafeteria.db)                        │
│  ├── PDF Generator (ReportLab)                             │
│  └── Thermal Printer (Windows Driver)                      │
└─────────────────────────────────────────────────────────────┘
```

**Patrón de Arquitectura**: MVC (Model-View-Controller)
- **Models**: Lógica de negocio (Producto, Pedido, Factura)
- **Views**: Interfaces gráficas (Caja, Cocina)
- **Controllers**: Gestión de datos y flujo (DatabaseManager)

---

## 📁 Estructura del Proyecto

```
sistema_cafeteria/
├── 📄 main.py                     # Punto de entrada principal
├── 📄 requirements.txt            # Dependencias del proyecto
├── 📄 README.md                   # Documentación completa
├── 
├── 📂 models/                     # 🎯 Modelos de negocio
│   ├── __init__.py
│   └── models.py                  # Producto, Pedido, ItemPedido, Factura, Cliente
│
├── 📂 database/                   # 💾 Gestión de datos
│   ├── __init__.py
│   └── db_manager.py             # DatabaseManager + menú completo
│
├── 📂 gui/                       # 🖥️ Interfaces gráficas
│   ├── __init__.py
│   ├── interfaz_moderna.py       # POS moderna con doble clic
│   └── interfaz_cocina.py        # Sistema de cocina
│
├── 📂 utils/                     # 🛠️ Utilidades
│   ├── __init__.py
│   └── factura_generator.py     # Generación PDF + impresión térmica
│
├── 📂 facturas_generadas/        # 📁 PDFs de facturas (auto-generado)
├── 📂 reports/                   # 📊 Reportes del sistema (auto-generado)
└── 📄 cafeteria.db               # 🗄️ Base de datos SQLite (auto-generado)
```

### **Archivos Clave:**

| Archivo | Propósito | Líneas de Código |
|---------|-----------|------------------|
| `main.py` | Inicialización y menú principal | ~50 |
| `models/models.py` | Clases de negocio y cálculos | ~200 |
| `database/db_manager.py` | Gestión BD + menú completo | ~300+ |
| `gui/interfaz_moderna.py` | POS moderna | ~800+ |
| `gui/interfaz_cocina.py` | Sistema de cocina | ~400 |
| `utils/factura_generator.py` | Facturación e impresión | ~250 |

---

## ⚡ Instalación Rápida

### **Prerrequisitos**
- 🐍 **Python 3.7+** (Recomendado: Python 3.9+)
- 🖥️ **Windows 10/11** (Probado y optimizado)
- 🖨️ **Impresora** configurada (opcional para impresión)

### **1. Clonar/Descargar el Proyecto**
```powershell
# Si usas Git
git clone <repository-url>
cd sistema_cafeteria

# O descargar ZIP y extraer
```

### **2. Instalar Dependencias**
```powershell
# Instalar ReportLab para PDFs
pip install reportlab

# Las demás dependencias vienen con Python:
# - tkinter (GUI)
# - sqlite3 (Base de datos)
# - datetime (Fechas)
# - os, sys (Sistema)
```

### **3. Ejecutar el Sistema**
```powershell
# Navegar a la carpeta
cd sistema_cafeteria

# Ejecutar
python main.py
```

### **4. Primera Ejecución**
El sistema automáticamente:
- ✅ Crea la base de datos `cafeteria.db`
- ✅ Inserta los 47 productos del menú URBAN VIVES
- ✅ Configura las tablas necesarias
- ✅ Muestra el menú principal

---

## 🎯 Cómo Usar el Sistema

### **🏪 Modo Caja (Cajero)**

#### **1. Agregar Productos al Pedido**
```
📱 DOBLE CLIC en cualquier producto
   ↓
✅ Se agrega con cantidad 1
   ↓
🔄 Mismo producto = Aumenta cantidad automáticamente
```

#### **2. Gestionar Cantidades**
- **Aumentar**: Botón **[+]** verde
- **Disminuir**: Botón **[-]** gris
- **Eliminar**: Botón **[×]** rojo

#### **3. Procesar Pago**
```
1. 👤 Datos del cliente (opcional)
   ├── Nombre
   └── NIT/Cédula

2. 💳 Seleccionar método de pago
   ├── Efectivo
   ├── Transferencia
   └── Tarjeta

3. 🧾 Generar factura
   ├── PDF automático
   ├── Impresión térmica
   └── Envío a cocina
```

### **🍳 Modo Cocina**

#### **Vista de Pedidos**
- 📋 **Pendientes**: Nuevos pedidos recibidos
- 👨‍🍳 **En Preparación**: Pedidos siendo preparados
- ✅ **Listos**: Pedidos completados

#### **Gestión de Estados**
1. **Recibir pedido** → Automático desde caja
2. **Marcar "En Preparación"** → Botón azul
3. **Marcar "Listo"** → Botón verde
4. **Auto-actualización** → Cada 30 segundos

### **📦 Gestión de Productos**

#### **Acceso al Sistema**
1. **Clic en "📦 Productos"** en la barra de navegación
2. Se abre la ventana de gestión de productos

#### **Agregar Nuevo Producto**
```
1. 📱 Clic en "➕ Agregar Producto"
   ↓
2. 📝 Llenar formulario:
   ├── Nombre del producto
   ├── Categoría (8 opciones + Otros)
   ├── Precio (solo números)
   └── Estado disponible (checkbox)
   ↓
3. 💾 Clic en "Guardar"
   ↓
4. ✅ Producto agregado y visible en POS
```

#### **Editar Producto Existente**
```
1. 📋 Seleccionar producto en la tabla
   ↓
2. ✏️ Clic en "Editar"
   ↓
3. 📝 Modificar campos necesarios
   ↓
4. 💾 Guardar cambios
```

#### **Cambiar Estado de Producto**
```
1. 📋 Seleccionar producto
   ↓
2. 🔄 Clic en "Cambiar Estado"
   ↓
3. ✅ Confirmar acción
   ↓
4. 🔄 Producto disponible/no disponible en POS
```

#### **Eliminar Producto**
```
⚠️ CUIDADO: Esta acción no se puede deshacer

1. 📋 Seleccionar producto
   ↓
2. 🗑️ Clic en "Eliminar"
   ↓
3. ⚠️ Confirmar eliminación
   ↓
4. ❌ Producto eliminado permanentemente
```

#### **Funciones Adicionales**
- **🔄 Actualizar Lista**: Refresca la tabla de productos
- **📊 Ordenamiento**: Por categoría y nombre automático
- **✅ Validaciones**: No permite nombres duplicados
- **🔄 Actualización Automática**: El POS se actualiza al guardar cambios

---

## ☕ Menú Completo URBAN VIVES

### **🔥 CAFÉS CALIENTES** (7 productos)
| Producto | Precio | Descripción |
|----------|--------|-------------|
| ☕ Espresso Simple | $5,000 | Shot puro de café |
| ☕ Espresso Doble | $7,000 | Doble shot intenso |
| ☕ Americano | $6,000 | Espresso + agua caliente |
| ☕ Latte | $8,000 | Espresso + leche vaporizada |
| ☕ Cappuccino | $8,500 | Espresso + espuma de leche |
| ☕ Macchiato | $7,500 | Espresso "manchado" |
| ☕ Flat White | $9,500 | Café australiano premium |

### **🧊 CAFÉS FRÍOS** (5 productos)
| Producto | Precio | Descripción |
|----------|--------|-------------|
| ❄️ Cold Brew | $9,000 | Café frío en frío 12h |
| ❄️ Iced Latte | $8,500 | Latte servido con hielo |
| ❄️ Iced Americano | $7,000 | Americano frío |
| ❄️ Affogato | $10,000 | Helado + shot espresso |
| ❄️ Caramel Macchiato Frío | $9,500 | Macchiato helado |

### **🍫 BEBIDAS ESPECIALES** (8 productos)
| Producto | Precio | Descripción |
|----------|--------|-------------|
| 🍫 Mocha | $9,000 | Café + chocolate |
| 🤍 White Mocha | $9,000 | Mocha con chocolate blanco |
| 🍫 Iced Mocha | $9,000 | Mocha frío |
| 🤍 Iced White Mocha | $9,000 | White mocha frío |
| 🍃 Matcha Latte | $9,000 | Té verde japonés + leche |
| 🌶️ Chai Latte | $9,000 | Té especiado indio |
| 🟡 Golden Milk | $9,500 | Cúrcuma + leche + especias |
| 🍯 Honey Latte | $8,500 | Latte endulzado con miel |

### **🥤 FRAPPÉS** (5 productos)
| Producto | Precio | Descripción |
|----------|--------|-------------|
| 🌪️ Frappé Café Clásico | $9,000 | Café batido con hielo |
| 🍫 Mocha Frappé | $10,000 | Frappé de chocolate |
| 🍮 Caramel Frappé | $10,000 | Frappé de caramelo |
| 🍪 Cookies & Cream Frappé | $10,500 | Frappé de galleta |
| 🍃 Matcha Frappé | $11,000 | Frappé de té verde |

### **🍵 TÉS** (4 productos)
| Producto | Precio | Descripción |
|----------|--------|-------------|
| 🍵 Té Negro | $6,000 | Earl Grey, English Breakfast |
| 🌿 Té Verde | $6,000 | Sencha, Jasmine |
| 🌸 Té de Hierbas | $6,000 | Manzanilla, menta |
| 🍋 Té de Frutos | $6,000 | Frutas del bosque |

### **🧁 POSTRES** (8 productos)
| Producto | Precio | Descripción |
|----------|--------|-------------|
| 🧁 Muffin de Arándanos | $5,500 | Recién horneado |
| 🧁 Muffin de Chocolate | $5,500 | Con chips de chocolate |
| 🥐 Croissant Simple | $6,500 | Masa hojaldre francesa |
| 🥐 Croissant de Almendras | $7,500 | Con crema de almendras |
| 🍰 Cheesecake | $8,000 | Porción individual |
| 🍰 Tiramisu | $8,000 | Postre italiano |
| 🍪 Galleta Chocochips | $5,000 | Galleta artesanal |
| 🍫 Brownie | $6,000 | Con nueces |

### **🥪 COMIDAS** (10 productos)
| Producto | Precio | Descripción |
|----------|--------|-------------|
| 🥪 Sandwich Club | $11,000 | Pavo, tocino, lechuga |
| 🥪 Sandwich Vegetariano | $9,000 | Verduras frescas |
| 🥪 Sandwich de Pollo | $10,000 | Pollo grillado |
| 🌯 Wrap de Pollo | $9,500 | Tortilla integral |
| 🌯 Wrap Vegetariano | $9,000 | Sin proteína animal |
| 🥖 Panini Caprese | $9,500 | Tomate, mozzarella, albahaca |
| 🥖 Panini de Jamón | $9,500 | Jamón serrano y queso |
| 🥗 Ensalada César | $10,000 | Con pollo opcional |
| 🥗 Ensalada Griega | $9,500 | Queso feta y aceitunas |
| 🍯 Tostada con Palta | $8,000 | Aguacate y semillas |

**📊 ESTADÍSTICAS DEL MENÚ:**
- **Total productos**: 47 items
- **Categorías**: 8 categorías
- **Rango de precios**: $5,000 - $11,000
- **Promedio**: $8,200 por producto
- **Estilo**: Premium café internacional

---

## 🧾 Sistema de Facturación

### **📋 Información Fiscal**
```
🏢 URBAN VIVES
📍 Calle 123 #45-67, Bogotá, Colombia
📞 (601) 234-5678
📧 info@urbanvives.com
🆔 NIT: 900.123.456-7
💼 Régimen Común
```

### **📄 Formato de Factura**

```
===============================================
           🏢 URBAN VIVES
        FACTURA DE VENTA
===============================================
📅 Fecha: 20/10/2025 14:30:15
🧾 Factura N°: UV-001234
👤 Cliente: Juan Pérez
🆔 NIT/CC: 12345678
💰 Método: Efectivo
===============================================
DETALLE DE PRODUCTOS:
-----------------------------------------------
☕ Latte                  1x  $8,000   $8,000
🧁 Muffin Chocolate       2x  $5,500  $11,000
                                    ----------
                         Subtotal:   $19,000
                         IVA (19%):   $3,610
                                    ----------
                         TOTAL:      $22,610
===============================================
👨‍💼 Cajero: Sistema URBAN VIVES
🖨️ Caja: 001
⏰ Proc: 20/10/2025 14:30:15

    ¡Gracias por su compra!
      www.urbanvives.com
===============================================
```

### **💾 Archivos Generados**
- **PDF**: `facturas_generadas/factura_UV-001234.pdf`
- **Backup DB**: Registro en tabla `facturas`
- **Impresión**: Directo a impresora térmica

---

## 🖨️ Configuración de Impresión

### **🎯 Impresoras Soportadas**
- ✅ **Impresoras térmicas** (58mm, 80mm)
- ✅ **Impresoras láser/inyección** (formato A4)
- ✅ **Impresoras virtuales** (PDF)

### **⚙️ Configuración Windows**

#### **1. Instalar Impresora**
```
Panel de Control → Dispositivos e impresoras → Agregar impresora
```

#### **2. Configurar como Predeterminada**
```
Clic derecho en impresora → Establecer como predeterminada
```

#### **3. Probar Impresión**
```
En el sistema: Procesar Pago → Imprimir Factura
```

### **🔧 Solución de Problemas de Impresión**

| Problema | Solución |
|----------|----------|
| 🚫 No imprime | Verificar que la impresora esté encendida y conectada |
| 📄 Formato incorrecto | Ajustar configuración de papel en Windows |
| ⏳ Impresión lenta | Usar impresoras térmicas para velocidad |
| 💾 Solo PDF | Normal si no hay impresora física configurada |

### **📐 Configuraciones Recomendadas**

#### **Impresora Térmica (58mm)**
```
- Ancho: 58mm
- Velocidad: Alta
- Densidad: Media
- Corte automático: Sí
```

#### **Impresora Convencional**
```
- Papel: A4
- Orientación: Retrato
- Márgenes: Mínimos
- Calidad: Normal
```

---

## 💾 Base de Datos

### **🗄️ Estructura de Tablas**

#### **`productos`** (47+ registros - Gestión dinámica)
```sql
CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    categoria TEXT NOT NULL,
    precio REAL NOT NULL,
    disponible BOOLEAN DEFAULT TRUE  -- NUEVO: Control de disponibilidad
);
```

**Funcionalidades de gestión:**
- ✅ **CRUD completo**: Crear, leer, actualizar, eliminar
- ✅ **Validación de duplicados**: No permite nombres repetidos
- ✅ **Control de disponibilidad**: Productos disponibles/no disponibles
- ✅ **Migración automática**: De campo 'activo' a 'disponible'
- ✅ **Categorías predefinidas**: 8 categorías + "Otros"
- ✅ **Actualización en tiempo real**: Cambios reflejados inmediatamente en POS

#### **`pedidos`** (Numeración UV-XXXXXX)
```sql
CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero TEXT UNIQUE NOT NULL,
    cliente_nombre TEXT,
    cliente_nit TEXT,
    estado TEXT DEFAULT 'pendiente',
    subtotal REAL,
    impuestos REAL,
    total REAL,
    metodo_pago TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **`items_pedido`** (Detalle de productos)
```sql
CREATE TABLE items_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER,
    producto_id INTEGER,
    cantidad INTEGER,
    precio_unitario REAL,
    subtotal REAL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);
```

#### **`facturas`** (Respaldo fiscal)
```sql
CREATE TABLE facturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero TEXT UNIQUE NOT NULL,
    pedido_id INTEGER,
    cliente_nombre TEXT,
    cliente_nit TEXT,
    subtotal REAL,
    impuestos REAL,
    total REAL,
    metodo_pago TEXT,
    archivo_pdf TEXT,
    fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
);
```

### **🔄 Operaciones Automáticas**

#### **Al Iniciar el Sistema**
1. ✅ Verificar existencia de `cafeteria.db`
2. ✅ Crear tablas si no existen
3. ✅ Insertar menú URBAN VIVES (47 productos)
4. ✅ Verificar integridad de datos

#### **Al Procesar Pedido**
1. ✅ Generar número único (UV-XXXXXX)
2. ✅ Calcular totales con IVA 19%
3. ✅ Guardar en `pedidos` e `items_pedido`
4. ✅ Generar factura en `facturas`
5. ✅ Crear archivo PDF

#### **Backup y Mantenimiento**
```powershell
# Backup manual de la base de datos
copy cafeteria.db cafeteria_backup_20251020.db

# Ver estadísticas
sqlite3 cafeteria.db "SELECT COUNT(*) as total_pedidos FROM pedidos;"
sqlite3 cafeteria.db "SELECT SUM(total) as ventas_totales FROM pedidos;"
```

---

## 🛠️ Solución de Problemas

### **🚨 Errores Comunes**

#### **1. Error al Iniciar**
```
❌ ModuleNotFoundError: No module named 'reportlab'
✅ Solución: pip install reportlab
```

#### **2. Error de Base de Datos**
```
❌ sqlite3.OperationalError: database is locked
✅ Solución: Cerrar todas las instancias del programa
```

#### **3. Error de Impresión**
```
❌ No se puede imprimir
✅ Verificar:
   - Impresora encendida
   - Drivers instalados
   - Papel disponible
```

#### **4. Interfaz No Responde**
```
❌ La ventana se congela
✅ Solución:
   - Reiniciar el programa
   - Verificar recursos del sistema
   - Actualizar drivers gráficos
```

### **🔍 Modo Debug**

Para activar logs detallados, modificar en `main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### **📊 Verificar Estado del Sistema**

#### **Base de Datos**
```python
# En terminal Python
import sqlite3
conn = sqlite3.connect('cafeteria.db')
cursor = conn.cursor()

# Verificar productos
cursor.execute("SELECT COUNT(*) FROM productos")
print(f"Productos: {cursor.fetchone()[0]}")

# Verificar pedidos
cursor.execute("SELECT COUNT(*) FROM pedidos")
print(f"Pedidos: {cursor.fetchone()[0]}")
```

#### **Archivos Críticos**
```powershell
# Verificar archivos esenciales
dir main.py              # ✅ Debe existir
dir cafeteria.db         # ✅ Se crea automáticamente
dir models\models.py     # ✅ Debe existir
dir gui\interfaz_moderna.py  # ✅ Debe existir
```

---

## 🔧 Personalización

### **🎨 Cambiar Branding**

#### **1. Datos de la Empresa**
Modificar en `models/models.py`:
```python
def obtener_datos_empresa():
    return {
        'nombre': 'TU CAFÉ',           # Cambiar nombre
        'nit': '900.123.456-7',        # Cambiar NIT
        'direccion': 'Tu dirección',    # Cambiar dirección
        'telefono': '(601) 234-5678',   # Cambiar teléfono
        'email': 'tu@email.com'         # Cambiar email
    }
```

#### **2. Colores de la Interfaz**
Modificar en `gui/interfaz_moderna.py`:
```python
# Cambiar colores principales
COLOR_PRINCIPAL = '#2c3e50'    # Azul oscuro
COLOR_SECUNDARIO = '#3498db'   # Azul claro
COLOR_ACENTO = '#e74c3c'       # Rojo
COLOR_EXITO = '#27ae60'        # Verde
```

### **🍽️ Modificar Menú**

#### **1. Agregar Productos**
En `database/db_manager.py`, agregar en `insertar_productos_inicial()`:
```python
productos.append(('Nuevo Producto', 'Categoría', 12000))
```

#### **2. Cambiar Precios**
```sql
UPDATE productos SET precio = 15000 WHERE nombre = 'Latte';
```

#### **3. Agregar Categorías**
Agregar nueva categoría en la lista de productos y en la interfaz.

### **💰 Cambiar Impuestos**

En `models/models.py`, método `calcular_totales()`:
```python
def calcular_totales(self):
    self.subtotal = sum(item.subtotal for item in self.items)
    self.impuestos = self.subtotal * 0.16  # Cambiar a 16% si necesario
    self.total = self.subtotal + self.impuestos
```

### **🎯 Funcionalidades Adicionales**

#### **1. Descuentos**
Agregar campo `descuento` en modelo `Pedido` y lógica en interfaz.

#### **2. Propinas**
Agregar campo `propina` y modificar cálculo de totales.

#### **3. Múltiples Sucursales**
Agregar tabla `sucursales` y campo `sucursal_id` en pedidos.

#### **4. Inventario**
Agregar campo `stock` en productos y decrementar con ventas.

---

## 📞 Soporte

### **🆘 Soporte Técnico**

Para soporte técnico, consultas o personalizaciones:

- 📧 **Email**: soporte@urbanvives.com
- 📱 **WhatsApp**: +57 300 123 4567
- 🌐 **Web**: www.urbanvives.com/soporte
- 📋 **Tickets**: sistema.urbanvives.com/tickets

### **📚 Recursos Adicionales**

- 📖 **Manual de Usuario**: `docs/manual_usuario.pdf`
- 🎥 **Videos Tutorial**: `docs/videos/`
- ❓ **FAQ**: `docs/preguntas_frecuentes.md`
- 🔧 **API Docs**: `docs/api_reference.md`

### **🤝 Contribuir**

¿Encontraste un bug o tienes una sugerencia?

1. 🐛 **Reportar Bug**: GitHub Issues
2. 💡 **Sugerir Mejora**: GitHub Discussions  
3. 🔧 **Pull Request**: Fork y PR
4. 📧 **Contacto Directo**: dev@urbanvives.com

### **📄 Licencia**

```
© 2025 URBAN VIVES - Sistema de Cafetería POS
Desarrollado para uso comercial interno.
Todos los derechos reservados.

Para licencias comerciales adicionales contactar:
licensing@urbanvives.com
```

---

## 🎯 Próximas Actualizaciones

### **🚀 Version 3.0 (Q1 2025)**
- [ ] 📱 **App móvil** para meseros
- [ ] ☁️ **Sincronización en la nube**
- [ ] 📊 **Dashboard de analytics**
- [ ] 🔔 **Notificaciones push**
- [ ] 💳 **Integración con datáfonos**

### **🔧 Version 2.1 (Próxima)**
- [ ] 🎯 **Descuentos y promociones**
- [ ] 👥 **Múltiples usuarios**
- [ ] 📦 **Control de inventario**
- [ ] 🧾 **Reportes avanzados**
- [ ] 🔄 **Sincronización automática**

---

**📍 URBAN VIVES - Sistema de Cafetería POS v2.0**  
*🚀 Desarrollado para optimizar las operaciones de caja y cocina*  
*☕ Menú premium estilo internacional con cumplimiento fiscal colombiano*  
*💻 Interfaz moderna y experiencia de usuario excepcional*

---

[![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red.svg)](https://urbanvives.com)
[![Python](https://img.shields.io/badge/Built%20with-Python-blue.svg)](https://python.org)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)](https://docs.python.org/3/library/tkinter.html)
[![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)](https://sqlite.org)