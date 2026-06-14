import tkinter as tk
from tkinter import ttk

class RecuperarView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="TFrame")
        self.controller = controller
        
        container = ttk.Frame(self, style="Card.TFrame", padding=30)
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(container, text="Recuperar Contraseña", style="Title.TLabel", background="white").pack(pady=(0, 20))
        ttk.Label(container, text="Ingresa tu correo para recibir un enlace de recuperación.", wraplength=250, background="white").pack(pady=(0, 20))
        
        ttk.Label(container, text="Correo Electrónico", background="white").pack(anchor="w")
        ttk.Entry(container, width=40).pack(pady=(0, 20))
        
        ttk.Button(container, text="Enviar Enlace", command=self.controller.recover).pack(fill="x", pady=5)
        ttk.Button(container, text="Volver al Login", command=self.controller.go_to_login).pack(fill="x", pady=5)
