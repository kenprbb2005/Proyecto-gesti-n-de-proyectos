from tkinter import messagebox
from views.categorias_view import CategoriasView
from utils.ui import clear_tree
from controllers.helpers import get_selected_values


class CategoriasController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = CategoriasView(app_controller.content_frame, self)

    def on_show(self): self.load_categories()

    def load_categories(self, categorias=None):
        categorias = categorias if categorias is not None else self.app_controller.services.categoria_service.listar()
        clear_tree(self.view.tabla)
        for c in categorias:
            self.view.tabla.insert("", "end", values=(c.id_categoria, c.nombre, c.descripcion, c.estado, c.fecha_creacion))

    def create_category(self):
        try:
            self.app_controller.services.categoria_service.crear(self.view.nombre.get(), self.view.descripcion.get(), self.view.estado.get())
            self.clear_form(); self.load_categories(); messagebox.showinfo("Categorías", "Categoría registrada.")
        except Exception as e: messagebox.showerror("Error", str(e))

    def update_category(self):
        try:
            self.app_controller.services.categoria_service.actualizar(self.view.id_categoria.get(), self.view.nombre.get(), self.view.descripcion.get(), self.view.estado.get())
            self.clear_form(); self.load_categories(); messagebox.showinfo("Categorías", "Categoría actualizada.")
        except Exception as e: messagebox.showerror("Error", str(e))

    def delete_category(self):
        try:
            cat_id = self.view.id_categoria.get() or (get_selected_values(self.view.tabla) or [""])[0]
            if cat_id and messagebox.askyesno("Confirmar", "¿Deseas eliminar esta categoría?"):
                self.app_controller.services.categoria_service.eliminar(cat_id)
                self.clear_form(); self.load_categories()
        except Exception as e: messagebox.showerror("Error", str(e))

    def search_categories(self):
        self.load_categories(self.app_controller.services.categoria_service.buscar(self.view.buscar.get()))

    def fill_form_from_selection(self):
        values = get_selected_values(self.view.tabla)
        if not values: return
        self.clear_form()
        self.view.id_categoria.insert(0, values[0]); self.view.nombre.insert(0, values[1]); self.view.descripcion.insert(0, values[2]); self.view.estado.set(values[3])

    def clear_form(self):
        self.view.id_categoria.delete(0,"end"); self.view.nombre.delete(0,"end"); self.view.descripcion.delete(0,"end"); self.view.estado.set("Activa")
