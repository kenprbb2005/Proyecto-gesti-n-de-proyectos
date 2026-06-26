from tkinter import ttk
from utils.ui import page, card


class HistorialView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Main.TFrame")
        self.controller = controller
        root = page(self, "Historial de compras", "Registro de acciones, pedidos y trazabilidad de los usuarios.")
        buttons = ttk.Frame(root, style="Main.TFrame"); buttons.pack(fill="x", pady=(0, 12))
        ttk.Button(buttons, text="Actualizar", style="Primary.TButton", command=self.controller.load_history).pack(side="left", padx=4)
        ttk.Label(buttons, text="ID usuario:", background="#eef2f7").pack(side="left", padx=(25,4))
        self.id_usuario = ttk.Entry(buttons, width=30); self.id_usuario.pack(side="left")
        ttk.Button(buttons, text="Filtrar", command=self.controller.filter_by_user).pack(side="left", padx=4)
        table_card = card(root, padding=12); table_card.pack(fill="both", expand=True)
        self.tabla = ttk.Treeview(table_card, columns=("id", "usuario", "pedido", "accion", "descripcion", "fecha"), show="headings")
        headers = {"id":"ID", "usuario":"Usuario", "pedido":"Pedido", "accion":"Acción", "descripcion":"Descripción", "fecha":"Fecha"}
        for col, text in headers.items(): self.tabla.heading(col, text=text); self.tabla.column(col, width=130)
        self.tabla.column("descripcion", width=420)
        self.tabla.pack(fill="both", expand=True)
