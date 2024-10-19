from src.model.errors import UnidadesInsuficientesError, AlimentoNoEncontradoError, CarritoVacioError, AlimentosNoSeleccionadosError

class SistemaDonaciones:
    alimentosADonar = []
    notificaciones = []

    def __init__(self) -> None:
        self.donantes: list[Donante] = []
        self.receptores: list[Receptor] = []
    
    def registrarDonante(self, nombre: str, contacto: str, ubicacion: str):
        nuevoDonante: Donante = Donante(nombre, contacto, ubicacion)
        self.donantes.append(nuevoDonante)
        return nuevoDonante

    def registrarReceptor(self, nombre: str, contacto: str):
        nuevoReceptor = Receptor(nombre, contacto)
        self.receptores.append(nuevoReceptor)
        return nuevoReceptor  # Asegúrate de que siempre devuelva un receptor

    @classmethod
    def filtrar(cls, filtro: str) -> list[str] | None:
        filtrado: list[str] = []
        for donante, alimento in cls.alimentosADonar:
            if (filtro.lower().strip() in alimento.nombre.lower().strip() or
                filtro == str(alimento.unidadesDisponibles) or
                filtro.lower().strip() in alimento.tag.lower().strip() or
                filtro.lower().strip() in donante.lower().strip()):
                filtrado.append(f"{donante}: {alimento.nombre} - {alimento.unidadesDisponibles} - {alimento.fechaCaducidad}")
        
        if filtrado:
            return filtrado
        return None

class Usuario:

    def __init__ (self, nombreUsuario: str, email: str, password: str, rol: str):
        self.nombre_usuario: str = nombreUsuario
        self.email: str = email
        self.password: str = password
        self.chat: list[Mensajes] = []
        self.historial: list[str] = []

    def contactarse(self, destinatario, mensaje: str):
        nuevoMensaje: Mensajes = Mensajes(destinatario.contacto, mensaje)
        destinatario.chat.append(f"Chat con {self.nombre.capitalize()}: {nuevoMensaje.mensaje.capitalize()}")

class Alimento:
    def __init__(self, nombre: str, fechaCaducidad: str, descripcion: str, unidadesDisponibles: int, tag: str = ""):
        self.nombre: str = nombre
        self.fechaCaducidad: str = fechaCaducidad
        self.descripcion: str = descripcion
        self.unidadesDisponibles: int = unidadesDisponibles
        self.tag: str = tag

class Receptor(Usuario):
    
    def __init__(self, nombreUsuario: str, email: str, password: str, rol: str):
        super().__init__(nombreUsuario, email, password, rol)
        self.carrito = Carrito()

    def buscarAlimento(self, nombreAlimento: str, unidadesDeseadas: int):
        resultado = SistemaDonaciones.filtrar(nombreAlimento)
        if resultado:
            for item in resultado:
                donante, alimento_info = item.split(": ", 1)
                nombre, unidades, fechaCaducidad = alimento_info.split(" - ")
                unidades = int(unidades)
                self.carrito.agregarACarrito(Alimento(nombre, fechaCaducidad, "", unidades), unidadesDeseadas)
                return True
        raise AlimentoNoEncontradoError(f'{nombreAlimento.capitalize} no esta disponible, o no es un nombre valido. Intenta de nuevo.')
    
    def notificaciones(self) -> list[str|None]:
        return SistemaDonaciones.notificaciones
    

class Donante(Usuario):

    def __init__(self, nombreUsuario: str, email: str, password: str, rol: str, ubicación: str):
        super().__init__(nombreUsuario, email, password, rol)
        self.ubicacion = ubicación

    def publicarAlimento(self, nombre: str, fechaCaducidad: str, descripcion: str, unidadesDisponibles: int, tag: str = ""):
        nuevoAlimento: Alimento = Alimento(nombre, fechaCaducidad, descripcion, unidadesDisponibles, tag)
        SistemaDonaciones.alimentosADonar.append((self.nombre.capitalize(), nuevoAlimento))

    def enviarNoti(self, anuncio: str):
        nuevoAnuncio: str = Notificaciones(anuncio)
        SistemaDonaciones.notificaciones.append(f"Notificación de {self.nombre.capitalize()}: {nuevoAnuncio.notificacion.capitalize()}")


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

    def adquirirTodo(self) -> bool:
        if not self.contenidoCarrito:
            raise CarritoVacioError('El carrito se encuentra vacio.')
        
        for alimento, unidades in self.contenidoCarrito:
            if alimento.unidadesDisponibles < unidades:
                raise UnidadesInsuficientesError(f'La cantidad de {alimento} que deseas no se encuentra disponible. Intenta de nuevo.')
            alimento.unidadesDisponibles -= unidades
        
        self.contenidoCarrito.clear()
        return True

    def adquirir(self, *alimentos: tuple[Alimento, int]) -> bool:
        if alimentos:
            for nombre, unidades in alimentos:
                for elemento, unidadesCarrito in self.contenidoCarrito:
                    if elemento.nombre.lower().strip() == nombre.lower().strip():
                        if elemento.unidadesDisponibles < unidades:
                            raise UnidadesInsuficientesError(f'La cantidad {elemento.nombre.capitalize()} que deseas no se encuentra disponible. Intenta de nuevo.')
                        elemento.unidadesDisponibles -= unidades
                        self.contenidoCarrito.remove((elemento, unidadesCarrito))
                        return True
        raise AlimentosNoSeleccionadosError('No seleccionaste ningun alimento.')

    def eliminarTodo(self):
        self.contenidoCarrito.clear()

    def eliminar(self, *alimentos):
        for nombre in alimentos:
            for elemento, unidades in self.contenidoCarrito:
                if elemento.nombre.lower().strip() == nombre.lower().strip():
                    self.contenidoCarrito.remove((elemento, unidades))
                    break
    
    def verCarrito(self) -> list[str]:
        carrito = []
        for alimento, unidades in self.contenidoCarrito:
            carrito.append(f"{alimento.nombre.capitalize()}: {unidades}")
        return carrito
