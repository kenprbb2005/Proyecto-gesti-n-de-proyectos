from tkinter import ttk
import tkinter as tk
from utils.ui import page, card, money


class CatalogoView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Main.TFrame")
        self.controller = controller
        root = page(self, "Catálogo de productos", "Consulta productos, filtra por categoría y agrega al carrito.")

        header = ttk.Frame(root, style="Main.TFrame")
        header.pack(fill="x", pady=(0, 12))
        ttk.Button(header, text="Iniciar sesión", command=self.controller.go_to_login).pack(side="right", padx=4)
        ttk.Button(header, text="Mi carrito", style="Primary.TButton", command=self.controller.go_to_cart).pack(side="right", padx=4)

        body = ttk.Frame(root, style="Main.TFrame")
        body.pack(fill="both", expand=True)

        filtros = card(body, padding=14)
        filtros.pack(side="left", fill="y", padx=(0, 12))
        ttk.Label(filtros, text="Filtros", style="Title.TLabel").pack(anchor="w", pady=(0, 12))
        ttk.Label(filtros, text="Buscar", style="Field.TLabel").pack(anchor="w")
        self.buscar = ttk.Entry(filtros, width=26)
        self.buscar.pack(pady=(4, 10))
        ttk.Label(filtros, text="Categoría", style="Field.TLabel").pack(anchor="w")
        self.categoria = ttk.Combobox(filtros, values=["Todas"], width=23, state="readonly")
        self.categoria.set("Todas")
        self.categoria.pack(pady=(4, 10))
        ttk.Label(filtros, text="Marca", style="Field.TLabel").pack(anchor="w")
        self.marca = ttk.Combobox(filtros, values=["Todas"], width=23, state="readonly")
        self.marca.set("Todas")
        self.marca.pack(pady=(4, 10))
        ttk.Label(filtros, text="Precio máximo", style="Field.TLabel").pack(anchor="w")
        self.precio_maximo = ttk.Entry(filtros, width=26)
        self.precio_maximo.pack(pady=(4, 14))
        ttk.Button(filtros, text="Aplicar filtros", style="Primary.TButton", command=self.controller.load_products).pack(fill="x", pady=4)
        ttk.Button(filtros, text="Limpiar", command=self.controller.clear_filters).pack(fill="x", pady=4)

        tabla_card = card(body, padding=12)
        tabla_card.pack(side="left", fill="both", expand=True, padx=(0, 12))
        ttk.Label(tabla_card, text="Productos disponibles", style="Title.TLabel").pack(anchor="w", pady=(0, 10))
        self.tabla = ttk.Treeview(tabla_card, columns=("id", "nombre", "categoria", "marca", "precio", "stock"), show="headings")
        encabezados = {"id": "ID", "nombre": "Producto", "categoria": "Categoría", "marca": "Marca", "precio": "Precio", "stock": "Stock"}
        for col, text in encabezados.items():
            self.tabla.heading(col, text=text)
            self.tabla.column(col, width=120)
        self.tabla.column("nombre", width=230)
        self.tabla.column("id", width=90)
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", lambda e: self.controller.show_selected_detail())

        detalle = card(body, padding=14)
        detalle.pack(side="right", fill="y")
        ttk.Label(detalle, text="Detalle", style="Title.TLabel").pack(anchor="w", pady=(0, 12))
        self.detalle_nombre = ttk.Label(detalle, text="Seleccione un producto", wraplength=250)
        self.detalle_nombre.pack(anchor="w", pady=4)
        self.detalle_precio = ttk.Label(detalle, text="Precio: ₡0.00")
        self.detalle_precio.pack(anchor="w", pady=4)
        self.detalle_stock = ttk.Label(detalle, text="Stock: 0")
        self.detalle_stock.pack(anchor="w", pady=4)
        self.detalle_descripcion = ttk.Label(detalle, text="Descripción: -", wraplength=250)
        self.detalle_descripcion.pack(anchor="w", pady=8)
        ttk.Label(detalle, text="Cantidad", style="Field.TLabel").pack(anchor="w", pady=(14, 0))
        self.cantidad = ttk.Spinbox(detalle, from_=1, to=99, width=10)
        self.cantidad.set(1)
        self.cantidad.pack(anchor="w", pady=5)
        ttk.Button(detalle, text="Agregar al carrito", style="Success.TButton", command=self.controller.add_to_cart).pack(fill="x", pady=(14, 4))

    def set_detail(self, producto=None):
        if not producto:
            self.detalle_nombre.config(text="Seleccione un producto")
            self.detalle_precio.config(text="Precio: ₡0.00")
            self.detalle_stock.config(text="Stock: 0")
            self.detalle_descripcion.config(text="Descripción: -")
            return
        self.detalle_nombre.config(text=producto.nombre)
        self.detalle_precio.config(text=f"Precio: {money(producto.precio)}")
        self.detalle_stock.config(text=f"Stock: {producto.stock}")
        self.detalle_descripcion.config(text=f"Descripción: {producto.descripcion or '-'}")



