from tkinter import ttk
import tkinter as tk
from utils.ui import page, card


class NotificacionesView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Main.TFrame")
        self.controller = controller
        root = page(self, "Notificaciones", "Mensajes del sistema, pedidos, pagos, inventario y reseñas.")
        form = card(root, padding=14); form.pack(fill="x", pady=(0, 12))
        self.id_usuario = ttk.Entry(form, width=30)
        self.titulo = ttk.Entry(form, width=30)
        self.tipo = ttk.Combobox(form, values=["Sistema", "Pedido", "Pago", "Inventario", "Reseña"], state="readonly", width=27); self.tipo.set("Sistema")
        ttk.Label(form, text="ID usuario", style="Field.TLabel").grid(row=0, column=0, padx=8, sticky="w")
        self.id_usuario.grid(row=1, column=0, padx=8, pady=(2,8), sticky="ew")
        ttk.Label(form, text="Título", style="Field.TLabel").grid(row=0, column=1, padx=8, sticky="w")
        self.titulo.grid(row=1, column=1, padx=8, pady=(2,8), sticky="ew")
        ttk.Label(form, text="Tipo", style="Field.TLabel").grid(row=0, column=2, padx=8, sticky="w")
        self.tipo.grid(row=1, column=2, padx=8, pady=(2,8), sticky="ew")
        ttk.Label(form, text="Mensaje", style="Field.TLabel").grid(row=2, column=0, padx=8, sticky="w")
        self.mensaje = tk.Text(form, height=3, font=("Segoe UI", 10))
        self.mensaje.grid(row=3, column=0, columnspan=3, padx=8, pady=(2,8), sticky="ew")
        for i in range(3): form.columnconfigure(i, weight=1)
        buttons = ttk.Frame(root, style="Main.TFrame"); buttons.pack(fill="x", pady=(0, 12))
        ttk.Button(buttons, text="Crear notificación", style="Success.TButton", command=self.controller.create_notification).pack(side="left", padx=4)
        ttk.Button(buttons, text="Marcar leída", style="Primary.TButton", command=self.controller.mark_read).pack(side="left", padx=4)
        ttk.Button(buttons, text="Eliminar", style="Danger.TButton", command=self.controller.delete_notification).pack(side="left", padx=4)
        ttk.Button(buttons, text="Actualizar", command=self.controller.load_notifications).pack(side="left", padx=4)
        table_card = card(root, padding=12); table_card.pack(fill="both", expand=True)
        self.tabla = ttk.Treeview(table_card, columns=("id", "usuario", "titulo", "mensaje", "tipo", "leida", "fecha"), show="headings")
        headers = {"id":"ID", "usuario":"Usuario", "titulo":"Título", "mensaje":"Mensaje", "tipo":"Tipo", "leida":"Leída", "fecha":"Fecha"}
        for col, text in headers.items(): self.tabla.heading(col, text=text); self.tabla.column(col, width=130)
        self.tabla.column("mensaje", width=380)
        self.tabla.pack(fill="both", expand=True)

