import random
from flask import Flask, jsonify
import threading


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
        if alimento.unidades_disponibles >= cantidad:
            alimento.unidades_disponibles -= cantidad
            self.carrito.append((alimento, cantidad))
            print(
                f"Agregado {cantidad} de '{alimento.nombre}' al carrito de {self.nombre}."
            )
        else:
            print(
                f"No hay suficientes unidades de '{alimento.nombre}'. Disponibles: {alimento.unidades_disponibles}."
            )

    def finalizar_adquisiciones(self):
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
        self.donante = donante  # Añadimos referencia al donante


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
        print("Credenciales incorrectas. Intenta nuevamente.")
        return None

    def publicar_alimento(
        self, nombre, fecha_caducidad, descripcion, unidades_disponibles, tag
    ):
        if isinstance(self.usuario_actual, Donante):
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
        else:
            print("Solo los donantes pueden publicar alimentos.")

    def buscar_alimento(self, nombre_alimento):
        resultados = [
            alimento
            for alimento in self.alimentos
            if nombre_alimento.lower() in alimento.nombre.lower()
        ]
        return resultados

    def filtrar_alimentos(self, filtro):
        resultados = [
            alimento
            for alimento in self.alimentos
            if filtro.lower() in alimento.nombre.lower()
            or filtro.lower() in alimento.tag.lower()
        ]
        return resultados

    def ver_historial_donaciones(self):
        if isinstance(self.usuario_actual, Donante):
            if self.usuario_actual.alimentos:
                print("Historial de Donaciones:")
                for alimento in self.usuario_actual.alimentos:
                    print(f"- {alimento.nombre}")
            else:
                print("No hay donaciones registradas.")
        else:
            print("Solo los donantes pueden ver su historial de donaciones.")

    def ver_historial_adquisiciones(self):
        if isinstance(self.usuario_actual, Receptor):
            if self.usuario_actual.historial_adquisiciones:
                print("Historial de Adquisiciones:")
                for alimento, cantidad in self.usuario_actual.historial_adquisiciones:
                    print(f"- {cantidad} de {alimento.nombre}")
            else:
                print("No hay adquisiciones registradas.")
        else:
            print("Solo los receptores pueden ver su historial de adquisiciones.")

    def ver_carrito(self):
        if isinstance(self.usuario_actual, Receptor):
            if self.usuario_actual.carrito:
                print("Carrito de Compras:")
                for alimento, cantidad in self.usuario_actual.carrito:
                    print(f"- {cantidad} de {alimento.nombre}")
            else:
                print("El carrito está vacío.")
        else:
            print("Solo los receptores pueden ver su carrito.")

    def finalizar_adquisiciones(self):
        if isinstance(self.usuario_actual, Receptor):
            self.usuario_actual.finalizar_adquisiciones()
        else:
            print("Solo los receptores pueden finalizar adquisiciones.")

    def generar_recomendaciones(self):
        if isinstance(self.usuario_actual, Receptor):
            if self.usuario_actual.historial_adquisiciones:
                recomendaciones = random.sample(
                    self.alimentos, min(3, len(self.alimentos))
                )
                return recomendaciones
            else:
                print("No hay historial de adquisiciones para generar recomendaciones.")
                return []
        else:
            print("Solo los receptores pueden ver recomendaciones.")
            return []

    def ver_donante_destacado(self):
        if isinstance(self.usuario_actual, Receptor) and self.donantes:
            # Elegimos un donante aleatorio para destacar
            donante_destacado = random.choice(self.donantes)
            print(
                f"Donante Destacado: {donante_destacado.nombre} - {donante_destacado.contacto}"
            )
            if donante_destacado.alimentos:
                print("Alimentos disponibles de este donante:")
                for alimento in donante_destacado.alimentos:
                    print(
                        f"- {alimento.nombre} (Disponibles: {alimento.unidades_disponibles})"
                    )
            else:
                print("Este donante no tiene alimentos disponibles.")
        else:
            print("No hay donantes registrados.")


# Clase para la API
class SistemaDonacionesAPI:
    def __init__(self, sistema_donaciones):
        self.app = Flask(__name__)
        self.sistema = sistema_donaciones

    def run(self):
        @self.app.route("/recomendaciones", methods=["GET"])
        def get_recomendaciones():
            recomendaciones = self.sistema.generar_recomendaciones()
            if recomendaciones:
                return jsonify([alimento.nombre for alimento in recomendaciones]), 200
            return jsonify([]), 200


