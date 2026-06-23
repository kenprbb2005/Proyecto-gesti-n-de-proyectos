from views.panel_admin_view import PanelAdminView

class PanelAdminController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = PanelAdminView(self.app_controller.content_frame, self)

    def ir_a_modulo(self, vista):
        self.app_controller.show_view(vista)
