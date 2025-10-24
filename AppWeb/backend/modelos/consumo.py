class Consumo:
    def __init__(self, id, id_instancia, id_recurso, fecha, tiempo):
        self.id = id
        self.id_instancia = id_instancia
        self.id_recurso = id_recurso
        self.fecha = fecha
        self.tiempo = float(tiempo)
    
    def to_dict(self):
        """Convierte el objeto a un diccionario para almacenamiento XML"""
        return {
            "id": self.id,
            "id_instancia": self.id_instancia,
            "id_recurso": self.id_recurso,
            "fecha": self.fecha,
            "tiempo": str(self.tiempo)
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crea un objeto Consumo desde un diccionario"""
        return cls(
            id=data.get("id"),
            id_instancia=data.get("id_instancia"),
            id_recurso=data.get("id_recurso"),
            fecha=data.get("fecha"),
            tiempo=data.get("tiempo")
        )