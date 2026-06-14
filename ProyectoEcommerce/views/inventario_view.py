import tkinter as tk
from tkinter import ttk

class InventarioView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Main.TFrame")
        self.controller = controller
        
        contenedor = ttk.Frame(self, style="Main.TFrame")
        contenedor.pack(fill="both", expand=True, padx=30, pady=25)

        ttk.Label(contenedor, text="Módulo de Inventario", style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            contenedor,
            text="Control visual de existencias, entradas, salidas y estado del stock.",
            style="Subheader.TLabel"
        ).pack(anchor="w", pady=(0, 20))

        formulario = ttk.Frame(contenedor, style="Card.TFrame")
        formulario.pack(fill="x", pady=10)

        campos = [
            ("ID Inventario", 0, 0),
            ("ID Producto", 0, 2),
            ("Nombre del producto", 1, 0),
            ("Cantidad disponible", 1, 2),
            ("Stock mínimo", 2, 0),
            ("Fecha actualización", 2, 2),
        ]

        for texto, fila, columna in campos:
            ttk.Label(formulario, text=texto, style="Field.TLabel").grid(row=fila, column=columna, padx=18, pady=14, sticky="w")
            ttk.Entry(formulario, width=34).grid(row=fila, column=columna + 1, padx=18, pady=14)

        ttk.Label(formulario, text="Categoría", style="Field.TLabel").grid(row=3, column=0, padx=18, pady=14, sticky="w")
        ttk.Combobox(
            formulario,
            values=["Tecnología", "Ropa", "Hogar", "Librería", "Alimentos", "Otros"],
            width=31
        ).grid(row=3, column=1, padx=18, pady=14)

        ttk.Label(formulario, text="Estado de stock", style="Field.TLabel").grid(row=3, column=2, padx=18, pady=14, sticky="w")
        ttk.Combobox(
            formulario,
            values=["Disponible", "Bajo stock", "Agotado", "Inactivo"],
            width=31
        ).grid(row=3, column=3, padx=18, pady=14)

        botones = ttk.Frame(contenedor, style="Main.TFrame")
        botones.pack(fill="x", pady=15)

        ttk.Button(botones, text="Registrar producto").pack(side="left", padx=5)
        ttk.Button(botones, text="Actualizar stock").pack(side="left", padx=5)
        ttk.Button(botones, text="Eliminar registro").pack(side="left", padx=5)
        ttk.Button(botones, text="Buscar producto").pack(side="left", padx=5)
        ttk.Button(botones, text="Limpiar campos").pack(side="left", padx=5)

        tabla_frame = ttk.Frame(contenedor, style="Card.TFrame")
        tabla_frame.pack(fill="both", expand=True, pady=10)

        tabla = ttk.Treeview(
            tabla_frame,
            columns=("id_inventario", "id_producto", "producto", "categoria", "cantidad", "stock_minimo", "fecha", "estado"),
            show="headings"
        )

        encabezados = {
            "id_inventario": "ID Inventario",
            "id_producto": "ID Producto",
            "producto": "Producto",
            "categoria": "Categoría",
            "cantidad": "Cantidad",
            "stock_minimo": "Stock mínimo",
            "fecha": "Fecha actualización",
            "estado": "Estado"
        }

        for columna, texto in encabezados.items():
            tabla.heading(columna, text=texto)
            tabla.column(columna, width=145)

        tabla.column("producto", width=230)

        scroll_y = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla.yview)
        scroll_x = ttk.Scrollbar(tabla_frame, orient="horizontal", command=tabla.xview)

        tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        tabla.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        tabla_frame.rowconfigure(0, weight=1)
        tabla_frame.columnconfigure(0, weight=1)
