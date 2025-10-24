import requests
import xmltodict
from django.shortcuts import render, redirect
from django.contrib import messages

API_URL = "http://127.0.0.1:5000"


def inicio(request):

    return render(request, 'sistema_web/inicio.html')

def cargar_xml(request):
    """Página para cargar archivos XML de configuración o consumos"""
    if request.method == "POST":
        tipo = request.POST.get('tipo')  # 'configuracion' o 'consumo'
        archivo = request.FILES.get('archivo')
        
        if archivo:
            contenido_xml = archivo.read().decode('utf-8')
            
            # Determinar endpoint según el tipo
            if tipo == 'configuracion':
                endpoint = f"{API_URL}/crearConfiguracion"
            elif tipo == 'consumo':
                endpoint = f"{API_URL}/cargarConsumos"
            else:
                messages.error(request, "Tipo de archivo no válido")
                return render(request, 'sistema_web/cargar_xml.html')
            
            # Enviar XML a la API
            headers = {'Content-Type': 'application/xml'}
            respuesta = requests.post(endpoint, data=contenido_xml, headers=headers)
            
            if respuesta.status_code == 200:
                # Parsear respuesta XML
                resultado = xmltodict.parse(respuesta.content)
                messages.success(request, f"Archivo cargado exitosamente: {resultado}")
                return redirect('sistema_web:ver_datos')
            else:
                resultado = xmltodict.parse(respuesta.content)
                messages.error(request, f"Error al cargar archivo: {resultado}")
        else:
            messages.error(request, "Debe seleccionar un archivo")
    
    return render(request, 'sistema_web/cargar_xml.html')


def ver_datos(request):
    """Página para ver datos del sistema (recursos, categorías, etc.)"""
    tipo = request.GET.get('tipo', 'recursos')  # Por defecto muestra recursos
    
    # Consultar datos de la API
    respuesta = requests.get(f"{API_URL}/consultarDatos", params={'tipo': tipo})
    
    datos = []
    if respuesta.status_code == 200:
        # Parsear respuesta XML
        resultado = xmltodict.parse(respuesta.content)
        # Extraer datos según el tipo
        if 'respuesta' in resultado and tipo in resultado['respuesta']:
            tipo_singular = tipo[:-1]  # 'recursos' -> 'recurso'
            datos_raw = resultado['respuesta'][tipo].get(tipo_singular, [])
            # Asegurar que sea una lista
            datos = datos_raw if isinstance(datos_raw, list) else [datos_raw] if datos_raw else []
    
    context = {
        'tipo': tipo,
        'datos': datos,
        'tipos_disponibles': ['recursos', 'categorias', 'clientes', 'instancias', 'consumos', 'facturas']
    }
    
    return render(request, 'sistema_web/ver_datos.html', context)

