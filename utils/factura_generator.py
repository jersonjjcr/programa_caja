from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os
import subprocess
from models.models import Factura, Pedido
from .configurador_impresora import ConfiguradorImpresora

class GeneradorFacturas:
    def __init__(self):
        # Crear carpeta de facturas si no existe
        self.directorio_facturas = "facturas_generadas"
        if not os.path.exists(self.directorio_facturas):
            os.makedirs(self.directorio_facturas)
        
        # Inicializar configurador de impresora
        self.configurador = ConfiguradorImpresora()
        self.impresoras_disponibles = self.configurador.obtener_impresoras_disponibles()
        self.impresora_predeterminada = self.configurador.obtener_impresora_predeterminada()
    
    def generar_factura_pdf(self, factura: Factura) -> str:
        """Genera una factura en PDF y retorna la ruta del archivo"""
        filename = f"{self.directorio_facturas}/factura_{factura.numero}.pdf"
        
        # Configurar el documento para ticket (más angosto)
        doc = SimpleDocTemplate(
            filename,
            pagesize=(80*mm, 200*mm),  # Ancho de ticket térmico
            rightMargin=2*mm,
            leftMargin=2*mm,
            topMargin=5*mm,
            bottomMargin=5*mm
        )
        
        # Estilos
        styles = getSampleStyleSheet()
        
        # Estilo para encabezado
        estilo_encabezado = ParagraphStyle(
            'EncabezadoTicket',
            parent=styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            spaceAfter=2
        )
        
        # Estilo para texto normal
        estilo_normal = ParagraphStyle(
            'NormalTicket',
            parent=styles['Normal'],
            fontSize=7,
            alignment=TA_LEFT,
            spaceAfter=1
        )
        
        # Estilo para texto centrado
        estilo_centrado = ParagraphStyle(
            'CentradoTicket',
            parent=styles['Normal'],
            fontSize=7,
            alignment=TA_CENTER,
            spaceAfter=1
        )
        
        # Crear el contenido
        contenido = []
        
        # Datos de la empresa
        datos_empresa = factura.obtener_datos_empresa()
        
        contenido.append(Paragraph(f"Pedido {factura.pedido.numero_pedido}", estilo_encabezado))
        contenido.append(Paragraph(datos_empresa["nombre"], estilo_encabezado))
        contenido.append(Paragraph(datos_empresa["tienda"], estilo_encabezado))
        contenido.append(Paragraph(datos_empresa["direccion"], estilo_encabezado))
        contenido.append(Paragraph(datos_empresa["nit"], estilo_encabezado))
        contenido.append(Spacer(1, 3*mm))
        
        # Información de la factura
        contenido.append(Paragraph(f"Factura Electrónica de venta No.{factura.numero}", estilo_normal))
        contenido.append(Paragraph(f"FECHA:{factura.fecha_facturacion.strftime('%d/%m/%Y')}", estilo_normal))
        contenido.append(Paragraph(f"HORA:{factura.fecha_facturacion.strftime('%H:%M:%S')}", estilo_normal))
        contenido.append(Paragraph(f"CAJA No {factura.caja_numero}", estilo_normal))
        
        # Información del cliente
        if factura.pedido.cliente.nombre:
            contenido.append(Paragraph(f"CLIENTE:{factura.pedido.cliente.nombre}", estilo_normal))
        if factura.pedido.cliente.nit:
            contenido.append(Paragraph(f"NIT/C.C:{factura.pedido.cliente.nit}", estilo_normal))
        if factura.pedido.cliente.direccion and factura.pedido.cliente.direccion != "None":
            contenido.append(Paragraph(f"DIRECCION:{factura.pedido.cliente.direccion}", estilo_normal))
        else:
            contenido.append(Paragraph("DIRECCION:None", estilo_normal))
        
        contenido.append(Spacer(1, 3*mm))
        
        # Línea separadora
        contenido.append(Paragraph("=" * 40, estilo_centrado))
        
        # Encabezados de productos
        contenido.append(Paragraph("DESCRIPCION       CANT   PVP    VALOR", estilo_normal))
        contenido.append(Paragraph("=" * 40, estilo_centrado))
        
        # Items del pedido
        for item in factura.pedido.items:
            if item.cantidad == 0:
                cantidad_str = "0"
                valor_str = "0"
            else:
                cantidad_str = str(item.cantidad)
                valor_str = f"{item.subtotal:,.0f}"
            
            # Línea del producto
            linea_producto = f"{item.producto.nombre:<18} {cantidad_str:>2} {item.producto.precio:>7,.0f} {valor_str:>7}"
            contenido.append(Paragraph(linea_producto, estilo_normal))
        
        contenido.append(Paragraph("=" * 40, estilo_centrado))
        contenido.append(Spacer(1, 2*mm))
        
        # Discriminación de impuestos
        contenido.append(Paragraph("DISCRIMINACION DE IMPUESTOS", estilo_centrado))
        contenido.append(Paragraph("=" * 40, estilo_centrado))
        contenido.append(Paragraph("IMPUESTOS        BASE    %      CUOTA", estilo_normal))
        contenido.append(Paragraph("=" * 40, estilo_centrado))
        
        for impuesto in factura.pedido.impuestos:
            linea_impuesto = f"{impuesto.nombre:<12} {impuesto.base:>7,.0f} {impuesto.porcentaje:>2.0f} {impuesto.valor:>8,.0f}"
            contenido.append(Paragraph(linea_impuesto, estilo_normal))
        
        contenido.append(Paragraph("=" * 40, estilo_centrado))
        contenido.append(Spacer(1, 2*mm))
        
        # Totales
        contenido.append(Paragraph(f"TOTAL IMPTOS $ {factura.pedido.total_impuestos:>15,.0f}", estilo_normal))
        contenido.append(Paragraph(f"FORMA DE PAGO   CONTADO    TOTAL $ {factura.pedido.total:>7,.0f}", estilo_normal))
        
        # Formas de pago
        for pago in factura.pedido.formas_pago:
            contenido.append(Paragraph(f"MEDIO DE PAGO   {pago.tipo:<12} $ {pago.valor:>7,.0f}", estilo_normal))
        
        contenido.append(Spacer(1, 5*mm))
        contenido.append(Paragraph("Gracias por su compra", estilo_centrado))
        
        # Generar el PDF
        doc.build(contenido)
        return filename
    
    def generar_factura_texto(self, factura: Factura) -> str:
        """Genera una factura en formato texto para impresión directa"""
        lineas = []
        datos_empresa = factura.obtener_datos_empresa()
        
        # Encabezado
        lineas.append(f"Pedido {factura.pedido.numero_pedido}")
        lineas.append(datos_empresa["nombre"])
        lineas.append(datos_empresa["tienda"])
        lineas.append(datos_empresa["direccion"])
        lineas.append(datos_empresa["nit"])
        lineas.append("")
        
        # Información de factura
        lineas.append(f"Factura Electrónica de venta No.{factura.numero}")
        lineas.append(f"FECHA:{factura.fecha_facturacion.strftime('%d/%m/%Y')}    HORA:{factura.fecha_facturacion.strftime('%H:%M:%S')}")
        
        # Cliente
        if factura.pedido.cliente.nombre:
            lineas.append(f"CLIENTE:{factura.pedido.cliente.nombre}")
        if factura.pedido.cliente.nit:
            lineas.append(f"NIT/C.C:{factura.pedido.cliente.nit}")
        lineas.append(f"DIRECCION:{factura.pedido.cliente.direccion if factura.pedido.cliente.direccion else 'None'}")
        lineas.append(f"CAJA No {factura.caja_numero}")
        lineas.append("")
        
        # Separador
        lineas.append("=" * 48)
        lineas.append("DESCRIPCION          CANT   PVP      VALOR")
        lineas.append("=" * 48)
        
        # Items
        for item in factura.pedido.items:
            cantidad = item.cantidad if item.cantidad > 0 else 0
            valor = item.subtotal if item.cantidad > 0 else 0
            lineas.append(f"{item.producto.nombre:<20} {cantidad:>3} {item.producto.precio:>8,.0f} {valor:>8,.0f}")
        
        lineas.append("=" * 48)
        lineas.append("")
        
        # Impuestos
        lineas.append("DISCRIMINACION DE IMPUESTOS")
        lineas.append("=" * 48)
        lineas.append("IMPUESTOS          BASE    %        CUOTA")
        lineas.append("=" * 48)
        
        for impuesto in factura.pedido.impuestos:
            lineas.append(f"{impuesto.nombre:<15} {impuesto.base:>8,.0f} {impuesto.porcentaje:>2.0f} {impuesto.valor:>12,.0f}")
        
        lineas.append("=" * 48)
        lineas.append("")
        
        # Totales
        lineas.append(f"TOTAL IMPTOS $ {factura.pedido.total_impuestos:>25,.0f}")
        lineas.append(f"FORMA DE PAGO  CONTADO    TOTAL $ {factura.pedido.total:>12,.0f}")
        
        # Formas de pago
        for pago in factura.pedido.formas_pago:
            lineas.append(f"MEDIO DE PAGO  {pago.tipo:<15} $ {pago.valor:>12,.0f}")
        
        lineas.append("")
        lineas.append("Gracias por su compra")
        lineas.append("")
        
        return "\n".join(lineas)
    
    def imprimir_factura(self, factura: Factura, impresora: str = None):
        """Imprime la factura en una impresora térmica o por defecto"""
        contenido_texto = self.generar_factura_texto(factura)
        
        # Guardar archivo permanente para referencia
        archivo_factura = f"{self.directorio_facturas}/factura_{factura.numero}.txt"
        with open(archivo_factura, 'w', encoding='utf-8') as f:
            f.write(contenido_texto)
        
        print(f"Factura guardada en: {archivo_factura}")
        print(f"Impresoras disponibles: {self.impresoras_disponibles}")
        print(f"Impresora predeterminada: {self.impresora_predeterminada}")
        
        # Usar el configurador de impresora para métodos mejorados
        try:
            # Método 1: Usar el configurador de impresora
            if self.configurador.imprimir_archivo_directo(archivo_factura, impresora):
                print("Factura enviada a impresión correctamente")
                return True
            
        except Exception as e1:
            print(f"Error con configurador: {e1}")
        
        # Métodos de respaldo
        try:
            # Método 2: Usar notepad para imprimir (más confiable en Windows)
            if impresora:
                # Imprimir en impresora específica usando notepad
                cmd = f'notepad /p "{archivo_factura}"'
                result = subprocess.run(cmd, shell=True, timeout=30)
                if result.returncode == 0:
                    print("Factura impresa con notepad")
                    return True
            else:
                # Abrir notepad para que el usuario pueda imprimir manualmente
                cmd = f'notepad "{archivo_factura}"'
                subprocess.Popen(cmd, shell=True)
                print("Archivo abierto en Notepad para impresión manual")
                return True
            
        except Exception as e2:
            print(f"Error con notepad: {e2}")
            
        try:
            # Método 3: Comando print de Windows
            if impresora:
                cmd = f'print /D:"{impresora}" "{archivo_factura}"'
            else:
                cmd = f'print "{archivo_factura}"'
            
            result = subprocess.run(cmd, shell=True, timeout=30)
            if result.returncode == 0:
                print("Factura impresa con comando print")
                return True
            else:
                print(f"Error en comando print: código {result.returncode}")
                
        except Exception as e3:
            print(f"Error con comando print: {e3}")
        
        try:
            # Método 4: Usar PowerShell para imprimir
            if impresora:
                ps_cmd = f'powershell -Command "Get-Content \'{archivo_factura}\' | Out-Printer -Name \'{impresora}\'"'
            else:
                ps_cmd = f'powershell -Command "Get-Content \'{archivo_factura}\' | Out-Printer"'
            
            result = subprocess.run(ps_cmd, shell=True, timeout=30)
            if result.returncode == 0:
                print("Factura impresa con PowerShell")
                return True
            else:
                print(f"Error en PowerShell: código {result.returncode}")
                
        except Exception as e4:
            print(f"Error con PowerShell: {e4}")
        
        # Si todos los métodos fallan, mostrar información
        print("=" * 60)
        print("No se pudo imprimir automáticamente.")
        print("Contenido de la factura:")
        print("-" * 50)
        print(contenido_texto)
        print("-" * 50)
        print(f"Archivo guardado en: {archivo_factura}")
        print("Puede imprimir manualmente este archivo desde el explorador de archivos.")
        print("=" * 60)
        return False
    
    def obtener_impresoras_disponibles(self):
        """Retorna la lista de impresoras disponibles"""
        return self.impresoras_disponibles