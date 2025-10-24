class Categoria:
    def __init__(self, id, nombre, descripcion, carga_trabajo):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.carga_trabajo = float(carga_trabajo)
    
    def to_dict(self):
        """Convierte el objeto a un diccionario para almacenamiento XML"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "carga_trabajo": str(self.carga_trabajo)
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crea un objeto Categoria desde un diccionario"""
        return cls(
            id=data.get("id"),
            nombre=data.get("nombre"),
            descripcion=data.get("descripcion"),
            carga_trabajo=data.get("carga_trabajo")
        )