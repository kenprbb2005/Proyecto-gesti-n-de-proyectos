from typing import Optional, Tuple

from models.pedido import Pedido
from models.pago import Pago
from services.pedido_service import PedidoService
from services.pago_service import PagoService
from services.carrito_service import CarritoService
from services.historial_service import HistorialService
from services.notificacion_service import NotificacionService


class CheckoutService:
    """Orquesta la compra completa: carrito seleccionado -> pedido -> pago -> historial."""

    def __init__(
        self,
        pedido_service: Optional[PedidoService] = None,
        pago_service: Optional[PagoService] = None,
        carrito_service: Optional[CarritoService] = None,
        historial_service: Optional[HistorialService] = None,
        notificacion_service: Optional[NotificacionService] = None,
    ):
        self.pedido_service = pedido_service or PedidoService()
        self.pago_service = pago_service or PagoService(pedido_service=self.pedido_service)
        self.carrito_service = carrito_service or CarritoService()
        self.historial_service = historial_service or HistorialService()
        self.notificacion_service = notificacion_service or NotificacionService()

    def realizar_compra(
        self,
        id_usuario: str,
        canton_envio: str,
        direccion_envio: str,
        metodo_pago: str,
        referencia_pago: str = "",
    ) -> Tuple[Pedido, Pago]:
        """Compra únicamente los productos marcados en el carrito.

        Reglas de negocio:
        - El usuario debe estar logueado.
        - Debe existir al menos un producto marcado para compra.
        - Se valida stock al confirmar.
        - Se descuenta stock al crear el pedido.
        - Se procesa un pago simulado por el total exacto.
        - Si el pago falla, se cancela el pedido, se restaura el stock y se devuelven
          los productos al carrito.
        """
        if not id_usuario:
            raise ValueError("Debes iniciar sesión antes de comprar.")

        direccion_envio = direccion_envio.strip()
        if not direccion_envio:
            raise ValueError("La dirección de envío es obligatoria para realizar la compra.")

        pedido = self.pedido_service.crear_desde_carrito(id_usuario, canton_envio, direccion_envio)

        try:
            pago = self.pago_service.procesar_pago(
                pedido.id_pedido,
                metodo_pago,
                pedido.total,
                referencia_pago,
            )
        except Exception:
            self.pedido_service.cancelar(pedido.id_pedido)
            self.carrito_service.restaurar_items(id_usuario, pedido.items)
            raise

        if pago.estado != "Aprobado":
            self.pedido_service.cancelar(pedido.id_pedido)
            self.carrito_service.restaurar_items(id_usuario, pedido.items)
            raise ValueError(pago.mensaje)

        pedido = self.pedido_service.obtener(pedido.id_pedido) or pedido

        self.historial_service.registrar(
            id_usuario,
            "Compra realizada",
            f"Compra finalizada con pago aprobado. Pedido {pedido.id_pedido}, pago {pago.id_pago}.",
            pedido.id_pedido,
        )
        self.notificacion_service.crear(
            id_usuario,
            "Compra realizada",
            f"Tu compra fue realizada correctamente. Pedido: {pedido.id_pedido}.",
            "Pedido",
        )
        return pedido, pago
