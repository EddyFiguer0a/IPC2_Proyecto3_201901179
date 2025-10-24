import uuid
from datetime import datetime

class Factura:
    def __init__(self, id_cliente, fecha_emision, monto_total, items=None, id=None):
        self.id = id if id else str(uuid.uuid4())  # Generar ID único si no se proporciona
        self.id_cliente = id_cliente
        self.fecha_emision = fecha_emision
        self.monto_total = float(monto_total)
        self.items = items if items else []
    
    def agregar_item(self, id_instancia, nombre_instancia, consumos):
        """Agrega un item a la factura"""
        item = {
            "id_instancia": id_instancia,
            "nombre_instancia": nombre_instancia,
            "consumos": consumos,
            "subtotal": sum(float(c.get("monto", 0)) for c in consumos)
        }
        self.items.append(item)
        # Recalcular monto total
        self.monto_total = sum(item["subtotal"] for item in self.items)
    
    def to_dict(self):
        """Convierte el objeto a un diccionario para almacenamiento XML"""
        return {
            "id": self.id,
            "id_cliente": self.id_cliente,
            "fecha_emision": self.fecha_emision,
            "monto_total": str(self.monto_total),
            "items": self.items
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crea un objeto Factura desde un diccionario"""
        return cls(
            id=data.get("id"),
            id_cliente=data.get("id_cliente"),
            fecha_emision=data.get("fecha_emision"),
            monto_total=data.get("monto_total"),
            items=data.get("items", [])
        )