from views.notificaciones_view import NotificacionesView

class NotificacionesController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = NotificacionesView(self.app_controller.content_frame, self)
