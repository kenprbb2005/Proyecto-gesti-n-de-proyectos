from tkinter import ttk
from utils.ui import card


class RecuperarView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Main.TFrame")
        self.controller = controller
        container = card(self, padding=34)
        container.place(relx=0.5, rely=0.5, anchor="center")
        ttk.Label(container, text="Recuperar contraseña", style="Title.TLabel").pack(pady=(0, 10))
        ttk.Label(container, text="Recuperación simulada para el proyecto académico.", wraplength=310).pack(pady=(0, 18))
        ttk.Label(container, text="Correo electrónico", style="Field.TLabel").pack(anchor="w")
        self.email = ttk.Entry(container, width=42)
        self.email.pack(pady=(4, 18))
        ttk.Button(container, text="Enviar recuperación", style="Primary.TButton", command=self.controller.recover).pack(fill="x", pady=4)
        ttk.Button(container, text="Volver al login", command=self.controller.go_to_login).pack(fill="x", pady=4)
