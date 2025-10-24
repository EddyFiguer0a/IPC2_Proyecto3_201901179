from flask import Flask, request, Response
import xmltodict
import os
from flask_cors import CORS
from datetime import datetime
from modelos.factura import Factura


# Importamos nuestros módulos
from utilidades.manejador_xml import XMLManager 
from utilidades.validadores import valida_fecha, valida_nit 

app = Flask(__name__)
CORS(app)  # Habilitamos CORS para permitir peticiones desde el frontend

# Aseguramos que exista la carpeta de datos
os.makedirs('datos', exist_ok=True)

# Función para convertir a XML
def to_xml(data):
    return Response(
        xmltodict.unparse({"respuesta": data}, pretty=True),
        mimetype="application/xml"
    )

# Endpoint inicial para verificar que la API está funcionando
@app.route('/', methods=['GET'])
def index():
    return to_xml({"estado": "API en funcionamiento", "version": "1.0"})

# GET: Consultar datos (recursos, categorías, clientes, etc.)
@app.route('/consultarDatos', methods=['GET'])
def consultar_datos():
    try:
        tipo = request.args.get('tipo', 'recursos')  # Por defecto consulta recursos
        
        # Mapeo de tipos a archivos XML
        tipo_archivo = {
            'recursos': 'recursos.xml',
            'categorias': 'categorias.xml',
            'clientes': 'clientes.xml',
            'instancias': 'instancias.xml',
            'consumos': 'consumos.xml',
            'facturas': 'facturas.xml'
        }
        
        if tipo not in tipo_archivo:
            return to_xml({"error": f"Tipo de datos '{tipo}' no válido"})
        
        xml_manager = XMLManager(f'datos/{tipo_archivo[tipo]}')
        datos = xml_manager.obtener_todos()
        
        # Construir respuesta según el tipo
        respuesta = {tipo: {tipo[:-1]: datos if datos else []}}
        return to_xml(respuesta)
    except Exception as e:
        return to_xml({"error": str(e)})

# POST: Crear nuevo recurso
@app.route('/crearRecurso', methods=['POST'])
def crear_recurso():
    try:
        data = xmltodict.parse(request.data)
        nuevo_recurso = data["recurso"]
        
        xml_manager = XMLManager('datos/recursos.xml')
        xml_manager.agregar(nuevo_recurso)
        
        return to_xml({"mensaje": "Recurso creado con éxito", "recurso": nuevo_recurso})
    except Exception as e:
        return to_xml({"error": str(e)})

# POST: Crear nueva categoría
@app.route('/crearCategoria', methods=['POST'])
def crear_categoria():
    try:
        data = xmltodict.parse(request.data)
        nueva_categoria = data["categoria"]
        
        xml_manager = XMLManager('datos/categorias.xml')
        xml_manager.agregar(nueva_categoria)
        
        return to_xml({"mensaje": "Categoría creada con éxito", "categoria": nueva_categoria})
    except Exception as e:
        return to_xml({"error": str(e)})

# POST: Crear nuevo cliente
@app.route('/crearCliente', methods=['POST'])
def crear_cliente():
    try:
        data = xmltodict.parse(request.data)
        nuevo_cliente = data["cliente"]
        
        # Validar NIT
        if not valida_nit(nuevo_cliente.get("nit", "")):
            return to_xml({"error": "NIT inválido"})
        
        xml_manager = XMLManager('datos/clientes.xml')
        xml_manager.agregar(nuevo_cliente)
        
        return to_xml({"mensaje": "Cliente creado con éxito", "cliente": nuevo_cliente})
    except Exception as e:
        return to_xml({"error": str(e)})

# POST: Crear nueva instancia
@app.route('/crearInstancia', methods=['POST'])
def crear_instancia():
    try:
        data = xmltodict.parse(request.data)
        nueva_instancia = data["instancia"]
        
        xml_manager = XMLManager('datos/instancias.xml')
        xml_manager.agregar(nueva_instancia)
        
        return to_xml({"mensaje": "Instancia creada con éxito", "instancia": nueva_instancia})
    except Exception as e:
        return to_xml({"error": str(e)})

