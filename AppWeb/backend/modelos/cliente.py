class Cliente:
    def __init__(self, id, nit, nombre, direccion, correo=None, telefono=None):
        self.id = id
        self.nit = nit
        self.nombre = nombre
        self.direccion = direccion
        self.correo = correo
        self.telefono = telefono
    
    def to_dict(self):
        """Convierte el objeto a un diccionario para almacenamiento XML"""
        cliente_dict = {
            "id": self.id,
            "nit": self.nit,
            "nombre": self.nombre,
            "direccion": self.direccion
        }
        
        # Agregar campos opcionales si existen
        if self.correo:
            cliente_dict["correo"] = self.correo
        if self.telefono:
            cliente_dict["telefono"] = self.telefono
        
        return cliente_dict
    
    @classmethod
    def from_dict(cls, data):
        """Crea un objeto Cliente desde un diccionario"""
        return cls(
            id=data.get("id"),
            nit=data.get("nit"),
            nombre=data.get("nombre"),
            direccion=data.get("direccion"),
            correo=data.get("correo"),
            telefono=data.get("telefono")
        )