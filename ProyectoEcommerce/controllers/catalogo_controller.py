from tkinter import messagebox
from views.catalogo_view import CatalogoView
from utils.ui import clear_tree, money
from controllers.helpers import get_selected_values


class CatalogoController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = CatalogoView(app_controller.content_frame, self)
        self.product_cache = {}

    def on_show(self):
        self.refresh_filters()
        self.load_products()

    def refresh_filters(self):
        categorias = ["Todas"] + [c.nombre for c in self.app_controller.services.categoria_service.listar(solo_activas=True)]
        productos = self.app_controller.services.producto_service.listar_productos()
        marcas = ["Todas"] + sorted(set(p.marca for p in productos if p.marca))
        self.view.categoria.configure(values=categorias)
        self.view.marca.configure(values=marcas)
        if self.view.categoria.get() not in categorias:
            self.view.categoria.set("Todas")
        if self.view.marca.get() not in marcas:
            self.view.marca.set("Todas")

    def load_products(self):
        try:
            precio_max = self.view.precio_maximo.get().strip()
            precio_max = float(precio_max) if precio_max else None
            productos = self.app_controller.services.producto_service.buscar_productos(
                self.view.buscar.get(), self.view.categoria.get(), self.view.marca.get(), precio_max
            )
            productos = [p for p in productos if p.estado == "Disponible" and p.stock > 0]
            self.product_cache = {p.id_producto: p for p in productos}
            clear_tree(self.view.tabla)
            for p in productos:
                self.view.tabla.insert("", "end", values=(p.id_producto, p.nombre, p.categoria, p.marca, money(p.precio), p.stock))
            self.view.set_detail(None)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_filters(self):
        self.view.buscar.delete(0, "end")
        self.view.precio_maximo.delete(0, "end")
        self.view.categoria.set("Todas")
        self.view.marca.set("Todas")
        self.load_products()

    def show_selected_detail(self):
        values = get_selected_values(self.view.tabla)
        if not values:
            return
        producto = self.product_cache.get(values[0])
        self.view.set_detail(producto)

    def add_to_cart(self):
        if not self.app_controller.current_user:
            messagebox.showwarning("Login requerido", "Debes iniciar sesión para agregar productos al carrito.")
            self.app_controller.show_view("login")
            return
        values = get_selected_values(self.view.tabla)
        if not values:
            return
        try:
            cantidad = int(self.view.cantidad.get())
            self.app_controller.services.carrito_service.agregar_producto(self.app_controller.current_user.id_usuario, values[0], cantidad)
            messagebox.showinfo("Carrito", "Producto agregado al carrito.")
            self.load_products()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def go_to_login(self):
        self.app_controller.show_view("login")

    def go_to_cart(self):
        if not self.app_controller.current_user:
            messagebox.showwarning("Login requerido", "Debes iniciar sesión para ver tu carrito.")
            self.app_controller.show_view("login")
            return
        self.app_controller.show_view("carrito")
