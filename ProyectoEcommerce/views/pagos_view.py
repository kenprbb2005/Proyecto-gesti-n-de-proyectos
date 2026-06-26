from tkinter import ttk
from utils.ui import page, card


class PagosView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Main.TFrame")
        self.controller = controller
        root = page(self, "Pagos simulados", "Procesamiento académico de pagos: aprobación, rechazo y anulación.")
        form = card(root, padding=14); form.pack(fill="x", pady=(0, 12))
        self.id_pedido = ttk.Entry(form, width=30)
        self.metodo = ttk.Combobox(form, values=["Tarjeta", "SINPE Móvil", "Transferencia", "Efectivo"], state="readonly", width=27); self.metodo.set("Tarjeta")
        self.monto = ttk.Entry(form, width=30)
        self.referencia = ttk.Entry(form, width=30)
        fields = [("ID pedido", self.id_pedido), ("Método", self.metodo), ("Monto exacto", self.monto), ("Referencia", self.referencia)]
        for i, (label, widget) in enumerate(fields):
            ttk.Label(form, text=label, style="Field.TLabel").grid(row=0, column=i, padx=8, sticky="w")
            widget.grid(row=1, column=i, padx=8, pady=(2,8), sticky="ew")
        for i in range(4): form.columnconfigure(i, weight=1)
        buttons = ttk.Frame(root, style="Main.TFrame"); buttons.pack(fill="x", pady=(0, 12))
        ttk.Button(buttons, text="Procesar pago", style="Success.TButton", command=self.controller.process_payment).pack(side="left", padx=4)
        ttk.Button(buttons, text="Anular pago", style="Danger.TButton", command=self.controller.cancel_payment).pack(side="left", padx=4)
        ttk.Button(buttons, text="Actualizar", command=self.controller.load_payments).pack(side="left", padx=4)
        table_card = card(root, padding=12); table_card.pack(fill="both", expand=True)
        self.tabla = ttk.Treeview(table_card, columns=("id", "pedido", "usuario", "metodo", "monto", "estado", "referencia", "fecha"), show="headings")
        headers = {"id":"ID pago", "pedido":"Pedido", "usuario":"Usuario", "metodo":"Método", "monto":"Monto", "estado":"Estado", "referencia":"Referencia", "fecha":"Fecha"}
        for col, text in headers.items(): self.tabla.heading(col, text=text); self.tabla.column(col, width=130)
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", lambda e: self.controller.fill_from_selection())
