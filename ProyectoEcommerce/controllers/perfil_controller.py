from views.perfil_view import PerfilView
from tkinter import messagebox

class PerfilController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = PerfilView(self.app_controller.content_frame, self)

    def change_password(self):
        messagebox.showinfo("Éxito", "Contraseña actualizada correctamente.")
