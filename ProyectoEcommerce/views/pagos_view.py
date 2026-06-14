import tkinter as tk
from tkinter import ttk

class PagosView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="TFrame")
        self.controller = controller
        
        header = ttk.Frame(self)
        header.pack(fill="x", padx=25, pady=(20, 10))

        ttk.Label(header, text="Módulo de Pagos", style="Title.TLabel").pack(anchor="w")

        card = ttk.Frame(self, style="Card.TFrame")
        card.pack(fill="x", padx=25, pady=10)

        campos = [
            ("ID Pago", 0, 0),
            ("ID Compra", 0, 2),
            ("Monto", 1, 0),
            ("Fecha de pago", 1, 2),
        ]

        for texto, fila, columna in campos:
            ttk.Label(card, text=texto).grid(row=fila, column=columna, padx=15, pady=12, sticky="w")
            ttk.Entry(card, width=32).grid(row=fila, column=columna + 1, padx=15, pady=12)

        ttk.Label(card, text="Método de pago").grid(row=2, column=0, padx=15, pady=12, sticky="w")
        ttk.Combobox(card, values=["Tarjeta", "SINPE Móvil", "Transferencia", "Efectivo"], width=30).grid(row=2, column=1, padx=15, pady=12)

        ttk.Label(card, text="Estado").grid(row=2, column=2, padx=15, pady=12, sticky="w")
        ttk.Combobox(card, values=["Pendiente", "Pagado", "Rechazado", "Cancelado"], width=30).grid(row=2, column=3, padx=15, pady=12)

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
            columns=("id_pago", "id_compra", "metodo", "monto", "fecha", "estado"),
            show="headings"
        )

        encabezados = {
            "id_pago": "ID Pago",
            "id_compra": "ID Compra",
            "metodo": "Método de pago",
            "monto": "Monto",
            "fecha": "Fecha de pago",
            "estado": "Estado"
        }

        for columna, texto in encabezados.items():
            tabla.heading(columna, text=texto)
            tabla.column(columna, width=150)

        scroll = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scroll.set)

        tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
