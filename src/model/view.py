# main.py

from main import SistemaDonaciones
from errors import (
    SistemaOperativoError,
    AlimentoNoEncontradoError,
    UnidadesInsuficientesError,
    CarritoVacioError,
    AlimentosNoSeleccionadosError,
)


def main():
    sistema = SistemaDonaciones()

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
        print("12. Salir")
        opcion = input("Selecciona una opción: ")

        try:
            if opcion == "1":
                nombre = input("Nombre del donante: ")
                contacto = input("Contacto del donante: ")
                username = input("Nombre de usuario: ")
                password = input("Contraseña: ")
                ubicacion = input("Ubicación del donante: ")
                sistema.registrar_donante(
                    nombre, contacto, username, password, ubicacion
                )

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
                nombre = input("Nombre del alimento: ")
                fecha_caducidad = input("Fecha de caducidad: ")
                descripcion = input("Descripción: ")
                unidades = int(input("Unidades disponibles: "))
                tag = input("Tag del alimento: ")
                sistema.publicar_alimento(
                    nombre, fecha_caducidad, descripcion, unidades, tag
                )

            elif opcion == "5":
                nombre_alimento = input("Nombre del alimento a buscar: ")
                resultados = sistema.buscar_alimento(nombre_alimento)
                for alimento in resultados:
                    print(f"Alimento encontrado: {alimento.nombre}")

            elif opcion == "6":
                filtro = input("Ingresa un filtro (nombre o tag): ")
                resultados = sistema.filtrar_alimentos(filtro)
                for alimento in resultados:
                    print(f"Alimento encontrado: {alimento.nombre}")

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
                print("Gracias por usar el sistema de donaciones.")
                break

            else:
                print("Opción no válida. Intenta de nuevo.")

        except SistemaOperativoError as e:
            print(f"Error del sistema: {e}")
        except AlimentoNoEncontradoError as e:
            print(f"Error de búsqueda: {e}")
        except UnidadesInsuficientesError as e:
            print(f"Error de cantidad: {e}")
        except CarritoVacioError as e:
            print(f"Error del carrito: {e}")
        except AlimentosNoSeleccionadosError as e:
            print(f"Error de filtro: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")


if __name__ == "__main__":
    main()
