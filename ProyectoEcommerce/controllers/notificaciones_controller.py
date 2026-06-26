from tkinter import messagebox
from views.notificaciones_view import NotificacionesView
from utils.ui import clear_tree
from controllers.helpers import get_selected_values

class NotificacionesController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = NotificacionesView(app_controller.content_frame, self)

    def on_show(self): self.load_notifications()

    def load_notifications(self):
        clear_tree(self.view.tabla)
        for n in self.app_controller.services.notificacion_service.listar():
            self.view.tabla.insert("", "end", values=(n.id_notificacion, n.id_usuario, n.titulo, n.mensaje, n.tipo, "Sí" if n.leida else "No", n.fecha))

    def create_notification(self):
        try:
            self.app_controller.services.notificacion_service.crear(
                self.view.id_usuario.get(), self.view.titulo.get(), self.view.mensaje.get("1.0", "end").strip(), self.view.tipo.get()
            )
            self.clear_form(); self.load_notifications(); messagebox.showinfo("Notificaciones", "Notificación creada.")
        except Exception as e: messagebox.showerror("Error", str(e))

    def mark_read(self):
        try:
            values = get_selected_values(self.view.tabla)
            if values:
                self.app_controller.services.notificacion_service.marcar_leida(values[0])
                self.load_notifications()
        except Exception as e: messagebox.showerror("Error", str(e))

    def delete_notification(self):
        try:
            values = get_selected_values(self.view.tabla)
            if values and messagebox.askyesno("Confirmar", "¿Deseas eliminar esta notificación?"):
                self.app_controller.services.notificacion_service.eliminar(values[0])
                self.load_notifications()
        except Exception as e: messagebox.showerror("Error", str(e))

    def clear_form(self):
        self.view.id_usuario.delete(0,"end"); self.view.titulo.delete(0,"end"); self.view.mensaje.delete("1.0","end"); self.view.tipo.set("Sistema")
