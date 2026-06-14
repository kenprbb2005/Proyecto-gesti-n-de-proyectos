from views.catalogo_view import CatalogoView
from tkinter import messagebox

class CatalogoController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = CatalogoView(self.app_controller.content_frame, self)

    def go_to_login(self):
        self.app_controller.show_view("login")

    def go_to_cart(self):
        self.app_controller.show_view("carrito")

    def add_to_cart(self):
        messagebox.showinfo("Carrito", "Producto agregado al carrito con éxito.")
