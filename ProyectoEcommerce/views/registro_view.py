import tkinter as tk
from tkinter import ttk

class RegistroView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="TFrame")
        self.controller = controller
        
        container = ttk.Frame(self, style="Card.TFrame", padding=30)
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(container, text="Crear Cuenta", style="Title.TLabel", background="white").pack(pady=(0, 20))
        
        ttk.Label(container, text="Nombre Completo", background="white").pack(anchor="w")
        ttk.Entry(container, width=40).pack(pady=(0, 10))

        ttk.Label(container, text="Correo Electrónico", background="white").pack(anchor="w")
        ttk.Entry(container, width=40).pack(pady=(0, 10))
        
        ttk.Label(container, text="Contraseña", background="white").pack(anchor="w")
        ttk.Entry(container, width=40, show="*").pack(pady=(0, 10))

        ttk.Button(container, text="Registrarse", command=self.controller.register).pack(fill="x", pady=5)
        ttk.Button(container, text="Volver al Login", command=self.controller.go_to_login).pack(fill="x", pady=5)
