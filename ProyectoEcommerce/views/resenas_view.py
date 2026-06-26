from tkinter import ttk
import tkinter as tk
from utils.ui import page, card


class ResenasView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Main.TFrame")
        self.controller = controller
        root = page(self, "Reseñas", "Opiniones, calificaciones y moderación de comentarios.")
        form = card(root, padding=14); form.pack(fill="x", pady=(0, 12))
        self.id_resena = ttk.Entry(form, width=24)
        self.id_usuario = ttk.Entry(form, width=24)
        self.producto = ttk.Combobox(form, values=[], state="readonly", width=35)
        self.calificacion = ttk.Combobox(form, values=["1", "2", "3", "4", "5"], state="readonly", width=22); self.calificacion.set("5")
        self.estado = ttk.Combobox(form, values=["Publicada", "Pendiente", "Oculta", "Eliminada"], state="readonly", width=22); self.estado.set("Publicada")
        fields = [("ID reseña", self.id_resena), ("ID usuario", self.id_usuario), ("Producto", self.producto), ("Calificación", self.calificacion), ("Estado", self.estado)]
        for i, (label, widget) in enumerate(fields):
            ttk.Label(form, text=label, style="Field.TLabel").grid(row=0, column=i, padx=8, sticky="w")
            widget.grid(row=1, column=i, padx=8, pady=(2,8), sticky="ew")
        ttk.Label(form, text="Comentario", style="Field.TLabel").grid(row=2, column=0, padx=8, sticky="w")
        self.comentario = tk.Text(form, height=3, font=("Segoe UI", 10))
        self.comentario.grid(row=3, column=0, columnspan=5, padx=8, pady=(2,8), sticky="ew")
        for i in range(5): form.columnconfigure(i, weight=1)
        buttons = ttk.Frame(root, style="Main.TFrame"); buttons.pack(fill="x", pady=(0, 12))
        ttk.Button(buttons, text="Registrar", style="Success.TButton", command=self.controller.create_review).pack(side="left", padx=4)
        ttk.Button(buttons, text="Cambiar estado", style="Primary.TButton", command=self.controller.moderate_review).pack(side="left", padx=4)
        ttk.Button(buttons, text="Eliminar", style="Danger.TButton", command=self.controller.delete_review).pack(side="left", padx=4)
        ttk.Button(buttons, text="Actualizar", command=self.controller.load_reviews).pack(side="left", padx=4)
        table_card = card(root, padding=12); table_card.pack(fill="both", expand=True)
        self.tabla = ttk.Treeview(table_card, columns=("id", "usuario", "producto", "calificacion", "comentario", "estado", "fecha"), show="headings")
        headers = {"id":"ID", "usuario":"Usuario", "producto":"Producto", "calificacion":"Calificación", "comentario":"Comentario", "estado":"Estado", "fecha":"Fecha"}
        for col, text in headers.items(): self.tabla.heading(col, text=text); self.tabla.column(col, width=130)
        self.tabla.column("comentario", width=350)
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", lambda e: self.controller.fill_from_selection())
