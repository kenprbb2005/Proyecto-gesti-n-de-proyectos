from tkinter import messagebox
from views.registro_view import RegistroView


class RegistroController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = RegistroView(app_controller.content_frame, self)

    def register(self):
        try:
            usuario = self.app_controller.services.auth_service.registro_cliente(
                self.view.nombre.get(), self.view.email.get(), self.view.password.get()
            )
            messagebox.showinfo("Registro", f"Usuario creado: {usuario.correo}")
            self.app_controller.show_view("login")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def go_to_login(self):
        self.app_controller.show_view("login")
