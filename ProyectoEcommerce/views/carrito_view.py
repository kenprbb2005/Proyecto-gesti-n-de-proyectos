from tkinter import ttk
from utils.ui import page, card, money


class CarritoView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Main.TFrame")
        self.controller = controller

        root = page(
            self,
            "Carrito de compras",
            "Marca los productos que sí quieres comprar ahora. Los no marcados quedan guardados para después.",
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
            text="Doble clic sobre un producto para marcarlo o quitarlo de la compra.",
            style="Field.TLabel",
        ).pack(anchor="w", pady=(0, 8))

        self.tabla = ttk.Treeview(
            left,
            columns=("comprar", "id", "producto", "cantidad", "precio", "subtotal"),
            show="headings",
            selectmode="extended",
        )
        encabezados = {
            "comprar": "Comprar",
            "id": "ID producto",
            "producto": "Producto",
            "cantidad": "Cantidad",
            "precio": "Precio",
            "subtotal": "Subtotal",
        }
        for col, text in encabezados.items():
            self.tabla.heading(col, text=text)
            self.tabla.column(col, width=120)
        self.tabla.column("comprar", width=80, anchor="center")
        self.tabla.column("id", width=110)
        self.tabla.column("producto", width=260)
        self.tabla.column("cantidad", width=90, anchor="center")
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<Double-1>", self.controller.toggle_selected_purchase_event)
        self.tabla.bind("<space>", self.controller.toggle_selected_purchase_event)

        buttons = ttk.Frame(left, style="Card.TFrame")
        buttons.pack(fill="x", pady=(10, 0))
        ttk.Button(buttons, text="+1", command=lambda: self.controller.change_quantity(1)).pack(side="left", padx=4)
        ttk.Button(buttons, text="-1", command=lambda: self.controller.change_quantity(-1)).pack(side="left", padx=4)
        ttk.Button(buttons, text="Eliminar producto", style="Danger.TButton", command=self.controller.remove_item).pack(side="left", padx=4)

        select_buttons = ttk.Frame(left, style="Card.TFrame")
        select_buttons.pack(fill="x", pady=(8, 0))
        ttk.Button(select_buttons, text="Marcar seleccionado", style="Success.TButton", command=lambda: self.controller.mark_selected_for_purchase(True)).pack(side="left", padx=4)
        ttk.Button(select_buttons, text="Quitar seleccionado", command=lambda: self.controller.mark_selected_for_purchase(False)).pack(side="left", padx=4)
        ttk.Button(select_buttons, text="Marcar todos", command=lambda: self.controller.mark_all_for_purchase(True)).pack(side="left", padx=4)
        ttk.Button(select_buttons, text="Quitar todos", command=lambda: self.controller.mark_all_for_purchase(False)).pack(side="left", padx=4)

        right = card(body, padding=16)
        right.pack(side="right", fill="y")
        ttk.Label(right, text="Resumen de productos marcados", style="Title.TLabel").pack(anchor="w", pady=(0, 12))

        self.info_lbl = ttk.Label(right, text="Productos seleccionados: 0")
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

        ttk.Label(right, text="Método de pago simulado", style="Field.TLabel").pack(anchor="w", pady=(8, 0))
        self.metodo_pago = ttk.Combobox(
            right,
            values=["Tarjeta", "SINPE Móvil", "Transferencia", "Efectivo"],
            width=28,
            state="readonly",
        )
        self.metodo_pago.set("SINPE Móvil")
        self.metodo_pago.pack(anchor="w", pady=5)

        ttk.Label(right, text="Referencia del pago", style="Field.TLabel").pack(anchor="w", pady=(8, 0))
        self.referencia_pago = ttk.Entry(right, width=34)
        self.referencia_pago.insert(0, "SIMULADO-001")
        self.referencia_pago.pack(anchor="w", pady=5)
        ttk.Label(
            right,
            text="Nota: si la referencia termina en 0000, el pago se rechaza para probar la regla de negocio.",
            wraplength=260,
        ).pack(anchor="w", pady=(2, 8))

        self.envio_lbl = ttk.Label(right, text="Envío: ₡0.00")
        self.envio_lbl.pack(anchor="w", pady=5)
        self.total_lbl = ttk.Label(right, text="Total: ₡0.00", font=("Segoe UI", 16, "bold"))
        self.total_lbl.pack(anchor="w", pady=(18, 8))

        ttk.Button(right, text="Comprar productos marcados", style="Success.TButton", command=self.controller.checkout_and_pay).pack(fill="x", pady=5)
        ttk.Button(right, text="Crear pedido con productos marcados", style="Primary.TButton", command=self.controller.checkout).pack(fill="x", pady=5)

    def set_totals(self, subtotal, impuesto, envio, total, cantidad_seleccionada=0):
        self.info_lbl.config(text=f"Productos seleccionados: {cantidad_seleccionada}")
        self.subtotal_lbl.config(text=f"Subtotal: {money(subtotal)}")
        self.impuesto_lbl.config(text=f"IVA 13%: {money(impuesto)}")
        self.envio_lbl.config(text=f"Envío: {money(envio)}")
        self.total_lbl.config(text=f"Total: {money(total)}")

        



