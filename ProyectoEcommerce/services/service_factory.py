from services.usuario_service import UsuarioService
from services.auth_service import AuthService
from services.categoria_service import CategoriaService
from services.producto_service import ProductoService
from services.inventario_service import InventarioService
from services.carrito_service import CarritoService
from services.pedido_service import PedidoService
from services.pago_service import PagoService
from services.historial_service import HistorialService
from services.resena_service import ResenaService
from services.notificacion_service import NotificacionService
from services.admin_service import AdminService
from services.checkout_service import CheckoutService


class ServiceFactory:
    """Centraliza servicios y mantiene reglas de negocio separadas de las vistas."""

    def __init__(self):
        self.usuario_service = UsuarioService()
        self.auth_service = AuthService(self.usuario_service)
        self.categoria_service = CategoriaService()
        self.producto_service = ProductoService()
        self.historial_service = HistorialService()
        self.notificacion_service = NotificacionService()
        self.carrito_service = CarritoService(producto_service=self.producto_service)
        self.pedido_service = PedidoService(
            carrito_service=self.carrito_service,
            producto_service=self.producto_service,
            historial_service=self.historial_service,
            notificacion_service=self.notificacion_service,
        )
        self.pago_service = PagoService(
            pedido_service=self.pedido_service,
            historial_service=self.historial_service,
            notificacion_service=self.notificacion_service,
        )
        self.resena_service = ResenaService(
            pedido_service=self.pedido_service,
            historial_service=self.historial_service,
            notificacion_service=self.notificacion_service,
        )
        self.inventario_service = InventarioService(producto_service=self.producto_service)
        self.checkout_service = CheckoutService(
            pedido_service=self.pedido_service,
            pago_service=self.pago_service,
            carrito_service=self.carrito_service,
            historial_service=self.historial_service,
            notificacion_service=self.notificacion_service,
        )
        self.admin_service = AdminService(
            self.usuario_service,
            self.producto_service,
            self.pedido_service,
            self.pago_service,
            self.resena_service,
            self.notificacion_service,
        )
