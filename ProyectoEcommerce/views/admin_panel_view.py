from tkinter import ttk
from utils.ui import page, card, money


class AdminPanelView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Main.TFrame")
        self.controller = controller
        root = page(self, "Panel administrativo", "Indicadores generales del sistema y alertas importantes.")
        ttk.Button(root, text="Actualizar indicadores", style="Primary.TButton", command=self.controller.load_dashboard).pack(anchor="e", pady=(0, 10))
        self.cards_frame = ttk.Frame(root, style="Main.TFrame")
        self.cards_frame.pack(fill="x")
        self.labels = {}
        metricas = [
            ("usuarios", "Usuarios"),
            ("productos", "Productos"),
            ("pedidos", "Pedidos"),
            ("ventas_aprobadas", "Ventas aprobadas"),
            ("pedidos_pendientes", "Pedidos pendientes"),
            ("productos_bajo_stock", "Bajo stock"),
            ("resenas", "Reseñas"),
            ("notificaciones", "Notificaciones"),
        ]
        for i, (key, title) in enumerate(metricas):
            c = card(self.cards_frame, padding=16)
            c.grid(row=i // 4, column=i % 4, sticky="nsew", padx=8, pady=8)
            ttk.Label(c, text=title, style="Field.TLabel").pack(anchor="w")
            lbl = ttk.Label(c, text="0", style="Title.TLabel")
            lbl.pack(anchor="w", pady=(6, 0))
            self.labels[key] = lbl
        for i in range(4):
            self.cards_frame.columnconfigure(i, weight=1)

        alert = card(root, padding=16)
        alert.pack(fill="both", expand=True, pady=14)
        ttk.Label(alert, text="Productos con bajo stock", style="Title.TLabel").pack(anchor="w", pady=(0, 8))
        self.tabla = ttk.Treeview(alert, columns=("id", "producto", "stock", "minimo", "estado"), show="headings")
        for col, text in {"id": "ID", "producto": "Producto", "stock": "Stock", "minimo": "Mínimo", "estado": "Estado"}.items():
            self.tabla.heading(col, text=text)
            self.tabla.column(col, width=140)
        self.tabla.column("producto", width=260)
        self.tabla.pack(fill="both", expand=True)

    def set_summary(self, resumen):
        for key, lbl in self.labels.items():
            value = resumen.get(key, 0)
            if key == "ventas_aprobadas":
                value = money(value)
            lbl.config(text=str(value))
