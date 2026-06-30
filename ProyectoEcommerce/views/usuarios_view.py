from tkinter import ttk
from utils.ui import page, card



class UsuariosView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Main.TFrame")
        self.controller = controller
        root = page(self, "Usuarios", "Administración de cuentas, roles y estado de acceso.")
        form = card(root, padding=14)
        form.pack(fill="x", pady=(0, 12))
        self.id_usuario = ttk.Entry(form, width=28)
        self.nombre = ttk.Entry(form, width=28)
        self.correo = ttk.Entry(form, width=28)
        self.contrasena = ttk.Entry(form, width=28, show="*")
        self.rol = ttk.Combobox(form, values=["Administrador", "Cliente", "Vendedor", "Soporte"], state="readonly", width=25)
        self.estado = ttk.Combobox(form, values=["Activo", "Inactivo", "Bloqueado"], state="readonly", width=25)
        self.rol.set("Cliente"); self.estado.set("Activo")
        fields = [("ID", self.id_usuario), ("Nombre", self.nombre), ("Correo", self.correo), ("Contraseña", self.contrasena), ("Rol", self.rol), ("Estado", self.estado)]
        for i, (label, widget) in enumerate(fields):
            ttk.Label(form, text=label, style="Field.TLabel").grid(row=i//3*2, column=i%3, padx=8, pady=(4,0), sticky="w")
            widget.grid(row=i//3*2+1, column=i%3, padx=8, pady=(2,8), sticky="ew")
        for i in range(3): form.columnconfigure(i, weight=1)
        buttons = ttk.Frame(root, style="Main.TFrame"); buttons.pack(fill="x", pady=(0, 12))
        ttk.Button(buttons, text="Registrar", style="Success.TButton", command=self.controller.create_user).pack(side="left", padx=4)
        ttk.Button(buttons, text="Guardar cambios", style="Primary.TButton", command=self.controller.update_user).pack(side="left", padx=4)
        ttk.Button(buttons, text="Activar/Inactivar", command=self.controller.toggle_user_status).pack(side="left", padx=4)
        ttk.Button(buttons, text="Eliminar", style="Danger.TButton", command=self.controller.delete_user).pack(side="left", padx=4)
        ttk.Button(buttons, text="Limpiar", command=self.controller.clear_form).pack(side="left", padx=4)
        ttk.Label(buttons, text="Buscar:", background="#eef2f7").pack(side="left", padx=(25,4))
        self.buscar = ttk.Entry(buttons, width=30); self.buscar.pack(side="left", padx=4)
        ttk.Button(buttons, text="Buscar", command=self.controller.search_users).pack(side="left", padx=4)
        table_card = card(root, padding=12); table_card.pack(fill="both", expand=True)
        self.tabla = ttk.Treeview(table_card, columns=("id", "nombre", "correo", "rol", "estado", "fecha"), show="headings")
        for col, text in {"id":"ID", "nombre":"Nombre", "correo":"Correo", "rol":"Rol", "estado":"Estado", "fecha":"Registro"}.items():
            self.tabla.heading(col, text=text); self.tabla.column(col, width=140)
        self.tabla.column("nombre", width=220); self.tabla.column("correo", width=240)
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", lambda e: self.controller.fill_form_from_selection())
