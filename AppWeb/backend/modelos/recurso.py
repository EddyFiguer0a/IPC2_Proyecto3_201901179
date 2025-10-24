class Recurso:
    def __init__(self, id, nombre, abreviatura, metrica, precio_hora):
        self.id = id
        self.nombre = nombre
        self.abreviatura = abreviatura
        self.metrica = metrica
        self.precio_hora = float(precio_hora)
    
    def to_dict(self):
        """Convierte el objeto a un diccionario para almacenamiento XML"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "abreviatura": self.abreviatura,
            "metrica": self.metrica,
            "precio_hora": str(self.precio_hora)
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crea un objeto Recurso desde un diccionario"""
        return cls(
            id=data.get("id"),
            nombre=data.get("nombre"),
            abreviatura=data.get("abreviatura"),
            metrica=data.get("metrica"),
            precio_hora=data.get("precio_hora")
        )