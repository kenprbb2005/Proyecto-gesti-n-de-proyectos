from tkinter import messagebox
from views.resenas_view import ResenasView
from utils.ui import clear_tree
from controllers.helpers import get_selected_values, parse_combo_id


class ResenasController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = ResenasView(app_controller.content_frame, self)

    def on_show(self):
        self.load_products_combo(); self.load_reviews()

    def load_products_combo(self):
        productos = self.app_controller.services.producto_service.listar_productos()
        values = [f"{p.id_producto} | {p.nombre}" for p in productos]
        self.view.producto.configure(values=values)
        if values and not self.view.producto.get(): self.view.producto.set(values[0])

    def load_reviews(self):
        clear_tree(self.view.tabla)
        for r in self.app_controller.services.resena_service.listar_resenas():
            self.view.tabla.insert("", "end", values=(r.id_resena, r.id_usuario, r.id_producto, r.calificacion, r.comentario, r.estado, r.fecha))

    def create_review(self):
        try:
            self.app_controller.services.resena_service.crear_resena_admin(
                self.view.id_usuario.get(), parse_combo_id(self.view.producto.get()), int(self.view.calificacion.get()),
                self.view.comentario.get("1.0", "end").strip(), self.view.estado.get()
            )
            self.clear_form(); self.load_reviews(); messagebox.showinfo("Reseñas", "Reseña registrada.")
        except Exception as e: messagebox.showerror("Error", str(e))

    def moderate_review(self):
        try:
            rid = self.view.id_resena.get() or (get_selected_values(self.view.tabla) or [""])[0]
            self.app_controller.services.resena_service.moderar(rid, self.view.estado.get())
            self.load_reviews(); messagebox.showinfo("Reseñas", "Estado actualizado.")
        except Exception as e: messagebox.showerror("Error", str(e))

    def delete_review(self):
        try:
            rid = self.view.id_resena.get() or (get_selected_values(self.view.tabla) or [""])[0]
            if rid and messagebox.askyesno("Confirmar", "¿Deseas eliminar esta reseña?"):
                self.app_controller.services.resena_service.eliminar_resena(rid)
                self.load_reviews()
        except Exception as e: messagebox.showerror("Error", str(e))

    def fill_from_selection(self):
        values = get_selected_values(self.view.tabla)
        if not values: return
        self.clear_form()
        self.view.id_resena.insert(0, values[0]); self.view.id_usuario.insert(0, values[1]); self.view.producto.set(values[2]); self.view.calificacion.set(values[3]); self.view.estado.set(values[5])
        self.view.comentario.insert("1.0", values[4])

    def clear_form(self):
        self.view.id_resena.delete(0,"end"); self.view.id_usuario.delete(0,"end"); self.view.comentario.delete("1.0","end"); self.view.calificacion.set("5"); self.view.estado.set("Publicada")
