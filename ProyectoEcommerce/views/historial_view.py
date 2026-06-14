import tkinter as tk
from tkinter import ttk

class HistorialView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="TFrame")
        self.controller = controller
        
        header = ttk.Frame(self)
        header.pack(fill="x", padx=25, pady=(20, 10))

        ttk.Label(header, text="Historial de Compras", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="Consulta visual del historial de compras realizadas por los usuarios.", style="Subtitle.TLabel").pack(anchor="w")

        card = ttk.Frame(self, style="Card.TFrame")
        card.pack(fill="x", padx=25, pady=10)

        campos = [
            ("ID Historial", 0, 0),
            ("ID Usuario", 0, 2),
            ("ID Compra", 1, 0),
            ("Acción", 1, 2),
            ("Descripción", 2, 0),
            ("Fecha", 2, 2),
        ]

        for texto, fila, columna in campos:
            ttk.Label(card, text=texto).grid(row=fila, column=columna, padx=15, pady=12, sticky="w")
            ttk.Entry(card, width=32).grid(row=fila, column=columna + 1, padx=15, pady=12)

        botones = ttk.Frame(self)
        botones.pack(fill="x", padx=25, pady=10)

        ttk.Button(botones, text="Registrar").pack(side="left", padx=5)
        ttk.Button(botones, text="Editar").pack(side="left", padx=5)
        ttk.Button(botones, text="Eliminar").pack(side="left", padx=5)
        ttk.Button(botones, text="Buscar").pack(side="left", padx=5)
        ttk.Button(botones, text="Limpiar").pack(side="left", padx=5)

        tabla_frame = ttk.Frame(self)
        tabla_frame.pack(fill="both", expand=True, padx=25, pady=10)

        tabla = ttk.Treeview(
            tabla_frame,
            columns=("id_historial", "id_usuario", "id_compra", "accion", "descripcion", "fecha"),
            show="headings"
        )

        encabezados = {
            "id_historial": "ID Historial",
            "id_usuario": "ID Usuario",
            "id_compra": "ID Compra",
            "accion": "Acción",
            "descripcion": "Descripción",
            "fecha": "Fecha"
        }

        for columna, texto in encabezados.items():
            tabla.heading(columna, text=texto)
            tabla.column(columna, width=160)

        scroll = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scroll.set)

        tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
