from views.historial_view import HistorialView
from utils.ui import clear_tree



class HistorialController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = HistorialView(app_controller.content_frame, self)

    def on_show(self): self.load_history()

    def load_history(self, data=None):
        data = data if data is not None else self.app_controller.services.historial_service.listar()
        clear_tree(self.view.tabla)
        for h in data:
            self.view.tabla.insert("", "end", values=(h.id_historial, h.id_usuario, h.id_pedido, h.accion, h.descripcion, h.fecha))

    def filter_by_user(self):
        uid = self.view.id_usuario.get().strip()
        if not uid: self.load_history(); return
        self.load_history(self.app_controller.services.historial_service.listar_por_usuario(uid))
