from views.registro_view import RegistroView
from tkinter import messagebox

class RegistroController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = RegistroView(self.app_controller.content_frame, self)

    def register(self):
        messagebox.showinfo("Éxito", "Cuenta registrada correctamente. Iniciando sesión...")
        self.app_controller.login_success()

    def go_to_login(self):
        self.app_controller.show_auth_view("login")
