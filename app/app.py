class SistemaDonaciones:
    alimentosADonar = []
    notificaciones = []

    def __init__(self) -> None:
        self.donantes: list[Donante] = []
        self.receptores: list[Receptor] = []
    
    def registrarDonante(self, nombre: str, contacto: str, ubicacion: str):
        nuevoDonante: Donante = Donante(nombre, contacto, ubicacion)
        self.donantes.append(nuevoDonante)

    def registrarReceptor(self, nombre: str, contacto: str, ubicacion: str):
        nuevoReceptor: Receptor = Receptor(nombre, contacto, ubicacion)
        self.donantes.append(nuevoReceptor)

    def filtrar(filtro: str) -> list[str]|None:
        filtrado: list[str] = []
        for donante, alimento in SistemaDonaciones.alimentosADonar:
            if filtro.lower().strip() == alimento.nombre.lower().strip():
                filtrado.append(f"{donante}: {alimento.nombre} - {alimento.unidadesDisponibles} - {alimento.fechaCaducidad}")
            if filtro == alimento.unidadesDisponibles:
                filtrado.append(f"{donante}: {alimento.nombre} - {alimento.unidadesDisponibles} - {alimento.fechaCaducidad}")
            if filtro.lower().strip() == alimento.tag.lower().strip():
                filtrado.append(f"{donante}: {alimento.nombre} - {alimento.unidadesDisponibles} - {alimento.fechaCaducidad}")
            if filtro.lower().strip() == donante.lower().strip():
                filtrado.append(f"{donante}: {alimento.nombre} - {alimento.unidadesDisponibles} - {alimento.fechaCaducidad}")
        
        if filtrado:
            return filtrado
        return None

    
class Alimento:
    def __init__(self, nombre: str, fechaCaducidad: str, descripcion: str, unidadesDisponibles: int, tag: str = ""):
        self.nombre: str = nombre
        self.fechaCaducidad: str = fechaCaducidad
        self.descripcion: str = descripcion
        self.unidadesDisponibles: str = unidadesDisponibles
        self.tag: str = tag

    def __str__(self) -> str:
        return f"Nombre: {self.nombre.capitalize()}\nFecha de caducidad: {self.fechaCaducidad}\nDescripción: {self.descripcion.capitalize()}\nUnidades: {self.unidadesDisponibles}"

class Donante:
    def __init__(self, nombre: str, contacto: str, ubicacion: str):
        self.nombre: str = nombre
        self.contacto: str = contacto
        self.ubicacion: str = ubicacion
        self.chat: list = []

    def publicarAlimento(self, nombre: str, fechaCaducidad: str, descripcion: str, unidadesDisponibles: int, tag: str = ""):
        nuevoAlimento: Alimento = Alimento(nombre, fechaCaducidad, descripcion, unidadesDisponibles, tag)
        SistemaDonaciones.alimentosADonar.append((self.nombre.capitalize(), nuevoAlimento))

    def enviarNoti(self, anuncio: str):
        nuevoAnuncio: str = Notificaciones(anuncio)
        SistemaDonaciones.notificaciones.append(f"Notificación de {self.nombre.capitalize()}: {nuevoAnuncio.notificacion.capitalize()}")
    
    def contactarse(self, receptor: "Receptor", mensaje: str):
        nuevoMensaje: Mensajes = Mensajes(receptor.contacto, mensaje)
        receptor.chat.append(f"Chat con {self.nombre.capitalize()}: {nuevoMensaje.mensaje.capitalize()}")

class Receptor:
    def __init__(self, nombre: str, contacto: str):
        self.nombre: str = nombre
        self.contacto: str = contacto
        self.chat: list = []
        self.carrito = Carrito()

    def buscarAlimento(self, nombreAlimento: str, unidadesDeseadas: int):
        for donante, alimento in SistemaDonaciones.alimentosADonar:
            if nombreAlimento.lower().strip() == alimento.nombre.lower().strip():
                self.carrito.agregarACarrito(alimento, unidadesDeseadas)
                return False
        return False
            
    def contactarse(self, donante: Donante, mensaje: str):
        nuevoMensaje: Mensajes = Mensajes(donante.contacto, mensaje)
        donante.chat.append(f"Chat con {self.nombre.capitalize()}: {nuevoMensaje.mensaje.capitalize()}")

    def notificaciones(self) -> list[str|None]:
        return SistemaDonaciones.notificaciones
    
class Mensajes:
    def __init__(self, contacto: str, mensaje: str):
        self.contacto: str = contacto
        self.mensaje: str = mensaje

class Notificaciones:
    def __init__(self, notificacion: str):
        self.notificacion = notificacion

class Carrito:
    def __init__(self,):
        self.contenidoCarrito: list[tuple[Alimento, int]] = [] 
    
    def agregarACarrito(self, alimento: Alimento, unidadesDeseadas: int):
        self.contenidoCarrito.append((alimento, unidadesDeseadas))

    def adquirirTodo(self):
        for elemento, unidades in self.contenidoCarrito:
            if elemento.unidadesDisponibles >= unidades:
                elemento.unidadesDisponibles -= unidades
            else:
                return False
        self.contenidoCarrito.clear()

    def adquirir(self, *alimentos):
        for alimento in alimentos:
            for elemento, unidades in self.contenidoCarrito:
                if elemento.nombre.lower().strip() == alimento.lower().strip():
                    if elemento.unidadesDisponibles >= unidades:
                        elemento.unidadesDisponibles -= unidades
                        self.contenidoCarrito.remove((elemento, unidades))
                    else:
                        return False
        return False

    def eliminarTodo(self):
        self.contenidoCarrito.clear()

    def eliminar(self, *alimentos):
        for alimento in alimentos:
            for elemento, unidades in self.contenidoCarrito:
                if elemento.nombre.lower().strip() == alimento.lower().strip():
                    self.contenidoCarrito.remove((elemento, unidades))
                    break
        return False
    
    def verCarrito(self) -> list[str]:
        carrito = []
        for elemento, unidades in self.contenidoCarrito:
            carrito.append(f"{elemento.nombre.capitalize()}: {unidades}")
        return carrito


    
















#¡PRUEBAS!

sistema = SistemaDonaciones()
donante = Donante("Exito", "Email", "Buenos Aires")
sistema.registrarDonante("Exito", "Email", "Buenos Aires")
donante.publicarAlimento("Banano", "23/11/2025", "Fruta en buen estado", 100, "fruta")
donante.publicarAlimento("Pera", "23/12/2025", "...", 15, "fruta")
donante2 = Donante("Parmesano", "Whatsapp", "Laureles")
donante2.publicarAlimento("Manzana", "10/08/2023", "Ya no vendemos manzanas", 15, "fruta")
receptor = Receptor("Santiago", "333 2331664")
receptor2 = Receptor("Santi", "333 2331664")
receptor2.buscarAlimento("Manzana", 10)
receptor2.contactarse(donante, "Ubi")
receptor.buscarAlimento("Pera", 10)
receptor.buscarAlimento("Banano", 12)
receptor.contactarse(donante, "Holaaa")
donante.contactarse(receptor, "Holaaa, tenemos peras disponibles.")
donante.contactarse(receptor2, "Hi, tenemos peras disponibles.")
donante.enviarNoti("Tomates para donacion")

# print(SistemaDonaciones.filtrar("Pera"))
# print(SistemaDonaciones.filtrar("Banano"))
receptor.carrito.eliminar("pera")
print(receptor.carrito.verCarrito())
print(receptor.notificaciones())
print(sistema.donantes[0].nombre)