# POST: Cargar configuración completa
@app.route('/crearConfiguracion', methods=['POST'])
def crear_configuracion():
    try:
        data = xmltodict.parse(request.data)
        
        if "configuracion" not in data:
            return to_xml({"error": "Formato XML incorrecto"})
        
        config = data["configuracion"]
        resultado = {
            "recursos_creados": 0,
            "categorias_creadas": 0,
            "clientes_creados": 0,
            "instancias_creadas": 0
        }
        
        # Procesar recursos
        if "recursos" in config and "recurso" in config["recursos"]:
            recursos = config["recursos"]["recurso"]
            recursos = [recursos] if not isinstance(recursos, list) else recursos
            
            xml_manager = XMLManager('datos/recursos.xml')
            for recurso in recursos:
                xml_manager.agregar(recurso)
                resultado["recursos_creados"] += 1
        
        # Procesar categorías
        if "categorias" in config and "categoria" in config["categorias"]:
            categorias = config["categorias"]["categoria"]
            categorias = [categorias] if not isinstance(categorias, list) else categorias
            
            xml_manager = XMLManager('datos/categorias.xml')
            for categoria in categorias:
                xml_manager.agregar(categoria)
                resultado["categorias_creadas"] += 1
        
        # Procesar clientes
        if "clientes" in config and "cliente" in config["clientes"]:
            clientes = config["clientes"]["cliente"]
            clientes = [clientes] if not isinstance(clientes, list) else clientes
            
            xml_manager = XMLManager('datos/clientes.xml')
            for cliente in clientes:
                if valida_nit(cliente.get("nit", "")):
                    xml_manager.agregar(cliente)
                    resultado["clientes_creados"] += 1
        
        # Procesar instancias
        if "instancias" in config and "instancia" in config["instancias"]:
            instancias = config["instancias"]["instancia"]
            instancias = [instancias] if not isinstance(instancias, list) else instancias
            
            xml_manager = XMLManager('datos/instancias.xml')
            for instancia in instancias:
                xml_manager.agregar(instancia)
                resultado["instancias_creadas"] += 1
        
        return to_xml({"mensaje": "Configuración cargada con éxito", "resultado": resultado})
    except Exception as e:
        return to_xml({"error": str(e)})

# POST: Cargar consumos
@app.route('/cargarConsumos', methods=['POST'])
def cargar_consumos():
    try:
        data = xmltodict.parse(request.data)
        
        if "consumos" not in data or "consumo" not in data["consumos"]:
            return to_xml({"error": "Formato XML incorrecto"})
        
        consumos = data["consumos"]["consumo"]
        consumos = [consumos] if not isinstance(consumos, list) else consumos
        
        xml_manager = XMLManager('datos/consumos.xml')
        consumos_procesados = 0
        
        for consumo in consumos:
            # Validar fecha
            if "fecha" in consumo and valida_fecha(consumo["fecha"]):
                xml_manager.agregar(consumo)
                consumos_procesados += 1
        
        return to_xml({
            "mensaje": "Consumos cargados con éxito", 
            "total_procesados": consumos_procesados
        })
    except Exception as e:
        return to_xml({"error": str(e)})

