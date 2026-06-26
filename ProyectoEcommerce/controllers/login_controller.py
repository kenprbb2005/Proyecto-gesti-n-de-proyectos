from tkinter import messagebox
from views.login_view import LoginView


class LoginController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = LoginView(app_controller.content_frame, self)

    def login(self):
        try:
            usuario = self.app_controller.services.auth_service.login(self.view.email.get(), self.view.password.get())
            self.app_controller.current_user = usuario
            self.app_controller.refresh_navbar()
            messagebox.showinfo("Sesión", f"Bienvenido, {usuario.nombre}.")
            if usuario.rol == "Administrador":
                self.app_controller.show_view("admin")
            else:
                self.app_controller.show_view("catalogo")
        except Exception as e:
            messagebox.showerror("Error de login", str(e))

    def go_to_register(self):
        self.app_controller.show_view("registro")

    def go_to_recover(self):
        self.app_controller.show_view("recuperar")
