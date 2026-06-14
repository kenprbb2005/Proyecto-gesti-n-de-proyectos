import tkinter as tk
from tkinter import ttk

class LoginView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="TFrame")
        self.controller = controller
        
        container = ttk.Frame(self, style="Card.TFrame", padding=30)
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(container, text="Iniciar Sesión", style="Title.TLabel", background="white").pack(pady=(0, 20))
        
        ttk.Label(container, text="Correo Electrónico", background="white").pack(anchor="w")
        self.email = ttk.Entry(container, width=40)
        self.email.pack(pady=(0, 10))
        
        ttk.Label(container, text="Contraseña", background="white").pack(anchor="w")
        self.password = ttk.Entry(container, width=40, show="*")
        self.password.pack(pady=(0, 10))
        
        self.remember = tk.BooleanVar()
        ttk.Checkbutton(container, text="Mantener sesión iniciada", variable=self.remember, style="TCheckbutton").pack(anchor="w", pady=(0, 20))
        
        ttk.Button(container, text="Ingresar", command=self.controller.login).pack(fill="x", pady=5)
        ttk.Button(container, text="Registrarse", command=self.controller.go_to_register).pack(fill="x", pady=5)
        ttk.Button(container, text="Recuperar Contraseña", command=self.controller.go_to_recover).pack(fill="x", pady=5)
        
        ttk.Label(container, text="", background="white").pack(pady=5)
        ttk.Button(container, text="Volver a la Tienda", command=lambda: self.controller.app_controller.show_view("catalogo")).pack(fill="x", pady=(10, 5))
