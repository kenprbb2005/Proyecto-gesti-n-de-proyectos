from tkinter import ttk
from utils.ui import page, card


class InventarioView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Main.TFrame")
        self.controller = controller
        root = page(self, "Inventario", "Entradas, salidas y ajustes de stock con control de existencias.")
        form = card(root, padding=14); form.pack(fill="x", pady=(0, 12))
        self.producto = ttk.Combobox(form, values=[], state="readonly", width=36)
        self.tipo = ttk.Combobox(form, values=["Entrada", "Salida", "Ajuste"], state="readonly", width=24); self.tipo.set("Entrada")
        self.cantidad = ttk.Entry(form, width=24)
        self.motivo = ttk.Entry(form, width=70)
        fields = [("Producto", self.producto), ("Tipo", self.tipo), ("Cantidad", self.cantidad)]
        for i, (label, widget) in enumerate(fields):
            ttk.Label(form, text=label, style="Field.TLabel").grid(row=0, column=i, padx=8, pady=(4,0), sticky="w")
            widget.grid(row=1, column=i, padx=8, pady=(2,8), sticky="ew")
        ttk.Label(form, text="Motivo", style="Field.TLabel").grid(row=2, column=0, padx=8, sticky="w")
        self.motivo.grid(row=3, column=0, columnspan=3, padx=8, pady=(2,8), sticky="ew")
        for i in range(3): form.columnconfigure(i, weight=1)
        buttons = ttk.Frame(root, style="Main.TFrame"); buttons.pack(fill="x", pady=(0, 12))
        ttk.Button(buttons, text="Registrar movimiento", style="Success.TButton", command=self.controller.create_movement).pack(side="left", padx=4)
        ttk.Button(buttons, text="Actualizar", style="Primary.TButton", command=self.controller.load_movements).pack(side="left", padx=4)
        ttk.Button(buttons, text="Limpiar", command=self.controller.clear_form).pack(side="left", padx=4)
        table_card = card(root, padding=12); table_card.pack(fill="both", expand=True)
        self.tabla = ttk.Treeview(table_card, columns=("id", "producto", "tipo", "cantidad", "anterior", "nuevo", "motivo", "fecha"), show="headings")
        headers = {"id":"ID", "producto":"ID producto", "tipo":"Tipo", "cantidad":"Cantidad", "anterior":"Anterior", "nuevo":"Nuevo", "motivo":"Motivo", "fecha":"Fecha"}
        for col, text in headers.items(): self.tabla.heading(col, text=text); self.tabla.column(col, width=120)
        self.tabla.column("motivo", width=260)
        self.tabla.pack(fill="both", expand=True)