# Función principal para la interfaz de consola
def main():
    sistema = SistemaDonaciones()
    api = SistemaDonacionesAPI(sistema)

    # Iniciar el hilo de la API
    threading.Thread(target=api.run, daemon=True).start()

    while True:
        print("\n--- Sistema de Donaciones ---")
        print("1. Registrar Donante")
        print("2. Registrar Receptor")
        print("3. Iniciar Sesión")
        print("4. Publicar Alimento")
        print("5. Buscar Alimentos")
        print("6. Filtrar Alimentos")
        print("7. Mostrar Historial de Donaciones")
        print("8. Mostrar Historial de Adquisiciones")
        print("9. Ver Carrito")
        print("10. Finalizar Adquisiciones")
        print("11. Cerrar Sesión")
        print("12. Ver Recomendaciones")
        print("13. Ver Donante Destacado")
        print("14. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            nombre = input("Nombre del donante: ")
            contacto = input("Contacto del donante: ")
            username = input("Nombre de usuario: ")
            password = input("Contraseña: ")
            ubicacion = input("Ubicación del donante: ")
            sistema.registrar_donante(nombre, contacto, username, password, ubicacion)

        elif opcion == "2":
            nombre = input("Nombre del receptor: ")
            contacto = input("Contacto del receptor: ")
            username = input("Nombre de usuario: ")
            password = input("Contraseña: ")
            sistema.registrar_receptor(nombre, contacto, username, password)

        elif opcion == "3":
            username = input("Nombre de usuario: ")
            password = input("Contraseña: ")
            sistema.iniciar_sesion(username, password)

        elif opcion == "4":
            if sistema.usuario_actual is None:
                print("Debes iniciar sesión primero.")
                continue
            nombre = input("Nombre del alimento: ")
            fecha_caducidad = input("Fecha de caducidad (DD/MM/YYYY): ")
            descripcion = input("Descripción del alimento: ")
            unidades_disponibles = int(input("Unidades disponibles: "))
            tag = input("Tag: ")
            sistema.publicar_alimento(
                nombre, fecha_caducidad, descripcion, unidades_disponibles, tag
            )

        elif opcion == "5":
            nombre_alimento = input("Nombre del alimento a buscar: ")
            resultados = sistema.buscar_alimento(nombre_alimento)
            if resultados:
                print("\nResultados de la búsqueda:")
                for alimento in resultados:
                    print(
                        f"- {alimento.nombre} (Disponibles: {alimento.unidades_disponibles}, Caduca: {alimento.fecha_caducidad})"
                    )

                # Ofrecer la opción de agregar al carrito
                if isinstance(sistema.usuario_actual, Receptor):
                    cantidad = int(
                        input("¿Cuántas unidades deseas agregar al carrito? ")
                    )
                    for alimento in resultados:
                        sistema.usuario_actual.agregar_a_carrito(alimento, cantidad)

        elif opcion == "6":
            filtro = input("Introduce el nombre o tag para filtrar alimentos: ")
            resultados = sistema.filtrar_alimentos(filtro)
            if resultados:
                print("\nResultados de la búsqueda filtrada:")
                for alimento in resultados:
                    print(
                        f"- {alimento.nombre} (Disponibles: {alimento.unidades_disponibles}, Caduca: {alimento.fecha_caducidad})"
                    )

                # Permitir al receptor elegir un alimento específico
                if isinstance(sistema.usuario_actual, Receptor):
                    nombre_alimento = input(
                        "¿Qué alimento deseas agregar al carrito? Ingresa el nombre: "
                    )
                    for alimento in resultados:
                        if alimento.nombre.lower() == nombre_alimento.lower():
                            cantidad = int(
                                input("¿Cuántas unidades deseas agregar al carrito? ")
                            )
                            sistema.usuario_actual.agregar_a_carrito(alimento, cantidad)
                            break
                    else:
                        print("Alimento no encontrado en los resultados filtrados.")

        elif opcion == "7":
            sistema.ver_historial_donaciones()

        elif opcion == "8":
            sistema.ver_historial_adquisiciones()

        elif opcion == "9":
            sistema.ver_carrito()

        elif opcion == "10":
            sistema.finalizar_adquisiciones()

        elif opcion == "11":
            sistema.usuario_actual = None
            print("Sesión cerrada.")

        elif opcion == "12":
            recomendaciones = sistema.generar_recomendaciones()
            if recomendaciones:
                print("Recomendaciones:")
                for alimento in recomendaciones:
                    print(
                        f"- {alimento.nombre} (Disponibles: {alimento.unidades_disponibles})"
                    )
            else:
                print("No hay recomendaciones disponibles.")

        elif opcion == "13":
            sistema.ver_donante_destacado()

        elif opcion == "14":
            print("Saliendo del sistema...")
            break


if __name__ == "__main__":
    main()
