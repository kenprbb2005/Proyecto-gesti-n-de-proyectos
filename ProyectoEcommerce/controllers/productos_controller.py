from tkinter import messagebox
from views.productos_view import ProductosView
from utils.ui import clear_tree, money
from controllers.helpers import get_selected_values, parse_combo_id


class ProductosController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = ProductosView(app_controller.content_frame, self)
        self.categorias = []
        self.selected_product_id = None

    def on_show(self):
        self.load_categories_combo()
        self.load_products()

    def load_categories_combo(self):
        self.categorias = self.app_controller.services.categoria_service.listar(solo_activas=True)
        values = [f"{c.id_categoria} | {c.nombre}" for c in self.categorias]
        self.view.categoria.configure(values=values)
        if values and not self.view.categoria.get():
            self.view.categoria.set(values[0])

    def load_products(self, productos=None):
        productos = productos if productos is not None else self.app_controller.services.producto_service.listar_productos()
        clear_tree(self.view.tabla)
        for p in productos:
            self.view.tabla.insert("", "end", iid=p.id_producto, values=(p.id_producto, p.nombre, p.categoria, p.marca, money(p.precio), p.stock, p.stock_minimo, p.estado))

    def _form(self):
        return dict(
            nombre=self.view.nombre.get(),
            id_categoria=parse_combo_id(self.view.categoria.get()),
            marca=self.view.marca.get(),
            precio=float(self.view.precio.get()),
            stock=int(self.view.stock.get()),
            stock_minimo=int(self.view.stock_minimo.get()),
            descripcion=self.view.descripcion.get(),
            estado=self.view.estado.get(),
        )

    def create_product(self):
        try:
            self.app_controller.services.producto_service.crear_producto(**self._form())
            self.clear_form()
            self.load_categories_combo()
            self.load_products()
            messagebox.showinfo("Productos", "Producto registrado.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_product(self):
        try:
            self.app_controller.services.producto_service.actualizar_producto(self.view.id_producto.get(), **self._form())
            self.clear_form()
            self.load_categories_combo()
            self.load_products()
            messagebox.showinfo("Productos", "Producto actualizado.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_product(self):
        try:
            prod_id = self.view.id_producto.get() or (get_selected_values(self.view.tabla) or [""])[0]
            if prod_id and messagebox.askyesno("Confirmar", "¿Deseas eliminar este producto?"):
                self.app_controller.services.producto_service.eliminar_producto(prod_id)
                self.clear_form()
                self.load_products()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_products(self):
        self.load_products(self.app_controller.services.producto_service.buscar_productos(self.view.buscar.get()))

    def fill_form_from_selection(self):
        values = get_selected_values(self.view.tabla)
        if not values:
            return
        self.selected_product_id = values[0]
        producto = self.app_controller.services.producto_service.obtener_producto(values[0])
        if not producto:
            return
        self.clear_form()
        self.view.id_producto.insert(0, producto.id_producto)
        self.view.nombre.insert(0, producto.nombre)
        self.view.categoria.set(f"{producto.id_categoria} | {producto.categoria}")
        self.view.marca.insert(0, producto.marca)
        self.view.precio.insert(0, str(producto.precio))
        self.view.stock.insert(0, str(producto.stock))
        self.view.stock_minimo.insert(0, str(producto.stock_minimo))
        self.view.estado.set(producto.estado)
        self.view.descripcion.insert(0, producto.descripcion)

    def add_selected_to_cart(self, abrir_carrito=False):
        if not self.app_controller.current_user:
            messagebox.showwarning("Login requerido", "Debes iniciar sesión para agregar productos al carrito.")
            self.app_controller.show_view("login")
            return
        values = get_selected_values(self.view.tabla)
        if values:
            self.selected_product_id = values[0]
        if not self.selected_product_id:
            messagebox.showwarning("Catálogo", "Selecciona un producto de la tabla.")
            return
        try:
            cantidad = int(self.view.cantidad_carrito.get())
            self.app_controller.services.carrito_service.agregar_producto(
                self.app_controller.current_user.id_usuario,
                self.selected_product_id,
                cantidad,
            )
            producto = self.app_controller.services.producto_service.obtener_producto(self.selected_product_id)
            messagebox.showinfo("Carrito", f"{producto.nombre if producto else 'Producto'} agregado al carrito.")
            self.load_products()
            if abrir_carrito:
                self.app_controller.show_view("carrito")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_selected_to_cart_and_open(self):
        self.add_selected_to_cart(abrir_carrito=True)

    def clear_form(self):
        for e in [self.view.id_producto, self.view.nombre, self.view.marca, self.view.precio, self.view.stock, self.view.stock_minimo, self.view.descripcion]:
            e.delete(0, "end")
        self.view.estado.set("Disponible")
