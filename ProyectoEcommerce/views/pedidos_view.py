from tkinter import ttk
from utils.ui import page, card


class PedidosView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Main.TFrame")
        self.controller = controller
        root = page(self, "Órdenes / pedidos", "Seguimiento de pedidos, estados y cancelaciones.")
        form = card(root, padding=14); form.pack(fill="x", pady=(0, 12))
        self.id_pedido = ttk.Entry(form, width=30)
        self.estado = ttk.Combobox(form, values=["Pendiente", "Pagado", "Preparando", "Enviado", "Entregado", "Cancelado"], state="readonly", width=27); self.estado.set("Pendiente")
        ttk.Label(form, text="ID pedido", style="Field.TLabel").grid(row=0, column=0, padx=8, sticky="w")
        self.id_pedido.grid(row=1, column=0, padx=8, pady=(2,8), sticky="ew")
        ttk.Label(form, text="Nuevo estado", style="Field.TLabel").grid(row=0, column=1, padx=8, sticky="w")
        self.estado.grid(row=1, column=1, padx=8, pady=(2,8), sticky="ew")
        form.columnconfigure(0, weight=1); form.columnconfigure(1, weight=1)
        buttons = ttk.Frame(root, style="Main.TFrame"); buttons.pack(fill="x", pady=(0, 12))
        ttk.Button(buttons, text="Cambiar estado", style="Primary.TButton", command=self.controller.change_status).pack(side="left", padx=4)
        ttk.Button(buttons, text="Cancelar pedido", style="Danger.TButton", command=self.controller.cancel_order).pack(side="left", padx=4)
        ttk.Button(buttons, text="Actualizar", command=self.controller.load_orders).pack(side="left", padx=4)
        table_card = card(root, padding=12); table_card.pack(fill="both", expand=True)
        self.tabla = ttk.Treeview(table_card, columns=("id", "usuario", "subtotal", "iva", "envio", "total", "estado", "fecha"), show="headings")
        headers = {"id":"ID pedido", "usuario":"Usuario", "subtotal":"Subtotal", "iva":"IVA", "envio":"Envío", "total":"Total", "estado":"Estado", "fecha":"Fecha"}
        for col, text in headers.items(): self.tabla.heading(col, text=text); self.tabla.column(col, width=130)
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", lambda e: self.controller.fill_from_selection())