# POST: Generar factura
@app.route('/generarFactura', methods=['POST'])
def generar_factura():
    try:
        data = xmltodict.parse(request.data)
        
        if "periodo" not in data:
            return to_xml({"error": "Debe especificar un periodo"})
        
        periodo = data["periodo"]
        if "fecha_inicio" not in periodo or "fecha_fin" not in periodo:
            return to_xml({"error": "El periodo debe incluir fecha de inicio y fin"})
        
        # Validar fechas
        if not valida_fecha(periodo["fecha_inicio"]) or not valida_fecha(periodo["fecha_fin"]):
            return to_xml({"error": "Formato de fecha inválido"})
        
        # Convertir fechas de string a datetime para comparación
        def parsear_fecha(fecha_str):
            """Convierte string en formato dd/mm/yyyy o dd/mm/yyyy hh:mm a datetime"""
            try:
                # Intentar con hora
                if len(fecha_str) > 10:
                    return datetime.strptime(fecha_str, "%d/%m/%Y %H:%M")
                else:
                    return datetime.strptime(fecha_str, "%d/%m/%Y")
            except ValueError:
                return None
        
        fecha_inicio = parsear_fecha(periodo["fecha_inicio"])
        fecha_fin = parsear_fecha(periodo["fecha_fin"])
        
        if not fecha_inicio or not fecha_fin:
            return to_xml({"error": "Error al procesar las fechas"})
        
        # Si fecha_fin no tiene hora, establecer al final del día (23:59)
        if fecha_fin.hour == 0 and fecha_fin.minute == 0 and len(periodo["fecha_fin"]) <= 10:
            fecha_fin = fecha_fin.replace(hour=23, minute=59, second=59)
        
        # Cargar datos necesarios
        mgr_consumos = XMLManager('datos/consumos.xml')
        mgr_instancias = XMLManager('datos/instancias.xml')
        mgr_recursos = XMLManager('datos/recursos.xml')
        mgr_clientes = XMLManager('datos/clientes.xml')
        mgr_facturas = XMLManager('datos/facturas.xml')
        
        consumos_totales = mgr_consumos.obtener_todos()
        instancias_totales = mgr_instancias.obtener_todos()
        recursos_totales = mgr_recursos.obtener_todos()
        clientes_totales = mgr_clientes.obtener_todos()
        
        # Filtrar consumos dentro del periodo
        consumos_filtrados = []
        for consumo in consumos_totales:
            fecha_consumo = parsear_fecha(consumo.get("fecha", ""))
            if fecha_consumo and fecha_inicio <= fecha_consumo <= fecha_fin:
                consumos_filtrados.append(consumo)
        
        if not consumos_filtrados:
            return to_xml({"mensaje": "No hay consumos en el periodo especificado", "facturas_generadas": 0})
        
        # Agrupar consumos por cliente
        consumos_por_cliente = {}
        
        for consumo in consumos_filtrados:
            id_instancia = consumo.get("id_instancia")
            
            # Buscar la instancia asociada
            instancia = None
            for inst in instancias_totales:
                if str(inst.get("id")) == str(id_instancia):
                    instancia = inst
                    break
            
            if not instancia:
                continue  # Saltar si no se encuentra la instancia
            
            id_cliente = instancia.get("id_cliente")
            
            # Inicializar estructura para el cliente si no existe
            if id_cliente not in consumos_por_cliente:
                consumos_por_cliente[id_cliente] = {
                    "instancias": {}
                }
            
            # Inicializar estructura para la instancia si no existe
            if id_instancia not in consumos_por_cliente[id_cliente]["instancias"]:
                consumos_por_cliente[id_cliente]["instancias"][id_instancia] = {
                    "nombre": instancia.get("nombre", "Sin nombre"),
                    "consumos": []
                }
            
            # Buscar el recurso asociado al consumo
            id_recurso = consumo.get("id_recurso")
            recurso = None
            for rec in recursos_totales:
                if str(rec.get("id")) == str(id_recurso):
                    recurso = rec
                    break
            
            if not recurso:
                continue  # Saltar si no se encuentra el recurso
            
            # Calcular el monto del consumo
            tiempo = float(consumo.get("tiempo", 0))
            precio_hora = float(recurso.get("precio_hora", 0))
            monto = tiempo * precio_hora
            
            # Agregar consumo detallado
            consumos_por_cliente[id_cliente]["instancias"][id_instancia]["consumos"].append({
                "id_recurso": id_recurso,
                "nombre_recurso": recurso.get("nombre", ""),
                "abreviatura": recurso.get("abreviatura", ""),
                "tiempo": str(tiempo),
                "precio_hora": str(precio_hora),
                "monto": str(round(monto, 2))
            })
        
        # Generar facturas por cliente
        facturas_generadas = []
        fecha_emision = fecha_fin.strftime("%d/%m/%Y")
        
        for id_cliente, datos_cliente in consumos_por_cliente.items():
            # Buscar información del cliente
            cliente = None
            for cli in clientes_totales:
                if str(cli.get("id")) == str(id_cliente):
                    cliente = cli
                    break
            
            if not cliente:
                continue
            
            # Crear objeto Factura
            factura = Factura(
                id_cliente=id_cliente,
                fecha_emision=fecha_emision,
                monto_total=0
            )
            
            # Agregar items (instancias con sus consumos)
            for id_instancia, datos_instancia in datos_cliente["instancias"].items():
                factura.agregar_item(
                    id_instancia=id_instancia,
                    nombre_instancia=datos_instancia["nombre"],
                    consumos=datos_instancia["consumos"]
                )
            
            # Guardar factura en XML
            factura_dict = factura.to_dict()
            factura_dict["nit_cliente"] = cliente.get("nit")
            factura_dict["nombre_cliente"] = cliente.get("nombre")
            
            mgr_facturas.agregar(factura_dict)
            facturas_generadas.append({
                "id_factura": factura.id,
                "cliente": cliente.get("nombre"),
                "nit": cliente.get("nit"),
                "monto_total": str(factura.monto_total)
            })
        
        return to_xml({
            "mensaje": "Facturas generadas con éxito",
            "periodo": {
                "fecha_inicio": periodo["fecha_inicio"],
                "fecha_fin": periodo["fecha_fin"]
            },
            "facturas_generadas": len(facturas_generadas),
            "facturas": {"factura": facturas_generadas if facturas_generadas else []}
        })
    except Exception as e:
        return to_xml({"error": str(e)})

# Endpoint para reiniciar el sistema
@app.route('/reiniciarSistema', methods=['POST'])
def reiniciar_sistema():
    try:
        # Eliminar todos los archivos XML
        for archivo in ['recursos.xml', 'categorias.xml', 'clientes.xml', 
                        'instancias.xml', 'consumos.xml', 'facturas.xml']:
            if os.path.exists(f'datos/{archivo}'):
                os.remove(f'datos/{archivo}')
        
        return to_xml({"mensaje": "Sistema reiniciado con éxito"})
    except Exception as e:
        return to_xml({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)