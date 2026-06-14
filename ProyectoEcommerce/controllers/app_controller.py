import tkinter as tk
from tkinter import ttk
from controllers.historial_controller import HistorialController
from controllers.inventario_controller import InventarioController
from controllers.pagos_controller import PagosController
from controllers.resenas_controller import ResenasController
from controllers.login_controller import LoginController
from controllers.registro_controller import RegistroController
from controllers.recuperar_controller import RecuperarController
from controllers.perfil_controller import PerfilController
from controllers.usuarios_controller import UsuariosController
from controllers.catalogo_controller import CatalogoController
from controllers.carrito_controller import CarritoController
from tkinter import messagebox

class AppController:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto Ecommerce MVC")
        self.root.geometry("1300x750")
        self.root.configure(bg="#eef2f7")
        
        self._setup_styles()
        
        self.nav_frame = None
        self.content_frame = ttk.Frame(self.root, style="Main.TFrame")
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        self.controllers = {
            "login": LoginController(self),
            "registro": RegistroController(self),
            "recuperar": RecuperarController(self),
            "inventario": InventarioController(self),
            "pagos": PagosController(self),
            "resenas": ResenasController(self),
            "historial": HistorialController(self),
            "perfil": PerfilController(self),
            "usuarios": UsuariosController(self),
            "catalogo": CatalogoController(self),
            "carrito": CarritoController(self)
        }
        
        self.current_controller = None
        self.show_view("catalogo") # Inicia en el catalogo
        
    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Main.TFrame", background="#edf1f7")
        style.configure("TFrame", background="#eef2f7")
        style.configure("Card.TFrame", background="white", relief="flat")
        style.configure("TLabel", background="white", font=("Segoe UI", 10))
        style.configure("Header.TLabel", background="#edf1f7", font=("Segoe UI", 24, "bold"))
        style.configure("Title.TLabel", background="white", font=("Segoe UI", 22, "bold"))
        style.configure("Subtitle.TLabel", background="#eef2f7", font=("Segoe UI", 10))
        style.configure("Subheader.TLabel", background="#edf1f7", font=("Segoe UI", 10))
        style.configure("Field.TLabel", background="white", font=("Segoe UI", 10))
        style.configure("Nav.TButton", font=("Segoe UI", 12, "bold"), padding=10)
        style.configure("TButton", font=("Segoe UI", 10), padding=8)
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("TCheckbutton", background="white", font=("Segoe UI", 10))

    def _setup_navbar(self):
        self.nav_frame = ttk.Frame(self.root, style="Card.TFrame")
        self.nav_frame.pack(side="left", fill="y", padx=(0, 5), before=self.content_frame)
        
        ttk.Label(self.nav_frame, text="Panel Admin", style="Title.TLabel", background="white").pack(pady=20, padx=20)
        
        ttk.Button(self.nav_frame, text="Inventario", style="Nav.TButton", command=lambda: self.show_view("inventario")).pack(fill="x", padx=15, pady=8)
        ttk.Button(self.nav_frame, text="Pagos", style="Nav.TButton", command=lambda: self.show_view("pagos")).pack(fill="x", padx=15, pady=8)
        ttk.Button(self.nav_frame, text="Reseñas", style="Nav.TButton", command=lambda: self.show_view("resenas")).pack(fill="x", padx=15, pady=8)
        ttk.Button(self.nav_frame, text="Historial", style="Nav.TButton", command=lambda: self.show_view("historial")).pack(fill="x", padx=15, pady=8)
        ttk.Button(self.nav_frame, text="Usuarios", style="Nav.TButton", command=lambda: self.show_view("usuarios")).pack(fill="x", padx=15, pady=8)
        ttk.Button(self.nav_frame, text="Mi Perfil", style="Nav.TButton", command=lambda: self.show_view("perfil")).pack(fill="x", padx=15, pady=8)
        ttk.Button(self.nav_frame, text="Ir a Tienda", style="Nav.TButton", command=lambda: self.show_view("catalogo")).pack(fill="x", padx=15, pady=8)
        
        ttk.Label(self.nav_frame, text="", background="white").pack(fill="y", expand=True) # Spacer
        ttk.Button(self.nav_frame, text="Cerrar Sesión", style="Nav.TButton", command=self.logout).pack(fill="x", padx=15, pady=20, side="bottom")

    def show_view(self, view_name):
        admin_views = ["inventario", "pagos", "resenas", "historial", "perfil", "usuarios"]
        
        if view_name in admin_views:
            if not self.nav_frame:
                self._setup_navbar()
            self.nav_frame.pack(side="left", fill="y", padx=(0, 5), before=self.content_frame)
        else:
            if self.nav_frame:
                self.nav_frame.pack_forget()
                
        if self.current_controller:
            self.current_controller.view.pack_forget()
            
        self.current_controller = self.controllers[view_name]
        self.current_controller.view.pack(fill="both", expand=True)

    def show_auth_view(self, view_name):
        self.show_view(view_name)

    def login_success(self):
        # Para el mockup, el login exitoso enviará al panel admin
        self.show_view("inventario")
        
    def logout(self):
        messagebox.showinfo("Sesión", "Sesión cerrada correctamente.")
        self.show_view("catalogo")
