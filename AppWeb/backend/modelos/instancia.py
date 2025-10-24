class Instancia:
    def __init__(self, id, id_cliente, id_configuracion, nombre, fecha_inicio):
        self.id = id
        self.id_cliente = id_cliente
        self.id_configuracion = id_configuracion
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.estado = "activa"  # Por defecto, la instancia está activa
    
    def to_dict(self):
        """Convierte el objeto a un diccionario para almacenamiento XML"""
        return {
            "id": self.id,
            "id_cliente": self.id_cliente,
            "id_configuracion": self.id_configuracion,
            "nombre": self.nombre,
            "fecha_inicio": self.fecha_inicio,
            "estado": self.estado
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crea un objeto Instancia desde un diccionario"""
        instancia = cls(
            id=data.get("id"),
            id_cliente=data.get("id_cliente"),
            id_configuracion=data.get("id_configuracion"),
            nombre=data.get("nombre"),
            fecha_inicio=data.get("fecha_inicio")
        )
        if "estado" in data:
            instancia.estado = data["estado"]
        return instancia