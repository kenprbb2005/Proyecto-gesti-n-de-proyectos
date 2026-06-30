from copy import deepcopy
from typing import List, Optional

from models.pedido import Pedido
from models.base import now_iso
from repositories.pedido_repository import PedidoRepository
from services.carrito_service import CarritoService
from services.producto_service import ProductoService
from services.historial_service import HistorialService
from services.notificacion_service import NotificacionService


class PedidoService:
    """Reglas de negocio para pedidos.

    Norma del negocio aplicada:
    1. El carrito no registra pagos.
    2. El carrito procesa un pedido con los productos marcados.
    3. El pedido se guarda en pedidos.json y aparece en la tabla de pedidos.
    4. Desde pedidos se envía al módulo de pagos.
    """

    ESTADOS_VALIDOS = ["Pendiente", "Pagado", "Preparando", "Enviado", "Entregado", "Cancelado"]
    COSTOS_ENVIO = {
        "San José": 2500,
        "Alajuela": 3000,
        "Cartago": 3000,
        "Heredia": 2800,
        "Guanacaste": 4500,
        "Puntarenas": 4500,
        "Limón": 4500,
    }

    def __init__(
        self,
        pedido_repository: Optional[PedidoRepository] = None,
        carrito_service: Optional[CarritoService] = None,
        producto_service: Optional[ProductoService] = None,
        historial_service: Optional[HistorialService] = None,
        notificacion_service: Optional[NotificacionService] = None,
    ):
        self.pedido_repository = pedido_repository or PedidoRepository()
        self.carrito_service = carrito_service or CarritoService()
        self.producto_service = producto_service or ProductoService()
        self.historial_service = historial_service or HistorialService()
        self.notificacion_service = notificacion_service or NotificacionService()

    def listar_pedidos(self) -> List[Pedido]:
        return sorted(self.pedido_repository.find_all(), key=lambda p: p.fecha_creacion, reverse=True)

    def listar_por_usuario(self, id_usuario: str) -> List[Pedido]:
        return sorted(self.pedido_repository.find_by_usuario(id_usuario), key=lambda p: p.fecha_creacion, reverse=True)

    def obtener(self, id_pedido: str) -> Optional[Pedido]:
        return self.pedido_repository.find_by_id(id_pedido)

    def crear_desde_carrito(self, id_usuario: str, canton_envio: str, direccion_envio: str) -> Pedido:
        if not id_usuario:
            raise ValueError("Debes iniciar sesión antes de crear un pedido.")

        carrito = self.carrito_service.obtener_carrito_activo(id_usuario)
        if not carrito.items:
            raise ValueError("El carrito está vacío.")
        if not canton_envio:
            raise ValueError("Debes seleccionar una provincia de envío.")
        if not direccion_envio.strip():
            raise ValueError("La dirección de envío es obligatoria.")

        items_a_comprar = self.carrito_service.obtener_items_detallados(carrito, solo_seleccionados=True)
        if not items_a_comprar:
            raise ValueError("Selecciona al menos un producto del carrito para procesar el pedido.")

        items_pedido = []
        for item in items_a_comprar:
            producto = self.producto_service.obtener_producto(item["id_producto"])
            if not producto or producto.estado != "Disponible":
                raise ValueError(f"El producto {item['nombre']} ya no está disponible.")
            if int(item["cantidad"]) > int(producto.stock):
                raise ValueError(f"No hay stock suficiente para {item['nombre']}.")

            # El pedido conserva una fotografía del producto, precio y cantidad
            # al momento de procesar el carrito.
            items_pedido.append({
                "id_producto": producto.id_producto,
                "nombre": producto.nombre,
                "categoria": producto.categoria,
                "marca": producto.marca,
                "cantidad": int(item["cantidad"]),
                "precio_unitario": float(producto.precio),
                "subtotal": round(int(item["cantidad"]) * float(producto.precio), 2),
            })

        # Se descuenta stock al crear el pedido porque el pedido reserva los productos.
        for item in items_pedido:
            self.producto_service.descontar_stock(item["id_producto"], int(item["cantidad"]))

        subtotal = round(sum(float(item["subtotal"]) for item in items_pedido), 2)
        impuesto = round(subtotal * 0.13, 2)
        envio = float(self.COSTOS_ENVIO.get(canton_envio, 3500))
        total = round(subtotal + impuesto + envio, 2)

        pedido = Pedido(
            id_usuario=id_usuario,
            items=deepcopy(items_pedido),
            subtotal=subtotal,
            impuesto=impuesto,
            envio=envio,
            total=total,
            canton_envio=canton_envio,
            direccion_envio=direccion_envio.strip(),
            estado="Pendiente",
        )
        pedido = self.pedido_repository.save(pedido)

        # Los productos ya procesados como pedido salen del carrito.
        self.carrito_service.finalizar_items_comprados(
            carrito.id_carrito,
            [item["id_producto"] for item in items_pedido],
        )

        self.historial_service.registrar(
            id_usuario,
            "Pedido registrado",
            f"Se registró el pedido {pedido.id_pedido} por ₡{pedido.total:,.2f}. Pendiente de pago.",
            pedido.id_pedido,
        )
        self.notificacion_service.crear(
            id_usuario,
            "Pedido registrado",
            f"Tu pedido {pedido.id_pedido} fue registrado. Continúa con el proceso de pago.",
            "Pedido",
        )
        return pedido

    def cambiar_estado(self, id_pedido: str, estado: str) -> Pedido:
        pedido = self._obtener_o_error(id_pedido)
        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError("El estado del pedido no es válido.")
        if pedido.estado == "Cancelado":
            raise ValueError("No se puede cambiar un pedido cancelado.")
        if pedido.estado == "Entregado" and estado != "Entregado":
            raise ValueError("Un pedido entregado no debe devolverse a estados anteriores.")
        pedido.estado = estado
        pedido.fecha_actualizacion = now_iso()
        pedido = self.pedido_repository.save(pedido)
        self.historial_service.registrar(pedido.id_usuario, "Estado de pedido", f"El pedido {pedido.id_pedido} cambió a {estado}.", pedido.id_pedido)
        self.notificacion_service.crear(pedido.id_usuario, "Actualización de pedido", f"Tu pedido {pedido.id_pedido} ahora está: {estado}.", "Pedido")
        return pedido

    def cancelar(self, id_pedido: str) -> Pedido:
        pedido = self._obtener_o_error(id_pedido)
        if pedido.estado in ["Enviado", "Entregado"]:
            raise ValueError("No se puede cancelar un pedido enviado o entregado.")
        if pedido.estado != "Cancelado":
            for item in pedido.items:
                self.producto_service.aumentar_stock(item["id_producto"], int(item["cantidad"]))
        pedido.estado = "Cancelado"
        pedido.fecha_actualizacion = now_iso()
        pedido = self.pedido_repository.save(pedido)
        self.historial_service.registrar(pedido.id_usuario, "Pedido cancelado", f"Se canceló el pedido {pedido.id_pedido} y se restauró el stock.", pedido.id_pedido)
        self.notificacion_service.crear(pedido.id_usuario, "Pedido cancelado", f"Tu pedido {pedido.id_pedido} fue cancelado.", "Pedido")
        return pedido

    def _obtener_o_error(self, id_pedido: str) -> Pedido:
        pedido = self.pedido_repository.find_by_id(id_pedido)
        if not pedido:
            raise ValueError("No existe un pedido con ese ID.")
        return pedido