def crear_datos(request):
    """Página para crear recursos, categorías, clientes, etc. manualmente"""
    errores = {}
    
    if request.method == "POST":
        tipo = request.POST.get('tipo')  # 'recurso', 'categoria', 'cliente', etc.
        
        # Construir XML según el tipo
        if tipo == 'recurso':
            xml_data = f"""<?xml version="1.0" encoding="UTF-8"?>
            <recurso>
                <id>{request.POST.get('id')}</id>
                <nombre>{request.POST.get('nombre')}</nombre>
                <abreviatura>{request.POST.get('abreviatura')}</abreviatura>
                <metrica>{request.POST.get('metrica')}</metrica>
                <precio_hora>{request.POST.get('precio_hora')}</precio_hora>
            </recurso>"""
            endpoint = f"{API_URL}/crearRecurso"
            
        elif tipo == 'categoria':
            xml_data = f"""<?xml version="1.0" encoding="UTF-8"?>
            <categoria>
                <id>{request.POST.get('id')}</id>
                <nombre>{request.POST.get('nombre')}</nombre>
                <descripcion>{request.POST.get('descripcion')}</descripcion>
                <carga_trabajo>{request.POST.get('carga_trabajo')}</carga_trabajo>
            </categoria>"""
            endpoint = f"{API_URL}/crearCategoria"
            
        elif tipo == 'cliente':
            xml_data = f"""<?xml version="1.0" encoding="UTF-8"?>
            <cliente>
                <id>{request.POST.get('id')}</id>
                <nit>{request.POST.get('nit')}</nit>
                <nombre>{request.POST.get('nombre')}</nombre>
                <direccion>{request.POST.get('direccion')}</direccion>
                <correo>{request.POST.get('correo', '')}</correo>
                <telefono>{request.POST.get('telefono', '')}</telefono>
            </cliente>"""
            endpoint = f"{API_URL}/crearCliente"
            
        elif tipo == 'instancia':
            xml_data = f"""<?xml version="1.0" encoding="UTF-8"?>
            <instancia>
                <id>{request.POST.get('id')}</id>
                <id_cliente>{request.POST.get('id_cliente')}</id_cliente>
                <id_configuracion>{request.POST.get('id_configuracion')}</id_configuracion>
                <nombre>{request.POST.get('nombre')}</nombre>
                <fecha_inicio>{request.POST.get('fecha_inicio')}</fecha_inicio>
            </instancia>"""
            endpoint = f"{API_URL}/crearInstancia"
        else:
            messages.error(request, "Tipo de dato no válido")
            return render(request, 'sistema_web/crear_datos.html', {'errores': errores})
        
        # Enviar a la API
        headers = {'Content-Type': 'application/xml'}
        respuesta = requests.post(endpoint, data=xml_data, headers=headers)
        
        if respuesta.status_code == 200:
            resultado = xmltodict.parse(respuesta.content)
            messages.success(request, "Dato creado exitosamente")
            return redirect('sistema_web:ver_datos')
        else:
            resultado = xmltodict.parse(respuesta.content)
            errores = resultado.get('respuesta', {}).get('error', 'Error desconocido')
            messages.error(request, f"Error: {errores}")
    
    return render(request, 'sistema_web/crear_datos.html', {'errores': errores})

def generar_facturas(request):
    """Página para generar facturas por periodo"""
    if request.method == "POST":
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        
        # Construir XML para generar facturas
        xml_data = f"""<?xml version="1.0" encoding="UTF-8"?>
        <periodo>
            <fecha_inicio>{fecha_inicio}</fecha_inicio>
            <fecha_fin>{fecha_fin}</fecha_fin>
        </periodo>"""
        
        # Enviar a la API
        headers = {'Content-Type': 'application/xml'}
        respuesta = requests.post(f"{API_URL}/generarFactura", data=xml_data, headers=headers)
        
        if respuesta.status_code == 200:
            resultado = xmltodict.parse(respuesta.content)
            messages.success(request, f"Facturas generadas: {resultado}")
            return redirect('sistema_web:ver_facturas')
        else:
            resultado = xmltodict.parse(respuesta.content)
            messages.error(request, f"Error: {resultado}")
    
    return render(request, 'sistema_web/generar_facturas.html')


def ver_facturas(request):
    """Página para ver todas las facturas generadas"""
    respuesta = requests.get(f"{API_URL}/consultarDatos", params={'tipo': 'facturas'})
    
    facturas = []
    if respuesta.status_code == 200:
        resultado = xmltodict.parse(respuesta.content)
        if 'respuesta' in resultado and 'facturas' in resultado['respuesta']:
            facturas_raw = resultado['respuesta']['facturas'].get('factura', [])
            facturas = facturas_raw if isinstance(facturas_raw, list) else [facturas_raw] if facturas_raw else []
    
    return render(request, 'sistema_web/ver_facturas.html', {'facturas': facturas})


def reportes(request):
    """Página para generar reportes PDF"""
    # Esta vista se completará cuando implementemos la generación de PDF
    return render(request, 'sistema_web/reportes.html')


def ayuda(request):
    """Página de ayuda y documentación"""
    return render(request, 'sistema_web/ayuda.html')


def reiniciar_sistema(request):
    """Reinicia el sistema eliminando todos los datos"""
    if request.method == "POST":
        respuesta = requests.post(f"{API_URL}/reiniciarSistema")
        
        if respuesta.status_code == 200:
            messages.success(request, "Sistema reiniciado exitosamente")
        else:
            messages.error(request, "Error al reiniciar el sistema")
        
        return redirect('sistema_web:inicio')
    
    return render(request, 'sistema_web/reiniciar_sistema.html')