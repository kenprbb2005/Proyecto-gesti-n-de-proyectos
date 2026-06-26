from tkinter import messagebox
from views.pedidos_view import PedidosView
from utils.ui import clear_tree, money
from controllers.helpers import get_selected_values


class PedidosController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = PedidosView(app_controller.content_frame, self)

    def on_show(self): self.load_orders()

    def load_orders(self):
        clear_tree(self.view.tabla)
        for p in self.app_controller.services.pedido_service.listar_pedidos():
            self.view.tabla.insert("", "end", values=(p.id_pedido, p.id_usuario, money(p.subtotal), money(p.impuesto), money(p.envio), money(p.total), p.estado, p.fecha_creacion))

    def fill_from_selection(self):
        values = get_selected_values(self.view.tabla)
        if not values: return
        self.view.id_pedido.delete(0,"end"); self.view.id_pedido.insert(0, values[0]); self.view.estado.set(values[6])

    def change_status(self):
        try:
            self.app_controller.services.pedido_service.cambiar_estado(self.view.id_pedido.get(), self.view.estado.get())
            self.load_orders(); messagebox.showinfo("Pedidos", "Estado actualizado.")
        except Exception as e: messagebox.showerror("Error", str(e))

    def cancel_order(self):
        try:
            pedido_id = self.view.id_pedido.get() or (get_selected_values(self.view.tabla) or [""])[0]
            if pedido_id and messagebox.askyesno("Confirmar", "¿Deseas cancelar este pedido? Se restaurará el stock si aplica."):
                self.app_controller.services.pedido_service.cancelar(pedido_id)
                self.load_orders()
        except Exception as e: messagebox.showerror("Error", str(e))
