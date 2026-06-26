from tkinter import messagebox
from views.inventario_view import InventarioView
from utils.ui import clear_tree
from controllers.helpers import parse_combo_id




class InventarioController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = InventarioView(app_controller.content_frame, self)

    def on_show(self):
        self.load_products_combo(); self.load_movements()

    def load_products_combo(self):
        productos = self.app_controller.services.producto_service.listar_productos()
        values = [f"{p.id_producto} | {p.nombre} | stock: {p.stock}" for p in productos]
        self.view.producto.configure(values=values)
        if values and not self.view.producto.get(): self.view.producto.set(values[0])

    def load_movements(self):
        clear_tree(self.view.tabla)
        for m in self.app_controller.services.inventario_service.listar_movimientos():
            self.view.tabla.insert("", "end", values=(m.id_movimiento, m.id_producto, m.tipo, m.cantidad, m.stock_anterior, m.stock_nuevo, m.motivo, m.fecha))
        self.load_products_combo()

    def create_movement(self):
        try:
            self.app_controller.services.inventario_service.registrar_movimiento(
                parse_combo_id(self.view.producto.get()), self.view.tipo.get(), int(self.view.cantidad.get()), self.view.motivo.get()
            )
            self.clear_form(); self.load_movements(); messagebox.showinfo("Inventario", "Movimiento registrado.")
        except Exception as e: messagebox.showerror("Error", str(e))

    def clear_form(self):
        self.view.cantidad.delete(0,"end"); self.view.motivo.delete(0,"end"); self.view.tipo.set("Entrada")
