from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime
import io

class GeneradorPDF:
    """Clase para generar reportes PDF del sistema"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._configurar_estilos()
    
    def _configurar_estilos(self):
        """Configura estilos personalizados para el PDF"""
        # Estilo para el título principal
        self.styles.add(ParagraphStyle(
            name='TituloCustom',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#0066cc'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        # Estilo para subtítulos
        self.styles.add(ParagraphStyle(
            name='SubtituloCustom',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#333333'),
            spaceAfter=12,
            spaceBefore=12
        ))
    
    def generar_factura_pdf(self, factura_data):
        """
        Genera un PDF con el detalle completo de una factura
        
        Args:
            factura_data (dict): Diccionario con la información de la factura
        
        Returns:
            BytesIO: Buffer con el contenido del PDF
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elementos = []
        
        # Encabezado
        elementos.append(Paragraph("FACTURA DE SERVICIOS EN LA NUBE", self.styles['TituloCustom']))
        elementos.append(Spacer(1, 0.3*inch))
        
        # Información de la factura
        info_factura = [
            ['No. Factura:', factura_data.get('id', 'N/A')],
            ['Fecha de Emisión:', factura_data.get('fecha_emision', 'N/A')],
            ['', '']
        ]
        
        tabla_info = Table(info_factura, colWidths=[2*inch, 4*inch])
        tabla_info.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elementos.append(tabla_info)
        elementos.append(Spacer(1, 0.2*inch))
        
        # Información del cliente
        elementos.append(Paragraph("Datos del Cliente", self.styles['SubtituloCustom']))
        
        info_cliente = [
            ['NIT:', factura_data.get('nit_cliente', 'N/A')],
            ['Nombre:', factura_data.get('nombre_cliente', 'N/A')],
            ['ID Cliente:', factura_data.get('id_cliente', 'N/A')]
        ]
        
        tabla_cliente = Table(info_cliente, colWidths=[1.5*inch, 4.5*inch])
        tabla_cliente.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elementos.append(tabla_cliente)
        elementos.append(Spacer(1, 0.3*inch))
        
        # Detalle de consumos por instancia
        elementos.append(Paragraph("Detalle de Consumos", self.styles['SubtituloCustom']))
        
        items = factura_data.get('items', [])
        if not isinstance(items, list):
            items = [items] if items else []
        
        for item in items:
            # Nombre de la instancia
            elementos.append(Paragraph(f"<b>Instancia:</b> {item.get('nombre_instancia', 'N/A')}", self.styles['Normal']))
            elementos.append(Spacer(1, 0.1*inch))
            
            # Tabla de consumos
            consumos = item.get('consumos', [])
            if not isinstance(consumos, list):
                consumos = [consumos] if consumos else []
            
            datos_tabla = [['Recurso', 'Tiempo (hrs)', 'Precio/Hora', 'Monto (Q.)']]
            
            for consumo in consumos:
                datos_tabla.append([
                    consumo.get('nombre_recurso', 'N/A'),
                    consumo.get('tiempo', '0'),
                    f"Q. {consumo.get('precio_hora', '0')}",
                    f"Q. {consumo.get('monto', '0')}"
                ])
            
            # Subtotal de la instancia
            subtotal = item.get('subtotal', '0')
            datos_tabla.append(['', '', 'Subtotal:', f"Q. {subtotal}"])
            
            tabla_consumos = Table(datos_tabla, colWidths=[2.5*inch, 1.2*inch, 1.2*inch, 1.3*inch])
            tabla_consumos.setStyle(TableStyle([
                # Encabezado
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                
                # Contenido
                ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -2), 9),
                ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
                
                # Subtotal
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, -1), (-1, -1), 10),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f0f0f0')),
                
                # Bordes y padding
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            
            elementos.append(tabla_consumos)
            elementos.append(Spacer(1, 0.2*inch))
        
        # Total general
        elementos.append(Spacer(1, 0.2*inch))
        total_data = [['TOTAL A PAGAR:', f"Q. {factura_data.get('monto_total', '0')}"]]
        tabla_total = Table(total_data, colWidths=[4.5*inch, 1.7*inch])
        tabla_total.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0066cc')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elementos.append(tabla_total)
        
        # Pie de página
        elementos.append(Spacer(1, 0.5*inch))
        elementos.append(Paragraph("Sistema de Facturación en la Nube - IPC2", self.styles['Normal']))
        elementos.append(Paragraph(f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M')}", self.styles['Normal']))
        
        # Construir PDF
        doc.build(elementos)
        buffer.seek(0)
        return buffer
    
    def generar_reporte_ventas_pdf(self, datos_ventas):
        """
        Genera un PDF con análisis de ventas por categorías y recursos
        
        Args:
            datos_ventas (dict): Diccionario con información de ventas
        
        Returns:
            BytesIO: Buffer con el contenido del PDF
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elementos = []
        
        # Encabezado
        elementos.append(Paragraph("REPORTE DE ANÁLISIS DE VENTAS", self.styles['TituloCustom']))
        elementos.append(Spacer(1, 0.2*inch))
        
        # Periodo
        periodo = datos_ventas.get('periodo', {})
        info_periodo = [
            ['Periodo:', f"{periodo.get('fecha_inicio', 'N/A')} - {periodo.get('fecha_fin', 'N/A')}"],
            ['Fecha de Generación:', datetime.now().strftime('%d/%m/%Y %H:%M')]
        ]
        
        tabla_periodo = Table(info_periodo, colWidths=[2*inch, 4*inch])
        tabla_periodo.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elementos.append(tabla_periodo)
        elementos.append(Spacer(1, 0.3*inch))
        
        # Resumen general
        elementos.append(Paragraph("Resumen General", self.styles['SubtituloCustom']))
        resumen = datos_ventas.get('resumen', {})
        
        datos_resumen = [
            ['Total de Facturas:', resumen.get('total_facturas', '0')],
            ['Ingresos Totales:', f"Q. {resumen.get('ingresos_totales', '0')}"]
        ]
        
        tabla_resumen = Table(datos_resumen, colWidths=[2*inch, 3*inch])
        tabla_resumen.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8f4f8')),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        elementos.append(tabla_resumen)
        elementos.append(Spacer(1, 0.3*inch))
        
        # Top Recursos más consumidos
        elementos.append(Paragraph("Recursos con Mayor Ingreso", self.styles['SubtituloCustom']))
        
        recursos = datos_ventas.get('top_recursos', [])
        if recursos:
            datos_recursos = [['Recurso', 'Abreviatura', 'Total Consumido', 'Ingresos (Q.)']]
            
            for recurso in recursos:
                datos_recursos.append([
                    recurso.get('nombre', 'N/A'),
                    recurso.get('abreviatura', 'N/A'),
                    f"{recurso.get('total_tiempo', '0')} hrs",
                    f"Q. {recurso.get('ingresos', '0')}"
                ])
            
            tabla_recursos = Table(datos_recursos, colWidths=[2.5*inch, 1*inch, 1.5*inch, 1.2*inch])
            tabla_recursos.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#28a745')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elementos.append(tabla_recursos)
        else:
            elementos.append(Paragraph("No hay datos de recursos disponibles", self.styles['Normal']))
        
        elementos.append(Spacer(1, 0.3*inch))
        
        # Top Categorías
        elementos.append(Paragraph("Categorías con Mayor Ingreso", self.styles['SubtituloCustom']))
        
        categorias = datos_ventas.get('top_categorias', [])
        if categorias:
            datos_categorias = [['Categoría', 'Instancias', 'Ingresos (Q.)']]
            
            for categoria in categorias:
                datos_categorias.append([
                    categoria.get('nombre', 'N/A'),
                    categoria.get('total_instancias', '0'),
                    f"Q. {categoria.get('ingresos', '0')}"
                ])
            
            tabla_categorias = Table(datos_categorias, colWidths=[3*inch, 1.5*inch, 1.7*inch])
            tabla_categorias.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007bff')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elementos.append(tabla_categorias)
        else:
            elementos.append(Paragraph("No hay datos de categorías disponibles", self.styles['Normal']))
        
        # Pie de página
        elementos.append(Spacer(1, 0.5*inch))
        elementos.append(Paragraph("Sistema de Facturación en la Nube - IPC2", self.styles['Normal']))
        
        # Construir PDF
        doc.build(elementos)
        buffer.seek(0)
        return buffer