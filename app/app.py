class Restaurante:
    def __init__(self, nombre: str, *alimentosUsados: str) -> None:
        self.nombre = nombre
        self.alimentos = alimentosUsados
