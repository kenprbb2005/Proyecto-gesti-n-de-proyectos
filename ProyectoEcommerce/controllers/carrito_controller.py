from views.carrito_view import CarritoView
from tkinter import messagebox

class CarritoController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = CarritoView(self.app_controller.content_frame, self)

    def go_to_catalogo(self):
        self.app_controller.show_view("catalogo")

    def empty_cart(self):
        confirm = messagebox.askyesno("Vaciar Carrito", "¿Estás seguro de que deseas vaciar el carrito?")
        if confirm:
            messagebox.showinfo("Carrito", "El carrito ha sido vaciado.")

    def remove_item(self):
        confirm = messagebox.askyesno("Eliminar", "¿Deseas eliminar este producto del carrito?")
        if confirm:
            messagebox.showinfo("Eliminado", "Producto eliminado.")

    def checkout(self):
        messagebox.showinfo("Compra Exitosa", "¡Tu compra se ha procesado con éxito!\nNúmero de pedido: #10024")
        self.empty_cart()
        self.go_to_catalogo()
