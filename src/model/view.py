import tkinter as tk
from tkinter import messagebox
from main import SistemaDonaciones, Donante, Receptor
from errors import (
    SistemaOperativoError,
    AlimentoNoEncontradoError,
    UnidadesInsuficientesError,
    CarritoVacioError,
    AlimentosNoSeleccionadosError,
)
import requests  # Necesario para realizar peticiones a la API


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Donaciones")
        self.sistema = SistemaDonaciones()
        self.usuario_actual = None
        self.carrito = []  # Inicializamos el carrito como una lista vacía
        self.main_frame = tk.Frame(root)
        self.main_frame.pack()
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_frame()
        tk.Label(
            self.main_frame,
            text="Bienvenido al Sistema de Donaciones",
            font=("Arial", 16),
        ).pack(pady=10)
        tk.Button(
            self.main_frame, text="Registrar Donante", command=self.register_donante
        ).pack(pady=5)
        tk.Button(
            self.main_frame, text="Registrar Receptor", command=self.register_receptor
        ).pack(pady=5)
        tk.Button(self.main_frame, text="Iniciar Sesión", command=self.login).pack(
            pady=5
        )

    def register_donante(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Registrar Donante", font=("Arial", 14)).pack(
            pady=10
        )
        tk.Label(self.main_frame, text="Nombre:").pack(pady=2)
        nombre_entry = tk.Entry(self.main_frame)
        nombre_entry.pack(pady=2)
        tk.Label(self.main_frame, text="Contacto:").pack(pady=2)
        contacto_entry = tk.Entry(self.main_frame)
        contacto_entry.pack(pady=2)
        tk.Label(self.main_frame, text="Usuario:").pack(pady=2)
        username_entry = tk.Entry(self.main_frame)
        username_entry.pack(pady=2)
        tk.Label(self.main_frame, text="Contraseña:").pack(pady=2)
        password_entry = tk.Entry(self.main_frame, show="*")
        password_entry.pack(pady=2)
        tk.Label(self.main_frame, text="Ubicación:").pack(pady=2)
        ubicacion_entry = tk.Entry(self.main_frame)
        ubicacion_entry.pack(pady=2)

        def save_donante():
            nombre = nombre_entry.get()
            contacto = contacto_entry.get()
            username = username_entry.get()
            password = password_entry.get()
            ubicacion = ubicacion_entry.get()
            try:
                self.sistema.registrar_donante(
                    nombre, contacto, username, password, ubicacion
                )
                messagebox.showinfo("Registro", "Donante registrado exitosamente.")
                self.create_main_menu()
            except SistemaOperativoError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.main_frame, text="Registrar", command=save_donante).pack(pady=5)
        tk.Button(self.main_frame, text="Volver", command=self.create_main_menu).pack(
            pady=5
        )

    def register_receptor(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Registrar Receptor", font=("Arial", 14)).pack(
            pady=10
        )
        tk.Label(self.main_frame, text="Nombre:").pack(pady=2)
        nombre_entry = tk.Entry(self.main_frame)
        nombre_entry.pack(pady=2)
        tk.Label(self.main_frame, text="Contacto:").pack(pady=2)
        contacto_entry = tk.Entry(self.main_frame)
        contacto_entry.pack(pady=2)
        tk.Label(self.main_frame, text="Usuario:").pack(pady=2)
        username_entry = tk.Entry(self.main_frame)
        username_entry.pack(pady=2)
        tk.Label(self.main_frame, text="Contraseña:").pack(pady=2)
        password_entry = tk.Entry(self.main_frame, show="*")
        password_entry.pack(pady=2)

        def save_receptor():
            nombre = nombre_entry.get()
            contacto = contacto_entry.get()
            username = username_entry.get()
            password = password_entry.get()
            try:
                self.sistema.registrar_receptor(nombre, contacto, username, password)
                messagebox.showinfo("Registro", "Receptor registrado exitosamente.")
                self.create_main_menu()
            except SistemaOperativoError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.main_frame, text="Registrar", command=save_receptor).pack(pady=5)
        tk.Button(self.main_frame, text="Volver", command=self.create_main_menu).pack(
            pady=5
        )

    def login(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Iniciar Sesión", font=("Arial", 14)).pack(
            pady=10
        )
        tk.Label(self.main_frame, text="Usuario:").pack(pady=2)
        username_entry = tk.Entry(self.main_frame)
        username_entry.pack(pady=2)
        tk.Label(self.main_frame, text="Contraseña:").pack(pady=2)
        password_entry = tk.Entry(self.main_frame, show="*")
        password_entry.pack(pady=2)

        def authenticate():
            username = username_entry.get()
            password = password_entry.get()
            try:
                self.sistema.iniciar_sesion(username, password)
                self.usuario_actual = self.sistema.usuario_actual
                if self.usuario_actual:
                    messagebox.showinfo(
                        "Inicio de Sesión", "Sesión iniciada exitosamente."
                    )
                    self.user_dashboard()
                else:
                    messagebox.showerror("Error", "Credenciales inválidas.")
            except SistemaOperativoError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.main_frame, text="Iniciar", command=authenticate).pack(pady=5)
        tk.Button(self.main_frame, text="Volver", command=self.create_main_menu).pack(
            pady=5
        )

    def user_dashboard(self):
        self.clear_frame()
        tk.Label(
            self.main_frame,
            text=f"Bienvenido, {self.usuario_actual.nombre}",
            font=("Arial", 16),
        ).pack(pady=10)

        if isinstance(self.usuario_actual, Donante):
            tk.Button(
                self.main_frame, text="Publicar Alimento", command=self.publish_food
            ).pack(pady=5)
            tk.Button(
                self.main_frame,
                text="Ver Historial de Donaciones",
                command=self.view_donations,
            ).pack(pady=5)
        elif isinstance(self.usuario_actual, Receptor):
            tk.Button(
                self.main_frame, text="Buscar Alimentos", command=self.search_food
            ).pack(pady=5)
            tk.Button(
                self.main_frame, text="Filtrar Alimentos", command=self.filter_food
            ).pack(pady=5)
            tk.Button(self.main_frame, text="Ver Carrito", command=self.view_cart).pack(
                pady=5
            )
            tk.Button(
                self.main_frame,
                text="Finalizar Adquisiciones",
                command=self.finalize_acquisitions,
            ).pack(pady=5)
            tk.Button(
                self.main_frame,
                text="Ver Historial de Adquisiciones",
                command=self.view_acquisitions,
            ).pack(pady=5)

            # Botón para obtener recomendaciones
            tk.Button(
                self.main_frame,
                text="Obtener Recomendaciones",
                command=self.get_recommendations,
            ).pack(pady=5)

        tk.Button(self.main_frame, text="Cerrar Sesión", command=self.logout).pack(
            pady=5
        )

    def publish_food(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Publicar Alimento", font=("Arial", 14)).pack(
            pady=10
        )
        tk.Label(self.main_frame, text="Nombre:").pack(pady=2)
        nombre_entry = tk.Entry(self.main_frame)
        nombre_entry.pack(pady=2)
        tk.Label(self.main_frame, text="Fecha de Caducidad:").pack(pady=2)
        fecha_caducidad_entry = tk.Entry(self.main_frame)
        fecha_caducidad_entry.pack(pady=2)
        tk.Label(self.main_frame, text="Descripción:").pack(pady=2)
        descripcion_entry = tk.Entry(self.main_frame)
        descripcion_entry.pack(pady=2)
        tk.Label(self.main_frame, text="Unidades Disponibles:").pack(pady=2)
        unidades_entry = tk.Entry(self.main_frame)
        unidades_entry.pack(pady=2)
        tk.Label(self.main_frame, text="Tag:").pack(pady=2)
        tag_entry = tk.Entry(self.main_frame)
        tag_entry.pack(pady=2)

        def save_food():
            nombre = nombre_entry.get()
            fecha_caducidad = fecha_caducidad_entry.get()
            descripcion = descripcion_entry.get()
            try:
                unidades = int(unidades_entry.get())
                tag = tag_entry.get()
                self.sistema.publicar_alimento(
                    nombre, fecha_caducidad, descripcion, unidades, tag
                )
                messagebox.showinfo("Publicar Alimento", "Alimento publicado.")
                self.user_dashboard()
            except (ValueError, SistemaOperativoError) as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.main_frame, text="Publicar", command=save_food).pack(pady=5)
        tk.Button(self.main_frame, text="Volver", command=self.user_dashboard).pack(
            pady=5
        )

    def view_donations(self):
        self.clear_frame()
        tk.Label(
            self.main_frame, text="Historial de Donaciones", font=("Arial", 14)
        ).pack(pady=10)
        donations = self.sistema.obtener_historial_donaciones()
        for donation in donations:
            tk.Label(self.main_frame, text=str(donation)).pack(pady=2)
        tk.Button(self.main_frame, text="Volver", command=self.user_dashboard).pack(
            pady=5
        )

    def search_food(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Buscar Alimentos", font=("Arial", 14)).pack(
            pady=10
        )
        tk.Label(self.main_frame, text="Ingrese un tag para buscar:").pack(pady=2)
        tag_entry = tk.Entry(self.main_frame)
        tag_entry.pack(pady=2)

        def search():
            tag = tag_entry.get()
            try:
                results = self.sistema.buscar_alimentos_por_tag(tag)
                self.clear_frame()
                tk.Label(
                    self.main_frame, text="Resultados de búsqueda:", font=("Arial", 14)
                ).pack(pady=10)
                for food in results:
                    tk.Label(self.main_frame, text=str(food)).pack(pady=2)

                tk.Button(
                    self.main_frame,
                    text="Agregar al Carrito",
                    command=lambda: self.add_to_cart(results),
                ).pack(pady=5)
                tk.Button(
                    self.main_frame, text="Volver", command=self.user_dashboard
                ).pack(pady=5)
            except AlimentoNoEncontradoError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.main_frame, text="Buscar", command=search).pack(pady=5)
        tk.Button(self.main_frame, text="Volver", command=self.user_dashboard).pack(
            pady=5
        )

    def add_to_cart(self, results):
        self.clear_frame()
        tk.Label(self.main_frame, text="Agregar al Carrito", font=("Arial", 14)).pack(
            pady=10
        )
        tk.Label(self.main_frame, text="Seleccione el alimento para agregar:").pack(
            pady=2
        )

        for food in results:
            tk.Button(
                self.main_frame,
                text=str(food),
                command=lambda f=food: self.add_food_to_cart(f),
            ).pack(pady=2)

        tk.Button(self.main_frame, text="Volver", command=self.user_dashboard).pack(
            pady=5
        )

    def add_food_to_cart(self, food):
        self.carrito.append(food)
        messagebox.showinfo("Carrito", f"{food.nombre} ha sido agregado al carrito.")

    def view_cart(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Carrito", font=("Arial", 14)).pack(pady=10)
        if not self.carrito:
            tk.Label(self.main_frame, text="El carrito está vacío.").pack(pady=2)
        else:
            for food in self.carrito:
                tk.Label(self.main_frame, text=str(food)).pack(pady=2)
        tk.Button(self.main_frame, text="Volver", command=self.user_dashboard).pack(
            pady=5
        )

    def finalize_acquisitions(self):
        self.clear_frame()
        tk.Label(
            self.main_frame, text="Finalizar Adquisiciones", font=("Arial", 14)
        ).pack(pady=10)
        try:
            self.sistema.finalizar_adquisiciones(self.carrito)
            messagebox.showinfo("Finalizar", "Adquisiciones finalizadas exitosamente.")
            self.carrito.clear()  # Limpiar el carrito después de finalizar
            self.user_dashboard()
        except (CarritoVacioError, AlimentosNoSeleccionadosError) as e:
            messagebox.showerror("Error", str(e))

    def view_acquisitions(self):
        self.clear_frame()
        tk.Label(
            self.main_frame, text="Historial de Adquisiciones", font=("Arial", 14)
        ).pack(pady=10)
        acquisitions = self.sistema.obtener_historial_adquisiciones()
        for acquisition in acquisitions:
            tk.Label(self.main_frame, text=str(acquisition)).pack(pady=2)
        tk.Button(self.main_frame, text="Volver", command=self.user_dashboard).pack(
            pady=5
        )

    def get_recommendations(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Recomendaciones", font=("Arial", 14)).pack(
            pady=10
        )
        try:
            recommendations = self.sistema.obtener_recomendaciones()
            for rec in recommendations:
                tk.Label(self.main_frame, text=str(rec)).pack(pady=2)
            tk.Button(self.main_frame, text="Volver", command=self.user_dashboard).pack(
                pady=5
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def logout(self):
        self.usuario_actual = None
        self.carrito.clear()
        messagebox.showinfo("Cerrar Sesión", "Sesión cerrada.")
        self.create_main_menu()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
