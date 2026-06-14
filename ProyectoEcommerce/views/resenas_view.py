import tkinter as tk
from tkinter import ttk

class ResenasView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Main.TFrame")
        self.controller = controller
        
        contenedor = ttk.Frame(self, style="Main.TFrame")
        contenedor.pack(fill="both", expand=True, padx=30, pady=25)

        ttk.Label(contenedor, text="Módulo de Reseñas", style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            contenedor,
            text="Gestión visual de opiniones, calificaciones y comentarios de productos.",
            style="Subheader.TLabel"
        ).pack(anchor="w", pady=(0, 20))

        formulario = ttk.Frame(contenedor, style="Card.TFrame")
        formulario.pack(fill="x", pady=10)

        campos = [
            ("ID Reseña", 0, 0),
            ("ID Usuario", 0, 2),
            ("ID Producto", 1, 0),
            ("Fecha", 1, 2),
        ]

        for texto, fila, columna in campos:
            ttk.Label(formulario, text=texto, style="Field.TLabel").grid(row=fila, column=columna, padx=18, pady=14, sticky="w")
            ttk.Entry(formulario, width=34).grid(row=fila, column=columna + 1, padx=18, pady=14)

        ttk.Label(formulario, text="Calificación", style="Field.TLabel").grid(row=2, column=0, padx=18, pady=14, sticky="w")
        ttk.Combobox(
            formulario,
            values=["1 estrella", "2 estrellas", "3 estrellas", "4 estrellas", "5 estrellas"],
            width=31
        ).grid(row=2, column=1, padx=18, pady=14)

        ttk.Label(formulario, text="Estado", style="Field.TLabel").grid(row=2, column=2, padx=18, pady=14, sticky="w")
        ttk.Combobox(
            formulario,
            values=["Publicada", "Pendiente", "Oculta", "Eliminada"],
            width=31
        ).grid(row=2, column=3, padx=18, pady=14)

        ttk.Label(formulario, text="Comentario", style="Field.TLabel").grid(row=3, column=0, padx=18, pady=14, sticky="nw")
        comentario = tk.Text(formulario, width=86, height=4, font=("Segoe UI", 10), relief="solid", bd=1)
        comentario.grid(row=3, column=1, columnspan=3, padx=18, pady=14, sticky="w")

        botones = ttk.Frame(contenedor, style="Main.TFrame")
        botones.pack(fill="x", pady=15)

        ttk.Button(botones, text="Registrar reseña").pack(side="left", padx=5)
        ttk.Button(botones, text="Editar reseña").pack(side="left", padx=5)
        ttk.Button(botones, text="Eliminar reseña").pack(side="left", padx=5)
        ttk.Button(botones, text="Buscar reseña").pack(side="left", padx=5)
        ttk.Button(botones, text="Limpiar campos").pack(side="left", padx=5)

        tabla_frame = ttk.Frame(contenedor, style="Card.TFrame")
        tabla_frame.pack(fill="both", expand=True, pady=10)

        tabla = ttk.Treeview(
            tabla_frame,
            columns=("id_resena", "id_usuario", "id_producto", "calificacion", "comentario", "fecha", "estado"),
            show="headings"
        )

        encabezados = {
            "id_resena": "ID Reseña",
            "id_usuario": "ID Usuario",
            "id_producto": "ID Producto",
            "calificacion": "Calificación",
            "comentario": "Comentario",
            "fecha": "Fecha",
            "estado": "Estado"
        }

        for columna, texto in encabezados.items():
            tabla.heading(columna, text=texto)
            tabla.column(columna, width=150)

        tabla.column("comentario", width=280)

        scroll_y = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla.yview)
        scroll_x = ttk.Scrollbar(tabla_frame, orient="horizontal", command=tabla.xview)

        tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        tabla.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        tabla_frame.rowconfigure(0, weight=1)
        tabla_frame.columnconfigure(0, weight=1)
