from views.recuperar_view import RecuperarView
from tkinter import messagebox

class RecuperarController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = RecuperarView(self.app_controller.content_frame, self)

    def recover(self):
        messagebox.showinfo("Enviado", "Se ha enviado un enlace de recuperación a tu correo.")
        self.app_controller.show_auth_view("login")

    def go_to_login(self):
        self.app_controller.show_auth_view("login")
