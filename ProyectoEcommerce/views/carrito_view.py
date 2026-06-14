import tkinter as tk
from tkinter import ttk

class CarritoView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Main.TFrame")
        self.controller = controller
        
        header = ttk.Frame(self, style="Card.TFrame")
        header.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(header, text="Mi Carrito de Compras", style="Title.TLabel", background="white").pack(side="left", padx=10, pady=10)
        
        botones_header = ttk.Frame(header, style="Card.TFrame")
        botones_header.pack(side="right", padx=10)
        
        ttk.Button(botones_header, text="Volver al Catálogo", command=self.controller.go_to_catalogo).pack(side="left", padx=5)
        ttk.Button(botones_header, text="Vaciar Carrito", command=self.controller.empty_cart).pack(side="left", padx=5)
        
        content = ttk.Frame(self, style="Main.TFrame")
        content.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left Panel (Cart Items)
        items_frame = ttk.Frame(content, style="Card.TFrame")
        items_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.tabla = ttk.Treeview(items_frame, columns=("id", "nombre", "cantidad", "precio", "subtotal"), show="headings")
        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Producto")
        self.tabla.heading("cantidad", text="Cantidad")
        self.tabla.heading("precio", text="Precio Unit.")
        self.tabla.heading("subtotal", text="Subtotal")
        
        self.tabla.column("id", width=50)
        self.tabla.column("nombre", width=250)
        self.tabla.column("cantidad", width=80)
        self.tabla.column("precio", width=100)
        self.tabla.column("subtotal", width=100)
        
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)
        
        botones_items = ttk.Frame(items_frame, style="Card.TFrame")
        botones_items.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(botones_items, text="+1 Cantidad").pack(side="left", padx=5)
        ttk.Button(botones_items, text="-1 Cantidad").pack(side="left", padx=5)
        ttk.Button(botones_items, text="Eliminar Producto", command=self.controller.remove_item).pack(side="left", padx=5)
        
        # Right Panel (Checkout)
        checkout_frame = ttk.Frame(content, style="Card.TFrame")
        checkout_frame.pack(side="right", fill="y")
        
        ttk.Label(checkout_frame, text="Resumen de Compra", style="Title.TLabel", background="white").pack(pady=10, padx=15)
        
        ttk.Label(checkout_frame, text="Subtotal: $0.00", background="white").pack(anchor="w", padx=15, pady=5)
        ttk.Label(checkout_frame, text="IVA (13%): $0.00", background="white").pack(anchor="w", padx=15, pady=5)
        
        ttk.Label(checkout_frame, text="Cantón de Envío:", background="white").pack(anchor="w", padx=15, pady=(10,0))
        ttk.Combobox(checkout_frame, values=["San José", "Alajuela", "Cartago", "Heredia", "Guanacaste", "Puntarenas", "Limón"], width=22).pack(padx=15, pady=5)
        
        ttk.Label(checkout_frame, text="Costo de Envío: $0.00", background="white").pack(anchor="w", padx=15, pady=5)
        
        ttk.Label(checkout_frame, text="Método de Pago:", background="white").pack(anchor="w", padx=15, pady=(10,0))
        ttk.Combobox(checkout_frame, values=["Tarjeta de Crédito", "Transferencia", "Efectivo", "SINPE Móvil"], width=22).pack(padx=15, pady=5)
        
        ttk.Label(checkout_frame, text="Total Final: $0.00", font=("Segoe UI", 16, "bold"), background="white").pack(anchor="w", padx=15, pady=20)
        
        ttk.Button(checkout_frame, text="Confirmar Compra", command=self.controller.checkout).pack(fill="x", padx=15, pady=10)
