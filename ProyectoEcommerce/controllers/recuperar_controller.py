from tkinter import messagebox
from views.recuperar_view import RecuperarView


class RecuperarController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = RecuperarView(app_controller.content_frame, self)

    def recover(self):
        try:
            msg = self.app_controller.services.auth_service.recuperar_contrasena(self.view.email.get())
            messagebox.showinfo("Recuperación", msg)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def go_to_login(self):
        self.app_controller.show_view("login")
