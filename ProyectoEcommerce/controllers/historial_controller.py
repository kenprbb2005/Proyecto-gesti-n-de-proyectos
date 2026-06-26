from views.historial_view import HistorialView


class HistorialController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = HistorialView(self.app_controller.content_frame, self)
