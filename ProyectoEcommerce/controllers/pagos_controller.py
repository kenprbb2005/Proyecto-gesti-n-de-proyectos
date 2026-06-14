from views.pagos_view import PagosView

class PagosController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = PagosView(self.app_controller.content_frame, self)
