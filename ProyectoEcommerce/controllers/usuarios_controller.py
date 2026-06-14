from views.usuarios_view import UsuariosView

class UsuariosController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = UsuariosView(self.app_controller.content_frame, self)
