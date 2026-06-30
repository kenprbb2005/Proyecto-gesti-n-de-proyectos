from tkinter import ttk
from utils.ui import page, card, money


class PedidosView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Main.TFrame")
        self.controller = controller
        root = page(self, "Pedidos", "Aquí se registran los pedidos procesados desde el carrito. Desde esta tabla se pasan a pagos.")

        form = card(root, padding=14)
        form.pack(fill="x", pady=(0, 12))
        self.id_pedido = ttk.Entry(form, width=30)
        self.estado = ttk.Combobox(form, values=["Pendiente", "Pagado", "Preparando", "Enviado", "Entregado", "Cancelado"], state="readonly", width=27)
        self.estado.set("Pendiente")
        ttk.Label(form, text="ID pedido", style="Field.TLabel").grid(row=0, column=0, padx=8, sticky="w")
        self.id_pedido.grid(row=1, column=0, padx=8, pady=(2,8), sticky="ew")
        ttk.Label(form, text="Nuevo estado", style="Field.TLabel").grid(row=0, column=1, padx=8, sticky="w")
        self.estado.grid(row=1, column=1, padx=8, pady=(2,8), sticky="ew")
        self.detalle_lbl = ttk.Label(form, text="Seleccione un pedido para ver el detalle.", wraplength=560)
        self.detalle_lbl.grid(row=0, column=2, rowspan=2, padx=8, sticky="w")
        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)
        form.columnconfigure(2, weight=2)

        buttons = ttk.Frame(root, style="Main.TFrame")
        buttons.pack(fill="x", pady=(0, 12))
        ttk.Button(buttons, text="Enviar a proceso de pago", style="Success.TButton", command=self.controller.go_to_payment).pack(side="left", padx=4)
        ttk.Button(buttons, text="Cambiar estado", style="Primary.TButton", command=self.controller.change_status).pack(side="left", padx=4)
        ttk.Button(buttons, text="Cancelar pedido", style="Danger.TButton", command=self.controller.cancel_order).pack(side="left", padx=4)
        ttk.Button(buttons, text="Actualizar", command=self.controller.load_orders).pack(side="left", padx=4)

        table_card = card(root, padding=12)
        table_card.pack(fill="both", expand=True)
        table_area = ttk.Frame(table_card, style="Card.TFrame")
        table_area.pack(fill="both", expand=True)
        self.tabla = ttk.Treeview(
            table_area,
            columns=("id", "usuario", "cantidad", "items", "subtotal", "iva", "envio", "total", "estado", "fecha"),
            show="headings",
        )
        headers = {
            "id": "ID pedido",
            "usuario": "Usuario",
            "cantidad": "Cant.",
            "items": "Productos",
            "subtotal": "Subtotal",
            "iva": "IVA",
            "envio": "Envío",
            "total": "Total",
            "estado": "Estado",
            "fecha": "Fecha",
        }
        for col, text in headers.items():
            self.tabla.heading(col, text=text)
            self.tabla.column(col, width=120)
        self.tabla.column("items", width=280)
        self.tabla.column("cantidad", width=70, anchor="center")
        self.tabla.column("id", width=110)
        scroll_y = ttk.Scrollbar(table_area, orient="vertical", command=self.tabla.yview)
        scroll_x = ttk.Scrollbar(table_area, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.tabla.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        table_area.rowconfigure(0, weight=1)
        table_area.columnconfigure(0, weight=1)
        self.tabla.bind("<<TreeviewSelect>>", lambda e: self.controller.fill_from_selection())

    def set_detail(self, pedido):
        productos = ", ".join([f"{item.get('nombre', 'Producto')} x{item.get('cantidad', 1)}" for item in pedido.items])
        self.detalle_lbl.config(
            text=(
                f"Pedido {pedido.id_pedido} | Estado: {pedido.estado} | "
                f"Total: {money(pedido.total)} | Envío: {pedido.canton_envio}.\n"
                f"Productos: {productos or '-'}"
            )
        )
