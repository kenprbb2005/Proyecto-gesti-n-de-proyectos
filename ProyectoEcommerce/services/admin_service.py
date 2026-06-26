from typing import Dict
from services.usuario_service import UsuarioService
from services.producto_service import ProductoService
from services.pedido_service import PedidoService
from services.pago_service import PagoService
from services.resena_service import ResenaService
from services.notificacion_service import NotificacionService


class AdminService:
    def __init__(
        self,
        usuario_service: UsuarioService,
        producto_service: ProductoService,
        pedido_service: PedidoService,
        pago_service: PagoService,
        resena_service: ResenaService,
        notificacion_service: NotificacionService,
    ):
        self.usuario_service = usuario_service
        self.producto_service = producto_service
        self.pedido_service = pedido_service
        self.pago_service = pago_service
        self.resena_service = resena_service
        self.notificacion_service = notificacion_service

    def resumen(self) -> Dict[str, float]:
        usuarios = self.usuario_service.listar_usuarios()
        productos = self.producto_service.listar_productos()
        pedidos = self.pedido_service.listar_pedidos()
        pagos = self.pago_service.listar_pagos()
        resenas = self.resena_service.listar_resenas()
        ventas_aprobadas = sum(p.monto for p in pagos if p.estado == "Aprobado")
        pendientes = len([p for p in pedidos if p.estado == "Pendiente"])
        bajo_stock = len(self.producto_service.productos_bajo_stock())
        return {
            "usuarios": len(usuarios),
            "productos": len(productos),
            "pedidos": len(pedidos),
            "pagos_aprobados": len([p for p in pagos if p.estado == "Aprobado"]),
            "ventas_aprobadas": round(ventas_aprobadas, 2),
            "pedidos_pendientes": pendientes,
            "productos_bajo_stock": bajo_stock,
            "resenas": len(resenas),
            "notificaciones": len(self.notificacion_service.listar()),
        }
