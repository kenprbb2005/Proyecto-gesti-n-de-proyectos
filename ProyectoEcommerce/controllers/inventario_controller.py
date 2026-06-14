from views.inventario_view import InventarioView

class InventarioController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = InventarioView(self.app_controller.content_frame, self)
