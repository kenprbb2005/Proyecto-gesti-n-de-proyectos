from tkinter import messagebox
from views.catalogo_view import CatalogoView
from utils.ui import clear_tree, money
from controllers.helpers import get_selected_values


class CatalogoController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = CatalogoView(app_controller.content_frame, self)
        self.product_cache = {}
        self.selected_product_id = None

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
                self.view.tabla.insert("", "end", iid=p.id_producto, values=(p.id_producto, p.nombre, p.categoria, p.marca, money(p.precio), p.stock))
            if self.selected_product_id in self.product_cache:
                self.view.tabla.selection_set(self.selected_product_id)
                self.view.tabla.focus(self.selected_product_id)
                self.view.tabla.see(self.selected_product_id)
                self.view.set_detail(self.product_cache[self.selected_product_id])
            else:
                self.selected_product_id = None
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
        self.selected_product_id = values[0]
        producto = self.product_cache.get(self.selected_product_id)
        self.view.set_detail(producto)

    def _get_selected_product_id(self):
        values = get_selected_values(self.view.tabla)
        if values:
            self.selected_product_id = values[0]
        if not self.selected_product_id:
            raise ValueError("Selecciona un producto de la tabla del catálogo.")
        return self.selected_product_id

    def add_to_cart(self, abrir_carrito=False):
        if not self.app_controller.current_user:
            messagebox.showwarning("Login requerido", "Debes iniciar sesión para agregar productos al carrito.")
            self.app_controller.show_view("login")
            return
        try:
            id_producto = self._get_selected_product_id()
            cantidad = int(self.view.cantidad.get())
            carrito = self.app_controller.services.carrito_service.agregar_producto(
                self.app_controller.current_user.id_usuario,
                id_producto,
                cantidad,
            )
            producto = self.app_controller.services.producto_service.obtener_producto(id_producto)
            messagebox.showinfo("Carrito", f"{producto.nombre if producto else 'Producto'} agregado al carrito.")
            self.load_products()
            if abrir_carrito:
                self.app_controller.show_view("carrito")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_to_cart_and_open(self):
        self.add_to_cart(abrir_carrito=True)

    def go_to_login(self):
        self.app_controller.show_view("login")

    def go_to_cart(self):
        if not self.app_controller.current_user:
            messagebox.showwarning("Login requerido", "Debes iniciar sesión para ver tu carrito.")
            self.app_controller.show_view("login")
            return
        self.app_controller.show_view("carrito")
