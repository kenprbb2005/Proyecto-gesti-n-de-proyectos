import tkinter as tk
from tkinter import ttk

class UsuariosView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Main.TFrame")
        self.controller = controller
        
        contenedor = ttk.Frame(self, style="Main.TFrame")
        contenedor.pack(fill="both", expand=True, padx=30, pady=25)

        ttk.Label(contenedor, text="Gestión de Usuarios", style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            contenedor,
            text="Administración de cuentas, roles y estado de acceso de los usuarios.",
            style="Subheader.TLabel"
        ).pack(anchor="w", pady=(0, 20))

        formulario = ttk.Frame(contenedor, style="Card.TFrame")
        formulario.pack(fill="x", pady=10)

        campos = [
            ("ID Usuario", 0, 0),
            ("Nombre Completo", 0, 2),
            ("Correo Electrónico", 1, 0),
        ]

        for texto, fila, columna in campos:
            ttk.Label(formulario, text=texto, style="Field.TLabel").grid(row=fila, column=columna, padx=18, pady=14, sticky="w")
            ttk.Entry(formulario, width=34).grid(row=fila, column=columna + 1, padx=18, pady=14)

        ttk.Label(formulario, text="Contraseña", style="Field.TLabel").grid(row=1, column=2, padx=18, pady=14, sticky="w")
        ttk.Entry(formulario, width=34, show="*").grid(row=1, column=3, padx=18, pady=14)

        ttk.Label(formulario, text="Rol", style="Field.TLabel").grid(row=2, column=0, padx=18, pady=14, sticky="w")
        ttk.Combobox(
            formulario,
            values=["Administrador", "Cliente", "Vendedor", "Soporte"],
            width=31
        ).grid(row=2, column=1, padx=18, pady=14)

        ttk.Label(formulario, text="Estado", style="Field.TLabel").grid(row=2, column=2, padx=18, pady=14, sticky="w")
        ttk.Combobox(
            formulario,
            values=["Activo", "Inactivo", "Bloqueado"],
            width=31
        ).grid(row=2, column=3, padx=18, pady=14)

        botones = ttk.Frame(contenedor, style="Main.TFrame")
        botones.pack(fill="x", pady=15)

        ttk.Button(botones, text="Registrar Usuario").pack(side="left", padx=5)
        ttk.Button(botones, text="Guardar Cambios").pack(side="left", padx=5)
        ttk.Button(botones, text="Eliminar").pack(side="left", padx=5)
        ttk.Button(botones, text="Activar / Desactivar").pack(side="left", padx=5)
        ttk.Button(botones, text="Buscar").pack(side="left", padx=5)
        ttk.Button(botones, text="Limpiar").pack(side="left", padx=5)

        tabla_frame = ttk.Frame(contenedor, style="Card.TFrame")
        tabla_frame.pack(fill="both", expand=True, pady=10)

        tabla = ttk.Treeview(
            tabla_frame,
            columns=("id_usuario", "nombre", "correo", "rol", "estado"),
            show="headings"
        )

        encabezados = {
            "id_usuario": "ID Usuario",
            "nombre": "Nombre Completo",
            "correo": "Correo Electrónico",
            "rol": "Rol",
            "estado": "Estado"
        }

        for columna, texto in encabezados.items():
            tabla.heading(columna, text=texto)
            tabla.column(columna, width=150)
            
        tabla.column("nombre", width=220)
        tabla.column("correo", width=220)

        scroll_y = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla.yview)
        scroll_x = ttk.Scrollbar(tabla_frame, orient="horizontal", command=tabla.xview)

        tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        tabla.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        tabla_frame.rowconfigure(0, weight=1)
        tabla_frame.columnconfigure(0, weight=1)
