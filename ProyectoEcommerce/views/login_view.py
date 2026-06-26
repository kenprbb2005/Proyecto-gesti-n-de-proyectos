import tkinter as tk
from tkinter import ttk
from utils.ui import card














class LoginView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Main.TFrame")
        self.controller = controller
        container = card(self, padding=34)
        container.place(relx=0.5, rely=0.5, anchor="center")
        ttk.Label(container, text="Iniciar sesión", style="Title.TLabel").pack(pady=(0, 8))
        ttk.Label(container, text="Accede para comprar o administrar el sistema.").pack(pady=(0, 20))
        ttk.Label(container, text="Correo electrónico", style="Field.TLabel").pack(anchor="w")
        self.email = ttk.Entry(container, width=42)
        self.email.pack(pady=(4, 12))
        ttk.Label(container, text="Contraseña", style="Field.TLabel").pack(anchor="w")
        self.password = ttk.Entry(container, width=42, show="*")
        self.password.pack(pady=(4, 12))
        self.remember = tk.BooleanVar(value=True)
        ttk.Checkbutton(container, text="Mantener sesión iniciada", variable=self.remember).pack(anchor="w", pady=(0, 18))
        ttk.Button(container, text="Ingresar", style="Primary.TButton", command=self.controller.login).pack(fill="x", pady=4)
        ttk.Button(container, text="Crear cuenta", command=self.controller.go_to_register).pack(fill="x", pady=4)
        ttk.Button(container, text="Recuperar contraseña", command=self.controller.go_to_recover).pack(fill="x", pady=4)
        ttk.Button(container, text="Volver al catálogo", command=lambda: self.controller.app_controller.show_view("catalogo")).pack(fill="x", pady=(14, 0))
        self.email.insert(0, "admin@demo.com")
        self.password.insert(0, "admin123")
