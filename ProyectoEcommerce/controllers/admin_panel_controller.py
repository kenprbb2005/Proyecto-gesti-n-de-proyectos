from views.admin_panel_view import AdminPanelView
from utils.ui import clear_tree

class AdminPanelController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = AdminPanelView(app_controller.content_frame, self)

    def on_show(self): self.load_dashboard()

    def load_dashboard(self):
        resumen = self.app_controller.services.admin_service.resumen()
        self.view.set_summary(resumen)
        clear_tree(self.view.tabla)
        for p in self.app_controller.services.producto_service.productos_bajo_stock():
            self.view.tabla.insert("", "end", values=(p.id_producto, p.nombre, p.stock, p.stock_minimo, p.estado))
