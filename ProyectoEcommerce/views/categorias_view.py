from tkinter import ttk
from utils.ui import page, card


class CategoriasView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Main.TFrame")
        self.controller = controller
        root = page(self, "Categorías", "Clasificación de productos y control de categorías activas.")
        form = card(root, padding=14); form.pack(fill="x", pady=(0, 12))
        self.id_categoria = ttk.Entry(form, width=30)
        self.nombre = ttk.Entry(form, width=30)
        self.estado = ttk.Combobox(form, values=["Activa", "Inactiva"], state="readonly", width=27); self.estado.set("Activa")
        self.descripcion = ttk.Entry(form, width=80)
        fields = [("ID", self.id_categoria), ("Nombre", self.nombre), ("Estado", self.estado)]
        for i, (label, widget) in enumerate(fields):
            ttk.Label(form, text=label, style="Field.TLabel").grid(row=0, column=i, padx=8, pady=(4,0), sticky="w")
            widget.grid(row=1, column=i, padx=8, pady=(2,8), sticky="ew")
        ttk.Label(form, text="Descripción", style="Field.TLabel").grid(row=2, column=0, padx=8, sticky="w")
        self.descripcion.grid(row=3, column=0, columnspan=3, padx=8, pady=(2, 8), sticky="ew")
        for i in range(3): form.columnconfigure(i, weight=1)
        buttons = ttk.Frame(root, style="Main.TFrame"); buttons.pack(fill="x", pady=(0, 12))
        ttk.Button(buttons, text="Registrar", style="Success.TButton", command=self.controller.create_category).pack(side="left", padx=4)
        ttk.Button(buttons, text="Guardar cambios", style="Primary.TButton", command=self.controller.update_category).pack(side="left", padx=4)
        ttk.Button(buttons, text="Eliminar", style="Danger.TButton", command=self.controller.delete_category).pack(side="left", padx=4)
        ttk.Button(buttons, text="Limpiar", command=self.controller.clear_form).pack(side="left", padx=4)
        ttk.Label(buttons, text="Buscar:", background="#eef2f7").pack(side="left", padx=(25,4))
        self.buscar = ttk.Entry(buttons, width=30); self.buscar.pack(side="left")
        ttk.Button(buttons, text="Buscar", command=self.controller.search_categories).pack(side="left", padx=4)
        table_card = card(root, padding=12); table_card.pack(fill="both", expand=True)
        self.tabla = ttk.Treeview(table_card, columns=("id", "nombre", "descripcion", "estado", "fecha"), show="headings")
        for col, text in {"id":"ID", "nombre":"Nombre", "descripcion":"Descripción", "estado":"Estado", "fecha":"Creación"}.items():
            self.tabla.heading(col, text=text); self.tabla.column(col, width=150)
        self.tabla.column("descripcion", width=360)
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", lambda e: self.controller.fill_form_from_selection())
