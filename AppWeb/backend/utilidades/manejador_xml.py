import os
import xmltodict
from datetime import datetime

class XMLManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.archivo_existe()

    def archivo_existe(self):
        """Asegura que el archivo XML exista con una estructura básica"""
        directory = os.path.dirname(self.file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        if not os.path.exists(self.file_path):
            # Crear un XML básico
            root_name = os.path.basename(self.file_path).split('.')[0]
            data = {root_name: {"items": []}}
            with open(self.file_path, 'w') as file:
                file.write(xmltodict.unparse(data, pretty=True))
    
    def lee_archivo(self):
        """Lee el archivo XML y retorna su contenido como diccionario"""
        try:
            with open(self.file_path, 'r') as file:
                content = file.read()
                return xmltodict.parse(content) if content.strip() else {}
        except Exception as e:
            print(f"Error al leer {self.file_path}: {str(e)}")
            return {}

    def escribe_archivo(self, data):
        """Escribe el diccionario data en el archivo XML"""
        with open(self.file_path, 'w') as file:
            file.write(xmltodict.unparse(data, pretty=True))
    
    def obtener_todos(self):
        """Obtiene todos los items del archivo XML"""
        data = self.lee_archivo()
        root_name = os.path.basename(self.file_path).split('.')[0]
        
        if not data or root_name not in data or "items" not in data[root_name]:
            return []
        
        items = data[root_name]["items"]
        return items if items else []

    def obtener_por_id(self, id_value):
        """Obtiene un item por su ID"""
        items = self.obtener_todos()
        for item in items:
            if "id" in item and item["id"] == id_value:
                return item
        return None

    def agregar(self, new_item):
        """Agrega un nuevo item al archivo XML"""
        data = self.lee_archivo()
        root_name = os.path.basename(self.file_path).split('.')[0]
        
        if root_name not in data:
            data[root_name] = {"items": []}
        
        if "items" not in data[root_name]:
            data[root_name]["items"] = []
        
        # Si es el primer elemento, convertirlo en lista
        if data[root_name]["items"] is None:
            data[root_name]["items"] = []
        
        # Agregar timestamp si no tiene uno
        if "timestamp" not in new_item:
            new_item["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Agregar el nuevo item
        data[root_name]["items"].append(new_item)
        
        self.escribe_archivo(data)
        return True
    
    def actualizar(self, id_value, updated_data):
        """Actualiza un item existente por su ID"""
        data = self.lee_archivo()
        root_name = os.path.basename(self.file_path).split('.')[0]
        
        if root_name not in data or "items" not in data[root_name]:
            return False
        
        items = data[root_name]["items"]
        for i, item in enumerate(items):
            if "id" in item and item["id"] == id_value:
                # Actualizar solo los campos proporcionados
                for key, value in updated_data.items():
                    items[i][key] = value
                
                # Actualizar timestamp
                items[i]["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                self.escribe_archivo(data)
                return True
        
        return False
    
    def eliminar(self, id_value):
        """Elimina un item por su ID"""
        data = self.lee_archivo()
        root_name = os.path.basename(self.file_path).split('.')[0]
        
        if root_name not in data or "items" not in data[root_name]:
            return False
        
        items = data[root_name]["items"]
        for i, item in enumerate(items):
            if "id" in item and item["id"] == id_value:
                items.pop(i)
                self.escribe_archivo(data)
                return True
        
        return False