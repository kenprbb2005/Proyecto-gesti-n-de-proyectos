from tkinter import messagebox
from views.pagos_view import PagosView
from utils.ui import clear_tree, money
from controllers.helpers import get_selected_values


class PagosController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = PagosView(app_controller.content_frame, self)

    def on_show(self): self.load_payments()

    def load_payments(self):
        clear_tree(self.view.tabla)
        for p in self.app_controller.services.pago_service.listar_pagos():
            self.view.tabla.insert("", "end", values=(p.id_pago, p.id_pedido, p.id_usuario, p.metodo, money(p.monto), p.estado, p.referencia, p.fecha_pago))

    def fill_from_selection(self):
        values = get_selected_values(self.view.tabla)
        if not values: return
        self.view.id_pedido.delete(0,"end"); self.view.id_pedido.insert(0, values[1]); self.view.metodo.set(values[3]); self.view.referencia.delete(0,"end"); self.view.referencia.insert(0, values[6])

    def process_payment(self):
        try:
            pago = self.app_controller.services.pago_service.procesar_pago(self.view.id_pedido.get(), self.view.metodo.get(), float(self.view.monto.get()), self.view.referencia.get())
            self.load_payments(); messagebox.showinfo("Pago", pago.mensaje)
        except Exception as e: messagebox.showerror("Error", str(e))

    def cancel_payment(self):
        try:
            values = get_selected_values(self.view.tabla)
            if values and messagebox.askyesno("Confirmar", "¿Deseas anular este pago?"):
                self.app_controller.services.pago_service.anular_pago(values[0])
                self.load_payments()
        except Exception as e: messagebox.showerror("Error", str(e))
