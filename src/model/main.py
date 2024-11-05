# sistema_donaciones.py

from errors import (
    SistemaOperativoError,
    AlimentoNoEncontradoError,
    UnidadesInsuficientesError,
    CarritoVacioError,
    AlimentosNoSeleccionadosError,
)
import random


# Clase Usuario
class Usuario:
    def __init__(self, nombre, contacto, username, password):
        self.nombre = nombre
        self.contacto = contacto
        self.username = username
        self.password = password


# Clase Donante
class Donante(Usuario):
    def __init__(self, nombre, contacto, username, password, ubicacion):
        super().__init__(nombre, contacto, username, password)
        self.ubicacion = ubicacion
        self.alimentos = []

    def publicar_alimento(self, alimento):
        self.alimentos.append(alimento)
        print(f"Alimento '{alimento.nombre}' publicado por {self.nombre}.")


# Clase Receptor
class Receptor(Usuario):
    def __init__(self, nombre, contacto, username, password):
        super().__init__(nombre, contacto, username, password)
        self.carrito = []
        self.historial_adquisiciones = []

    def agregar_a_carrito(self, alimento, cantidad):
        if cantidad > alimento.unidades_disponibles:
            raise UnidadesInsuficientesError(
                f"No hay suficientes unidades de '{alimento.nombre}'. Disponibles: {alimento.unidades_disponibles}"
            )
        alimento.unidades_disponibles -= cantidad
        self.carrito.append((alimento, cantidad))
        print(
            f"Agregado {cantidad} de '{alimento.nombre}' al carrito de {self.nombre}."
        )

    def finalizar_adquisiciones(self):
        if not self.carrito:
            raise CarritoVacioError(
                "El carrito está vacío. No se puede finalizar la adquisición."
            )
        for alimento, cantidad in self.carrito:
            self.historial_adquisiciones.append((alimento, cantidad))
        self.carrito = []  # Vaciar carrito después de finalizar
        print(f"Adquisiciones finalizadas para {self.nombre}.")


# Clase Alimento
class Alimento:
    def __init__(
        self, nombre, fecha_caducidad, descripcion, unidades_disponibles, tag, donante
    ):
        self.nombre = nombre
        self.fecha_caducidad = fecha_caducidad
        self.descripcion = descripcion
        self.unidades_disponibles = unidades_disponibles
        self.tag = tag
        self.donante = donante


# Clase SistemaDonaciones
class SistemaDonaciones:
    def __init__(self):
        self.donantes = []
        self.receptores = []
        self.alimentos = []
        self.usuario_actual = None

    def registrar_donante(self, nombre, contacto, username, password, ubicacion):
        donante = Donante(nombre, contacto, username, password, ubicacion)
        self.donantes.append(donante)
        print(f"Donante {nombre} registrado exitosamente.")

    def registrar_receptor(self, nombre, contacto, username, password):
        receptor = Receptor(nombre, contacto, username, password)
        self.receptores.append(receptor)
        print(f"Receptor {nombre} registrado exitosamente.")

    def iniciar_sesion(self, username, password):
        for donante in self.donantes:
            if donante.username == username and donante.password == password:
                self.usuario_actual = donante
                print(f"Bienvenido, {donante.nombre}. Eres un donante.")
                return donante
        for receptor in self.receptores:
            if receptor.username == username and receptor.password == password:
                self.usuario_actual = receptor
                print(f"Bienvenido, {receptor.nombre}. Eres un receptor.")
                return receptor
        raise SistemaOperativoError("Credenciales incorrectas. Intenta nuevamente.")

    def publicar_alimento(
        self, nombre, fecha_caducidad, descripcion, unidades_disponibles, tag
    ):
        if not isinstance(self.usuario_actual, Donante):
            raise SistemaOperativoError("Solo los donantes pueden publicar alimentos.")
        alimento = Alimento(
            nombre,
            fecha_caducidad,
            descripcion,
            unidades_disponibles,
            tag,
            self.usuario_actual,
        )
        self.usuario_actual.publicar_alimento(alimento)
        self.alimentos.append(alimento)

    def buscar_alimento(self, nombre_alimento):
        resultados = [
            alimento
            for alimento in self.alimentos
            if nombre_alimento.lower() in alimento.nombre.lower()
        ]
        if not resultados:
            raise AlimentoNoEncontradoError(
                f"El alimento '{nombre_alimento}' no se ha encontrado."
            )
        return resultados

    def filtrar_alimentos(self, filtro):
        if not filtro:
            raise AlimentosNoSeleccionadosError(
                "Se necesita un nombre o un tag para filtrar los alimentos."
            )
        resultados = [
            alimento
            for alimento in self.alimentos
            if filtro.lower() in alimento.nombre.lower()
            or filtro.lower() in alimento.tag.lower()
        ]
        if not resultados:
            raise AlimentoNoEncontradoError(
                "No se han encontrado alimentos que coincidan con el filtro."
            )
        return resultados

    def ver_historial_donaciones(self):
        if not isinstance(self.usuario_actual, Donante):
            raise SistemaOperativoError(
                "Solo los donantes pueden ver su historial de donaciones."
            )
        if not self.usuario_actual.alimentos:
            print("No hay donaciones registradas.")
        else:
            print("Historial de Donaciones:")
            for alimento in self.usuario_actual.alimentos:
                print(f"- {alimento.nombre}")

    def ver_historial_adquisiciones(self):
        if not isinstance(self.usuario_actual, Receptor):
            raise SistemaOperativoError(
                "Solo los receptores pueden ver su historial de adquisiciones."
            )
        if not self.usuario_actual.historial_adquisiciones:
            print("No hay adquisiciones registradas.")
        else:
            print("Historial de Adquisiciones:")
            for alimento, cantidad in self.usuario_actual.historial_adquisiciones:
                print(f"- {cantidad} de {alimento.nombre}")

    def ver_carrito(self):
        if not isinstance(self.usuario_actual, Receptor):
            raise SistemaOperativoError("Solo los receptores pueden ver su carrito.")
        if not self.usuario_actual.carrito:
            print("El carrito está vacío.")
        else:
            print("Carrito de Compras:")
            for alimento, cantidad in self.usuario_actual.carrito:
                print(f"- {cantidad} de {alimento.nombre}")

    def finalizar_adquisiciones(self):
        if not isinstance(self.usuario_actual, Receptor):
            raise SistemaOperativoError(
                "Solo los receptores pueden finalizar adquisiciones."
            )
        self.usuario_actual.finalizar_adquisiciones()
