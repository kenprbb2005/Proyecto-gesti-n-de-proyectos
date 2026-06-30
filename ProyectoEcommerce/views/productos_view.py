from tkinter import ttk
from utils.ui import page, card


class ProductosView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Main.TFrame")
        self.controller = controller
        root = page(self, "Catálogo de productos", "Registro, edición y consulta administrativa. También permite agregar productos al carrito.")
        form = card(root, padding=14)
        form.pack(fill="x", pady=(0, 12))
        self.id_producto = ttk.Entry(form, width=24)
        self.nombre = ttk.Entry(form, width=24)
        self.categoria = ttk.Combobox(form, values=[], state="readonly", width=24)
        self.marca = ttk.Entry(form, width=24)
        self.precio = ttk.Entry(form, width=24)
        self.stock = ttk.Entry(form, width=24)
        self.stock_minimo = ttk.Entry(form, width=24)
        self.estado = ttk.Combobox(form, values=["Disponible", "Agotado", "Inactivo"], state="readonly", width=22)
        self.estado.set("Disponible")
        self.descripcion = ttk.Entry(form, width=90)
        fields = [("ID", self.id_producto), ("Nombre", self.nombre), ("Categoría", self.categoria), ("Marca", self.marca), ("Precio", self.precio), ("Stock", self.stock), ("Stock mínimo", self.stock_minimo), ("Estado", self.estado)]
        for i, (label, widget) in enumerate(fields):
            ttk.Label(form, text=label, style="Field.TLabel").grid(row=(i//4)*2, column=i%4, padx=8, pady=(4,0), sticky="w")
            widget.grid(row=(i//4)*2+1, column=i%4, padx=8, pady=(2,8), sticky="ew")
        ttk.Label(form, text="Descripción", style="Field.TLabel").grid(row=4, column=0, padx=8, sticky="w")
        self.descripcion.grid(row=5, column=0, columnspan=4, padx=8, pady=(2, 8), sticky="ew")
        for i in range(4):
            form.columnconfigure(i, weight=1)

        buttons = ttk.Frame(root, style="Main.TFrame")
        buttons.pack(fill="x", pady=(0, 12))
        ttk.Button(buttons, text="Registrar", style="Success.TButton", command=self.controller.create_product).pack(side="left", padx=4)
        ttk.Button(buttons, text="Guardar cambios", style="Primary.TButton", command=self.controller.update_product).pack(side="left", padx=4)
        ttk.Button(buttons, text="Eliminar", style="Danger.TButton", command=self.controller.delete_product).pack(side="left", padx=4)
        ttk.Button(buttons, text="Limpiar", command=self.controller.clear_form).pack(side="left", padx=4)
        ttk.Label(buttons, text="Buscar:", background="#eef2f7").pack(side="left", padx=(25,4))
        self.buscar = ttk.Entry(buttons, width=30)
        self.buscar.pack(side="left")
        ttk.Button(buttons, text="Buscar", command=self.controller.search_products).pack(side="left", padx=4)

        cart_buttons = ttk.Frame(root, style="Main.TFrame")
        cart_buttons.pack(fill="x", pady=(0, 12))
        ttk.Label(cart_buttons, text="Cantidad para carrito:", background="#eef2f7").pack(side="left", padx=(0, 4))
        self.cantidad_carrito = ttk.Spinbox(cart_buttons, from_=1, to=99, width=8)
        self.cantidad_carrito.set(1)
        self.cantidad_carrito.pack(side="left", padx=4)
        ttk.Button(cart_buttons, text="Agregar seleccionado al carrito", style="Success.TButton", command=self.controller.add_selected_to_cart).pack(side="left", padx=4)
        ttk.Button(cart_buttons, text="Agregar y abrir carrito", style="Primary.TButton", command=self.controller.add_selected_to_cart_and_open).pack(side="left", padx=4)

        table_card = card(root, padding=12)
        table_card.pack(fill="both", expand=True)
        table_area = ttk.Frame(table_card, style="Card.TFrame")
        table_area.pack(fill="both", expand=True)
        self.tabla = ttk.Treeview(table_area, columns=("id", "nombre", "categoria", "marca", "precio", "stock", "minimo", "estado"), show="headings")
        headers = {"id":"ID", "nombre":"Producto", "categoria":"Categoría", "marca":"Marca", "precio":"Precio", "stock":"Stock", "minimo":"Mínimo", "estado":"Estado"}
        for col, text in headers.items():
            self.tabla.heading(col, text=text)
            self.tabla.column(col, width=120)
        self.tabla.column("nombre", width=230)
        scroll_y = ttk.Scrollbar(table_area, orient="vertical", command=self.tabla.yview)
        scroll_x = ttk.Scrollbar(table_area, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.tabla.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        table_area.rowconfigure(0, weight=1)
        table_area.columnconfigure(0, weight=1)
        self.tabla.bind("<<TreeviewSelect>>", lambda e: self.controller.fill_form_from_selection())
