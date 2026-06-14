import tkinter as tk
from tkinter import ttk

class CatalogoView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Main.TFrame")
        self.controller = controller
        
        header = ttk.Frame(self, style="Card.TFrame")
        header.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(header, text="Mi Tienda - Catálogo", style="Title.TLabel", background="white").pack(side="left", padx=10, pady=10)
        
        botones_header = ttk.Frame(header, style="Card.TFrame")
        botones_header.pack(side="right", padx=10)
        
        ttk.Button(botones_header, text="Iniciar Sesión", command=self.controller.go_to_login).pack(side="left", padx=5)
        ttk.Button(botones_header, text="Mi Carrito", command=self.controller.go_to_cart).pack(side="left", padx=5)
        
        # Main content
        content = ttk.Frame(self, style="Main.TFrame")
        content.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left Panel (Filters)
        filtros = ttk.Frame(content, style="Card.TFrame")
        filtros.pack(side="left", fill="y", padx=(0, 10))
        
        ttk.Label(filtros, text="Filtros", style="Title.TLabel", background="white").pack(pady=10, padx=10)
        ttk.Label(filtros, text="Buscar por Nombre:", background="white").pack(anchor="w", padx=10)
        ttk.Entry(filtros, width=25).pack(padx=10, pady=5)
        
        ttk.Label(filtros, text="Categoría:", background="white").pack(anchor="w", padx=10, pady=(10,0))
        ttk.Combobox(filtros, values=["Todas", "Tecnología", "Ropa", "Hogar", "Deportes"], width=22).pack(padx=10, pady=5)
        
        ttk.Label(filtros, text="Marca:", background="white").pack(anchor="w", padx=10, pady=(10,0))
        ttk.Combobox(filtros, values=["Todas", "Marca A", "Marca B", "Marca C"], width=22).pack(padx=10, pady=5)
        
        ttk.Label(filtros, text="Precio Máximo:", background="white").pack(anchor="w", padx=10, pady=(10,0))
        ttk.Entry(filtros, width=25).pack(padx=10, pady=5)
        
        ttk.Button(filtros, text="Aplicar Filtros").pack(pady=20, padx=10, fill="x")
        
        # Center Panel (Products Treeview)
        productos_frame = ttk.Frame(content, style="Card.TFrame")
        productos_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ttk.Label(productos_frame, text="Productos Disponibles", style="Subtitle.TLabel", background="white").pack(anchor="w", padx=10, pady=10)
        
        self.tabla = ttk.Treeview(productos_frame, columns=("id", "nombre", "categoria", "precio", "stock"), show="headings")
        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre del Producto")
        self.tabla.heading("categoria", text="Categoría")
        self.tabla.heading("precio", text="Precio")
        self.tabla.heading("stock", text="Stock")
        
        self.tabla.column("id", width=50)
        self.tabla.column("nombre", width=200)
        self.tabla.column("categoria", width=100)
        self.tabla.column("precio", width=80)
        self.tabla.column("stock", width=80)
        
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Right Panel (Product Detail)
        detalle_frame = ttk.Frame(content, style="Card.TFrame")
        detalle_frame.pack(side="right", fill="y")
        
        ttk.Label(detalle_frame, text="Detalle del Producto", style="Title.TLabel", background="white").pack(pady=10, padx=10)
        
        img_placeholder = tk.Label(detalle_frame, text="[ Imagen del Producto ]", bg="#ccc", width=30, height=12)
        img_placeholder.pack(pady=10, padx=15)
        
        ttk.Label(detalle_frame, text="Nombre: Seleccione un producto", background="white", wraplength=200).pack(anchor="w", padx=15, pady=5)
        ttk.Label(detalle_frame, text="Precio: $0.00", background="white").pack(anchor="w", padx=15, pady=5)
        ttk.Label(detalle_frame, text="Stock: 0 unidades", background="white").pack(anchor="w", padx=15, pady=5)
        ttk.Label(detalle_frame, text="Descripción:\nLorem ipsum dolor sit amet, consectetur adipiscing elit.", background="white", wraplength=200).pack(anchor="w", padx=15, pady=5)
        
        ttk.Button(detalle_frame, text="Agregar al Carrito", command=self.controller.add_to_cart).pack(fill="x", padx=15, pady=20)
