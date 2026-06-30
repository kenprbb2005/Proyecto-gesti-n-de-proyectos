from tkinter import messagebox
from views.pedidos_view import PedidosView
from utils.ui import clear_tree, money
from controllers.helpers import get_selected_values


class PedidosController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = PedidosView(app_controller.content_frame, self)
        self.pedido_enfocado = None

    def on_show(self):
        self.load_orders()

    def load_orders(self):
        clear_tree(self.view.tabla)
        pedidos = self.app_controller.services.pedido_service.listar_pedidos()
        for p in pedidos:
            cantidad_items = sum(int(item.get("cantidad", 0)) for item in p.items)
            resumen = ", ".join([f"{item.get('nombre', 'Producto')} x{item.get('cantidad', 1)}" for item in p.items[:2]])
            if len(p.items) > 2:
                resumen += "..."
            self.view.tabla.insert(
                "",
                "end",
                iid=p.id_pedido,
                values=(
                    p.id_pedido,
                    p.id_usuario,
                    cantidad_items,
                    resumen,
                    money(p.subtotal),
                    money(p.impuesto),
                    money(p.envio),
                    money(p.total),
                    p.estado,
                    p.fecha_creacion,
                ),
            )

        if self.pedido_enfocado:
            self._select_order(self.pedido_enfocado)

    def _select_order(self, id_pedido: str):
        if id_pedido in self.view.tabla.get_children():
            self.view.tabla.selection_set(id_pedido)
            self.view.tabla.focus(id_pedido)
            self.view.tabla.see(id_pedido)
            self.fill_from_selection()

    def fill_from_selection(self):
        values = get_selected_values(self.view.tabla)
        if not values:
            return
        self.view.id_pedido.delete(0, "end")
        self.view.id_pedido.insert(0, values[0])
        self.view.estado.set(values[8])
        pedido = self.app_controller.services.pedido_service.obtener(values[0])
        if pedido:
            self.view.set_detail(pedido)

    def _get_order_id(self):
        pedido_id = self.view.id_pedido.get().strip()
        if pedido_id:
            return pedido_id
        values = get_selected_values(self.view.tabla)
        if values:
            return values[0]
        raise ValueError("Selecciona un pedido de la tabla.")

    def change_status(self):
        try:
            self.app_controller.services.pedido_service.cambiar_estado(self._get_order_id(), self.view.estado.get())
            self.load_orders()
            messagebox.showinfo("Pedidos", "Estado actualizado.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cancel_order(self):
        try:
            pedido_id = self._get_order_id()
            if pedido_id and messagebox.askyesno("Confirmar", "¿Deseas cancelar este pedido? Se restaurará el stock si aplica."):
                self.app_controller.services.pedido_service.cancelar(pedido_id)
                self.pedido_enfocado = pedido_id
                self.load_orders()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def go_to_payment(self):
        """Envía el pedido seleccionado al proceso de pagos."""
        try:
            pedido_id = self._get_order_id()
            pedido = self.app_controller.services.pedido_service.obtener(pedido_id)
            if not pedido:
                raise ValueError("El pedido seleccionado no existe.")
            if pedido.estado == "Cancelado":
                raise ValueError("No se puede pagar un pedido cancelado.")
            if pedido.estado == "Entregado":
                raise ValueError("No se puede pagar un pedido entregado.")
            if pedido.estado == "Pagado":
                raise ValueError("Este pedido ya tiene estado Pagado.")

            pagos_controller = self.app_controller.controllers["pagos"]
            pagos_controller.pedido_preparado = pedido.id_pedido
            self.app_controller.show_view("pagos")
            pagos_controller.prepare_payment_for_order(pedido.id_pedido)
        except Exception as e:
            messagebox.showerror("Error", str(e))
