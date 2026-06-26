import tkinter as tk
from tkinter import ttk, messagebox

from utils.ui import setup_styles
from services.service_factory import ServiceFactory

from controllers.login_controller import LoginController
from controllers.registro_controller import RegistroController
from controllers.recuperar_controller import RecuperarController
from controllers.catalogo_controller import CatalogoController
from controllers.carrito_controller import CarritoController
from controllers.usuarios_controller import UsuariosController
from controllers.categorias_controller import CategoriasController
from controllers.productos_controller import ProductosController
from controllers.inventario_controller import InventarioController
from controllers.pedidos_controller import PedidosController
from controllers.pagos_controller import PagosController
from controllers.historial_controller import HistorialController
from controllers.resenas_controller import ResenasController
from controllers.notificaciones_controller import NotificacionesController
from controllers.admin_panel_controller import AdminPanelController


class AppController:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Ecommerce MVC - JSON")
        self.root.geometry("1360x780")
        self.root.minsize(1180, 680)
        self.root.configure(bg="#eef2f7")
        setup_styles(root)

        self.services = ServiceFactory()
        self.current_user = None
        self._seed_initial_data()

        self.nav_frame = ttk.Frame(self.root, style="Sidebar.TFrame", width=240)
        self.nav_frame.pack(side="left", fill="y")
        self.nav_frame.pack_propagate(False)

        self.content_frame = ttk.Frame(self.root, style="Main.TFrame")
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.controllers = {
            "login": LoginController(self),
            "registro": RegistroController(self),
            "recuperar": RecuperarController(self),
            "catalogo": CatalogoController(self),
            "carrito": CarritoController(self),
            "usuarios": UsuariosController(self),
            "categorias": CategoriasController(self),
            "productos": ProductosController(self),
            "inventario": InventarioController(self),
            "pedidos": PedidosController(self),
            "pagos": PagosController(self),
            "historial": HistorialController(self),
            "resenas": ResenasController(self),
            "notificaciones": NotificacionesController(self),
            "admin": AdminPanelController(self),
        }
        self.current_controller = None
        self._setup_navbar()
        self.show_view("catalogo")

    def _setup_navbar(self):
        for widget in self.nav_frame.winfo_children():
            widget.destroy()
        ttk.Label(self.nav_frame, text="Ecommerce MVC", style="SidebarTitle.TLabel").pack(anchor="w", padx=18, pady=(22, 2))
        user_text = "Sin sesión" if not self.current_user else f"{self.current_user.nombre} · {self.current_user.rol}"
        ttk.Label(self.nav_frame, text=user_text, style="SidebarSub.TLabel", wraplength=200).pack(anchor="w", padx=18, pady=(0, 18))

        opciones = [
            ("🛍  Catálogo público", "catalogo"),
            ("🔐  Autenticación", "login"),
            ("🛒  Carrito de compras", "carrito"),
            ("📦  Órdenes / pedidos", "pedidos"),
            ("💳  Pagos simulados", "pagos"),
            ("🕘  Historial de compras", "historial"),
            ("⭐  Reseñas", "resenas"),
            ("👥  Usuarios", "usuarios"),
            ("🏷  Categorías", "categorias"),
            ("📚  Catálogo de productos", "productos"),
            ("📊  Inventario", "inventario"),
            ("🔔  Notificaciones", "notificaciones"),
            ("⚙  Panel administrativo", "admin"),
        ]
        for text, view_name in opciones:
            ttk.Button(self.nav_frame, text=text, style="Nav.TButton", command=lambda v=view_name: self.show_view(v)).pack(fill="x", padx=12, pady=2)
        ttk.Frame(self.nav_frame, style="Sidebar.TFrame").pack(fill="both", expand=True)
        ttk.Button(self.nav_frame, text="Cerrar sesión", style="Nav.TButton", command=self.logout).pack(fill="x", padx=12, pady=(2, 18))

    def show_view(self, view_name):
        if view_name in ["carrito"] and not self.current_user:
            messagebox.showwarning("Login requerido", "Debes iniciar sesión para usar este módulo.")
            view_name = "login"
        if self.current_controller:
            self.current_controller.view.pack_forget()
        self.current_controller = self.controllers[view_name]
        self.current_controller.view.pack(fill="both", expand=True)
        if hasattr(self.current_controller, "on_show"):
            self.current_controller.on_show()

    def logout(self):
        self.current_user = None
        self._setup_navbar()
        messagebox.showinfo("Sesión", "Sesión cerrada correctamente.")
        self.show_view("catalogo")

    def refresh_navbar(self):
        self._setup_navbar()

    def _seed_initial_data(self):
        """Datos mínimos para probar el sistema sin llenar los JSON a mano."""
        try:
            if not self.services.usuario_service.listar_usuarios():
                self.services.usuario_service.registrar_usuario("Administrador Demo", "admin@demo.com", "admin123", "Administrador")
                self.services.usuario_service.registrar_usuario("Cliente Demo", "cliente@demo.com", "cliente123", "Cliente")

            categorias = self.services.categoria_service.listar()
            if not categorias:
                self.services.categoria_service.crear("Tecnología", "Productos electrónicos y accesorios")
                self.services.categoria_service.crear("Hogar", "Artículos para casa")
                self.services.categoria_service.crear("Deportes", "Equipo deportivo")

            categorias = {c.nombre: c for c in self.services.categoria_service.listar(solo_activas=True)}
            productos = self.services.producto_service.listar_productos()
            if not productos and {"Tecnología", "Hogar", "Deportes"}.issubset(categorias.keys()):
                tecnologia = categorias["Tecnología"]
                hogar = categorias["Hogar"]
                deportes = categorias["Deportes"]
                self.services.producto_service.crear_producto("Audífonos Bluetooth", tecnologia.id_categoria, "SoundPro", 18500, 15, 5, "Audífonos inalámbricos con estuche de carga.")
                self.services.producto_service.crear_producto("Mouse inalámbrico", tecnologia.id_categoria, "TechLine", 9500, 8, 4, "Mouse ergonómico de 2.4 GHz.")
                self.services.producto_service.crear_producto("Botella térmica", hogar.id_categoria, "CasaPlus", 7200, 20, 5, "Botella de acero inoxidable.")
                self.services.producto_service.crear_producto("Guantes deportivos", deportes.id_categoria, "FitMax", 12500, 4, 5, "Guantes para entrenamiento funcional.")
        except Exception:
            # Si el seed ya existe o fue editado manualmente, no se detiene la app.
            pass
