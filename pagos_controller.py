from tkinter import messagebox
from views.pagos_view import PagosView
from utils.ui import clear_tree, money
from controllers.helpers import get_selected_values


class PagosController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = PagosView(app_controller.content_frame, self)
        self.pedido_preparado = None

    def on_show(self):
        self.load_payments()
        if self.pedido_preparado:
            self.prepare_payment_for_order(self.pedido_preparado)

    def load_payments(self):
        clear_tree(self.view.tabla)
        for p in self.app_controller.services.pago_service.listar_pagos():
            self.view.tabla.insert("", "end", iid=p.id_pago, values=(p.id_pago, p.id_pedido, p.id_usuario, p.metodo, money(p.monto), p.estado, p.referencia, p.fecha_pago))

    def prepare_payment_for_order(self, id_pedido: str):
        pedido = self.app_controller.services.pedido_service.obtener(id_pedido)
        if not pedido:
            raise ValueError("No existe el pedido seleccionado.")
        self.view.id_pedido.delete(0, "end")
        self.view.id_pedido.insert(0, pedido.id_pedido)
        self.view.monto.delete(0, "end")
        self.view.monto.insert(0, str(pedido.total))
        if not self.view.metodo.get():
            self.view.metodo.set("Tarjeta")
        if not self.view.referencia.get().strip():
            self.view.referencia.insert(0, f"PED-{pedido.id_pedido}")
        self.view.set_context(pedido)

    def fill_from_selection(self):
        values = get_selected_values(self.view.tabla)
        if not values:
            return
        self.view.id_pedido.delete(0, "end")
        self.view.id_pedido.insert(0, values[1])
        self.view.metodo.set(values[3])
        self.view.referencia.delete(0, "end")
        self.view.referencia.insert(0, values[6])
        pedido = self.app_controller.services.pedido_service.obtener(values[1])
        if pedido:
            self.view.monto.delete(0, "end")
            self.view.monto.insert(0, str(pedido.total))
            self.view.set_context(pedido)

    def process_payment(self):
        try:
            id_pedido = self.view.id_pedido.get().strip()
            if not id_pedido:
                raise ValueError("Primero debes recibir o seleccionar un pedido.")
            pedido = self.app_controller.services.pedido_service.obtener(id_pedido)
            if not pedido:
                raise ValueError("El pedido no existe.")
            monto_texto = self.view.monto.get().strip()
            monto = float(monto_texto) if monto_texto else float(pedido.total)
            pago = self.app_controller.services.pago_service.procesar_pago(
                id_pedido,
                self.view.metodo.get(),
                monto,
                self.view.referencia.get(),
            )
            self.pedido_preparado = None
            self.load_payments()
            pedidos_controller = self.app_controller.controllers["pedidos"]
            pedidos_controller.pedido_enfocado = id_pedido
            messagebox.showinfo("Pago", pago.mensaje)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cancel_payment(self):
        try:
            values = get_selected_values(self.view.tabla)
            if values and messagebox.askyesno("Confirmar", "¿Deseas anular este pago?"):
                self.app_controller.services.pago_service.anular_pago(values[0])
                self.load_payments()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def go_to_orders(self):
        self.app_controller.show_view("pedidos")
