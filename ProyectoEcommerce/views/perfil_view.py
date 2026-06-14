import tkinter as tk
from tkinter import ttk

class PerfilView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="TFrame")
        self.controller = controller
        
        header = ttk.Frame(self)
        header.pack(fill="x", padx=25, pady=(20, 10))

        ttk.Label(header, text="Mi Perfil", style="Title.TLabel", background="#eef2f7").pack(anchor="w")
        ttk.Label(header, text="Gestiona tu cuenta y seguridad.", style="Subtitle.TLabel").pack(anchor="w")

        card = ttk.Frame(self, style="Card.TFrame")
        card.pack(fill="x", padx=25, pady=10)

        ttk.Label(card, text="Cambiar Contraseña", style="Title.TLabel", background="white").pack(anchor="w", padx=15, pady=10)

        ttk.Label(card, text="Contraseña Actual", background="white").pack(anchor="w", padx=15)
        ttk.Entry(card, width=40, show="*").pack(anchor="w", padx=15, pady=(0, 10))

        ttk.Label(card, text="Nueva Contraseña", background="white").pack(anchor="w", padx=15)
        ttk.Entry(card, width=40, show="*").pack(anchor="w", padx=15, pady=(0, 10))

        ttk.Button(card, text="Actualizar Contraseña", command=self.controller.change_password).pack(anchor="w", padx=15, pady=10)
