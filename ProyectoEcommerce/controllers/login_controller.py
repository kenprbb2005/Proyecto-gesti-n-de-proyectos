from views.login_view import LoginView

class LoginController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = LoginView(self.app_controller.content_frame, self)

    def login(self):
        # MOCK LOGIN
        self.app_controller.login_success()

    def go_to_register(self):
        self.app_controller.show_auth_view("registro")

    def go_to_recover(self):
        self.app_controller.show_auth_view("recuperar")
