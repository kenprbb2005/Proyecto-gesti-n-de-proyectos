from tkinter import ttk
from utils.ui import page, card, money


class CarritoView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Main.TFrame")
        self.controller = controller

        root = page(
            self,
            "Carrito de compras",
            "Selecciona productos del catálogo, márcalos aquí y procesa un pedido. El pago se realiza después desde Pedidos/Pagos.",
        )

        top = ttk.Frame(root, style="Main.TFrame")
        top.pack(fill="x", pady=(0, 12))
        ttk.Button(top, text="Volver al catálogo", command=self.controller.go_to_catalogo).pack(side="right", padx=4)
        ttk.Button(top, text="Vaciar carrito", style="Danger.TButton", command=self.controller.empty_cart).pack(side="right", padx=4)

        body = ttk.Frame(root, style="Main.TFrame")
        body.pack(fill="both", expand=True)

        left = card(body, padding=12)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))

        ttk.Label(
            left,
            text="Doble clic sobre un producto para marcarlo o quitarlo del pedido.",
            style="Field.TLabel",
        ).pack(anchor="w", pady=(0, 8))

        table_area = ttk.Frame(left, style="Card.TFrame")
        table_area.pack(fill="both", expand=True)

        self.tabla = ttk.Treeview(
            table_area,
            columns=("comprar", "id", "producto", "cantidad", "precio", "subtotal", "estado_stock"),
            show="headings",
            selectmode="extended",
        )
        encabezados = {
            "comprar": "Pedido",
            "id": "ID producto",
            "producto": "Producto",
            "cantidad": "Cantidad",
            "precio": "Precio",
            "subtotal": "Subtotal",
            "estado_stock": "Estado stock",
        }
        for col, text in encabezados.items():
            self.tabla.heading(col, text=text)
            self.tabla.column(col, width=120)
        self.tabla.column("comprar", width=80, anchor="center")
        self.tabla.column("id", width=110)
        self.tabla.column("producto", width=260)
        self.tabla.column("cantidad", width=90, anchor="center")
        self.tabla.column("estado_stock", width=160)

        scroll_y = ttk.Scrollbar(table_area, orient="vertical", command=self.tabla.yview)
        scroll_x = ttk.Scrollbar(table_area, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.tabla.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        table_area.rowconfigure(0, weight=1)
        table_area.columnconfigure(0, weight=1)

        self.tabla.bind("<Double-1>", self.controller.toggle_selected_purchase_event)
        self.tabla.bind("<space>", self.controller.toggle_selected_purchase_event)

        buttons = ttk.Frame(left, style="Card.TFrame")
        buttons.pack(fill="x", pady=(10, 0))
        ttk.Button(buttons, text="+1", command=lambda: self.controller.change_quantity(1)).pack(side="left", padx=4)
        ttk.Button(buttons, text="-1", command=lambda: self.controller.change_quantity(-1)).pack(side="left", padx=4)
        ttk.Button(buttons, text="Eliminar producto", style="Danger.TButton", command=self.controller.remove_item).pack(side="left", padx=4)

        select_buttons = ttk.Frame(left, style="Card.TFrame")
        select_buttons.pack(fill="x", pady=(8, 0))
        ttk.Button(select_buttons, text="Incluir seleccionado", style="Success.TButton", command=lambda: self.controller.mark_selected_for_purchase(True)).pack(side="left", padx=4)
        ttk.Button(select_buttons, text="No incluir seleccionado", command=lambda: self.controller.mark_selected_for_purchase(False)).pack(side="left", padx=4)
        ttk.Button(select_buttons, text="Incluir todos", command=lambda: self.controller.mark_all_for_purchase(True)).pack(side="left", padx=4)
        ttk.Button(select_buttons, text="No incluir todos", command=lambda: self.controller.mark_all_for_purchase(False)).pack(side="left", padx=4)

        right = card(body, padding=16)
        right.pack(side="right", fill="y")
        ttk.Label(right, text="Resumen del pedido", style="Title.TLabel").pack(anchor="w", pady=(0, 12))

        self.info_lbl = ttk.Label(right, text="Carrito: 0 productos | Para pedido: 0")
        self.info_lbl.pack(anchor="w", pady=5)
        self.subtotal_lbl = ttk.Label(right, text="Subtotal: ₡0.00")
        self.subtotal_lbl.pack(anchor="w", pady=5)
        self.impuesto_lbl = ttk.Label(right, text="IVA 13%: ₡0.00")
        self.impuesto_lbl.pack(anchor="w", pady=5)

        ttk.Label(right, text="Provincia de envío", style="Field.TLabel").pack(anchor="w", pady=(14, 0))
        self.canton = ttk.Combobox(
            right,
            values=["San José", "Alajuela", "Cartago", "Heredia", "Guanacaste", "Puntarenas", "Limón"],
            width=28,
            state="readonly",
        )
        self.canton.set("San José")
        self.canton.pack(anchor="w", pady=5)
        self.canton.bind("<<ComboboxSelected>>", lambda e: self.controller.load_cart())

        ttk.Label(right, text="Dirección exacta", style="Field.TLabel").pack(anchor="w", pady=(8, 0))
        self.direccion = ttk.Entry(right, width=34)
        self.direccion.pack(anchor="w", pady=5)

        self.envio_lbl = ttk.Label(right, text="Envío: ₡0.00")
        self.envio_lbl.pack(anchor="w", pady=5)
        self.total_lbl = ttk.Label(right, text="Total del pedido: ₡0.00", font=("Segoe UI", 16, "bold"))
        self.total_lbl.pack(anchor="w", pady=(18, 8))

        ttk.Label(
            right,
            text="Regla de negocio: este botón NO cobra. Registra el pedido en la tabla Pedidos; el cobro se hace después en Pagos.",
            wraplength=270,
        ).pack(anchor="w", pady=(0, 8))

        ttk.Button(right, text="Procesar pedido", style="Success.TButton", command=self.controller.procesar_pedido).pack(fill="x", pady=5)

    def set_totals(self, subtotal, impuesto, envio, total, cantidad_seleccionada=0, cantidad_carrito=0):
        self.info_lbl.config(text=f"Carrito: {cantidad_carrito} productos | Para pedido: {cantidad_seleccionada}")
        self.subtotal_lbl.config(text=f"Subtotal: {money(subtotal)}")
        self.impuesto_lbl.config(text=f"IVA 13%: {money(impuesto)}")
        self.envio_lbl.config(text=f"Envío: {money(envio)}")
        self.total_lbl.config(text=f"Total del pedido: {money(total)}")
