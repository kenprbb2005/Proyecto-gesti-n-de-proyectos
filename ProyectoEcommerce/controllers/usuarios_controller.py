from tkinter import messagebox
from views.usuarios_view import UsuariosView
from utils.ui import clear_tree
from controllers.helpers import get_selected_values


class UsuariosController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = UsuariosView(app_controller.content_frame, self)

    def on_show(self):
        self.load_users()

    def load_users(self, usuarios=None):
        usuarios = usuarios if usuarios is not None else self.app_controller.services.usuario_service.listar_usuarios()
        clear_tree(self.view.tabla)
        for u in usuarios:
            self.view.tabla.insert("", "end", values=(u.id_usuario, u.nombre, u.correo, u.rol, u.estado, u.fecha_registro))

    def create_user(self):
        try:
            self.app_controller.services.usuario_service.registrar_usuario(
                self.view.nombre.get(), self.view.correo.get(), self.view.contrasena.get(), self.view.rol.get(), self.view.estado.get()
            )
            self.clear_form(); self.load_users()
            messagebox.showinfo("Usuarios", "Usuario registrado correctamente.")
        except Exception as e: messagebox.showerror("Error", str(e))

    def update_user(self):
        try:
            self.app_controller.services.usuario_service.actualizar_usuario(
                self.view.id_usuario.get(), self.view.nombre.get(), self.view.correo.get(), self.view.rol.get(), self.view.estado.get(), self.view.contrasena.get()
            )
            self.clear_form(); self.load_users()
            messagebox.showinfo("Usuarios", "Usuario actualizado correctamente.")
        except Exception as e: messagebox.showerror("Error", str(e))

    def toggle_user_status(self):
        try:
            user_id = self.view.id_usuario.get() or (get_selected_values(self.view.tabla) or [""])[0]
            self.app_controller.services.usuario_service.cambiar_estado(user_id)
            self.clear_form(); self.load_users()
        except Exception as e: messagebox.showerror("Error", str(e))

    def delete_user(self):
        try:
            user_id = self.view.id_usuario.get() or (get_selected_values(self.view.tabla) or [""])[0]
            if user_id and messagebox.askyesno("Confirmar", "¿Deseas eliminar este usuario?"):
                self.app_controller.services.usuario_service.eliminar_usuario(user_id)
                self.clear_form(); self.load_users()
        except Exception as e: messagebox.showerror("Error", str(e))

    def search_users(self):
        self.load_users(self.app_controller.services.usuario_service.buscar(self.view.buscar.get()))

    def fill_form_from_selection(self):
        values = get_selected_values(self.view.tabla)
        if not values: return
        self.clear_form()
        self.view.id_usuario.insert(0, values[0]); self.view.nombre.insert(0, values[1]); self.view.correo.insert(0, values[2])
        self.view.rol.set(values[3]); self.view.estado.set(values[4])

    def clear_form(self):
        for e in [self.view.id_usuario, self.view.nombre, self.view.correo, self.view.contrasena]:
            e.delete(0, "end")
        self.view.rol.set("Cliente"); self.view.estado.set("Activo")
