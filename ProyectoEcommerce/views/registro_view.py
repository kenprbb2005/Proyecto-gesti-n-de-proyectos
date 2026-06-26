from tkinter import ttk
from utils.ui import card


class RegistroView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Main.TFrame")
        self.controller = controller
        container = card(self, padding=34)
        container.place(relx=0.5, rely=0.5, anchor="center")
        ttk.Label(container, text="Crear cuenta", style="Title.TLabel").pack(pady=(0, 20))
        ttk.Label(container, text="Nombre completo", style="Field.TLabel").pack(anchor="w")
        self.nombre = ttk.Entry(container, width=42)
        self.nombre.pack(pady=(4, 12))
        ttk.Label(container, text="Correo electrónico", style="Field.TLabel").pack(anchor="w")
        self.email = ttk.Entry(container, width=42)
        self.email.pack(pady=(4, 12))
        ttk.Label(container, text="Contraseña", style="Field.TLabel").pack(anchor="w")
        self.password = ttk.Entry(container, width=42, show="*")
        self.password.pack(pady=(4, 18))
        ttk.Button(container, text="Registrarme", style="Primary.TButton", command=self.controller.register).pack(fill="x", pady=4)
        ttk.Button(container, text="Volver al login", command=self.controller.go_to_login).pack(fill="x", pady=4)
