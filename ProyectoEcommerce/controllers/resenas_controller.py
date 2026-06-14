from views.resenas_view import ResenasView

class ResenasController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = ResenasView(self.app_controller.content_frame, self)
